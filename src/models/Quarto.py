from __future__ import annotations
from typing import List, Optional
from src.database import DatabaseManager

class Quarto:
    def __init__(self, numero_quarto: int, tamanho: int, republica_id: int, id: Optional[int] = None, **kwargs):
        self.id = id
        self.numero_quarto = numero_quarto
        self.tamanho = tamanho
        self.republica_id = republica_id
        self._moradores = None

    @property
    def moradores(self) -> List[str]:
        if self._moradores is None:
            if self.id is None:
                self._moradores = []
                return self._moradores
            db_manager = DatabaseManager()
            query = "SELECT u.nome FROM usuario u JOIN contrato c ON u.id = c.morador_id WHERE c.quarto_id = ? AND c.status = 'ativo'"
            self._moradores = [row['nome'] for row in db_manager.executar_query(query, (self.id,))]
        return self._moradores

    # ANOTAÇÃO: Nova propriedade 'status' que é calculada em tempo real
    @property
    def status(self) -> str:
        return "Ocupado" if self.possui_contratos_ativos() else "Disponível"

    def salvar(self) -> Quarto:
        db_manager = DatabaseManager()
        if self.id is None:
            comando = "INSERT INTO quarto (numero_quarto, tamanho, republica_id) VALUES (?, ?, ?)"
            params = (self.numero_quarto, self.tamanho, self.republica_id)
            self.id = db_manager.executar_comando(comando, params)
        else:
            comando = "UPDATE quarto SET numero_quarto = ?, tamanho = ? WHERE id = ?"
            params = (self.numero_quarto, self.tamanho, self.id)
            db_manager.executar_comando(comando, params)
        return self

    @staticmethod
    def buscar_todos() -> List[Quarto]:
        db_manager = DatabaseManager()
        query = "SELECT * FROM quarto ORDER BY numero_quarto"
        return [Quarto(**r) for r in db_manager.executar_query(query)]

    @staticmethod
    def buscar_por_id(quarto_id: int) -> Optional[Quarto]:
        db_manager = DatabaseManager()
        query = "SELECT * FROM quarto WHERE id = ?"
        resultados = db_manager.executar_query(query, (quarto_id,))
        return Quarto(**resultados[0]) if resultados else None

    @staticmethod
    def deletar(quarto_id: int) -> int:
        db_manager = DatabaseManager()
        comando = "DELETE FROM quarto WHERE id = ?"
        return db_manager.executar_comando(comando, (quarto_id,))

    def possui_contratos_ativos(self) -> bool:
        return len(self.moradores) > 0