from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="CRM de Gerenciamento de Estoque",
    description="API para gerenciamento de estoque e CRM",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configuração CORS Estrita (Hardening)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Estrito para o frontend Vue
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Adiciona Rate Limiting global em rotas sensíveis
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# Inclui as rotas da API
app.include_router(api_router, prefix="/api/v1")

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Melhora o serviço de arquivos estáticos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIST = os.path.join(BASE_DIR, "frontend", "dist")

if not os.path.exists(FRONTEND_DIST):
    os.makedirs(FRONTEND_DIST, exist_ok=True)

# Monta a pasta de assets especificamente para performance e clareza
app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

# Rota curinga para suportar o roteamento do Vue (SPA)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Se o caminho for vazio ou não for um arquivo existente, serve o index.html
    file_path = os.path.join(FRONTEND_DIST, full_path)
    if full_path and os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # Previne loop infinito se index.html estiver faltando
    index_path = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    return {"detail": "Frontend build not found. Please run 'npm run build' in the frontend directory."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "crm-estoque-api"}