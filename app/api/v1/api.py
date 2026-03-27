from fastapi import APIRouter
from . import usuarios, produtos, notificacoes, auth, clientes
import datetime

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
api_router.include_router(produtos.router, prefix="/produtos", tags=["Produtos"])
api_router.include_router(notificacoes.router, prefix="/notificacoes", tags=["Notificações"])
api_router.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])

@api_router.get("/time", tags=["Sistema"])
def get_current_time():
    now = datetime.datetime.now()
    return {
        "date": now.strftime("%d/%m/%Y"),
        "time": now.strftime("%H:%M")
    }

# api_router.include_router(categorias.router, prefix="/categorias", tags=["Categorias"])
# api_router.include_router(fornecedores.router, prefix="/fornecedores", tags=["Fornecedores"])
# api_router.include_router(vendas.router, prefix="/vendas", tags=["Vendas"])
# api_router.include_router(compras.router, prefix="/compras", tags=["Compras"])
# api_router.include_router(movimentos.router, prefix="/movimentos", tags=["Movimentações"])