"""
Database configuration and models
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime

#Base for models
Base = declarative_base()

# ==================== MODELS ====================

class AlbumDB(Base):
    """
    Model for picking your album
    """
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    artist = Column(String, nullable=False, index=True)
    #metadata
    release_date = Column(Integer, nullable=True,index=True)
    genre = Column(JSON, default=list) # ["rock", "jazz"]

    #album info
    tracks = Column(Integer, default=0)

    #media&links
    image_url = Column(String(1000), nullable=True)
    external_id = Column(String(100),nullable=True,index=True)
    external_link=Column(String(1000),nullable=True)

    #Tracks: (JSON with song lists)
    list_tracks = Column(JSON, default=list)

    def __repr__(self):
        return f"<Album(id={self.id}, nome='{self.name}', artiista='{self.artist}')>"

# ==================== DATABASE CONFIG ====================

DATABASE_URL = "sqlite:///darkmoon_records.db"

engine = create_engine(
    DATABASE_URL, 
    echo=False, #True for SQL debugging
    connect_args={"check_same_thread": False} 
    )

#Creating all tables...
Base.metadata.create_all(engine)

#Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ==================== DEPENDENCIES ====================

def get_db():
    """
    
    Dependency for FastAPI - database session

    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== HELPER FUNCTIONS ====================

def albums_by_genre(genre:str,db:Session) -> list:
    """
    Search for albums in database by genre
    """
    return db.query(AlbumDB).filter(
        AlbumDB.genre.contains([genre.lower()])
    ).all()

def save_album(albums_external:list, genre:str, db:Session) -> list:
    """
    Save external albums to database TBD
    """
    saved_albums = []

    for item in albums_external:
        exists = db.query(AlbumDB).filter(
            AlbumDB.name == item.get("name"),
            AlbumDB.artist == item.get("artist")
        ).first()

        if exists:
            saved_albums.append(exists)
            continue

        #Create new album
        new_album = AlbumDB(
            name=item.get('name'),
            artist=item.get('artist'),
            release_date=item.get('release_date'),
            genre=item.get("genre",[genre.lower()]),
            tracks=item.get('tracks', 0),
            image_url=item.get('image_url'),
            external_id=item.get('external_id'),
            external_link=item.get('external_link'),
            list_tracks=item.get('list_tracks', [])
        )

        db.add(new_album)
        saved_albums.append(new_album)

    db.commit()
    return saved_albums

def count_albums(db:Session) -> int:
    """
    Total albums in database
    """
    return db.query(AlbumDB).count()

def list_genres(db:Session) -> list:
    """
    List all unique possible genres in database
    """
    albums = db.query(AlbumDB).all()
    genres = set()

    for album in albums:
        if album.genre:
            genres.update(album.genre)

    return sorted(list(genres))