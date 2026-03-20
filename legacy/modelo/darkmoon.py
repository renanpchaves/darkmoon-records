from modelo.rating import Rating
from modelo import Albums
from modelo.database import Session, AlbumDB, RatingDB

class Albums:
    cd = []

    def __init__(self, nome, artista, quant_musicas=0):
        self._nome = nome.title()
        self._artista = artista.upper()
        self._quant_musicas = quant_musicas
        self._ativo = False
        self._avaliacao = []
        self._id = None #id na DB
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
    
    def deletar_album(self):
        '''
        Remove o album do banco de dados
        '''
        try:
            if self in Albums.album:
                Albums.album.remove(self)
            #remove do banco via ID
            if self._id:
                session = Session()
                try:
                    album_db = session.query(AlbumDB).filter_by(id=self._id).first()
                    if album_db:
                        session.delete(album_db)
                        session.commit()
                except Exception as e:
                    session.rollback()
                    print(f'❌ Erro ao deletar do banco: {e}')
                finally:
                    session.close()
            return True
        except Exception as e:
            print(f'❌ Erro ao deletar do banco: {e}')
            return False

    def salvar_db(self):
        '''
        salva o album no banco

        CORREÇÃO:
        - Se self._id for None -> cria (INSERT)
        - Se self._id existir  -> atualiza (UPDATE)
        '''
        session = Session()
        try:
            if self._id is None:
                # INSERT
                album_db = AlbumDB(
                    nome=self._nome,
                    artista=self._artista,
                    quant_musicas=self._quant_musicas,
                    ativo=self._ativo
                )

                # cria ratings no relacionamento
                for avaliacao in self._avaliacao:
                    album_db.avaliacoes.append(RatingDB(
                        cliente=avaliacao._cliente,
                        nota=avaliacao._nota
                    ))

                session.add(album_db)
                session.commit()

                self._id = album_db.id
                print(f'✅ Salvo na base de dados com o ID: {self._id}')

            else:
                # UPDATE
                album_db = session.get(AlbumDB, self._id)
                if not album_db:
                    print('❌ Álbum não encontrado no banco para atualizar.')
                    return

                #checando mudanças simples nos campos do album
                album_atualizou = (
                album_db.nome != self._nome or
                album_db.artista != self._artista or 
                album_db.quant_musicas != self._quant_musicas or
                album_db.ativo != self._ativo
                )

                #checando mudanças nas avaliaçoes (comparando listas)
                ratings_db = [(r.cliente, float(r.nota)) for r in album_db.avaliacoes]
                ratings_mem = [(r._cliente, float(r._nota)) for r in self._avaliacao]
                ratings_atualizou = ratings_db != ratings_mem

                if not album_atualizou and not ratings_atualizou:
                    print(f'ℹ️ Álbum (ID {self._id}) sem alterações. Nada para salvar.')
                    return

                #aplicando as mudanças
                album_db.avaliacoes.clear()
                for avaliacao in self._avaliacao:
                    album_db.avaliacoes.append(RatingDB(
                        cliente=avaliacao._cliente,
                        nota=avaliacao._nota
                    ))

                session.commit()
                print(f'✅ Álbum (ID {self._id}) atualizado no banco.')

        except Exception as e:
            session.rollback()
            print(f'❌ Erro ao salvar: {e}')
        finally:
            session.close()

    @classmethod
    def carregar_db(cls):
        '''
        carrega todos os albuns do banco
        '''
        session = Session()
        try:
            albums_db = session.query(AlbumDB).all()

            #limpa a lista atual
            cls.album.clear()

            #recriar os objetos:
            for album_db in albums_db:
                album = cls(
                    album_db.nome,
                    album_db.artista,
                    album_db.quant_musicas
                )
                album._ativo = album_db.ativo
                album._id = album_db.id

                #carrega as avaliaçoes pra listar:
                for rating_db in album_db.avaliacoes:
                    rating = Rating(rating_db.cliente, rating_db.nota)
                    album._avaliacao.append(rating)

            print(f'✅ {len(cls.album)} álbuns carregados do banco!')

        except Exception as e:
            print(f'❌ Erro ao carregar: {e}')
        finally:
            session.close()

