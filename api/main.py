from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import Session
import random

from models.database import (
    get_db,
    albums_by_genre,
    save_album,
    list_genres,
    count_albums
)
from services.music_service import MusicService

music_service = MusicService()

app = FastAPI(
    title="Darkmoon Records API",
    description="Music catalogue public API",
    version="1.0.0",
)


# =================================================
# ROOT
# =================================================

@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "🎵 Darkmoon Records - Music Discovery API",
        "version": "1.0.0",
        "docs": "/docs",
        "example": "/recommend?genre=rock"
    }


# =================================================
# POPULATE DATABASE
# =================================================

@app.post("/populate")
async def populate(
    genre: str = Query(..., description="Genre to populate"),
    limit: int = Query(50, ge=1, le=100, description="How many albums to fetch"),
    db: Session = Depends(get_db)
):
    """
    Populate the database with albums from Last.fm based on a genre/tag.

    Parameters:
    - genre: Musical genre/tag (rock, jazz, indie, etc.)
    - limit: Maximum number of albums to fetch
    """

    print(f"Fetching '{limit}' albums for genre '{genre}' from Last.fm...")

    albums = music_service.search_albums_by_genre(genre, limit=limit)

    if not albums:
        raise HTTPException(
            status_code=404,
            detail=f"No albums found for genre '{genre}'"
        )

    saved = save_album(albums, genre, db)
    total_now = len(albums_by_genre(genre, db))

    return {
        "message": f"Successfully populated genre '{genre}'",
        "albums_fetched": len(albums),
        "albums_saved": len(saved),
        "total_albums_in_genre": total_now
    }


# =================================================
# RANDOM RECOMMENDATION
# =================================================

@app.get("/recommend")
async def recommend_album(
    genre: str = Query(..., description="Musical genre, e.g. rock, jazz, indie"),
    db: Session = Depends(get_db)
):
    """
    Recommend a random album from the local database by genre.
    """

    albums = albums_by_genre(genre, db)

    if not albums:
        raise HTTPException(
            status_code=404,
            detail=f'No albums found for "{genre}". Populate first with POST /populate?genre={genre}'
        )

    album = random.choice(albums)

    return {
        "album": album.name,
        "artist": album.artist,
        "year": album.release_date,
        "genres": album.genre or [],
        "cover_url": album.image_url,
        "external_link": album.external_link,
    }


# =================================================
# GENRES
# =================================================

@app.get("/genres")
async def get_genres(db: Session = Depends(get_db)):
    """
    Return all genres currently stored in the database.
    """
    return {"genres": list_genres(db)}


# =================================================
# STATS
# =================================================

@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Return basic database stats.
    """
    return {"total_albums": count_albums(db)}


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