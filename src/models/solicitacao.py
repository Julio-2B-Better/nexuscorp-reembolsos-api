from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class SolicitacaoReembolso(Base):
    __tablename__ = "solicitacoes_reembolso"

    id = Column(Integer, primary_key=True, index=True)
    solicitante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    categoria_despesa = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False)
    justificativa = Column(Text, nullable=False)
    referencia_comprovante = Column(String, unique=True, nullable=False)
    situacao = Column(String, nullable=False, default="Rascunho")

    solicitante = relationship("Usuario", back_populates="solicitacoes")
    historicos = relationship("HistoricoAnalise", back_populates="solicitacao")