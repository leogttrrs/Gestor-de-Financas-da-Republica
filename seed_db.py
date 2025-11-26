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
            {'cpf': '12345678909', 'nome': 'Admin Padrão', 'email': 'admin@republica.com', 'telefone': '11987654321',
             'senha': 'Admin123', 'tipo': 'administrador'},
            {'cpf': '98765432100', 'nome': 'João da Silva', 'email': 'joao.silva@email.com', 'telefone': '11912345678',
             'senha': 'Joao123', 'tipo': 'morador'},
            {'cpf': '11122233344', 'nome': 'Maria Oliveira', 'email': 'maria.oliveira@email.com', 'telefone': '11923456789',
             'senha': 'Maria123', 'tipo': 'morador'},
            {'cpf': '55566677788', 'nome': 'Carlos Pereira', 'email': 'carlos.pereira@email.com', 'telefone': '11934567890',
             'senha': 'Carlos123', 'tipo': 'morador'}
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
        print("\n[PASSO 4/5] Criando contratos (ativos, agendados e finalizados)...")
        
        # Contrato ATIVO - João no quarto 101 (morador com dívida quitada)
        if not db_manager.executar_query("SELECT id FROM contrato WHERE morador_id = ? AND quarto_id = ? AND status = 'ativo'",
                                         (usuarios_ids['João da Silva'], quartos_ids[101])):
            db_manager.executar_comando(
                "INSERT INTO contrato (morador_id, quarto_id, data_inicio, data_fim, valor_aluguel, status) VALUES (?, ?, ?, ?, ?, 'ativo')",
                (usuarios_ids['João da Silva'], quartos_ids[101], date.today() - timedelta(days=90), 
                 date.today() + timedelta(days=275), 550.00))
            print(f"  - Contrato ATIVO criado para João da Silva no quarto 101.")
        
        # Contrato ATIVO - Maria no quarto 102 (morador com dívida vencida)
        if not db_manager.executar_query("SELECT id FROM contrato WHERE morador_id = ? AND quarto_id = ? AND status = 'ativo'",
                                         (usuarios_ids['Maria Oliveira'], quartos_ids[102])):
            db_manager.executar_comando(
                "INSERT INTO contrato (morador_id, quarto_id, data_inicio, data_fim, valor_aluguel, status) VALUES (?, ?, ?, ?, ?, 'ativo')",
                (usuarios_ids['Maria Oliveira'], quartos_ids[102], date.today() - timedelta(days=60), 
                 date.today() + timedelta(days=305), 600.00))
            print(f"  - Contrato ATIVO criado para Maria Oliveira no quarto 102.")
        
        # Contrato AGENDADO - Carlos no quarto 201 (morador com dívida vencida)
        if not db_manager.executar_query("SELECT id FROM contrato WHERE morador_id = ? AND quarto_id = ? AND status = 'agendado'",
                                         (usuarios_ids['Carlos Pereira'], quartos_ids[201])):
            db_manager.executar_comando(
                "INSERT INTO contrato (morador_id, quarto_id, data_inicio, data_fim, valor_aluguel, status) VALUES (?, ?, ?, ?, ?, 'agendado')",
                (usuarios_ids['Carlos Pereira'], quartos_ids[201], date.today() + timedelta(days=30), 
                 date.today() + timedelta(days=395), 580.00))
            print(f"  - Contrato AGENDADO criado para Carlos Pereira no quarto 201 (início em 30 dias).")
        
        # Contrato FINALIZADO - João no quarto 202 (contrato passado, sem dívidas)
        if not db_manager.executar_query("SELECT id FROM contrato WHERE morador_id = ? AND quarto_id = ? AND status = 'finalizado'",
                                         (usuarios_ids['João da Silva'], quartos_ids[202])):
            db_manager.executar_comando(
                "INSERT INTO contrato (morador_id, quarto_id, data_inicio, data_fim, valor_aluguel, status) VALUES (?, ?, ?, ?, ?, 'finalizado')",
                (usuarios_ids['João da Silva'], quartos_ids[202], date.today() - timedelta(days=400), 
                 date.today() - timedelta(days=35), 520.00))
            print(f"  - Contrato FINALIZADO criado para João da Silva no quarto 202 (encerrado há 35 dias).")

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