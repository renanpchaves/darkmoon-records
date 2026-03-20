from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#base para os modelos
Base = declarative_base()

#tabela principal
class AlbumDB(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    artista = Column(String, nullable=False)
    quant_musicas = Column(Integer, default=0)

#banco config:
engine = create_engine('sqlite:///darkmoon_records.db', echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)