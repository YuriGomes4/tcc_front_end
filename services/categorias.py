from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid

from flet import(
    Icon,
    icons
)

# Criação da conexão com o banco de dados SQLite
engine = create_engine('sqlite:///database.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Definição da classe Categoria
class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    pai_id = Column(Integer)
    nome = Column(String)
    icone = Column(String)

    def __repr__(self):
        return f"Categoria(id={self.id}, pai_id={self.pai_id}, nome='{self.nome}')"
    
def modify_category_row(cat_id, new_values):
    linha = session.query(Categoria).filter_by(id=cat_id).first()
    #print(linha)
    #print(row_id)
    linha.nome = new_values[0]
    linha.icone = new_values[1]
    session.commit()

def get_roots():
    return session.query(Categoria).filter_by(pai_id=0).all()

def get_cat(idd):
    return session.query(Categoria).filter_by(id=idd).first()

def get_subroots(id):
    return session.query(Categoria).filter_by(pai_id=id).all()

def teste():
    return session.query(Categoria).filter_by(id=80).first()

#session.add(Categoria(id=80,pai_id=0,nome="askjdhak", icone=icons.ADD))
#session.commit()