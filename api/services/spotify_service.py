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