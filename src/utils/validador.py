from datetime import datetime
import re


# validador desativado temporativamente
class Validador:
    VALIDAR_CPF = False
    VALIDAR_DATA_NASCIMENTO = True
    VALIDAR_NOME = True

    @staticmethod
    def validar_cpf(cpf=None):
        if cpf is None:
            return "CPF não fornecido."

        if Validador.VALIDAR_CPF:
            try:
                cpf = ''.join(filter(lambda c: c.isdigit(), cpf))
                if len(cpf) != 11:
                    return "CPF inválido! Deve conter 11 dígitos."

                soma = 0
                for i in range(9):
                    soma += int(cpf[i]) * (10 - i)
                resto = soma % 11
                digito1 = 0 if resto < 2 else 11 - resto

                soma = 0
                for i in range(10):
                    soma += int(cpf[i]) * (11 - i)
                resto = soma % 11
                digito2 = 0 if resto < 2 else 11 - resto

                if digito1 != int(cpf[9]) or digito2 != int(cpf[10]):
                    return "CPF inválido! Dígitos verificadores não correspondem."
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
                    # Verificar se o formato é ddmmaaaa
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

            if not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$', nome):
                return "Nome inválido! O nome não pode conter números ou símbolos."

        return nome.title()

    @staticmethod
    def validar_preco(preco):
        if preco is None or preco == '':
            return "inválido: o preço não pode estar vazio."
        try:
            preco_formatado = round(float(preco), 2)
            if preco_formatado < 0:
                return "inválido: o preço não pode ser negativo."
            return preco_formatado
        except (ValueError, TypeError):
            return "inválido: o preço deve ser um número."

    @staticmethod
    def validar_codigo(codigo):
        if codigo is None or codigo == '':
            return "inválido: o código não pode estar vazio."
        try:
            codigo_formatado = int(codigo)
            if codigo_formatado < 0:
                return "inválido: o código não pode ser negativo."
            return codigo_formatado
        except (ValueError, TypeError):
            return "inválido: o código deve ser um número inteiro."
