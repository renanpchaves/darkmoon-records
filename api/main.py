from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import Session
import random
# ==================== PROJECT IMPORTS ====================

from models.database import(
    get_db,
    AlbumDB,
    albums_by_genre,
    save_album,
    list_genres,
    count_albums
)
from services.spotify_service import SpotifyService

spotify = SpotifyService()
app = FastAPI(
    title="Darkmoon Records API",
    description="music catalogue public API",
    version="1.0.0",
)

# =================================================
# ENDPOINTS
# =================================================

#root
@app.get("/")
async def root():
    """Página inicial da API"""
    return {
        "message": "🎵 Darkmoon Records - Music Discovery API",
        "version": "1.0.0",
        "docs": "/docs",
        "example": "/recommend?genre=rock"
    }

# =========================== Populate database ===========================

@app.post("/populate")
async def populate(
    genre: str = Query(...,description="Genre to populate"),
    limit: int = Query(50, ge=10, le=200, description="How many albums to fetch"),
    min_popularity: int=Query(0,ge=0,le=100,description="Mininum popularity (0-100)") ,
    db: Session = Depends(get_db)
):
    """
    Manually populate database with albums

    **Parameters:**
    - genre: Musical genre (rock, jazz, etc)

    Popularity feature:
    - 0: All albums
    - 50: Medium popularity
    - 70: High popularity (popular albums)
    - 90: Very high popularity (hit albums only)
    """

    print(f"Fetching '{limit}' albums for '{genre}' from Spotify. ")

    fetch_limit = min(limit*2,200)
    spotify_albums = spotify.search_albums_by_genre(genre,limit=fetch_limit)

    if not spotify_albums:
        raise HTTPException(
            404,
            detail=f"No albums found for '{genre}'"
        )
    
    filtered_albums = [
        album for album in spotify_albums
        if album.get('popularity',0) >= min_popularity
    ]

    if not filtered_albums:
        raise HTTPException(
            404,
            detail=f"No albums found with popularity >= '{min_popularity}' for '{genre}'"
        )
    
    filtered_albums.sort(key=lambda x: x.get('popularity', 0), reverse=True)
    top_albums = filtered_albums[:limit]

    print(f"Found {len(filtered_albums)} albums with popularity >= {min_popularity}")
    print(f"Saving top {len(top_albums)} most popular...")

    saved = save_album(top_albums,genre,db)
    total_now = len(albums_by_genre(genre,db))

    return {
        "message": f"Successfully populated {genre}",
        "new_albums": len(saved),
        "total_albums": total_now,
        "min_popularity": min_popularity,
        "popularity_range": {
            "highest": top_albums[0].get('popularity', 0) if top_albums else 0,
            "lowest": top_albums[-1].get('popularity', 0) if top_albums else 0
        }
    }

# =========================== Listing recommendations ===========================

@app.get("/recommend")
async def recommend_album(
    genre: str = Query(..., description="Musical Genre: (ex: rock, jazz, etc)"),
    db: Session = Depends(get_db)
):
    """
    🎲 Recommends a random album based on chosen genre.
    
    >Example: /recommend?genre=rock<

    **Returns:**
    - Album name and artist
    - Album cover
    - Release year
    - 30s preview of first track
    - Spotify link
    - Track list
    """

    albums = albums_by_genre(genre,db)

    if not albums:
        raise HTTPException(
            status_code=404,
            detail=f'No albums for "{genre}" found, populate in route POST /populate?genre={genre}'
        )
    

    album = random.choice(albums)

    return {
        "album": album.name,
        "artist": album.artist,
        "year": album.release_date,
        "genres": album.genre or [],
        "cover_url": album.image_url,
        "spotify_link": album.spotify_link,
        "total_tracks": album.tracks,
        "popularity": album.spotify_popularity,
        "tracks": album.list_tracks or []  
    }

# =================================================
# MAIN 
# =================================================

if __name__ == "__main__":
    import uvicorn

    print("""
    ╔════════════════════════════════════════════╗
    ║  🎵 Darkmoon Records API                   ║
    ║                                            ║
    ║  📖 Docs: http://localhost:8000/docs       ║
    ║  🎲 Test: /recommend?genre=rock            ║
    ╚════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )