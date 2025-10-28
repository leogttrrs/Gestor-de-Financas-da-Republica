from __future__ import annotations
from typing import List, Optional
from src.database import DatabaseManager
from .Morador import Morador
from .Republica import Republica

class Quarto:
    def __init__(self, numero_quarto: int, tamanho: int, republica: Republica, id: Optional[int] = None):
        self.__id = id
        self.__numero_quarto = numero_quarto
        self.__tamanho = tamanho
        self.__republica = republica

    @classmethod
    def from_db_row(cls, row: dict) -> 'Quarto':
        republica = Republica.buscar_por_id(row['republica_id']) if 'republica_id' in row else None
        numero_quarto = row.get('numero_quarto')
        tamanho = row.get('tamanho')
        id = row.get('id')
        return cls(numero_quarto, tamanho, republica, id)
    
    @property
    def id(self) -> Optional[int]:
        return self.__id
    
    @id.setter
    def id(self, value: int):
        self.__id = value
    
    @property
    def numero_quarto(self) -> int:
        return self.__numero_quarto
    
    @numero_quarto.setter
    def numero_quarto(self, value: int):
        if value <= 0:
            raise ValueError("Número do quarto deve ser maior que zero")
        self.__numero_quarto = value
    
    @property
    def tamanho(self) -> int:
        return self.__tamanho
    
    @tamanho.setter
    def tamanho(self, value: int):
        if value <= 0:
            raise ValueError("Tamanho do quarto deve ser maior que zero")
        self.__tamanho = value
    
    @property
    def republica(self) -> 'Republica':
        return self.__republica
    
    @republica.setter
    def republica(self, value: 'Republica'):
        from .Republica import Republica
        if not isinstance(value, Republica):
            raise TypeError("Republica deve ser uma instância de Republica")
        self.__republica = value
    
    @property
    def republica_id(self) -> Optional[int]:
        return self.__republica.id if self.__republica else None

    @property
    def morador(self) -> List['Morador']:
        if not hasattr(self, '_Quarto__moradores_cache'):
            self.__moradores_cache = None
        if self.__moradores_cache is None:
            if self.id is None:
                self.__moradores_cache = []
                return self.__moradores_cache
            from .Morador import Morador
            db_manager = DatabaseManager()
            query = """SELECT u.* FROM usuario u 
                      JOIN contrato c ON u.id = c.morador_id 
                      WHERE c.quarto_id = ? AND c.status = 'ativo'"""
            resultados = db_manager.executar_query(query, (self.id,))
            self.__moradores_cache = [Morador(**r) for r in resultados]
        return self.__moradores_cache

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
            comando = "UPDATE quarto SET numero_quarto = ?, tamanho = ?, republica_id = ? WHERE id = ?"
            params = (self.numero_quarto, self.tamanho, self.republica_id, self.id)
            db_manager.executar_comando(comando, params)
        self.__moradores_cache = None
        return self
    
    def editar(self, numero_quarto: int = None, tamanho: int = None) -> Quarto:
        if self.id is None:
            raise ValueError("Não é possível editar um quarto sem ID")
        if numero_quarto is not None:
            self.numero_quarto = numero_quarto
        if tamanho is not None:
            self.tamanho = tamanho
        db_manager = DatabaseManager()
        comando = "UPDATE quarto SET numero_quarto = ?, tamanho = ? WHERE id = ?"
        params = (self.numero_quarto, self.tamanho, self.id)
        db_manager.executar_comando(comando, params)
        return self


    @staticmethod
    def buscar_todos() -> List['Quarto']:
        db_manager = DatabaseManager()
        query = "SELECT * FROM quarto ORDER BY numero_quarto"
        return [Quarto.from_db_row(r) for r in db_manager.executar_query(query)]


    @staticmethod
    def buscar_por_id(quarto_id: int) -> Optional['Quarto']:
        db_manager = DatabaseManager()
        query = "SELECT * FROM quarto WHERE id = ?"
        resultados = db_manager.executar_query(query, (quarto_id,))
        return Quarto.from_db_row(resultados[0]) if resultados else None
    

    @staticmethod
    def buscar_por_numero(numero_quarto: int, republica_id: int) -> Optional['Quarto']:
        db_manager = DatabaseManager()
        query = "SELECT * FROM quarto WHERE numero_quarto = ? AND republica_id = ?"
        resultados = db_manager.executar_query(query, (numero_quarto, republica_id))
        return Quarto.from_db_row(resultados[0]) if resultados else None

    @staticmethod
    def deletar(quarto_id: int) -> int:
        db_manager = DatabaseManager()

        query_ativos = "SELECT COUNT(*) as total FROM contrato WHERE quarto_id = ? AND status = 'ativo'"
        contratos_ativos = db_manager.executar_query(query_ativos, (quarto_id,))[0]['total']

        if contratos_ativos > 0:
            raise ValueError("Não é possível excluir um quarto com contratos ativos.")

        query_finalizados = "SELECT COUNT(*) as total FROM contrato WHERE quarto_id = ? AND status = 'finalizado'"
        contratos_finalizados = db_manager.executar_query(query_finalizados, (quarto_id,))[0]['total']

        if contratos_finalizados > 0:
            comando_update = "UPDATE contrato SET quarto_id = NULL WHERE quarto_id = ? AND status = 'finalizado'"
            db_manager.executar_comando(comando_update, (quarto_id,))

        comando = "DELETE FROM quarto WHERE id = ?"
        return db_manager.executar_comando(comando, (quarto_id,))
    
    def excluir(self) -> int:
        if self.id is None:
            return 0
        return Quarto.deletar(self.id)

    def possui_contratos_ativos(self) -> bool:
        if self.id is None:
            return False

        db_manager = DatabaseManager()
        query = """SELECT COUNT(*) as total FROM contrato 
                  WHERE quarto_id = ? AND status = 'ativo'"""
        resultado = db_manager.executar_query(query, (self.id,))
        return resultado[0]['total'] > 0 if resultado else False

    def possui_contratos_finalizados(self) -> bool:
        if self.id is None:
            return False

        db_manager = DatabaseManager()
        query = """SELECT COUNT(*) as total FROM contrato 
                  WHERE quarto_id = ? AND status = 'finalizado'"""
        resultado = db_manager.executar_query(query, (self.id,))
        return resultado[0]['total'] > 0 if resultado else False

    def obter_vagas_disponiveis(self) -> int:
        contratos_ativos = len(self.morador)
        return max(0, self.tamanho - contratos_ativos)
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'numero_quarto': self.numero_quarto,
            'tamanho': self.tamanho,
            'republica': self.republica.to_dict() if self.republica else None,
            'status': self.status
        }