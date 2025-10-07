from src.database import DatabaseManager
from src.utils.validador import Validador
from datetime import date


def popular_banco():
    print("Populando banco de dados com dados de teste...")
    db_manager = DatabaseManager()

    print("\n[Passo 1 de 3] Criando moradores...")
    moradores_para_criar = [
        {'cpf': '11122233344', 'nome': 'João da Silva', 'email': 'joao@email.com', 'telefone': '48999887766', 'senha': 'senha123'},
        {'cpf': '55566677788', 'nome': 'Maria Oliveira', 'email': 'maria@email.com', 'telefone': '48988776655', 'senha': 'senha123'},
        {'cpf': '99988877766', 'nome': 'Carlos Pereira', 'email': 'carlos@email.com', 'telefone': '48977665544', 'senha': 'senha123'}
    ]

    moradores_ids = {}
    for dados_morador in moradores_para_criar:
        try:
            # Verifica se o usuário já existe
            query_user = "SELECT id FROM usuario WHERE cpf = ?"
            resultado = db_manager.executar_query(query_user, (dados_morador['cpf'],))

            if resultado:
                usuario_id = resultado[0]['id']
                print(f"  - Morador '{dados_morador['nome']}' já existe (ID: {usuario_id}).")
            else:
                senha_hash = Validador.hash_senha(dados_morador['senha'])
                comando_usuario = "INSERT INTO usuario (cpf, nome, email, telefone, tipo_usuario, senhaCriptografada) VALUES (?, ?, ?, ?, ?, ?)"
                params_usuario = (dados_morador['cpf'], dados_morador['nome'], dados_morador['email'],
                                  dados_morador['telefone'], 'morador', senha_hash)
                usuario_id = db_manager.executar_comando(comando_usuario, params_usuario)
                print(f"  - Morador '{dados_morador['nome']}' criado com sucesso (ID: {usuario_id}).")

            moradores_ids[dados_morador['nome']] = usuario_id

        except Exception as e:
            print(f"  - Ocorreu um erro ao criar o morador '{dados_morador['nome']}': {e}")

    # --- 2. CRIAR QUARTO ---
    print("\n[Passo 2 de 3] Criando quarto de teste...")
    quarto_id = None
    try:
        admin_cpf = '00000000000'
        query_admin = "SELECT id FROM usuario WHERE cpf = ? AND tipo_usuario = 'administrador'"
        resultado_admin = db_manager.executar_query(query_admin, (admin_cpf,))

        if resultado_admin:
            admin_id = resultado_admin[0]['id']
            print(f"  - Administrador existente encontrado (ID: {admin_id}).")
        else:
            senha_admin = Validador.hash_senha('admin123')
            comando_admin = "INSERT INTO usuario (cpf, nome, email, telefone, tipo_usuario, senhaCriptografada) VALUES (?, ?, ?, ?, ?, ?)"
            params_admin = (admin_cpf, 'Admin Teste', 'admin@republica.com', '0000000000', 'administrador', senha_admin)
            admin_id = db_manager.executar_comando(comando_admin, params_admin)
            print(f"  - Administrador de teste criado (ID: {admin_id}).")

        query_rep = "SELECT id FROM republica WHERE administrador_id = ?"
        resultado_rep = db_manager.executar_query(query_rep, (admin_id,))
        if resultado_rep:
            republica_id = resultado_rep[0]['id']
            print(f"  - República já existe (ID: {republica_id}).")
        else:
            comando_rep = "INSERT INTO republica (nome, administrador_id) VALUES (?, ?)"
            republica_id = db_manager.executar_comando(comando_rep, ('Republica Teste', admin_id))
            print(f"  - República criada (ID: {republica_id}).")

        query_quarto = "SELECT id FROM quarto WHERE numero_quarto = ? AND republica_id = ?"
        resultado = db_manager.executar_query(query_quarto, (100, republica_id))

        if resultado:
            quarto_id = resultado[0]['id']
            print(f"  - Quarto 100 já existe (ID: {quarto_id}).")
        else:
            comando_quarto = "INSERT INTO quarto (numero_quarto, tamanho, republica_id) VALUES (?, ?, ?)"
            params_quarto = (100, 12, republica_id)
            quarto_id = db_manager.executar_comando(comando_quarto, params_quarto)
            print(f"  - Quarto 100 criado com sucesso (ID: {quarto_id}).")
    except Exception as e:
        print(f"  - Ocorreu um erro ao criar o quarto 100: {e}")

    # --- 3. CRIAR CONTRATO ---
    print("\n[Passo 3 de 3] Associando morador ao quarto...")
    if quarto_id and moradores_ids.get("João da Silva"):
        morador_id = moradores_ids["João da Silva"]
        try:
            query_contrato = "SELECT id FROM contrato WHERE morador_id = ? AND status = 'ativo'"
            resultado = db_manager.executar_query(query_contrato, (morador_id,))

            if resultado:
                print(f"  - Morador 'João da Silva' já possui um contrato ativo.")
            else:
                comando_contrato = "INSERT INTO contrato (morador_id, quarto_id, data_inicio, valor_aluguel, status) VALUES (?, ?, ?, ?, 'ativo')"
                params_contrato = (morador_id, quarto_id, date.today(), 550.00)
                contrato_id = db_manager.executar_comando(comando_contrato, params_contrato)
                print(
                    f"  - Contrato criado com sucesso para 'João da Silva' no quarto 100 (ID do Contrato: {contrato_id}).")
        except Exception as e:
            print(f"  - Ocorreu um erro ao criar o contrato: {e}")
    else:
        print(
            "  - Não foi possível criar o contrato pois o quarto 100 ou o morador 'João da Silva' não foram criados corretamente.")

    print("\nPopulação do banco de dados concluída!")


if __name__ == "__main__":
    popular_banco()