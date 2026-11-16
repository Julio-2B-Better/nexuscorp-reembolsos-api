from pydantic import BaseModel, Field
from typing import Optional

class AnaliseReembolsoSchema(BaseModel):
    decisao: str
    observacao: Optional[str] = None