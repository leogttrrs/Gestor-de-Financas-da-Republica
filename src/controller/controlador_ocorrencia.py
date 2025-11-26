from .abstract_controlador import AbstractControlador
from typing import List, Optional
from src.models.Ocorrencia import Ocorrencia
from src.models.Morador import Morador
from src.views.tela_ocorrencia import TelaOcorrencias
from src.views.tela_formulario_ocorrencia import TelaFormularioOcorrencia
from datetime import datetime
import tkinter as tk


class ControladorOcorrencia(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self._tela_ocorrencia = None

    def abre_tela(self, parent_view=None):
        if parent_view is None:
            return

        self._tela_ocorrencia = TelaOcorrencias(parent_view.content_frame, self)
        self._tela_ocorrencia.inicializar_componentes(parent_view.content_frame)
        self._atualizar_lista_ocorrencias()

    def _atualizar_lista_ocorrencias(self):
        if self._tela_ocorrencia:
            ocorrencias = self.listar_ocorrencias()
            self._tela_ocorrencia.exibir_ocorrencias(ocorrencias)

    def listar_ocorrencias(self):
        try:
            todos = Ocorrencia.buscar_todos()
            usuario = self._controlador_sistema.usuario_logado

            if not usuario:
                return []

            if usuario.tipo_usuario == 'administrador':
                return todos
            else:
                return [o for o in todos if o.morador_id == usuario.id]

        except Exception as e:
            print(f"Erro ao listar: {e}")
            return []

    def cadastrar_ocorrencia(self, dados: dict):
        try:
            if not self.usuario_pode_cadastrar():
                return "Apenas moradores podem cadastrar ocorrências."

            valido, msg = self.validar_campos(dados)
            if not valido:
                return msg

            morador = dados.get("morador")
            titulo = dados.get("titulo").strip()
            descricao = dados.get("descricao").strip()

            if not morador:
                return "Morador é obrigatório."

            data_atual = datetime.now().strftime("%Y-%m-%d")
            ocorrencia = Ocorrencia(
                morador=morador,
                titulo=titulo,
                descricao=descricao,
                data=data_atual
            )

            return ocorrencia.salvar()

        except Exception as e:
            return str(e)


    def atualizar_ocorrencia(self, ocorrencia_id: int, dados: dict) -> bool:
        try:
            ocorrencia = Ocorrencia.buscar_por_id(ocorrencia_id)
            if not ocorrencia: return False

            valido, msg = self.validarCampos(dados)
            if not valido: return False

            ocorrencia.titulo = dados.get("titulo", ocorrencia.titulo).strip()
            ocorrencia.descricao = dados.get("descricao", ocorrencia.descricao).strip()
            ocorrencia.salvar()
            return True
        except Exception:
            return False

    def excluir_ocorrencia(self, ocorrencia_id: int) -> bool:
        try:
            ocorr = Ocorrencia.buscar_por_id(ocorrencia_id)
            if not ocorr:
                self.mostrarMensagemErro("Ocorrência não encontrada!")
                return False

            ocorr.excluir()
            self._atualizar_lista_ocorrencias()
            return True
        except Exception as e:
            self.mostrarMensagemErro(f"Erro ao excluir: {str(e)}")
            return False

    def abrir_tela_formulario(self, ocorrencia_existente=None):
        usuario_logado = self._controlador_sistema.usuario_logado

        if not usuario_logado:
            self.mostrarMensagemErro("Apenas moradores podem criar  ocorrências.")
            return

        parent = None
        if self._tela_ocorrencia and hasattr(self._tela_ocorrencia, 'main_frame'):
            parent = self._tela_ocorrencia.main_frame
        else:
            parent = self._controlador_sistema.root if hasattr(self._controlador_sistema, 'root') else tk.Tk()

        TelaFormularioOcorrencia(parent, self, ocorrencia_existente)

    def abrir_tela_visualizacao(self, id_ocorrencia):
        try:
            ocorrencia = Ocorrencia.buscar_por_id(id_ocorrencia)
            if not ocorrencia:
                self.mostrarMensagemErro("Ocorrência não encontrada.")
                return

            parent = None
            if self._tela_ocorrencia and hasattr(self._tela_ocorrencia, 'main_frame'):
                parent = self._tela_ocorrencia.main_frame
            else:
                parent = self._controlador_sistema.root

            TelaFormularioOcorrencia(
                parent=parent,
                controlador_ocorrencia=self,
                ocorrencia_existente=ocorrencia,
                visualizar_apenas=True
            )
        except Exception as e:
            self.mostrarMensagemErro(f"Erro ao abrir visualização: {str(e)}")

    def alterar_status_ocorrencia(self, id_ocorrencia: int) -> bool:
        try:
            if not self.usuario_pode_alterar_status():
                self.mostrarMensagemErro("Apenas administradores podem alterar o status.")
                return False

            ocorrencia = Ocorrencia.buscar_por_id(id_ocorrencia)
            if not ocorrencia:
                self.mostrarMensagemErro("Ocorrência não encontrada.")
                return False

            novo_status = "Finalizado" if ocorrencia.status == "Pendente" else "Pendente"
            ocorrencia.status = novo_status
            ocorrencia.salvar()

            self._atualizar_lista_ocorrencias()
            return True

        except Exception as e:
            self.mostrarMensagemErro(f"Erro ao alterar status: {e}")
            return False

    def mostrarMensagemErro(self, msg: str):
        if self._tela_ocorrencia:
            if hasattr(self._tela_ocorrencia, 'mostrar_erro_modal'):
                self._tela_ocorrencia.mostrar_erro_modal(msg)
            else:
                tk.messagebox.showerror("Erro", msg)

    def validar_campos(self, dados: dict) -> (bool, str):
        titulo = str(dados.get('titulo', '')).strip()
        descricao = str(dados.get('descricao', '')).strip()

        # Se qualquer um estiver vazio → erro único
        if not titulo or not descricao:
            return False, "Campos obrigatórios não foram preenchidos"

        return True, ""

    def usuario_pode_alterar_status(self):
        usuario = self._controlador_sistema.usuario_logado
        return usuario and usuario.tipo_usuario.lower() == "administrador"
    
    def usuario_pode_cadastrar(self):
        usuario = self._controlador_sistema.usuario_logado
        return usuario and usuario.tipo_usuario.lower() == "morador"