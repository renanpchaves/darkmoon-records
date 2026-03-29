import os

from dotenv import load_dotenv
from fastapi import FastAPI, Query, Depends, HTTPException, status
from sqlalchemy.orm import Session
import random

from models.database import (
    AlbumDB,
    get_db,
    albums_by_genre,
    save_album,
    list_genres,
    count_albums,
)
from services.music_service import MusicService
from src.auth import create_access_token, verify_token

load_dotenv()

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
def root():
    """Endpoint raiz da API.

    Retorna informações básicas sobre a API Darkmoon Records, incluindo
    versão, documentação e exemplos de uso.

    Returns:
        dict: Dicionário contendo mensagem de boas-vindas, versão,
              URL da documentação e exemplo de uso.
    """
    return {
        "message": "🎵 Darkmoon Records - Music Discovery API",
        "version": "1.0.0",
        "docs": "/docs",
        "example": "/recommend?genre=rock",
    }


# =================================================
# AUTH
# =================================================


@app.post("/auth/token")
def get_token(api_key: str = Query(..., description="Admin API key")):
    """Gera um JWT de acesso para rotas protegidas.

    Valida a ADMIN_API_KEY e retorna um token JWT válido por 24 horas.
    Use o token no header: Authorization: Bearer <token>

    Args:
        api_key (str): Chave de admin definida em ADMIN_API_KEY no .env.

    Returns:
        dict: Dicionário com access_token e token_type.
    """
    if api_key != os.getenv("ADMIN_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return {"access_token": create_access_token(), "token_type": "bearer"}


# =================================================
# POPULATE DATABASE
# =================================================


@app.post("/populate")
def populate(
    genre: str = Query(..., description="Genre to populate"),
    limit: int = Query(50, ge=1, le=100, description="How many albums to fetch"),
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token),
):
    """Popula o banco de dados com álbuns de um gênero específico.

    Busca álbuns no Last.fm para um gênero específico e os armazena
    no banco de dados. Se o gênero já contiver álbuns, novos álbuns
    serão adicionados aos existentes.

    Args:
        genre (str): Gênero musical a ser populado (ex: 'rock', 'jazz').
        limit (int): Número de álbuns a serem buscados. Deve estar
                    entre 1 e 100. Padrão: 50.
        db (Session): Sessão do banco de dados (injetada automaticamente).

    Returns:
        dict: Dicionário com informações de sucesso, incluindo:
              - message (str): Mensagem de sucesso.
              - albums_fetched (int): Número de álbuns buscados.
              - albums_saved (int): Número de álbuns salvos.
              - total_albums_in_genre (int): Total de álbuns do gênero.
    """
    print(f"Fetching '{limit}' albums for genre '{genre}' from Last.fm...")

    albums = music_service.search_albums_by_genre(genre, limit=limit)

    if not albums:
        raise HTTPException(
            status_code=404, detail=f"No albums found for genre '{genre}'"
        )

    saved = save_album(albums, genre, db)
    total_now = len(albums_by_genre(genre, db))

    return {
        "message": f"Successfully populated genre '{genre}'",
        "albums_fetched": len(albums),
        "albums_saved": len(saved),
        "total_albums_in_genre": total_now,
    }


# =================================================
# RANDOM RECOMMENDATION
# =================================================


@app.get("/recommend")
def recommend_album(
    genre: str = Query(..., description="Musical genre, e.g. rock, jazz, indie"),
    db: Session = Depends(get_db),
):
    """Recomenda um álbum aleatório de um gênero específico.

    Busca todos os álbuns de um gênero no banco de dados e retorna
    um aleatoriamente. Útil para descoberta musical.

    Args:
        genre (str): Gênero musical desejado (ex: 'rock', 'jazz', 'indie').
        db (Session): Sessão do banco de dados (injetada automaticamente).

    Returns:
        AlbumDB: Objeto de álbum aleatório contendo dados como
               nome, artista e gênero.
    """
    albums = albums_by_genre(genre, db)

    if not albums:
        raise HTTPException(
            status_code=404,
            detail=f'No albums found for "{genre}". Populate first with POST /populate?genre={genre}',
        )

    album = random.choice(albums)
    return album


# =================================================
# LIST ALL ALBUMS IN DB
# =================================================


@app.get("/albums")
def list_albums(db: Session = Depends(get_db)):
    """Lista todos os álbuns armazenados no banco de dados.

    Retorna uma lista completa de todos os álbuns cadastrados,
    com informações como nome, artista e gênero.

    Args:
        db (Session): Sessão do banco de dados (injetada automaticamente).

    Returns:
        dict: Dicionário contendo a chave 'albums' com lista de
              todos os objetos AlbumDB armazenados.
    """
    albums = db.query(AlbumDB).all()
    return {"albums": albums}


# =================================================
# DELETE ALBUM BY ID
# =================================================


@app.delete("/albums/{album_id}")
def delete_album(
    album_id: int, db: Session = Depends(get_db), _: dict = Depends(verify_token)
):
    """Deleta um álbum específico do banco de dados.

    Remove permanentemente um álbum identificado pelo seu ID.

    Args:
        album_id (int): ID único do álbum a ser deletado.
        db (Session): Sessão do banco de dados (injetada automaticamente).

    Returns:
        dict: Dicionário contendo a mensagem de confirmação indicando
              qual álbum foi deletado (nome e artista).
    """
    album = db.query(AlbumDB).filter(AlbumDB.id == album_id).first()

    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    db.delete(album)
    db.commit()
    return {
        "message": f"Album '{album.name}' by '{album.artist}' deleted successfully."
    }


# =================================================
# GENRES
# =================================================


@app.get("/genres")
def get_genres(db: Session = Depends(get_db)):
    """Retorna lista de todos os gêneros disponíveis no banco de dados.

    Obtém uma lista única de todos os gêneros que possuem álbuns
    cadastrados na aplicação.

    Args:
        db (Session): Sessão do banco de dados (injetada automaticamente).

    Returns:
        dict: Dicionário contendo a chave 'genres' com lista de strings
              representando gêneros únicos disponíveis.
    """
    return {"genres": list_genres(db)}


# =================================================
# STATS
# =================================================


@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Retorna estatísticas básicas do banco de dados.

    Fornece informações gerais sobre o estado da aplicação,
    como número total de álbuns cadastrados.

    Args:
        db (Session): Sessão do banco de dados (injetada automaticamente).

    Returns:
        dict: Dicionário contendo a chave 'total_albums' com
              o número inteiro de álbuns armazenados.
    """
    return {"total_albums": count_albums(db)}


# =================================================
# MAIN
# =================================================

if __name__ == "__main__":
    import uvicorn

    print("🎵 Darkmoon Records API starting...")
    print("📖 Docs: http://localhost:8000/docs")
    print("🎲 Test: /recommend?genre=rock")

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
