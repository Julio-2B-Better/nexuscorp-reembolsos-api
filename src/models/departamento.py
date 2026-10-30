from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base # Volte um nível ou configure o path adequadamente

class Departamento(Base):
    __tablename__ = "departamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)

    # DICA CRUCIAL: Mantenha o nome do modelo como uma string ("Usuario")
    # Isso evita que você precise importar o arquivo do usuário aqui dentro.
    usuarios = relationship("Usuario", back_populates="departamento")