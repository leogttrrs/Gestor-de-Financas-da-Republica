from datetime import datetime
import re
import hashlib
from typing import Tuple


class Validador:
    VALIDAR_CPF = False
    VALIDAR_DATA_NASCIMENTO = False
    VALIDAR_NOME = False
    VALIDAR_TELEFONE = False
    VALIDAR_EMAIL = False
    VALIDAR_SENHA = False
    VALIDAR_DADOS_USUARIO = False
    VALIDAR_PRECO = False
    VALIDAR_CODIGO = False

    @staticmethod
    def validar_cpf(cpf=None):
        if cpf is None:
            return "CPF não fornecido."

        if Validador.VALIDAR_CPF:
            try:
                cpf = re.sub(r'[^0-9]', '', cpf)
                
                if len(cpf) != 11:
                    return "CPF inválido! Deve conter 11 dígitos."
                
                if cpf == cpf[0] * 11:
                    return "CPF inválido!"
                
                soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
                primeiro_digito = 11 - (soma % 11)
                if primeiro_digito >= 10:
                    primeiro_digito = 0
                
                if int(cpf[9]) != primeiro_digito:
                    return "CPF inválido!"
                
                soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
                segundo_digito = 11 - (soma % 11)
                if segundo_digito >= 10:
                    segundo_digito = 0
                
                if int(cpf[10]) != segundo_digito:
                    return "CPF inválido!"
                    
            except ValueError:
                return "Erro ao validar CPF!"

        return cpf

    @staticmethod
    def validar_data_nascimento(data_nasc=None):
        if data_nasc is None:
            return "Data de nascimento não fornecida."

        if Validador.VALIDAR_DATA_NASCIMENTO:
            try:
                if '/' in data_nasc:
                    if len(data_nasc) != 10:
                        return "Formato de data inválido! Use dd/mm/aaaa ou ddmmaaaa."
                    data = datetime.strptime(data_nasc, '%d/%m/%Y').date()
                else:
                    if len(data_nasc) != 8:
                        return "Formato de data inválido! Use dd/mm/aaaa ou ddmmaaaa."
                    data = datetime.strptime(data_nasc, '%d%m%Y').date()

                if data > datetime.today().date():
                    return "Data inválida! A data de nascimento não pode ser no futuro."

                return data.strftime('%d/%m/%Y')
            except ValueError:
                return "Formato de data inválido! Use dd/mm/aaaa ou ddmmaaaa."

        return data_nasc

    @staticmethod
    def validar_nome(nome=None):
        if nome is None:
            return "Nome não fornecido."

        if Validador.VALIDAR_NOME:
            if not isinstance(nome, str) or not nome:
                return "Nome inválido! O nome não pode estar vazio."

            if len(nome.strip()) < 2:
                return "Nome deve ter pelo menos 2 caracteres."

            if not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$', nome):
                return "Nome inválido! O nome não pode conter números ou símbolos."

        return nome.title()

    @staticmethod
    def validar_telefone(telefone):
        if telefone is None:
            return "Telefone não fornecido."

        if Validador.VALIDAR_TELEFONE:
            telefone_limpo = re.sub(r'[^0-9]', '', telefone)
            
            if len(telefone_limpo) not in [10, 11] or not telefone_limpo.isdigit():
                return "Telefone inválido."

        return telefone

    @staticmethod
    def validar_email(email):
        if email is None:
            return "Email não fornecido."

        if Validador.VALIDAR_EMAIL:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email):
                return "Email inválido."

        return email

    @staticmethod
    def validar_dados_usuario(cpf, nome, email, telefone, genero):
        if Validador.VALIDAR_DADOS_USUARIO:
            if not cpf or not nome or not email or not telefone or not genero:
                return False, "Todos os campos são obrigatórios"
            
            cpf_validado = Validador.validar_cpf(cpf)
            if "inválido" in str(cpf_validado) or "Erro" in str(cpf_validado):
                return False, "CPF inválido"
            
            nome_validado = Validador.validar_nome(nome)
            if "inválido" in str(nome_validado) or "deve ter" in str(nome_validado):
                return False, str(nome_validado)
            
            email_validado = Validador.validar_email(email)
            if "inválido" in str(email_validado):
                return False, "Email inválido"
            
            telefone_validado = Validador.validar_telefone(telefone)
            if "inválido" in str(telefone_validado):
                return False, "Telefone inválido"
            
            if genero.lower() not in ['masculino', 'feminino']:
                return False, "Gênero deve ser 'masculino' ou 'feminino'"
        
        return True, "Dados válidos"

    @staticmethod
    def validar_senha(senha):
        if senha is None:
            return False, "Senha não fornecida."

        if Validador.VALIDAR_SENHA:
            if len(senha) < 6:
                return False, "Senha deve ter pelo menos 6 caracteres"
            
            if not re.search(r'[A-Za-z]', senha):
                return False, "Senha deve conter pelo menos uma letra"
            
            if not re.search(r'[0-9]', senha):
                return False, "Senha deve conter pelo menos um número"
        
        return True, "Senha válida"

    @staticmethod
    def hash_senha(senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    @staticmethod
    def validar_preco(preco):
        if preco is None or preco == '':
            return "inválido: o preço não pode estar vazio."
        
        if Validador.VALIDAR_PRECO:
            try:
                preco_formatado = round(float(preco), 2)
                if preco_formatado < 0:
                    return "inválido: o preço não pode ser negativo."
                return preco_formatado
            except (ValueError, TypeError):
                return "inválido: o preço deve ser um número."
        
        return preco

    @staticmethod
    def validar_codigo(codigo):
        if codigo is None or codigo == '':
            return "inválido: o código não pode estar vazio."
        
        if Validador.VALIDAR_CODIGO:
            try:
                codigo_formatado = int(codigo)
                if codigo_formatado < 0:
                    return "inválido: o código não pode ser negativo."
                return codigo_formatado
            except (ValueError, TypeError):
                return "inválido: o código deve ser um número inteiro."
        
        return codigo
