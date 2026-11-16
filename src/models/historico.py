from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

class HistoricoAnalise(Base):
    __tablename__ = "historicos_analise"

    id = Column(Integer, primary_key=True, index=True)
    solicitacao_id = Column(Integer, ForeignKey("solicitacoes_reembolso.id"), nullable=False)
    responsavel_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    etapa = Column(String, nullable=False) 
    decisao = Column(String, nullable=False) 
    data = Column(DateTime, default=datetime.utcnow, nullable=False)
    observacao = Column(Text, nullable=True)

    solicitacao = relationship("SolicitacaoReembolso", back_populates="historicos")
    responsavel = relationship("Usuario", back_populates="historicos_analise")