from __future__ import annotations
from typing import List
from src.database import DatabaseManager
from datetime import date

class Contrato:
    @staticmethod
    def criar_contrato_simples(morador_id: int, quarto_id: int):
        db_manager = DatabaseManager()
        comando = "INSERT INTO contrato (morador_id, quarto_id, data_inicio, valor_aluguel, status) VALUES (?, ?, ?, ?, 'ativo')"
        parametros = (morador_id, quarto_id, date.today(), 0.00)
        db_manager.executar_comando(comando, parametros)

    @staticmethod
    def buscar_ids_moradores_por_quarto(quarto_id: int) -> List[int]:
        db_manager = DatabaseManager()
        query = "SELECT morador_id FROM contrato WHERE quarto_id = ? AND status = 'ativo'"
        resultados = db_manager.executar_query(query, (quarto_id,))
        return [row['morador_id'] for row in resultados]

    @staticmethod
    def finalizar_contrato(morador_id: int, quarto_id: int):
        db_manager = DatabaseManager()
        comando = "UPDATE contrato SET status = 'finalizado', data_fim = ? WHERE morador_id = ? AND quarto_id = ? AND status = 'ativo'"
        parametros = (date.today(), morador_id, quarto_id)
        db_manager.executar_comando(comando, parametros)