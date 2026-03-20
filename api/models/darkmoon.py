class Albums:
    album = []

    def __init__(self, nome, artista, quant_musicas=0):
        self._nome = nome.title()
        self._artista = artista.upper()
        self._quant_musicas = quant_musicas
        self._ativo = False
        self._avaliacao = []
        self._id = None #id na DB
        Albums.album.append(self)