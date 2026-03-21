"""
Spotify API integration service
Searches for albums and retrieves metadata
"""

import requests
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class SpotifyService:
    """
    Client for Spotify Web API
    """

    BASE_URL = "https://api.spotify.com/v1"
    AUTH_URL = "https://accounts.spotify.com/api/token"

    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.acess_token = None

        if not self.client_id or not self.client_secret:
            print("⚠️ WARNING: Spotify credentials not found in .env file")
            print("💡 The API will work but won't fetch real data from Spotify")
        else:
            self._authenticate()

    def authenticate(self):
        """
        Authenticate with spotify credentials
        """
        try:
            response = requests.post(
                self.AUTH_URL,
                data ={"grant_type": "client_credentials"},
                auth={self.client_id, self.client_secret},
                timeout=10
            )
            response.raise_for_status()

            self.acess_token = response.json().get("acess_token")
            print("Authenticated successfully!")

        except requests.RequestException as e:
            print(f"Authentication error: {e}")
            self.acess_token = None
    @property
    def headers(self):
        """
        Headers with authentication for the requests
        """
        return{
            "Authorization": f"Bearer {self.acess_token}" if self.acess_token else ""
        }

    def search_albums_by_genre(self, genre: str, limit: int = 50) -> List[Dict]:
        """
        Search albums by genre on Spotify
        """
        if not self.acess_token:
            print ('Spotify not authenticated, returning empty list.')
            return []
        
        try :
            #search endpoint
            url = f"self.BASE_URL/search"
            params = {
                "q": f"genre:{genre}",
                "type": "album",
                "limit": min(limit, 50)
            }

            print (f'Searching spotify for genre: {genre}')

            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            albums = data.get("albums", {}).get("items", [])

            print (f'Found {len(albums)} albums on spotify!')

            processed_albums = []
            for album in albums:
                details = self._process_album_data(album)
                if details:
                    processed_albums.append(details)

                return processed_albums
        except requests.RequestException as e:
            print(f"Error searching spotify: {e}")
            return []