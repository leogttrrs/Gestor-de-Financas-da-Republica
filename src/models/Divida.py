from __future__ import annotations
from typing import List, Optional
from src.database import DatabaseManager
from datetime import date, datetime


class Divida:
    def __init__(self, morador_id: int, valor: float, descricao: str, data_vencimento: str, status: str,
                 data_criacao: str = None, id: int = None, **kwargs):
        self.id = id
        self.morador_id = morador_id
        self.valor = valor
        self.descricao = descricao
        self.data_vencimento = data_vencimento
        self.status = status
        self.data_criacao = data_criacao
        self._nome_morador = None

    @property
    def is_vencida(self) -> bool:
        if self.status == 'pendente':
            try:
                vencimento = datetime.strptime(self.data_vencimento, '%Y-%m-%d').date()
                return date.today() > vencimento
            except (ValueError, TypeError):
                return False
        return False

    def salvar(self) -> Divida:
        db = DatabaseManager()
        if self.id:
            comando = "UPDATE divida SET morador_id=?, valor=?, descricao=?, data_vencimento=?, status=? WHERE id=?"
            params = (self.morador_id, self.valor, self.descricao, self.data_vencimento, self.status, self.id)
        else:
            comando = "INSERT INTO divida (morador_id, valor, descricao, data_vencimento, status) VALUES (?, ?, ?, ?, ?)"
            params = (self.morador_id, self.valor, self.descricao, self.data_vencimento, self.status)
        self.id = db.executar_comando(comando, params)
        return self

    def atualizar_status(self, novo_status: str) -> bool:
        if novo_status not in ['pendente', 'quitada']:
            return False
        db = DatabaseManager()
        comando = "UPDATE divida SET status = ? WHERE id = ?"
        db.executar_comando(comando, (novo_status, self.id))
        self.status = novo_status
        return True

    @staticmethod
    def deletar(divida_id: int) -> int:
        db = DatabaseManager()
        comando = "DELETE FROM divida WHERE id = ?"
        return db.executar_comando(comando, (divida_id,))

    @staticmethod
    def buscar_por_id(divida_id: int) -> Optional[Divida]:
        db = DatabaseManager()
        query = "SELECT * FROM divida WHERE id = ?"
        resultados = db.executar_query(query, (divida_id,))
        return Divida(**resultados[0]) if resultados else None

    @staticmethod
    def buscar_com_filtros(ordenar_por: str, incluir_quitadas: bool) -> List[Divida]:
        db = DatabaseManager()
        query = "SELECT d.*, u.nome as nome_morador FROM divida d JOIN usuario u ON d.morador_id = u.id"
        if not incluir_quitadas:
            query += " WHERE d.status = 'pendente'"

        if ordenar_por == "Morador":
            query += " ORDER BY u.nome ASC"
        elif ordenar_por == "Valor":
            query += " ORDER BY d.valor DESC"
        elif ordenar_por == "Data de Vencimento":
            query += " ORDER BY d.data_vencimento ASC"
        else:
            query += " ORDER BY d.data_criacao DESC"

        resultados = db.executar_query(query)
        dividas = []
        for r in resultados:
            divida = Divida(**r)
            divida._nome_morador = r['nome_morador']
            dividas.append(divida)
        return dividas

    @property
    def nome_morador(self) -> str:
        if self._nome_morador is None:
            if self.morador_id:
                db = DatabaseManager()
                query = "SELECT nome FROM usuario WHERE id = ?"
                resultado = db.executar_query(query, (self.morador_id,))
                self._nome_morador = resultado[0]['nome'] if resultado else "Desconhecido"
            else:
                self._nome_morador = "N/A"
        return self._nome_morador