from pydantic import BaseModel, Field
from datetime import date

class SolicitacaoCriacao(BaseModel):
    categoria: str
    valor: float = Field(..., gt=0)  # Garante que o valor é maior que zero
    data_despesa: date
    justificativa: str
    comprovante_ref: str