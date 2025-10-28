"""
Script para executar todos os seeds na ordem correta
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

from seed_moradores import seed_moradores
from seed_quartos import seed_quartos
from seed_contratos import seed_contratos


def seed_all():
    """Executa todos os seeds na ordem correta"""
    print("\n" + "="*70)
    print(" "*15 + "SEED COMPLETO - GESTÃO DE REPÚBLICA")
    print("="*70)
    print("\nEste script irá popular o banco de dados com:")
    print("  1. Moradores")
    print("  2. Quartos")
    print("  3. Contratos (alguns ativos)")
    print("\nCertifique-se de ter executado o seed_db.py para criar a república e admin.")
    print("="*70)
    
    input("\nPressione Enter para continuar ou Ctrl+C para cancelar...")
    
    try:
        # 1. Criar moradores
        print("\n\n>>> ETAPA 1: Criando moradores...")
        moradores = seed_moradores()
        
        if not moradores:
            print("\nERRO: Falha ao criar moradores. Abortando...")
            return
        
        # 2. Criar quartos
        print("\n\n>>> ETAPA 2: Criando quartos...")
        quartos = seed_quartos()
        
        if not quartos:
            print("\nERRO: Falha ao criar quartos. Abortando...")
            return
        
        # 3. Criar contratos
        print("\n\n>>> ETAPA 3: Criando contratos...")
        contratos = seed_contratos()
        
        # Resumo final
        print("\n\n" + "="*70)
        print(" "*20 + "SEED COMPLETO - RESUMO FINAL")
        print("="*70)
        print(f"\nMoradores criados: {len(moradores)}")
        print(f"Quartos criados: {len(quartos)}")
        print(f"Contratos criados: {len(contratos)}")
        
        if contratos:
            contratos_ativos = [c for c in contratos if c.status == 'ativo']
            print(f"\nContratos ativos: {len(contratos_ativos)}")
            print("\nMoradores com contrato ativo:")
            for contrato in contratos_ativos:
                from src.models.Morador import Morador
                from src.models.Quarto import Quarto
                morador = Morador.buscar_por_id(contrato.morador_id)
                quarto = Quarto.buscar_por_id(contrato.quarto_id)
                if morador and quarto:
                    print(f"  - {morador.nome} -> Quarto {quarto.numero_quarto} (R$ {contrato.valor_aluguel})")
        
        print("\n" + "="*70)
        print("SEED COMPLETO EXECUTADO COM SUCESSO!")
        print("="*70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nSeed cancelado pelo usuário.")
    except Exception as e:
        print(f"\n\nERRO durante seed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    seed_all()
