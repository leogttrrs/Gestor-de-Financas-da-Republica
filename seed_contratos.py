"""
Seed para popular a tabela de Contratos
Cria contratos para alguns moradores, incluindo contratos ativos
"""

import sys
import os
from datetime import date, timedelta
from decimal import Decimal

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

from src.models.Contrato import Contrato
from src.models.Morador import Morador
from src.models.Quarto import Quarto


def seed_contratos():
    """Cria contratos de exemplo no banco de dados"""
    print("\n" + "="*60)
    print("SEED: Populando tabela de Contratos")
    print("="*60)
    
    # Buscar moradores e quartos disponíveis
    moradores = Morador.listar_todos()
    quartos = Quarto.listar_todos()
    
    if not moradores:
        print("\nERRO: Nenhum morador encontrado no banco!")
        print("Execute o seed_moradores.py primeiro.")
        return []
    
    if not quartos:
        print("\nERRO: Nenhum quarto encontrado no banco!")
        print("Execute o seed_quartos.py primeiro.")
        return []
    
    print(f"\nMoradores disponíveis: {len(moradores)}")
    print(f"Quartos disponíveis: {len(quartos)}")
    
    # Definir contratos (alguns ativos, alguns expirados, alguns futuros)
    hoje = date.today()
    
    contratos_data = [
        {
            'morador_index': 0,  # João Silva
            'quarto_index': 0,   # Quarto 101
            'valor_aluguel': Decimal('800.00'),
            'data_inicio': hoje - timedelta(days=180),  # Começou há 6 meses
            'data_fim': hoje + timedelta(days=185),     # Termina em 6 meses
            'status': 'ativo',
            'descricao': 'Contrato ativo vigente'
        },
        {
            'morador_index': 1,  # Maria Santos
            'quarto_index': 1,   # Quarto 102
            'valor_aluguel': Decimal('950.00'),
            'data_inicio': hoje - timedelta(days=90),   # Começou há 3 meses
            'data_fim': hoje + timedelta(days=275),     # Termina em 9 meses
            'status': 'ativo',
            'descricao': 'Contrato ativo vigente'
        },
        {
            'morador_index': 2,  # Pedro Oliveira
            'quarto_index': 2,   # Quarto 103
            'valor_aluguel': Decimal('750.00'),
            'data_inicio': hoje - timedelta(days=400),  # Começou há mais de 1 ano
            'data_fim': hoje - timedelta(days=35),      # Terminou há 35 dias
            'status': 'finalizado',
            'descricao': 'Contrato encerrado'
        },
        {
            'morador_index': 3,  # Ana Costa
            'quarto_index': 4,   # Quarto 105
            'valor_aluguel': Decimal('650.00'),
            'data_inicio': hoje - timedelta(days=30),   # Começou há 1 mês
            'data_fim': hoje + timedelta(days=335),     # Termina em 11 meses
            'status': 'ativo',
            'descricao': 'Contrato ativo recente'
        },
        {
            'morador_index': 4,  # Carlos Ferreira
            'quarto_index': 5,   # Quarto 201
            'valor_aluguel': Decimal('900.00'),
            'data_inicio': hoje + timedelta(days=15),   # Começará em 15 dias
            'data_fim': hoje + timedelta(days=380),     # Termina em ~1 ano
            'status': 'ativo',
            'descricao': 'Contrato futuro (já confirmado)'
        },
        {
            'morador_index': 5,  # Juliana Almeida
            'quarto_index': 6,   # Quarto 202
            'valor_aluguel': Decimal('1000.00'),
            'data_inicio': hoje - timedelta(days=200),  # Começou há ~6 meses
            'data_fim': hoje + timedelta(days=165),     # Termina em ~5 meses
            'status': 'ativo',
            'descricao': 'Contrato ativo vigente'
        },
        {
            'morador_index': 6,  # Ricardo Souza
            'quarto_index': 3,   # Quarto 104
            'valor_aluguel': Decimal('850.00'),
            'data_inicio': hoje - timedelta(days=500),  # Começou há muito tempo
            'data_fim': hoje - timedelta(days=100),     # Terminou há 100 dias
            'status': 'finalizado',
            'descricao': 'Contrato antigo encerrado'
        }
    ]
    
    contratos_criados = []
    
    for i, dados in enumerate(contratos_data, 1):
        try:
            morador_index = dados['morador_index']
            quarto_index = dados['quarto_index']
            
            # Verificar se os índices são válidos
            if morador_index >= len(moradores):
                print(f"\n[{i}] ERRO: Índice de morador {morador_index} inválido")
                continue
            
            if quarto_index >= len(quartos):
                print(f"\n[{i}] ERRO: Índice de quarto {quarto_index} inválido")
                continue
            
            morador = moradores[morador_index]
            quarto = quartos[quarto_index]
            
            # Criar novo contrato
            contrato = Contrato(
                morador_id=morador.id,
                quarto_id=quarto.id,
                valor_aluguel=dados['valor_aluguel'],
                data_inicio=dados['data_inicio'],
                data_fim=dados['data_fim'],
                status=dados['status']
            )
            
            contrato = contrato.salvar()
            
            print(f"\n[{i}] Contrato criado com sucesso:")
            print(f"    Morador: {morador.nome} (ID: {morador.id})")
            print(f"    Quarto: {quarto.numero_quarto} (ID: {quarto.id})")
            print(f"    Valor: R$ {contrato.valor_aluguel}")
            print(f"    Início: {contrato.data_inicio}")
            print(f"    Fim: {contrato.data_fim}")
            print(f"    Status: {contrato.status}")
            print(f"    Descrição: {dados['descricao']}")
            print(f"    ID: {contrato.id}")
            
            # Atualizar status do quarto se contrato ativo
            if dados['status'] == 'ativo' and dados['data_inicio'] <= hoje <= dados['data_fim']:
                quarto.ocupar_vaga()
                print(f"    Quarto atualizado: {quarto.vagas_ocupadas}/{quarto.tamanho} vagas ocupadas")
            
            contratos_criados.append(contrato)
                
        except Exception as e:
            print(f"\n[{i}] EXCEÇÃO ao criar contrato: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print(f"SEED CONCLUÍDO: {len(contratos_criados)} contratos no banco")
    print("\nResumo:")
    contratos_ativos = [c for c in contratos_criados if c.status == 'ativo']
    contratos_finalizados = [c for c in contratos_criados if c.status == 'finalizado']
    print(f"  - Contratos ativos: {len(contratos_ativos)}")
    print(f"  - Contratos finalizados: {len(contratos_finalizados)}")
    print("="*60 + "\n")
    
    return contratos_criados


if __name__ == "__main__":
    seed_contratos()
