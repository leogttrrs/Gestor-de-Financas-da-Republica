from __future__ import annotations
from src.database import DatabaseManager
from typing import Optional
from .Administrador import Administrador

class Republica:
    def __init__(self, nome: str = None, administrador: Optional[Administrador] = None, 
                 id: Optional[int] = None, administrador_id: Optional[int] = None, **kwargs):
        self.__id = id
        self.__nome = nome
        self.__administrador = administrador
        
        if administrador is None and administrador_id is not None:
            self.__administrador = Administrador.buscar_por_id(administrador_id)
    
    @property
    def id(self) -> Optional[int]:
        return self.__id
    
    @id.setter
    def id(self, value: int):
        self.__id = value
    
    @property
    def nome(self) -> str:
        return self.__nome
    
    @nome.setter
    def nome(self, value: str):
        if not value or not value.strip():
            raise ValueError("Nome da república não pode ser vazio")
        self.__nome = value
    
    @property
    def administrador(self) -> Administrador:
        return self.__administrador
    
    @administrador.setter
    def administrador(self, value: Administrador):
        if not isinstance(value, Administrador):
            raise TypeError("Administrador deve ser uma instância de Administrador")
        self.__administrador = value
    
    @property
    def administrador_id(self) -> Optional[int]:
        return self.__administrador.id if self.__administrador else None

    def salvar(self) -> Republica:
        db = DatabaseManager()
        if self.id:
            comando = "UPDATE republica SET nome = ?, administrador_id = ? WHERE id = ?"
            params = (self.nome, self.administrador_id, self.id)
            db.executar_comando(comando, params)
        else:
            comando = "INSERT INTO republica (nome, administrador_id) VALUES (?, ?)"
            params = (self.nome, self.administrador_id)
            self.id = db.executar_comando(comando, params)
        return self
    
    def editar(self, novo_nome: str) -> Republica:
        if self.id is None:
            raise ValueError("Não é possível editar uma república sem ID")
        self.nome = novo_nome
        db = DatabaseManager()
        comando = "UPDATE republica SET nome = ? WHERE id = ?"
        params = (self.nome, self.id)
        db.executar_comando(comando, params)
        return self
    
    def excluir(self) -> int:
        if self.id is None:
            return 0
        db = DatabaseManager()
        comando = "DELETE FROM republica WHERE id = ?"
        return db.executar_comando(comando, (self.id,))

    @staticmethod
    def buscar_por_id(republica_id: int) -> Optional[Republica]:
        db = DatabaseManager()
        query = "SELECT * FROM republica WHERE id = ?"
        resultados = db.executar_query(query, (republica_id,))
        return Republica(**resultados[0]) if resultados else None

    @staticmethod
    def buscar_por_admin_id(admin_id: int) -> Optional[Republica]:
        db = DatabaseManager()
        query = "SELECT * FROM republica WHERE administrador_id = ?"
        resultados = db.executar_query(query, (admin_id,))
        return Republica(**resultados[0]) if resultados else None
    
    @staticmethod
    def listar_todas():
        db = DatabaseManager()
        query = "SELECT * FROM republica ORDER BY nome"
        resultados = db.executar_query(query)
        return [Republica(**r) for r in resultados] if resultados else []
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nome': self.nome,
            'administrador': self.administrador.to_dict() if self.administrador else None
        }