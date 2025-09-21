from abc import ABC, abstractmethod
from typing import Tuple
import hashlib


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
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        if len(cpf_limpo) != 11:
            return False
        
        if cpf_limpo == cpf_limpo[0] * 11:
            return False
        
        soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        if int(cpf_limpo[9]) != digito1:
            return False
        
        soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        return int(cpf_limpo[10]) == digito2

    def hash_senha(self, senha: str) -> str:
        return hashlib.sha256(senha.encode()).hexdigest()

    def verificar_senha(self, senha: str) -> bool:
        return self.hash_senha(senha) == self.__senhaCriptografada

    def validar_dados(self) -> Tuple[bool, str]:
        if not self.__nome or len(self.__nome.strip()) < 2:
            return False, "Nome deve ter pelo menos 2 caracteres"
        
        if not self.validar_cpf(self.__cpf):
            return False, "CPF inválido"
        
        if not self.__telefone or len(self.__telefone.strip()) < 10:
            return False, "Telefone deve ter pelo menos 10 dígitos"
        
        if self.__genero not in ['masculino', 'feminino']:
            return False, "Gênero deve ser 'masculino' ou 'feminino'"
        
        return True, "Dados válidos"

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