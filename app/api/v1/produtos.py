from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.database import db
from datetime import date

router = APIRouter()

@router.get("/")
def get_produtos():
    query = "SELECT * FROM PRODUTOS WHERE ativo = 1"
    result = db.execute_query(query)
    if result is None:
        return []
    return result

@router.post("/")
def create_produto(produto: dict):
    # Minimal insert logic
    query = """
    INSERT INTO PRODUTOS (nome, descricao, categoria_id, sku, codigo_barras, estoque_minimo, quantidade_atual, preco_custo, preco_venda, data_cadastro, ativo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        produto.get('nome', 'Novo Produto'),
        produto.get('descricao', ''),
        produto.get('categoria_id', None),
        produto.get('sku', f"SKU-{int(date.today().strftime('%Y%m%d'))}"),
        produto.get('codigo_barras', ''),
        produto.get('estoque_minimo', 0),
        produto.get('quantidade_atual', 0),
        produto.get('preco_custo', 0.0),
        produto.get('preco_venda', 0.0),
        date.today().strftime('%Y-%m-%d'),
        1
    )
    prod_id = db.execute_query(query, params)
    if not prod_id:
        raise HTTPException(status_code=400, detail="Erro ao criar produto")
    return {"id_produto": prod_id}

@router.delete("/{produto_id}")
def delete_produto(produto_id: int):
    query = "UPDATE PRODUTOS SET ativo = 0 WHERE id_produto = ?"
    db.execute_query(query, (produto_id,))
    return {"message": "Produto excluído"}
