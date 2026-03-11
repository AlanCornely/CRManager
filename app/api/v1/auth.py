from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.core.security import create_access_token
from authlib.integrations.starlette_client import OAuth
import uuid

router = APIRouter()
oauth = OAuth()

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=settings.GOOGLE_CLIENT_ID or "YOUR_CLIENT_ID",
    client_secret=settings.GOOGLE_CLIENT_SECRET or "YOUR_CLIENT_SECRET",
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get("/google/login")
async def google_login(request: Request):
    """
    Redirects to the Google Login Screen.
    """
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def auth_google(request: Request):
    """
    Receives the callback from Google, processes the user identity,
    and returns a JWT token redirecting back to the frontend.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
        if not user:
            raise HTTPException(status_code=400, detail="Authentication failed.")
        
        email = user.get('email')
        name = user.get('name')
        
        # NOTE: Here we would insert or update the user in our SQLite DB.
        # db.execute_query(...)
        
        # Generate JWT
        access_token = create_access_token(subject=email)
        
        # Redirect back to frontend
        return RedirectResponse(f"{settings.FRONTEND_URL}/login?token={access_token}")
        
    except Exception as e:
        # Falso positivo: Authlib sem setup joga exceção de secret missig
        # Apenas redireciona pro login com erro em produção
        return RedirectResponse(f"{settings.FRONTEND_URL}/login?error=auth_failed")
