# Lógica de negócio e interação com o banco de dados

from sqlmodel import Session, select
from database import get_engine
from models import Produto
from typing import Optional
from sqlalchemy import update  

class ProdutosService:
    def __init__(self):
        self.engine = get_engine()

    def get_produto_by_id(self, id: int):
        with Session(self.engine) as session:
            s = select(Produto).where(Produto.id == id)
            return session.exec(s).one_or_none()
    
    def get_all_produtos(self, nome: Optional[str] = None, preco_min: Optional[float] = None, preco_max: Optional[float] = None, categoria: Optional[str] = None, franquia: Optional[str] = None):
        with Session(self.engine) as session:
            s = select(Produto).where(Produto.qt_estoque > 0)

        if nome:
            s = s.where(Produto.nome == nome)
        
        if preco_min is not None:
            if preco_min < 0:
                raise ValueError("O preço mínimo não pode ser negativo.")
            s = s.where(Produto.preco >= preco_min)

        if preco_max is not None:
            if preco_max < 0:
                raise ValueError("O preço máximo não pode ser negativo.")
            s = s.where(Produto.preco <= preco_max)

        if categoria:
            s = s.where(Produto.categoria == categoria)

        if franquia:
            s = s.where(Produto.franquia == franquia)

        return session.exec(s).all()
    
    def get_and_update_produto(self,produto_id:int, qt_estoque: Optional[int] = None):
        with Session(self.engine) as session:
            produto = session.exec(select(Produto).where(Produto.id == produto_id)).one_or_none()

        if produto is None:
            raise ValueError("Produto não encontrado.")
        
        if produto.qt_estoque <= 0:
            raise ValueError("Produto indisponível.")
        
        if produto.qt_estoque > 0:
            updated_qt_estoque = produto.qt_estoque - 1
            session.execute(update(Produto).where(Produto.id == produto_id).values(qt_estoque=updated_qt_estoque))
            session.commit()
        
        return produto

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
