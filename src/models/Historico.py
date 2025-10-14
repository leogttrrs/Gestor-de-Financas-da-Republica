from __future__ import annotations
from typing import List, Optional
from src.database import DatabaseManager

class Historico:
    def __init__(self, evento: str, timestamp: str, morador_nome: Optional[str] = None,
                 divida_descricao: Optional[str] = None, valor: Optional[float] = None,
                 detalhes: Optional[str] = None, id: int = None, **kwargs):
        self.id = id
        self.timestamp = timestamp
        self.evento = evento
        self.morador_nome = morador_nome
        self.divida_descricao = divida_descricao
        self.valor = valor
        self.detalhes = detalhes

    @staticmethod
    def registrar_evento(evento: str, morador_nome: str = None, divida_descricao: str = None,
                         valor: float = None, detalhes: str = ""):
        db = DatabaseManager()
        comando = """
            INSERT INTO historico (evento, morador_nome, divida_descricao, valor, detalhes) 
            VALUES (?, ?, ?, ?, ?)
        """
        params = (evento, morador_nome, divida_descricao, valor, detalhes)
        db.executar_comando(comando, params)

    @staticmethod
    def buscar_todos() -> List[Historico]:
        db = DatabaseManager()
        query = "SELECT * FROM historico ORDER BY timestamp DESC"
        return [Historico(**r) for r in db.executar_query(query)]