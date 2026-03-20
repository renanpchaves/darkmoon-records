from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
from modelo.darkmoon import Albums
from typing import Optional, List
import random


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Carregando álbuns do banco...")
    Albums.carregar_db()
    print (f"{len(Albums.album)} álbuns carregados!")

    yield

    print("Encerrando aplicação...")

app = FastAPI(
    title="Darkmoon Records API",
    description="API Publica de catálogo musical",
    version="1.0.0",
    lifespan=lifespan
)

#listando todos os albuns do catalogo
def listar_albums():
    """
    Retoorna todos os albuns do catalogo"""
    return [
        {
            "id": i,
            "nome": album._nome,
            "artista": album._artista,
            "quant_musicas": album._quant_musicas,
            "avaliacao_media": album._media_avaliacoes
        }
        for i, album in enumerate(Albums.album,1)
    ]