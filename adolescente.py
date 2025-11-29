from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Adolescente:
    nome: str
    idade: int
    nome_pai: Optional[str] = None
    nome_mae: Optional[str] = None
    endereco: Dict[str, Any] = None
