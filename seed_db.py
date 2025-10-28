from src.database import DatabaseManager
from src.utils.validador import Validador
from datetime import date, timedelta
import sqlite3


def popular_banco():
    """Insere um conjunto completo de dados de teste: admin, república, moradores, quartos, contratos e dívidas."""

    print("Iniciando a população do banco de dados com dados de teste...")
    db_manager = DatabaseManager()

    try:
        # --- 1. CRIAR USUÁRIOS (ADMIN E MORADORES) ---
        print("\n[PASSO 1/5] Criando usuários...")
        usuarios_para_criar = [
            {'cpf': '1', 'nome': 'Admin Padrão', 'email': 'admin@rep.com', 'telefone': '111111111',
             'senha': '1', 'tipo': 'administrador'},
            {'cpf': '11122233344', 'nome': 'João da Silva', 'email': 'joao@email.com', 'telefone': '222222222',
             'senha': 'senha123', 'tipo': 'morador'},
            {'cpf': '55566677788', 'nome': 'Maria Oliveira', 'email': 'maria@email.com', 'telefone': '333333333',
             'senha': 'senha123', 'tipo': 'morador'},
            {'cpf': '99988877766', 'nome': 'Carlos Pereira', 'email': 'carlos@email.com', 'telefone': '444444444',
             'senha': 'senha123', 'tipo': 'morador'}
        ]

        usuarios_ids = {}
        for dados in usuarios_para_criar:
            if not db_manager.executar_query("SELECT id FROM usuario WHERE cpf = ?", (dados['cpf'],)):
                senha_hash = Validador.hash_senha(dados['senha'])
                comando = "INSERT INTO usuario (cpf, nome, email, telefone, senhaCriptografada, tipo_usuario) VALUES (?, ?, ?, ?, ?, ?)"
                params = (dados['cpf'], dados['nome'], dados['email'], dados['telefone'], senha_hash, dados['tipo'])
                user_id = db_manager.executar_comando(comando, params)
                usuarios_ids[dados['nome']] = user_id
                print(f"  - Usuário '{dados['nome']}' criado com sucesso (ID: {user_id}).")
            else:
                user_id = db_manager.executar_query("SELECT id FROM usuario WHERE cpf = ?", (dados['cpf'],))[0]['id']
                usuarios_ids[dados['nome']] = user_id
                print(f"  - Usuário '{dados['nome']}' já existe (ID: {user_id}).")

        # --- 2. CRIAR REPÚBLICA ---
        print("\n[PASSO 2/5] Criando república...")
        admin_id = usuarios_ids['Admin Padrão']
        republica_id = None
        if not db_manager.executar_query("SELECT id FROM republica WHERE administrador_id = ?", (admin_id,)):
            republica_id = db_manager.executar_comando("INSERT INTO republica (nome, administrador_id) VALUES (?, ?)",
                                                       ('República Prime', admin_id))
            print(f"  - República criada com sucesso (ID: {republica_id}).")
        else:
            republica_id = \
            db_manager.executar_query("SELECT id FROM republica WHERE administrador_id = ?", (admin_id,))[0]['id']

        # --- 3. CRIAR QUARTOS ---
        print("\n[PASSO 3/5] Criando quartos...")
        quartos_ids = {}
        for num in [101, 102, 201, 202]:
            if not db_manager.executar_query("SELECT id FROM quarto WHERE numero_quarto = ? AND republica_id = ?",
                                             (num, republica_id)):
                quarto_id = db_manager.executar_comando(
                    "INSERT INTO quarto (numero_quarto, tamanho, republica_id) VALUES (?, ?, ?)",
                    (num, 12, republica_id))
                quartos_ids[num] = quarto_id
                print(f"  - Quarto {num} criado (ID: {quarto_id}).")
            else:
                quartos_ids[num] = \
                db_manager.executar_query("SELECT id FROM quarto WHERE numero_quarto = ? AND republica_id = ?",
                                          (num, republica_id))[0]['id']

        # --- 4. CRIAR CONTRATOS ---
        print("\n[PASSO 4/5] Associando moradores aos quartos...")
        for morador_nome, quarto_num in [('João da Silva', 101), ('Maria Oliveira', 102)]:
            morador_id = usuarios_ids[morador_nome]
            quarto_id = quartos_ids[quarto_num]
            if not db_manager.executar_query("SELECT id FROM contrato WHERE morador_id = ? AND status = 'ativo'",
                                             (morador_id,)):
                db_manager.executar_comando(
                    "INSERT INTO contrato (morador_id, quarto_id, data_inicio, valor_aluguel, status) VALUES (?, ?, ?, ?, 'ativo')",
                    (morador_id, quarto_id, date.today(), 550.00))
                print(f"  - Contrato criado para '{morador_nome}' no quarto {quarto_num}.")

        # --- 5. CRIAR DÍVIDAS E PAGAMENTOS ---
        print("\n[PASSO 5/5] Criando dívidas e pagamentos de exemplo...")
        # Dívida 1: João - já paga (quitada)
        divida_joao_id = db_manager.executar_comando(
            "INSERT INTO divida (morador_id, valor, descricao, data_vencimento, status) VALUES (?, ?, ?, ?, ?)",
            (usuarios_ids['João da Silva'], 150.00, 'Conta de Luz', (date.today() - timedelta(days=5)).isoformat(), 'quitada'))
        print(f"  - Dívida 'Conta de Luz' (quitada) criada para João da Silva (ID: {divida_joao_id}).")
        db_manager.executar_comando(
            "INSERT INTO pagamento (divida_id, valor, data_pagamento, status) VALUES (?, ?, ?, ?)",
            (divida_joao_id, 150.00, date.today().isoformat(), 'confirmado'))
        print(f"  - Pagamento confirmado para 'Conta de Luz'.")

        # Dívida 2: Maria - vencida e pendente
        divida_maria_id = db_manager.executar_comando(
            "INSERT INTO divida (morador_id, valor, descricao, data_vencimento, status) VALUES (?, ?, ?, ?, ?)",
            (usuarios_ids['Maria Oliveira'], 75.50, 'Internet', (date.today() - timedelta(days=15)).isoformat(), 'pendente'))
        print(f"  - Dívida 'Internet' (vencida) criada para Maria Oliveira (ID: {divida_maria_id}).")

        # Dívida 3: Carlos - vencida há mais tempo (pendente)
        divida_carlos_id = db_manager.executar_comando(
            "INSERT INTO divida (morador_id, valor, descricao, data_vencimento, status) VALUES (?, ?, ?, ?, ?)",
            (usuarios_ids['Carlos Pereira'], 200.00, 'Aluguel Atrasado', (date.today() - timedelta(days=40)).isoformat(), 'pendente'))
        print(f"  - Dívida 'Aluguel Atrasado' (vencida) criada para Carlos Pereira (ID: {divida_carlos_id}).")

    except sqlite3.OperationalError as e:
        print(
            f"\nERRO de Tabela: {e}.\nCertifique-se de que o banco de dados 'republica.db' e suas tabelas já foram criados executando o main.py primeiro.")
    except Exception as e:
        print(f"\nUm erro inesperado ocorreu: {e}")

    print("\nPopulação do banco de dados concluída!")


if __name__ == "__main__":
    popular_banco()