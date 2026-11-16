from pydantic import BaseModel, Field, validator
from datetime import date

class SolicitacaoCriar(BaseModel):
    categoria: str
    valor: float = Field(gt=0, description="O valor deve ser maior que zero")
    data_despesa: date
    justificativa: str
    referencia_comprovante: str

    @validator("data_despesa")
    def validar_data(cls, v):
        if v > date.today():
            raise ValueError("Despesas com datas futuras não podem ser registadas")
        return v

class SolicitacaoResposta(BaseModel):
    id: int
    solicitante_id: int
    categoria: str
    valor: float
    data: date
    justificativa: str
    referencia_comprovante: str
    situacao: str

    class Config:
        from_attributes = True # Permite ao Pydantic ler dados de modelos SQLAlchemy