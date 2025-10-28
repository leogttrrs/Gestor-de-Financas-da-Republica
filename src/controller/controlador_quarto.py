import sqlite3
from .abstract_controlador import AbstractControlador
from src.views.tela_quarto import TelaQuarto
from src.views.tela_formulario_quarto import TelaFormularioQuarto
from src.models.Quarto import Quarto
from tkinter import messagebox
from src.models.Republica import Republica
from typing import List, Optional


class ControladorQuarto(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self.tela_gerenciar = None

    def abre_tela(self, parent_view):
        self.tela_gerenciar = TelaQuarto(parent_view.content_frame, self._controlador_sistema)
        self._controlador_sistema.tela_atual = self.tela_gerenciar
        self.tela_gerenciar.mostrar()

    def abrir_tela_formulario(self, quarto_existente=None):
        root_window = self._controlador_sistema.tela_atual.frame.winfo_toplevel()
        TelaFormularioQuarto(root_window, self, quarto_existente)

    def salvar_quarto(self, dados: dict):
        try:
            admin_logado = self._controlador_sistema.usuario_logado
            if not admin_logado:
                return False, "Nenhum administrador está logado."

            republica_atual = Republica.buscar_por_admin_id(admin_logado.id)
            if not republica_atual:
                return False, "Nenhuma república encontrada para o administrador atual."

            quarto = Quarto(
                id=dados.get("id"),
                numero_quarto=dados["numero_quarto"],
                tamanho=dados["tamanho"],
                republica=republica_atual
            )
            quarto.salvar()

            if self.tela_gerenciar:
                self.tela_gerenciar.atualizar_lista()
            return True, "Salvo com sucesso"

        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                num_quarto = dados.get('numero_quarto', '')
                return False, f"Já existe um quarto com o número {num_quarto}."
            else:
                return False, f"Erro de integridade no banco de dados: {e}"
        except Exception as e:
            return False, f"Um erro inesperado ocorreu: {e}"

    def excluir_quarto(self, quarto_id: int):
        quarto = Quarto.buscar_por_id(quarto_id)
        if quarto:
            if quarto.possui_contratos_ativos():
                messagebox.showerror("Ação Proibida", "Não é possível excluir um quarto com contratos ativos.")
                return
            Quarto.deletar(quarto_id)
            if self.tela_gerenciar:
                self.tela_gerenciar.atualizar_lista()

    def buscar_quarto_por_id(self, quarto_id: int) -> Optional['Quarto']:
        return Quarto.buscar_por_id(quarto_id)

    def listar_quartos_disponiveis(self) -> List[dict]:
        try:
            quartos = Quarto.buscar_todos()
            quartos_disponiveis = []
            
            for quarto in quartos:
                if quarto.obter_vagas_disponiveis() > 0:
                    quartos_disponiveis.append({
                        'id': quarto.id,
                        'numero_quarto': quarto.numero_quarto,
                        'tamanho': quarto.tamanho,
                        'vagas_disponiveis': quarto.obter_vagas_disponiveis(),
                        'status': quarto.status
                    })
            
            return quartos_disponiveis
            
        except Exception as e:
            print(f"Erro ao listar quartos disponíveis: {e}")
            return []

    def listar_quartos_ocupados(self) -> List[dict]:
        try:
            quartos = Quarto.buscar_todos()
            quartos_ocupados = []
            
            for quarto in quartos:
                if quarto.possui_contratos_ativos():
                    quartos_ocupados.append({
                        'id': quarto.id,
                        'numero_quarto': quarto.numero_quarto,
                        'tamanho': quarto.tamanho,
                        'vagas_disponiveis': quarto.obter_vagas_disponiveis(),
                        'status': quarto.status,
                        'moradores': quarto.morador
                    })
            
            return quartos_ocupados
            
        except Exception as e:
            print(f"Erro ao listar quartos ocupados: {e}")
            return []

    def listar_quartos_indisponiveis(self) -> List[dict]:
        try:
            quartos = Quarto.buscar_todos()
            quartos_indisponiveis = []
            
            for quarto in quartos:
                if quarto.obter_vagas_disponiveis() == 0:
                    quartos_indisponiveis.append({
                        'id': quarto.id,
                        'numero_quarto': quarto.numero_quarto,
                        'tamanho': quarto.tamanho,
                        'status': quarto.status
                    })
            
            return quartos_indisponiveis
            
        except Exception as e:
            print(f"Erro ao listar quartos indisponíveis: {e}")
            return []

    def listar_todos_quartos(self) -> List[dict]:
        try:
            quartos = Quarto.buscar_todos()
            todos_quartos = []
            
            for quarto in quartos:
                todos_quartos.append({
                    'id': quarto.id,
                    'numero_quarto': quarto.numero_quarto,
                    'tamanho': quarto.tamanho,
                    'vagas_disponiveis': quarto.obter_vagas_disponiveis(),
                    'status': quarto.status,
                    'moradores': quarto.morador,
                    'pode_receber_novos': quarto.obter_vagas_disponiveis() > 0,
                    'esta_lotado': quarto.obter_vagas_disponiveis() == 0
                })
            
            return todos_quartos
            
        except Exception as e:
            print(f"Erro ao listar todos os quartos: {e}")
            return []

    def alterar_status_quarto(self, quarto_id: int, novo_status: str) -> bool:
        try:
            quarto = Quarto.buscar_por_id(quarto_id)
            if not quarto:
                return False
            
            if quarto.alterar_status(novo_status):
                quarto.salvar()
                if self.tela_gerenciar:
                    self.tela_gerenciar.atualizar_lista()
                return True
            return False
            
        except Exception as e:
            print(f"Erro ao alterar status do quarto: {e}")
            return False

