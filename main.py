from fastapi import APIRouter, FastAPI, HTTPException
from dtos import RequisicaoProduto
from models import Produto
from product_service import ProdutosService

app = FastAPI()
router = APIRouter()
produto_service = ProdutosService()

@router.post("/produtos/", response_model=Produto)
def create_produto(produto: RequisicaoProduto, qt_estoque: int = 0):
    db_produto = Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        qt_estoque=qt_estoque,
        categoria=produto.categoria,
        franquia=produto.franquia
    )
    return produto_service.save_produto(db_produto)

@router.get("/produtos/{id}", response_model=Produto)
def produto_detail(id: int):
    produto = produto_service.get_produto_by_id(id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.get("/produtos/", response_model=list[Produto])
def list_produtos(preco: float = None):
    return produto_service.get_all_produtos(preco)

app.include_router(router, prefix="/api/geek")