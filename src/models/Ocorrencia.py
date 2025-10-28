from __future__ import annotations
from typing import List, Optional, Tuple, Dict
from src.database import DatabaseManager
from datetime import datetime, date
from decimal import Decimal
from .Morador import Morador
from dataclasses import dataclass, field

@dataclass
class Ocorrencia:

    def __init__(self, morador: Morador, titulo: str, descricao: str, data: str, status: str = 'Pendente', id: Optional[int] = None):
        
        self.__id = id
        self.__morador = morador
        self.__titulo = titulo
        self.__descricao = descricao
        self.__status = status
        self.__data = data

    @classmethod
    def from_db_row(cls, row: dict) -> 'Ocorrencia':
        morador = Morador.buscar_por_id(row['morador_id']) if 'morador_id' in row else None
        titulo = row.get('titulo', '')
        descricao = row.get('descricao', '')
        data = row.get('data', '')
        status = row.get('status', 'Pendente')
        id = row.get('id')
        return cls(morador, titulo, descricao, data, status, id)

    
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
    def status(self) -> str:
        return self.__status
    
    @status.setter
    def status(self, value: str):
        if value not in ['Pendente', 'Finalizado']:
            raise ValueError("status deve ser 'Pendente' ou 'Finalizado'")
        self.__status = value

    @property
    def morador_id(self) -> Optional[int]:
        return self.__morador.id if self.__morador else None
    
    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, value: str):
        self.__titulo = value

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, value: str):
        self.__descricao = value
    
    def salvar(self) -> 'Ocorrencia':
        Ocorrencia.criar_tabela_ocorrencia()  # garante que a tabela exista
        db_manager = DatabaseManager()
        if self.id is None:
            comando = """INSERT INTO ocorrencia (morador_id, titulo, descricao, data, status) 
                        VALUES (?, ?, ?, ?, ?)"""
            params = (self.morador_id, self.__titulo, self.__descricao, self.__data, self.status)
            self.id = db_manager.executar_comando(comando, params)
        else:
            comando = """UPDATE ocorrencia SET morador_id = ?, titulo = ?, descricao = ?, data = ?, status = ? 
                        WHERE id = ?"""
            params = (self.morador_id, self.__titulo, self.__descricao, self.__data, self.status, self.id)
            db_manager.executar_comando(comando, params)
        return self


    def excluir(self) -> int:
        if self.id is None:
            return 0
    def finalizar(self):
        self.data_fim = date.today()
        self.status = 'Finalizado'
        self.salvar()


    @staticmethod
    def buscar_todos() -> List['Ocorrencia']:
        db_manager = DatabaseManager()
        query = "SELECT * FROM ocorrencia ORDER BY data_inicio DESC"
        resultados = db_manager.executar_query(query)
        return [Ocorrencia.from_db_row(r) for r in resultados]

    @staticmethod
    def buscar_por_id(ocorrencia_id: int) -> Optional['Ocorrencia']:
        db_manager = DatabaseManager()
        query = "SELECT * FROM ocorrencia WHERE id = ?"
        resultados = db_manager.executar_query(query, (ocorrencia_id,))
        return Ocorrencia.from_db_row(resultados[0]) if resultados else None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'morador': self.morador.to_dict() if self.morador else None,
            
            'titulo': self.__titulo,
            'descricao': self.__descricao,
            'data': self.__data,
            'status': self.status
        }



    def validar_campos(self) -> Tuple[bool, str]:
        """
        Valida os campos essenciais da ocorrência.
        Retorna (True, "") se válido; (False, "mensagem") se inválido.
        Regras:
        - titulo não pode ser vazio
        - descricao não pode ser vazio
        """
        if not (self.titulo and self.titulo.strip()):
            return False, "Título é obrigatório."
        if not (self.descricao and self.descricao.strip()):
            return False, "Descrição é obrigatória."
        return True, ""
        if not (self.descricao and self.descricao.strip()):
            return False, "Descrição é obrigatória."
        return True, ""

    def criar_tabela_ocorrencia():
        db_manager = DatabaseManager()
        
        # Cria a tabela se não existir
        comando = """
        CREATE TABLE IF NOT EXISTS ocorrencia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            morador_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            data TEXT NOT NULL,
            status TEXT NOT NULL
        );
        """
        db_manager.executar_comando(comando)

        colunas_existentes = db_manager.executar_query(
            "PRAGMA table_info(ocorrencia);"
        )
        colunas_existentes = [c['name'] for c in colunas_existentes]

        colunas_necessarias = ['id','morador_id','titulo','descricao','data','status']
        for coluna in colunas_necessarias:
            if coluna not in colunas_existentes:
                comando = f"ALTER TABLE ocorrencia ADD COLUMN {coluna} TEXT;"
                db_manager.executar_comando(comando)
