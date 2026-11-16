from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def gerar_hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha_texto: str, senha_hash: str):
    return pwd_context.verify(senha_texto, senha_hash)

SECRET_KEY = "uma_chave_secreta_muito_segura"
ALGORITHM = "HS256"

def criar_token_acesso(dados_utilizador: dict, tempo_expiracao_minutos: int = 30):
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=tempo_expiracao_minutos)
    dados_utilizador.update({"exp": expiracao.timestamp()})
    token = jwt.encode(dados_utilizador, SECRET_KEY, algorithm=ALGORITHM)
    return token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def obter_utilizador_atual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        perfil = payload.get("perfil")
        if perfil is None:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")