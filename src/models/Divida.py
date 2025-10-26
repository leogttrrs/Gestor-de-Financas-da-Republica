from __future__ import annotations
from typing import List, Optional
from src.database import DatabaseManager
from datetime import date, datetime
from src.models.Morador import Morador


class Divida:
    def __init__(self, morador: Morador, valor: float, descricao: str, data_vencimento: str, status: str,
                 id: int = None):
        self.id = id
        self.morador = morador
        self.valor = valor
        self.descricao = descricao
        self.data_vencimento = data_vencimento
        self.status = status

    @property
    def is_vencida(self) -> bool:
        if self.status == 'pendente':
            try:
                vencimento = datetime.strptime(self.data_vencimento, '%Y-%m-%d').date()
                return date.today() > vencimento
            except (ValueError, TypeError):
                return False
        return False

    @property
    def nome_morador(self) -> str:
        if self.morador:
            return self.morador.nome
        return "Desconhecido"

    def salvar(self) -> Divida:
        db = DatabaseManager()
        if not self.morador or not self.morador.id:
            raise ValueError("Morador inválido ou sem ID para salvar a dívida.")

        if self.id:
            comando = "UPDATE divida SET morador_id=?, valor=?, descricao=?, data_vencimento=?, status=? WHERE id=?"
            params = (self.morador.id, self.valor, self.descricao, self.data_vencimento, self.status, self.id)
        else:
            comando = "INSERT INTO divida (morador_id, valor, descricao, data_vencimento, status) VALUES (?, ?, ?, ?, ?)"
            params = (self.morador.id, self.valor, self.descricao, self.data_vencimento, self.status)

        novo_id = db.executar_comando(comando, params)
        if self.id is None: self.id = novo_id
        return self

    def atualizar_status(self, novo_status: str) -> bool:
        if novo_status not in ['pendente', 'quitada']: return False
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
        resultados_divida = db.executar_query(query, (divida_id,))

        if not resultados_divida:
            return None

        dados_divida = resultados_divida[0]

        morador_obj = Morador.buscar_por_id(dados_divida['morador_id'])
        if not morador_obj:
            print(f"AVISO: Morador ID {dados_divida['morador_id']} não encontrado para a Dívida ID {divida_id}")
            return None
        dados_divida.pop('morador_id', None)

        return Divida(morador=morador_obj, **dados_divida)

    @staticmethod
    def buscar_com_filtros(ordenar_por: str, incluir_quitadas: bool) -> List[Divida]:
        db = DatabaseManager()
        query = "SELECT d.* FROM divida d"
        join_usuario = ""
        params = []

        if ordenar_por == "Morador":
            join_usuario = " JOIN usuario u ON d.morador_id = u.id"
            order_clause = " ORDER BY u.nome ASC"
        elif ordenar_por == "Valor":
            order_clause = " ORDER BY d.valor DESC"
        elif ordenar_por == "Data de Vencimento":
            order_clause = " ORDER BY d.data_vencimento ASC"
        else:
            order_clause = " ORDER BY d.data_criacao DESC"

        where_clause = ""
        if not incluir_quitadas:
            where_clause = " WHERE d.status = 'pendente'"

        query += join_usuario + where_clause + order_clause

        resultados = db.executar_query(query, tuple(params))
        dividas = []
        moradores_cache = {}

        for row in resultados:
            morador_id = row['morador_id']
            if morador_id not in moradores_cache:
                moradores_cache[morador_id] = Morador.buscar_por_id(morador_id)

            morador_obj = moradores_cache.get(morador_id)

            if morador_obj:
                row_copy = dict(row)
                row_copy.pop('morador_id', None)
                divida_obj = Divida(morador=morador_obj, **row_copy)
                dividas.append(divida_obj)
            else:
                print(f"AVISO: Morador ID {morador_id} não encontrado para Dívida ID {row['id']}")

        return dividas