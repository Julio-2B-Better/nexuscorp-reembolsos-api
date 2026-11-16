from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import date

class SolicitacaoCriar(BaseModel):
    categoria: str
    valor: float = Field(gt=0, description="O valor deve ser maior que zero")
    data_despesa: date
    justificativa: str
    referencia_comprovante: str

class SolicitacaoResposta(BaseModel):
    id: int
    solicitante_id: int
    categoria: str
    valor: float
    data: date
    justificativa: str
    referencia_comprovante: str
    situacao: str

    model_config = ConfigDict(from_attributes=True)

class AnaliseReembolsoSchema(BaseModel):
    decisao: str 
    observacao: Optional[str] = None