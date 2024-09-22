# DTO => Data transfer object

from pydantic import BaseModel, validator

class RequisicaoProduto(BaseModel):
    nome: str
    descricao: str
    preco: float
    categoria: str
    franquia: str

    @validator('nome', 'descricao', 'categoria', 'franquia')
    def check_non_empty(cls, value):
        if not value:
            raise ValueError("Este campo não pode ser vazio.")
        return value

    @validator('preco')
    def check_preco(cls, value):
        if value < 0:
            raise ValueError("O preço não pode ser negativo.")
        return value