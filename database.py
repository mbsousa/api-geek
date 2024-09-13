# objetivo: configurar e gerenciar a conexão com o banco de dados.

from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker 

DATABASE_URL = "sqlite:///./produtos.db"
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_engine():
    return engine

def init_db():
    SQLModel.metadata.create_all(bind=engine)