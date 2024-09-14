from fastapi import APIRouter, FastAPI, HTTPException, Query
from dtos import RequisicaoProduto
from models import Produto
from product_service import ProdutosService
from typing import List,Optional

app = FastAPI()
router = APIRouter()
produto_service = ProdutosService()

app.include_router(router, prefix="/api/geek")

# Create
@router.post("/produtos/", response_model=Produto)
def create_produto(produto: RequisicaoProduto, qt_estoque: int):
    db_produto = Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        qt_estoque=qt_estoque,
        categoria=produto.categoria,
        franquia=produto.franquia
    )
    return produto_service.save_produto(db_produto)

# Detail
@router.get("/produtos/{id}", response_model=Produto)
def produto_detail(id: int):
    produto = produto_service.get_produto_by_id(id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

""" Permitir a filtragem de produtos por nome, preço, categoria ou franquia. """
#List
@router.get("/produtos/", response_model=list[Produto])
def list_produtos(
    nome: Optional[str] = Query(None, description="Nome do produto"),
    preco_min: Optional[float] = Query(None, description="Preço mínimo"),
    preco_max: Optional[float] = Query(None, description="Preço máximo"),
    categoria: Optional[str] = Query(None, description="Categoria do produto"),
    franquia: Optional[str] = Query(None, description="Franquia")
):  
    return produto_service.get_all_produtos( 
        nome=nome,
        preco_min=preco_min,
        preco_max=preco_max,
        categoria=categoria,
        franquia=franquia)
    

#Update estoque
@router.put("/produtos/{produto_id}/att/")
def selecionar_produto(produto_id: int, qt_estoque: Optional[int] = None):
    try:
        produto = produto_service.get_and_update_produto(produto_id, qt_estoque)
        return {"message": "Produto selecionado com sucesso", "produto": produto}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))