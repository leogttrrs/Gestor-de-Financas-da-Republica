from src.database import DatabaseManager
from src.utils.validador import Validador
from datetime import date, timedelta
import sqlite3


def popular_dividas():
    """Popula apenas a tabela de dívidas (e pagamentos relacionados) com exemplos:
    - uma dívida quitada com pagamento confirmado
    - duas dívidas vencidas e pendentes
    Se os moradores não existirem, serão criados com senhas padrão.
    """
    print("Iniciando seed de dívidas...")
    db = DatabaseManager()

    try:
        moradores_exemplo = [
            { 'cpf': '11122233344', 'nome': 'João da Silva', 'email': 'joao@email.com', 'telefone': '222222222', 'senha': 'senha123' },
            { 'cpf': '55566677788', 'nome': 'Maria Oliveira', 'email': 'maria@email.com', 'telefone': '333333333', 'senha': 'senha123' },
            { 'cpf': '99988877766', 'nome': 'Carlos Pereira', 'email': 'carlos@email.com', 'telefone': '444444444', 'senha': 'senha123' }
        ]

        moradores_ids = {}
        for m in moradores_exemplo:
            encontrado = db.executar_query("SELECT id FROM usuario WHERE cpf = ?", (m['cpf'],))
            if encontrado:
                moradores_ids[m['nome']] = encontrado[0]['id']
                print(f"  - Morador existente: {m['nome']} (ID: {moradores_ids[m['nome']]})")
            else:
                senha_hash = Validador.hash_senha(m['senha'])
                comando = "INSERT INTO usuario (cpf, nome, email, telefone, senhaCriptografada, tipo_usuario) VALUES (?, ?, ?, ?, ?, ?)"
                params = (m['cpf'], m['nome'], m['email'], m['telefone'], senha_hash, 'morador')
                novo_id = db.executar_comando(comando, params)
                moradores_ids[m['nome']] = novo_id
                print(f"  - Morador criado: {m['nome']} (ID: {novo_id})")

        # Dívida quitada para João
        joao_id = moradores_ids['João da Silva']
        divida_joao = db.executar_comando(
            "INSERT INTO divida (morador_id, valor, descricao, data_vencimento, status) VALUES (?, ?, ?, ?, ?)",
            (joao_id, 150.00, 'Conta de Luz', (date.today() - timedelta(days=5)).isoformat(), 'quitada')
        )
        print(f"  - Dívida quitada criada para João (ID dívida: {divida_joao})")
        db.executar_comando(
            "INSERT INTO pagamento (divida_id, valor, data_pagamento, status) VALUES (?, ?, ?, ?)",
            (divida_joao, 150.00, date.today().isoformat(), 'confirmado')
        )
        print("  - Pagamento confirmado registrado para a dívida de João")

        # Dívida vencida para Maria (pendente)
        maria_id = moradores_ids['Maria Oliveira']
        divida_maria = db.executar_comando(
            "INSERT INTO divida (morador_id, valor, descricao, data_vencimento, status) VALUES (?, ?, ?, ?, ?)",
            (maria_id, 75.50, 'Internet', (date.today() - timedelta(days=15)).isoformat(), 'pendente')
        )
        print(f"  - Dívida vencida criada para Maria (ID dívida: {divida_maria})")

        # Dívida vencida para Carlos (pendente)
        carlos_id = moradores_ids['Carlos Pereira']
        divida_carlos = db.executar_comando(
            "INSERT INTO divida (morador_id, valor, descricao, data_vencimento, status) VALUES (?, ?, ?, ?, ?)",
            (carlos_id, 200.00, 'Aluguel Atrasado', (date.today() - timedelta(days=40)).isoformat(), 'pendente')
        )
        print(f"  - Dívida vencida criada para Carlos (ID dívida: {divida_carlos})")

    except sqlite3.OperationalError as e:
        print(f"Erro de tabela/DB: {e} - verifique se as tabelas estão criadas (execute main.py primeiro)")
    except Exception as e:
        print(f"Erro ao popular dívidas: {e}")

    print("Seed de dívidas concluída.")


if __name__ == '__main__':
    popular_dividas()
