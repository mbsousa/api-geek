# Lógica de negócio e interação com o banco de dados

from sqlmodel import Session, select
from database import get_engine, SessionLocal
from models import Produto

class ProdutosService:
    def __init__(self):
        self.engine = get_engine()

    def get_produto_by_id(self, id: int):
        with Session(self.engine) as session:
            s = select(Produto).where(Produto.id == id)
            return session.exec(s).one_or_none()
    
    def get_all_produtos(self, preco: float):
        with Session(self.engine) as session:
            s = select(Produto).where(Produto.qt_estoque > 0)
            if preco is not None:
                if preco < 0:
                    raise ValueError("O preço não pode ser negativo.")
                s = s.where(Produto.preco == preco)
            return session.exec(s).all()
        
    def save_produto(self, produto: Produto):
        try:
            with Session(self.engine) as session:
                session.add(produto)
                session.commit()
                session.refresh(produto)
                return produto
        except Exception as e:
            print(f"Erro ao salvar o produto: {e}")
            raise
