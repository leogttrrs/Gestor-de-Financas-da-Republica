import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.controller.controlador_sistema import ControladorSistema
from src.views.aplicacao_spa import iniciar_aplicacao_spa


def main():
    try:
        controlador_sistema = ControladorSistema()
        
        iniciar_aplicacao_spa(controlador_sistema)
        
    except Exception as e:
        print(f"Erro ao iniciar a aplicação: {e}")
        input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()
