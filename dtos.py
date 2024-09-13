# DTO => Data transfer object

from pydantic import BaseModel

class RequisicaoProduto(BaseModel):
    nome: str
    descricao: str
    preco: float
    categoria: str
    franquia: str