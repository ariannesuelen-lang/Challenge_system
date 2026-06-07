from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class RespostaItem(BaseModel):
    questao_id: UUID
    alternativa_id: Optional[UUID] = None
    texto_resposta: Optional[str] = None

class CorrecaoRequest(BaseModel):
    usuario_id: int  # ID int4 do usuario (Vincula à nova coluna)
    respostas: List[RespostaItem]