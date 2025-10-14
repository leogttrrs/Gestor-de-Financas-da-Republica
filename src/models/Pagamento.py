from __future__ import annotations
from typing import List
from src.database import DatabaseManager


class Pagamento:
    def __init__(self, divida_id: int, valor: float, data_pagamento: str, status: str, id: int = None, **kwargs):
        self.id = id
        self.divida_id = divida_id
        self.valor = valor
        self.data_pagamento = data_pagamento
        self.status = status

        self.descricao_divida = kwargs.get('descricao', '')
        self.nome_morador = kwargs.get('nome_morador', '')

    def atualizar_status(self, novo_status: str) -> bool:
        if novo_status not in ['confirmado', 'cancelado']:
            return False
        db = DatabaseManager()
        comando = "UPDATE pagamento SET status = ? WHERE id = ?"
        db.executar_comando(comando, (novo_status, self.id))
        self.status = novo_status
        return True

    @staticmethod
    def buscar_pendentes() -> List[Pagamento]:
        db = DatabaseManager()
        query = """
            SELECT p.*, d.descricao, u.nome as nome_morador
            FROM pagamento p
            JOIN divida d ON p.divida_id = d.id
            JOIN usuario u ON d.morador_id = u.id
            WHERE p.status = 'pendente'
        """
        return [Pagamento(**r) for r in db.executar_query(query)]

    @staticmethod
    def buscar_confirmados() -> List[Pagamento]:
        db = DatabaseManager()
        query = """
            SELECT p.*, d.descricao, u.nome as nome_morador
            FROM pagamento p
            JOIN divida d ON p.divida_id = d.id
            JOIN usuario u ON d.morador_id = u.id
            WHERE p.status = 'confirmado' ORDER BY p.data_pagamento DESC
        """
        return [Pagamento(**r) for r in db.executar_query(query)]