from pydantic import BaseModel, EmailStr, Field

class UsuarioSaida(BaseModel):
    id: int
    nome: str
    email: EmailStr
    departamento_id: int
    perfil: str

    class Config:
        from_attributes = True