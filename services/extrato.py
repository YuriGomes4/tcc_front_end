from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid

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

# Definição da classe Extrato
class Extrato(Base):
    __tablename__ = 'extrato'

    id = Column(String, primary_key=True)
    tipo = Column(String)
    valor = Column(Float)
    data = Column(String)
    descricao = Column(String)
    categoria_id = Column(String, ForeignKey('categorias.id'))

    categoria = relationship("Categoria")

    def __init__(self, id, tipo, valor, data, descricao, categoria):
        self.id = id
        self.tipo = tipo
        self.valor = valor
        self.data = data
        self.descricao = descricao
        self.categoria = categoria

    def __repr__(self):
        return f"Extrato(id='{self.id}', tipo='{self.tipo}', valor={self.valor}, data='{self.data}', " \
               f"descricao='{self.descricao}', categoria='{self.categoria}')"
    
def check_existing_id(id):
    existing_id = session.query(Extrato).filter_by(id=id).first()
    return existing_id is not None

def modify_extrato_row(row_id, new_values):
    linha = session.query(Extrato).filter_by(id=row_id).first()
    #print(linha)
    #print(row_id)
    linha.descricao = new_values[0]
    linha.valor = new_values[1]
    linha.tipo = new_values[2]
    linha.data = new_values[3]
    linha.categoria_id = new_values[4]
    session.commit()

def get_all():
    tudo = session.query(Extrato).all()
    return tudo

transactions = get_all()

def parse_ofx_file_and_add_to_db(filename):
    with open(filename, 'r') as file:
        content = file.readlines()

    transaction_list = []
    memo_list = []
    trntype_list = []
    trnamt_list = []
    fitid_list = []
    dtposted_list = []

    parsing_transactions = False

    for line in content:
        if "<STMTTRN>" in line:
            parsing_transactions = True
        elif "</STMTTRN>" in line:
            parsing_transactions = False
        elif parsing_transactions:
            if "<MEMO>" in line:
                memo = line.strip().replace("<MEMO>", "").replace("</MEMO>", "")
                memo_list.append(memo)
            elif "<TRNTYPE>" in line:
                trntype = line.strip().replace("<TRNTYPE>", "").replace("</TRNTYPE>", "")
                trntype_list.append(trntype)
            elif "<TRNAMT>" in line:
                trnamt = line.strip().replace("<TRNAMT>", "").replace("</TRNAMT>", "")
                trnamt_list.append(float(trnamt))
            elif "<FITID>" in line:
                fitid = line.strip().replace("<FITID>", "").replace("</FITID>", "")
                fitid_list.append(fitid)
            elif "<DTPOSTED>" in line:
                dtposted = line.strip().replace("<DTPOSTED>", "").replace("</DTPOSTED>", "")
                dtposted_list.append(dtposted)

    for i in range(len(memo_list)):
        id = fitid_list[i]
        if not check_existing_id(id):
            categoria = session.query(Categoria).filter_by(id=79).first()
            transaction = Extrato(
                id=id,
                tipo=trntype_list[i],
                valor=trnamt_list[i],
                data=dtposted_list[i],
                descricao=memo_list[i],
                categoria=categoria
            )
            session.add(transaction)

        trs = {
            "MEMO": memo_list[i],
            "TRNTYPE": trntype_list[i],
            "TRNAMT": trnamt_list[i],
            "FITID": fitid_list[i],
            "DTPOSTED": dtposted_list[i]
        }
        transaction_list.append(trs)

    session.commit()

    #session.close()


    return transaction_list
