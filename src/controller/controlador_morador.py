from .abstract_controlador import AbstractControlador
from src.models.Morador import Morador
from src.models.Contrato import Contrato
from src.views.tela_morador import TelaMoradores
from typing import List, Optional

class ControladorMorador(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self.tela_moradores = None
    
    def abre_tela(self, parent_view=None):
            # 1. Atualiza lista de moradores (somente ativos/agendados)
        self.moradores = Morador.buscar_com_contrato_ativo()

        self.tela_moradores = TelaMoradores(
                parent_view.content_frame,               # onde a tela será renderizada
                self._controlador_sistema, # para navegação
                self                    # referência ao controlador
            )

        # 3. Atualiza a exibição antes de mostrar
        self.tela_moradores.atualizar_lista()

        # 4. Define a tela atual no sistema
        self._controlador_sistema.tela_atual = self.tela_moradores
        self.tela_moradores.mostrar()
        

    def buscar_morador_por_id(self, morador_id: int) -> Optional['Morador']:
        return Morador.buscar_por_id(morador_id)
    
    def _atualizar_lista_moradores(self) -> List[dict]:
        contratos_ativos = self.listar_contratos(filtro_status='ativo')
        contratos_agendados = self.listar_contratos(filtro_status='agendado')
        contratos = contratos_ativos + contratos_agendados

        lista_moradores = []

        for contrato in contratos:
            morador = contrato.morador
            quarto = contrato.quarto

            lista_moradores.append({
                'morador_nome': morador.nome if morador else 'N/A',
                'email': morador.email if morador else 'N/A',
                'telefone': morador.telefone if morador else 'N/A',
                'quarto_numero': quarto.numero_quarto if quarto else 'N/A'
            })

        return lista_moradores
        

    def listar_moradores_nao_alocados(self) -> List[dict]:
        try:
            moradores = Morador.buscar_nao_alocados()
            return [{'id': m.id, 'nome': m.nome, 'cpf': m.cpf} for m in moradores]
        except Exception as e:
            print(f"Erro ao listar moradores não alocados: {e}")
            return []
        
    def listar_moradores_alocados(self) -> List[dict]:
        try:
            moradores = Morador.buscar_com_contrato_ativo()
            lista_moradores = []

            for morador in moradores:

                
                contratos_ativos = Contrato.buscar_ativos()

                contrato = next(
                    (c for c in contratos_ativos if c.morador_id == morador.id),
                    None
                )

                # Pega o número do quarto
                quarto_numero = contrato.quarto.numero_quarto if contrato and contrato.quarto else 'N/A'

                lista_moradores.append({
                    'morador_nome': morador.nome,
                    'email': morador.email,
                    'telefone': morador.telefone,
                    'quarto_numero': quarto_numero
                })

            return lista_moradores

        except Exception as e:
            print(f"Erro ao listar moradores alocados: {e}")
            return []

    def cadastrar_morador(self, dados: dict):
        try:
            cpf = dados["cpf"]

            # prevenir duplicidade
            if Morador.buscar_por_cpf(cpf):
                return False, "Já existe um morador cadastrado com este CPF."

            novo = Morador(
                cpf=dados["cpf"],
                nome=dados["nome"],
                email=dados["email"],
                telefone=dados["telefone"],
                senhaCriptografada=dados["senha"]
            )

            novo.salvar()

            return True, novo

        except Exception as e:
            return False, str(e)

