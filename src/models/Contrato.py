from __future__ import annotations
from typing import List, Optional
from src.database import DatabaseManager
from datetime import datetime, date
from decimal import Decimal
from .Morador import Morador
from .Quarto import Quarto

class Contrato:

    def __init__(self, morador: Morador, quarto: Quarto, data_inicio: date, valor_aluguel: Decimal, 
                 data_fim: Optional[date] = None, status: str = 'ativo', id: Optional[int] = None):
        self.__id = id
        self.__morador = morador
        self.__quarto = quarto
        self.__data_inicio = data_inicio
        self.__data_fim = data_fim
        self.__valor_aluguel = valor_aluguel
        self.__status = status

    @classmethod
    def from_db_row(cls, row: dict) -> 'Contrato':
        morador = Morador.buscar_por_id(row['morador_id']) if 'morador_id' in row else None
        quarto = Quarto.buscar_por_id(row['quarto_id']) if 'quarto_id' in row else None
        data_inicio = row.get('data_inicio')
        data_fim = row.get('data_fim')
        if isinstance(data_inicio, str):
            try:
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            except ValueError:
                try:
                    data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d %H:%M:%S').date()
                except Exception:
                    data_inicio = None
        if isinstance(data_fim, str):
            try:
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            except ValueError:
                try:
                    data_fim = datetime.strptime(data_fim, '%Y-%m-%d %H:%M:%S').date()
                except Exception:
                    data_fim = None
        valor_aluguel = row.get('valor_aluguel')
        status = row.get('status', 'ativo')
        id = row.get('id')
        return cls(morador, quarto, data_inicio, valor_aluguel, data_fim, status, id)
    
    @property
    def id(self) -> Optional[int]:
        return self.__id
    
    @id.setter
    def id(self, value: int):
        self.__id = value
    
    @property
    def morador(self) -> Morador:
        return self.__morador
    
    @morador.setter
    def morador(self, value: Morador):
        if not isinstance(value, Morador):
            raise TypeError("Morador deve ser uma instância de Morador")
        self.__morador = value
    
    @property
    def quarto(self) -> Quarto:
        return self.__quarto
    
    @quarto.setter
    def quarto(self, value: Quarto):
        if not isinstance(value, Quarto):
            raise TypeError("Quarto deve ser uma instância de Quarto")
        self.__quarto = value
    
    @property
    def data_inicio(self) -> date:
        return self.__data_inicio
    
    @data_inicio.setter
    def data_inicio(self, value: date):
        if not isinstance(value, date):
            raise TypeError("data_inicio deve ser uma instância de date")
        self.__data_inicio = value
    
    @property
    def data_fim(self) -> Optional[date]:
        return self.__data_fim
    
    @data_fim.setter
    def data_fim(self, value: Optional[date]):
        if value is not None and not isinstance(value, date):
            raise TypeError("data_fim deve ser uma instância de date ou None")
        self.__data_fim = value
    
    @property
    def valor_aluguel(self) -> Decimal:
        return self.__valor_aluguel
    
    @valor_aluguel.setter
    def valor_aluguel(self, value: Decimal):
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
        if value < 0:
            raise ValueError("valor_aluguel deve ser maior ou igual a zero")
        self.__valor_aluguel = value
    
    @property
    def status(self) -> str:
        return self.__status
    
    @status.setter
    def status(self, value: str):
        if value not in ['ativo', 'agendado', 'finalizado']:
            raise ValueError("status deve ser 'ativo', 'agendado' ou 'finalizado'")
        self.__status = value
    
    @property
    def morador_id(self) -> Optional[int]:
        return self.__morador.id if self.__morador else None
    
    @property
    def quarto_id(self) -> Optional[int]:
        return self.__quarto.id if self.__quarto else None

    def salvar(self) -> 'Contrato':
        db_manager = DatabaseManager()
        if self.id is None:
            comando = """INSERT INTO contrato (morador_id, quarto_id, data_inicio, 
                        data_fim, valor_aluguel, status) VALUES (?, ?, ?, ?, ?, ?)"""
            params = (self.morador_id, self.quarto_id, self.data_inicio, 
                     self.data_fim, float(self.valor_aluguel), self.status)
            self.id = db_manager.executar_comando(comando, params)
            
        else:
            comando = """UPDATE contrato SET morador_id = ?, quarto_id = ?, 
                        data_inicio = ?, data_fim = ?, valor_aluguel = ?, status = ? 
                        WHERE id = ?"""
            params = (self.morador_id, self.quarto_id, self.data_inicio,
                     self.data_fim, float(self.valor_aluguel), self.status, self.id)
            db_manager.executar_comando(comando, params)
        return self

    def excluir(self) -> int:
        if self.id is None:
            return 0
        db_manager = DatabaseManager()
        comando = "DELETE FROM contrato WHERE id = ?"
        return db_manager.executar_comando(comando, (self.id,))

    def finalizar(self):
        self.data_fim = date.today()
        self.status = 'finalizado'
        self.salvar()

    @staticmethod
    def buscar_todos() -> List['Contrato']:
        db_manager = DatabaseManager()
        query = "SELECT * FROM contrato ORDER BY data_inicio DESC"
        resultados = db_manager.executar_query(query)
        return [Contrato.from_db_row(r) for r in resultados]

    @staticmethod
    def buscar_por_quarto(quarto_id: int) -> List['Contrato']:
        db_manager = DatabaseManager()
        query = "SELECT * FROM contrato WHERE quarto_id = ? ORDER BY data_inicio DESC"
        resultados = db_manager.executar_query(query, (quarto_id,))
        return [Contrato.from_db_row(r) for r in resultados]

    @staticmethod
    def buscar_ativos() -> List['Contrato']:
        db_manager = DatabaseManager()
        query = "SELECT * FROM contrato WHERE status = 'ativo' ORDER BY data_inicio DESC"
        resultados = db_manager.executar_query(query)

        if not resultados:
            return []

        return [Contrato.from_db_row(r) for r in resultados]

    @staticmethod
    def buscar_por_id(contrato_id: int) -> Optional['Contrato']:
        db_manager = DatabaseManager()
        query = "SELECT * FROM contrato WHERE id = ?"
        resultados = db_manager.executar_query(query, (contrato_id,))
        return Contrato.from_db_row(resultados[0]) if resultados else None
    
    @staticmethod
    def existe_contrato_vigente_para_morador(morador_id: int, data_referencia: date) -> bool:

        if isinstance(data_referencia, str):
            for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
                try:
                    data_referencia = datetime.strptime(data_referencia, fmt).date()
                    break
                except ValueError:
                    continue
            else:
                return False

        db = DatabaseManager()
        query = """
            SELECT 1
              FROM contrato
             WHERE morador_id = ?
               AND status IN ('ativo', 'agendado')
               AND (data_fim IS NULL OR DATE(data_fim) >= DATE(?))
             LIMIT 1
        """
        rows = db.executar_query(query, (morador_id, data_referencia.isoformat()))
        return bool(rows)

    @staticmethod
    def existe_contrato_vigente_para_quarto(quarto_id: int, data_referencia: date) -> bool:
        if isinstance(data_referencia, str):
            for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
                try:
                    data_referencia = datetime.strptime(data_referencia, fmt).date()
                    break
                except ValueError:
                    continue
            else:
                return False

        db = DatabaseManager()
        query = """
            SELECT 1
              FROM contrato
             WHERE quarto_id = ?
               AND status IN ('ativo', 'agendado')
               AND (data_fim IS NULL OR DATE(data_fim) >= DATE(?))
             LIMIT 1
        """
        rows = db.executar_query(query, (quarto_id, data_referencia.isoformat()))
        return bool(rows)


    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'morador': self.morador.to_dict() if self.morador else None,
            'quarto': self.quarto.to_dict() if self.quarto else None,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'valor_aluguel': float(self.valor_aluguel),
            'status': self.status
        }
