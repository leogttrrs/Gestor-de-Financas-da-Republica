from __future__ import annotations
from typing import List
from src.database import DatabaseManager
from src.models.Divida import Divida


class Pagamento:
    def __init__(self, divida: Divida, valor: float, data_pagamento: str, status: str, id: int = None, **kwargs):
        self.id = id
        self.divida = divida
        self.valor = valor
        self.data_pagamento = data_pagamento
        self.status = status

    def atualizar_status(self, novo_status: str) -> bool:
        if novo_status not in ['confirmado', 'cancelado', 'pendente']:
            return False
        db = DatabaseManager()
        comando = "UPDATE pagamento SET status = ? WHERE id = ?"
        db.executar_comando(comando, (novo_status, self.id))
        self.status = novo_status
        return True

    def salvar(self) -> Pagamento:
        db = DatabaseManager()
        if self.id:
            comando = "UPDATE pagamento SET divida_id=?, valor=?, data_pagamento=?, status=? WHERE id=?"
            params = (self.divida.id, self.valor, self.data_pagamento, self.status, self.id)
        else:
            comando = "INSERT INTO pagamento (divida_id, valor, data_pagamento, status) VALUES (?, ?, ?, ?)"
            params = (self.divida.id, self.valor, self.data_pagamento, self.status)

        novo_id = db.executar_comando(comando, params)
        if self.id is None:
            self.id = novo_id
        return self

    @staticmethod
    def buscar_por_divida_e_status(divida_id: int, status: str) -> List[Pagamento]:
        db = DatabaseManager()
        query = "SELECT * FROM pagamento WHERE divida_id = ? AND status = ? ORDER BY id DESC"
        resultados = db.executar_query(query, (divida_id, status))

        pagamentos = []
        for row in resultados:
            divida_obj = Divida.buscar_por_id(divida_id)
            if divida_obj:
                pagamento_obj = Pagamento(divida=divida_obj, **row)
                pagamentos.append(pagamento_obj)

        return pagamentos

    @staticmethod
    def buscar_por_morador(morador_id: int) -> List[Pagamento]:
        db = DatabaseManager()
        query = """
            SELECT p.* FROM pagamento p
            JOIN divida d ON p.divida_id = d.id
            WHERE d.morador_id = ?
            ORDER BY p.data_pagamento DESC
        """
        resultados_pagamento = db.executar_query(query, (morador_id,))

        pagamentos = []
        for row in resultados_pagamento:
            divida_obj = Divida.buscar_por_id(row['divida_id'])
            if divida_obj:
                row_copy = dict(row)
                row_copy.pop('divida_id', None)
                pagamento_obj = Pagamento(divida=divida_obj, **row_copy)
                pagamentos.append(pagamento_obj)

        return pagamentos

    @staticmethod
    def buscar_pendentes() -> List[Pagamento]:
        db = DatabaseManager()
        query = "SELECT * FROM pagamento WHERE status = 'pendente'"
        resultados_pagamento = db.executar_query(query)

        pagamentos = []
        for row in resultados_pagamento:
            divida_obj = Divida.buscar_por_id(row['divida_id'])
            if divida_obj:
                row_copy = dict(row)
                row_copy.pop('divida_id', None)
                pagamento_obj = Pagamento(divida=divida_obj, **row_copy)
                pagamentos.append(pagamento_obj)
            else:
                print(f"AVISO: Dívida ID {row['divida_id']} não encontrada para o Pagamento ID {row['id']}")

        return pagamentos