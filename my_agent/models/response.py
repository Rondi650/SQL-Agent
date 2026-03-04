from pydantic import BaseModel, Field
from datetime import datetime


# Sobre default_factory: Precisa de um Callable, para gerar o valor padrao. 
# Se fosse apenas default="valor", o valor seria fixo. Com default_factory, 
# a função é chamada toda vez que um valor padrão é necessário, permitindo gerar 
# valores dinâmicos como timestamps.
# https://docs.pydantic.dev/latest/concepts/fields/#default-values
class RespostaModel(BaseModel):
    """Modelo para respostas de chat"""
    response: str
    data_hora: str = Field(
        default_factory=lambda: datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    thread_id: str
    total_tokens: int = 0