from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class Documento:
    """
    Representação estrita de um documento limpo e fatiado, pronto para vetorização.
    """
    conteudo: str
    metadados: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ResultadoBusca:
    """
    Estrutura imutável de dados retornada pelo banco vetorial após uma busca semântica.
    """
    conteudo: str
    metadados: Dict[str, Any]
    score_similaridade: float