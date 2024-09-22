from fastapi import APIRouter, HTTPException, Query
from dtos import RequisicaoProduto
from models import Produto
from product_service import ProdutosService
from typing import Optional


router = APIRouter()
produto_service = ProdutosService()


# Create
@router.post("/produtos/", response_model=RequisicaoProduto)  # Use RequisicaoProduto aqui
def create_produto(produto: RequisicaoProduto):
    db_produto = Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        qt_estoque=0,  # Ou qualquer valor padrão que você queira
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

#List with filters
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
    
# Atualizar estoque (venda ou reposição)
@router.put("/produtos/{produto_id}/estoque/")
def atualizar_estoque(produto_id: int, quantidade: int):
    produto = produto_service.get_produto_by_id(produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if quantidade < 0:
        if produto.qt_estoque + quantidade < 0:
            raise HTTPException(status_code=400, detail="Estoque insuficiente para a venda")
        produto.qt_estoque += quantidade  
        operacao = "vendido"
    else:
        produto.qt_estoque += quantidade 
        operacao = "reposto"

    produto_service.update_produto(produto)

    return {"message": f"Estoque {operacao} com sucesso", "produto": produto}

# Excluir produto
@router.delete("/produtos/{produto_id}/", status_code=204)
def excluir_produto(produto_id: int):
    produto = produto_service.get_produto_by_id(produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    if produto.qt_estoque > 0:
        raise HTTPException(status_code=400, detail="Produto não pode ser excluído enquanto tiver estoque.")

    produto_service.delete_produto(produto_id)
    return {"message": "Produto excluído com sucesso"}
