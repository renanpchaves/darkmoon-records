"""
Music discovery service using Last.fm as the primary source.

This service is responsible for:
- fetching albums by genre/tag from Last.fm
- normalizing the response into the project's internal album format
- returning clean album dictionaries ready to be saved in the database
"""

from __future__ import annotations
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

import requests

load_dotenv()

class MusicService:
    """
    Service for album discovery using Last.fm.
    """

    BASE_URL = "https://ws.audioscrobbler.com/2.0/"

    def __init__(self) -> None:
        self.api_key = os.getenv("LASTFM_API_KEY")

    def search_albums_by_genre(self, genre: str, limit: int = 50) -> List[Dict]:
        """
        Fetch top albums for a given genre/tag from Last.fm.

        Last.fm's tag.getTopAlbums returns albums ordered by tag count.

        Args:
            genre: Genre/tag name, e.g. "rock", "jazz", "indie"
            limit: Maximum number of albums to return

        Returns:
            A list of normalized album dictionaries
        """
        if not self.api_key:
            print("⚠️ LASTFM_API_KEY not found. Returning empty list.")
            return []

        normalized_genre = genre.strip().lower()

        try:
            print(f"🔍 Searching Last.fm albums for genre: {normalized_genre}")

            raw_albums = self._get_top_albums_by_tag(
                tag=normalized_genre,
                limit=limit
            )

            if not raw_albums:
                print(f'⚠️ No albums found for "{normalized_genre}"')
                return []

            normalized_albums: List[Dict] = []
            seen_keys = set()

            for item in raw_albums:
                album_data = self._normalize_lastfm_album(item, normalized_genre)

                if not album_data:
                    continue

                # Deduplicate by album + artist pair
                unique_key = (
                    album_data["name"].strip().lower(),
                    album_data["artist"].strip().lower()
                )

                if unique_key in seen_keys:
                    continue

                seen_keys.add(unique_key)
                normalized_albums.append(album_data)

                if len(normalized_albums) >= limit:
                    break

            print(f"✅ Collected {len(normalized_albums)} albums for genre '{normalized_genre}'")
            return normalized_albums

        except requests.RequestException as e:
            print(f"❌ Last.fm request error: {e}")
            return []

    def _get_top_albums_by_tag(self, tag: str, limit: int) -> List[Dict]:
        """
        Call Last.fm tag.getTopAlbums.

        The endpoint supports:
        - tag
        - limit
        - page
        - api_key
        - format=json

        Args:
            tag: Genre/tag name
            limit: Number of results to request

        Returns:
            Raw list of album objects from Last.fm
        """
        params = {
            "method": "tag.gettopalbums",
            "tag": tag,
            "api_key": self.api_key,
            "format": "json",
            "limit": min(limit, 100),
            "page": 1,
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        return data.get("albums", {}).get("album", [])

    def _normalize_lastfm_album(self, item: Dict, genre: str) -> Optional[Dict]:
        """
        Convert a Last.fm album object into the project's internal album format.

        Expected output keys match the structure used by save_album().
        """
        if not item:
            return None

        album_name = item.get("name")
        artist_data = item.get("artist", {})

        if isinstance(artist_data, dict):
            artist_name = artist_data.get("name")
        else:
            artist_name = str(artist_data) if artist_data else None

        if not album_name or not artist_name:
            return None

        image_url = self._extract_best_lastfm_image(item.get("image", []))
        lastfm_url = item.get("url")
        mbid = item.get("mbid") or None

        return {
            "name": album_name,
            "artist": artist_name,
            "release_date": None,          # Not reliably provided here
            "genre": [genre],
            "tracks": 0,                   # Not provided by tag.getTopAlbums
            "image_url": image_url,
            "spotify_id": mbid,            # Temporary unique external id slot
            "spotify_link": lastfm_url,    # Reusing this field for an external album link
            "list_tracks": []
        }

    @staticmethod
    def _extract_best_lastfm_image(images: List[Dict]) -> Optional[str]:
        """
        Return the best available image URL from Last.fm image array.

        Last.fm usually returns multiple sizes.
        We prefer the last non-empty image.
        """
        if not images:
            return None

        for image in reversed(images):
            url = image.get("#text")
            if url:
                return url

        return None