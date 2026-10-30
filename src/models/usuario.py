from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False) 
    perfil = Column(String, nullable=False) 
    departamento_id = Column(Integer, ForeignKey("departamentos.id"), nullable=False)

    departamento = relationship("Departamento", back_populates="usuarios")
    solicitacoes = relationship("SolicitacaoReembolso", back_populates="solicitante")
    historicos_analise = relationship("HistoricoAnalise", back_populates="responsavel")