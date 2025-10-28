from .abstract_controlador import AbstractControlador
from src.models.Morador import Morador
from typing import List, Optional

class ControladorMorador(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
    
    def abre_tela(self, parent_view=None):
        pass

    def buscar_morador_por_id(self, morador_id: int) -> Optional['Morador']:
        return Morador.buscar_por_id(morador_id)

    def listar_moradores_nao_alocados(self) -> List[dict]:
        try:
            moradores = Morador.buscar_nao_alocados()
            return [{'id': m.id, 'nome': m.nome, 'cpf': m.cpf} for m in moradores]
        except Exception as e:
            print(f"Erro ao listar moradores não alocados: {e}")
            return []


