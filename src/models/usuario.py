from abc import ABC, abstractmethod
from typing import Tuple
import hashlib
from ..utils.validador import Validador


class Usuario(ABC):
    @abstractmethod
    def __init__(self, cpf: str, nome: str, email: str, telefone: str, genero: str, senhaCriptografada: str = None, id: int = None):
        self.__id = None
        self.__cpf = None
        self.__nome = None
        self.__email = None
        self.__telefone = None
        self.__genero = None
        self.__senhaCriptografada = None
        if isinstance(id, int) or id is None:
            self.__id = id
        if isinstance(cpf, str):
            self.__cpf = cpf
        if isinstance(nome, str):
            self.__nome = nome
        if isinstance(email, str):
            self.__email = email
        if isinstance(telefone, str):
            self.__telefone = telefone
        if isinstance(genero, str) and genero in ['masculino', 'feminino']:
            self.__genero = genero
        if isinstance(senhaCriptografada, str) or senhaCriptografada is None:
            self.__senhaCriptografada = senhaCriptografada

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        if isinstance(cpf, str):
            self.__cpf = cpf

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome):
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email):
        if isinstance(email, str):
            self.__email = email

    @property
    def telefone(self) -> str:
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone):
        if isinstance(telefone, str):
            self.__telefone = telefone

    @property
    def genero(self) -> str:
        return self.__genero

    @genero.setter
    def genero(self, genero):
        if isinstance(genero, str) and genero in ['masculino', 'feminino']:
            self.__genero = genero

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id):
        if isinstance(id, int) or id is None:
            self.__id = id

    @property
    def senhaCriptografada(self) -> str:
        return self.__senhaCriptografada

    @senhaCriptografada.setter
    def senhaCriptografada(self, senha_criptografada):
        if isinstance(senha_criptografada, str):
            self.__senhaCriptografada = senha_criptografada

    def validar_cpf(self, cpf: str) -> bool:
        resultado = Validador.validar_cpf(cpf)
        if isinstance(resultado, str) and ("inválido" in resultado or "Erro" in resultado):
            return False
        return True

    def hash_senha(self, senha: str) -> str:
        return Validador.hash_senha(senha)

    def verificar_senha(self, senha: str) -> bool:
        return self.hash_senha(senha) == self.__senhaCriptografada

    def validar_dados(self) -> Tuple[bool, str]:
        return Validador.validar_dados_usuario(
            self.__cpf, 
            self.__nome, 
            self.__email, 
            self.__telefone, 
            self.__genero
        )

    @abstractmethod
    def salvar(self) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def atualizar(self) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def excluir(self) -> Tuple[bool, str]:
        pass

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'cpf': self.cpf,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'genero': self.genero,
            'senhaCriptografada': self.senhaCriptografada
        }