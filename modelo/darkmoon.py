from modelo.rating import Rating

class Albums:
    album = []

    def __init__(self, nome, artista, quant_musicas=0):
        self._nome = nome.title()
        self._artista = artista.upper()
        self._quant_musicas = quant_musicas
        self._ativo = False
        self._avaliacao = []
        Albums.album.append(self)

    def __str__(self):
        return f'{self._nome} | {self._artista} | {self._quant_musicas} | {self._ativo}'

    @classmethod
    def listar_albums(cls):
        print (f'{'Nome do Album'.ljust(28)} | {'Artista'.ljust(25)} | {'Número de faixas'.ljust(25)} | {'Avaliação'.ljust(26)} | Estoque')
        for i in Albums.album:
            print (f'{i._nome.ljust(28)} | {i._artista.ljust(25)} | {str(i._quant_musicas).ljust(25)} | {str(i.media_avaliacoes).ljust(25)} | {i.ativo}')

    @property
    def ativo(self):
        return '✅ - em estoque' if self._ativo else '❌ - fora de estoque'

    def estoque_alt(self):
        self._ativo = not self._ativo

    def receber_avaliacao(self, cliente, nota):
            if 0 <= nota <= 5:
                avaliacao = Rating(cliente, nota)
                self._avaliacao.append(avaliacao)
                return True
            return False

    @property
    def media_avaliacoes(self):
        if not self._avaliacao:
            return '⭐ ---'
        soma_notas = sum(avaliacao._nota for avaliacao in self._avaliacao)
        quantidade_notas = len(self._avaliacao)
        media = round(soma_notas / quantidade_notas, 1)
        return f'⭐ {media}'