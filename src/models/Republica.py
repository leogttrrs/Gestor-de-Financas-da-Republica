# arquivo: src/models/republica.py

from __future__ import annotations
from src.database import DatabaseManager
from typing import Optional

class Republica:
    def __init__(self, nome: str, administrador_id: int, id: int = None, **kwargs):
        self.id = id
        self.nome = nome
        self.administrador_id = administrador_id

    def salvar(self) -> Republica:
        db = DatabaseManager()
        if self.id:
            comando = "UPDATE republica SET nome = ? WHERE id = ?"
            params = (self.nome, self.id)
            db.executar_comando(comando, params)
        else:
            comando = "INSERT INTO republica (nome, administrador_id) VALUES (?, ?)"
            params = (self.nome, self.administrador_id)
            self.id = db.executar_comando(comando, params)
        return self

    @staticmethod
    def buscar_por_admin_id(admin_id: int) -> Optional[Republica]:
        db = DatabaseManager()
        query = "SELECT * FROM republica WHERE administrador_id = ?"
        resultados = db.executar_query(query, (admin_id,))
        return Republica(**resultados[0]) if resultados else None