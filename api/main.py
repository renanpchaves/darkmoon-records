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

app = FastAPI(
    title="Darkmoon Records API",
    description="API Publica de catálogo musical",
    version="1.0.0",
)

# ==================== ENDPOINTS ====================

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

#Endpoint for listing possible recommendations:
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

    #Search in database:
    albums = albums_by_genre(genre,db)

    if not albums:
        raise HTTPException(
            status_code=404,
            detail=f'Albums not found for genre "{genre}"'
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
        "popularity": album.popularity, 
        "tracks": album.list_tracks or []  
    }

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