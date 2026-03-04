from pydantic import BaseModel, Field
from typing import Annotated, Optional

class PerguntaModel(BaseModel):
    pergunta: Annotated[str, Field(min_length=1, max_length=200, examples=["Quanto é 2+2?"])]
    
class QueryParams(BaseModel):
    """Parâmetros para filtros de queries"""
    column: Optional[str] = Field(None, description="Coluna para filtro ou agregação")
    operator: Optional[str] = Field(None, description="Operador para filtro (>, <, =, >=, <=)")
    value: Optional[float] = Field(None, description="Valor para filtro")
    operation: Optional[str] = Field(None, description="Operação para agregação (AVG, SUM, MIN, MAX, COUNT)")
    group_by: Optional[str] = Field(None, description="Coluna para agrupar resultados")
    limit: Optional[int] = Field(10, description="Limite de resultados")