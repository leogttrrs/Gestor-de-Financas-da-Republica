import sys
import os
from src.utils.validador import Validador 

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.Morador import Morador


def seed_moradores():
    print("\n" + "="*60)
    print("SEED: Populando tabela de Moradores")
    print("="*60)
    
    moradores_data = [
        {"nome": "João Silva", "cpf": "11111111111", "email": "joao.silva@email.com",
         "senha": "senha123", "telefone": "11987654321"},
        {"nome": "Maria Santos", "cpf": "22222222222", "email": "maria.santos@email.com",
         "senha": "senha123", "telefone": "11987654322"},
        {"nome": "Pedro Oliveira", "cpf": "33333333333", "email": "pedro.oliveira@email.com",
         "senha": "senha123", "telefone": "11987654323"},
        {"nome": "Ana Costa", "cpf": "44444444444", "email": "ana.costa@email.com",
         "senha": "senha123", "telefone": "11987654324"},
        {"nome": "Carlos Ferreira", "cpf": "55555555555", "email": "carlos.ferreira@email.com",
         "senha": "senha123", "telefone": "11987654325"},
        {"nome": "Juliana Almeida", "cpf": "66666666666", "email": "juliana.almeida@email.com",
         "senha": "senha123", "telefone": "11987654326"},
        {"nome": "Ricardo Souza", "cpf": "77777777777", "email": "ricardo.souza@email.com",
         "senha": "senha123", "telefone": "11987654327"},
        {"nome": "Fernanda Lima", "cpf": "88888888888", "email": "fernanda.lima@email.com",
         "senha": "senha123", "telefone": "11987654328"},
    ]
    
    moradores_criados = 0
    moradores_existentes = 0
    
    for data in moradores_data:
        try:
            morador_existente = Morador.buscar_por_cpf(data["cpf"])
            if morador_existente:
                print(f"Morador {data['nome']} já existe (CPF: {data['cpf']})")
                moradores_existentes += 1
                continue

            senha_hash = Validador.hash_senha(data["senha"])
            morador = Morador(
                cpf=data["cpf"],
                nome=data["nome"],
                email=data["email"],
                telefone=data["telefone"],
                senhaCriptografada=senha_hash,
            )

            ok, msg = Morador.salvar_usuario(morador)
            if ok:
                print(f"Morador criado: {data['nome']} (CPF: {data['cpf']})")
                moradores_criados += 1
            else:
                print(f"Falha ao criar {data['nome']}: {msg}")

        except Exception as e:
            print(f"Erro ao criar morador {data['nome']}: {str(e)}")
    
    print("\n" + "-"*60)
    print("Resumo:")
    print(f"  • Moradores criados: {moradores_criados}")
    print(f"  • Moradores já existentes: {moradores_existentes}")
    print(f"  • Total processado: {len(moradores_data)}")
    print("="*60 + "\n")
    return moradores_criados


if __name__ == "__main__":
    seed_moradores()
