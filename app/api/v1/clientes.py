from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.database import db
from datetime import datetime
from pydantic import BaseModel

class ClienteBase(BaseModel):
    nome: str
    cpf_cnpj: str = None
    email: str = None
    telefone: str = None
    endereco: str = None
    cidade: str = None
    estado: str = None
    role: str = 'Cliente'
    spent: float = 0.0

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id_cliente: int

router = APIRouter()

@router.get("/", response_model=List[ClienteResponse])
def get_clientes():
    query = "SELECT * FROM CLIENTES"
    # Adicionando tratamento caso as colunas role e spent não existam na base antiga,
    # as criaremos no init_db.py.
    result = db.execute_query(query)
    if result is None:
        return []
    return result

@router.get("/top")
def get_top_clientes():
    query = "SELECT * FROM CLIENTES ORDER BY spent DESC LIMIT 5"
    result = db.execute_query(query)
    if result is None:
        return []
    return result

@router.post("/", response_model=ClienteResponse)
def create_cliente(cliente: ClienteCreate):
    query = """
    INSERT INTO CLIENTES (nome, cpf_cnpj, email, telefone, endereco, cidade, estado, role, spent)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (cliente.nome, cliente.cpf_cnpj, cliente.email, cliente.telefone, 
              cliente.endereco, cliente.cidade, cliente.estado, cliente.role, cliente.spent)
    cliente_id = db.execute_query(query, params)
    if not cliente_id:
        raise HTTPException(status_code=400, detail="Erro ao criar cliente")
    return {**cliente.model_dump(), "id_cliente": cliente_id}
