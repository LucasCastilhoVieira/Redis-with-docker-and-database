from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import VARCHAR, CHAR, Integer, Column



Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    nome = Column(VARCHAR(50))
    cpf = Column(CHAR(14), primary_key=True, nullable=True)
    telefone = Column(VARCHAR(15))
    email = Column(VARCHAR(50))