class Albums:
    album = []

    def __init__(self, nome, artista, quant_musicas=0):
        self._nome = nome.title()
        self._artista = artista.upper()
        self._quant_musicas = quant_musicas
        self._ativo = False
        Albums.album.append(self)

    def __str__(self):
        return f'{self._nome} | {self._artista} | {self._quant_musicas} | {self._ativo}'

    @classmethod
    def listar_albums(cls):
        print (f'{'Nome do Album'.ljust(28)} | {'Artista'.ljust(25)} | {'Número de faixas'.ljust(25)} | Estoque')
        for i in Albums.album:
            print (f'{i._nome.ljust(28)} | {i._artista.ljust(25)} | {i._quant_musicas:<25} | {i.ativo}')

    @property
    def ativo(self):
        return '✅ - em estoque' if self._ativo else '❌ - fora de estoque'

    def estoque_alt(self):
        self._ativo = not self._ativo