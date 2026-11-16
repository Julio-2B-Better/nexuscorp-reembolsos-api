from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.database import get_db
from src.models.usuario import Usuario
from src.services.seguranca import verificar_senha, criar_token_acesso

router = APIRouter(prefix="/auth", tags=["Autenticação"])

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=TokenSchema)
def login(
    credenciais: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.email == credenciais.username).first()
    
    if not usuario or not verificar_senha(credenciais.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    dados_token = {
        "sub": str(usuario.id),
        "perfil": usuario.perfil,
        "departamento_id": usuario.departamento_id
    }
    
    token = criar_token_acesso(dados_token)
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }