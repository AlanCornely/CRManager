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

# Create frontend directory if it doesn't exist (just to be safe, though we know it does)
if not os.path.exists("frontend"):
    os.makedirs("frontend")

app.mount("/assets", StaticFiles(directory="frontend"), name="assets")

@app.get("/")
async def root():
    return FileResponse('frontend/index.html')

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "crm-estoque-api"}