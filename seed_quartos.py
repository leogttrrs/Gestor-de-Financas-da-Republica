"""
Seed para popular a tabela de Quartos
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.models.Quarto import Quarto
from src.models.Republica import Republica


def seed_quartos():
    """Cria quartos de exemplo no banco de dados"""
    print("\n" + "="*60)
    print("SEED: Populando tabela de Quartos")
    print("="*60)
    
    republicas = Republica.listar_todas()
    
    if not republicas:
        print("\nERRO: Nenhuma república encontrada no banco!")
        print("Execute o seed_db.py primeiro para criar uma república.")
        return []
    
    republica = republicas[0]
    print(f"\nUsando República: {republica.nome} (ID: {republica.id})")
    
    quartos_data = [
        {
            'numero_quarto': 101,
            'tamanho': 5,
            'descricao': 'Quarto duplo com armário embutido'
        },
        {
            'numero_quarto': 102,
            'tamanho': 6,
            'descricao': 'Quarto individual com varanda'
        },
        {
            'numero_quarto': 103,
            'tamanho': 6, 
            'descricao': 'Quarto duplo espaçoso'
        },
        {
            'numero_quarto': 104,
            'tamanho': 4,
            'descricao': 'Quarto individual aconchegante'
        },
        {
            'numero_quarto': 105,
            'tamanho': 7,
            'descricao': 'Quarto triplo com banheiro privativo'
        },
        {
            'numero_quarto': 201,
            'tamanho': 3,
            'descricao': 'Quarto duplo no segundo andar'
        },
        {
            'numero_quarto': 202,
            'tamanho': 5,
            'descricao': 'Quarto individual silencioso'
        },
        {
            'numero_quarto': 203,
            'tamanho': 4,
            'descricao': 'Quarto duplo com vista'
        }
    ]
    
    quartos_criados = []
    
    for i, dados in enumerate(quartos_data, 1):
        try:
            # Verificar se já existe
            quarto_existente = Quarto.buscar_por_numero(dados['numero_quarto'], republica.id)
            if quarto_existente:
                print(f"\n[{i}] Quarto já existe: {dados['numero_quarto']} (Capacidade: {dados['tamanho']})")
                quartos_criados.append(quarto_existente)
                continue
            
            # Criar novo quarto
            quarto = Quarto(
                numero_quarto=dados['numero_quarto'],
                tamanho=dados['tamanho'],
                republica=republica 
            )
            
            quarto = quarto.salvar()
            
            print(f"\n[{i}] Quarto criado com sucesso:")
            print(f"    Número: {quarto.numero_quarto}")
            print(f"    Capacidade: {quarto.tamanho} vaga(s)")
            print(f"    Status: {quarto.status}")
            print(f"    Descrição: {dados['descricao']}")
            print(f"    ID: {quarto.id}")
            quartos_criados.append(quarto)
                
        except Exception as e:
            print(f"\n[{i}] EXCEÇÃO ao criar quarto {dados['numero_quarto']}: {str(e)}")
    
    print("\n" + "="*60)
    print(f"SEED CONCLUÍDO: {len(quartos_criados)} quartos no banco")
    print("="*60 + "\n")
    
    return quartos_criados


if __name__ == "__main__":
    seed_quartos()
