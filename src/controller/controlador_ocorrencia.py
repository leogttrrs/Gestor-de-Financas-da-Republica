from .abstract_controlador import AbstractControlador
from typing import List, Dict, Optional
from src.models.Ocorrencia import Ocorrencia
from src.models.Morador import Morador
from src.views.tela_ocorrencia import TelaOcorrencias
from src.views.tela_formulario_ocorrencia import TelaFormularioOcorrencia
from datetime import datetime
from tkinter import messagebox
import tkinter as tk
from tkinter import messagebox
import sqlite3


class ControladorOcorrencia(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self._tela_ocorrencia = None

    def abre_tela(self, parent_view=None):
        if parent_view is None:
            return

        self._tela_ocorrencia = TelaOcorrencias(self)
        self._tela_ocorrencia.inicializar_componentes(parent_view.content_frame)
        self._atualizar_lista_ocorrencias()

    def verificar_usuario_logado(self) -> Optional[Dict]:
        usuario = getattr(self.sessao, "usuario_atual", None)
        if not usuario:
            return None
        tipo = usuario.get("tipo_usuario", "").lower()
        if tipo in ("adm", "administrador"):
            # Administrador não pode criar ocorrência
            return {"tipo": "administrador", **usuario}
        elif tipo == "morador":
            return {"tipo": "morador", **usuario}
        return None
    
    def abrir_tela_formulario(self, ocorrencia_existente=None):
        usuario_logado = self._controlador_sistema.usuario_logado
        if not usuario_logado or usuario_logado.tipo_usuario != 'morador':
            messagebox.showerror("Acesso Negado", "Apenas moradores podem criar ocorrencias.")
            return

        parent = None
        if self._tela_ocorrencia:
            parent = self._tela_ocorrencia.main_frame
        else:
            parent = tk.Tk() 

        TelaFormularioOcorrencia(parent, self, ocorrencia_existente)


    def listar_ocorrencias(self) -> List[Ocorrencia]:
        try:
            return Ocorrencia.buscar_todos()
        except Exception:
            return []

    def _atualizar_lista_ocorrencias(self):
        if self._tela_ocorrencia is None:
            return

        ocorrencias = self.listar_ocorrencias()
        ocorrencias_dict = []

        for o in ocorrencias:
            ocorrencias_dict.append({
                'id': o.id,
                'morador_nome': o.morador.nome if o.morador else "N/A",
                'titulo': o.to_dict().get("titulo", ""),
                'descricao': o.to_dict().get("descricao", ""),
                'data': o.to_dict().get("data", ""),
                'status': o.status
            })

        self._tela_ocorrencia.exibir_ocorrencias(ocorrencias_dict)


    def criar_ocorrencia_interface(self, dados: dict, formulario: Optional[tk.Toplevel] = None):
        if not self._tela_ocorrencia:
            return

        try:
            campos_obrigatorios = ('morador_id', 'titulo', 'descricao')
            if not dados or any(not dados.get(campo) for campo in campos_obrigatorios):
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return

            morador_id = int(dados.get('morador_id'))
            titulo = dados.get('titulo').strip()
            descricao = dados.get('descricao').strip()

            morador = Morador.buscar_por_id(morador_id)
            if not morador:
                messagebox.showerror("Erro", "Morador não encontrado!")
                return

            ocorr = Ocorrencia(
                morador=morador,
                titulo=titulo,
                descricao=descricao,
                data=datetime.now().strftime("%d/%m/%Y"),
                status="Pendente"
            )

            valido, msg = ocorr.validar_campos()
            if not valido:
                messagebox.showerror("Erro", msg)
                return

            ocorr.salvar()

            self._atualizar_lista_ocorrencias()
            
            if formulario:
                formulario.destroy()

            messagebox.showinfo("Sucesso", "Ocorrência cadastrada com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar ocorrência: {str(e)}")

    def salvar_ocorrencia(self, dados: dict):
        try:
            morador = dados.get("morador")
            if not morador:
                return False, "Morador não encontrado!"

            titulo = dados.get("titulo", "").strip()
            descricao = dados.get("descricao", "").strip()

            if not titulo or not descricao:
                return False, "Preencha todos os campos obrigatórios!"

            ocorrencia = Ocorrencia(
                morador=morador,
                titulo=titulo,
                descricao=descricao,
                data=datetime.now().strftime("%d/%m/%Y"),
                status="Pendente"
            )

            ocorrencia.salvar()
            self._atualizar_lista_ocorrencias()

            return True, "Ocorrência cadastrada com sucesso!"

        except Exception as e:
            return False, f"Erro ao salvar ocorrência: {str(e)}"



    def finalizar_ocorrencia(self, ocorrencia_id: int) -> bool:
        try:
            ocorr = Ocorrencia.buscar_por_id(ocorrencia_id)
            if not ocorr:
                self._tela_ocorrencia.mostrar_erro("Ocorrência não encontrada!")
                return False

            ocorr.status = "Finalizado"
            ocorr.salvar()

            self._atualizar_lista_ocorrencias()
            self._tela_ocorrencia.mostrar_sucesso("Ocorrência finalizada!")
            return True

        except Exception as e:
            self._tela_ocorrencia.mostrar_erro(f"Erro ao finalizar: {str(e)}")
            return False

    def excluir_ocorrencia(self, ocorrencia_id: int) -> bool:
        try:
            ocorr = Ocorrencia.buscar_por_id(ocorrencia_id)
            if not ocorr:
                self._tela_ocorrencia.mostrar_erro("Ocorrência não encontrada!")
                return False

            ocorr.excluir()
            self._atualizar_lista_ocorrencias()
            return True

        except Exception as e:
            self._tela_ocorrencia.mostrar_erro(f"Erro ao excluir: {str(e)}")
            return False

    def listar_moradores(self) -> List[Dict]:
        try:
            moradores = Morador.buscar_todos()
            return [{'id': m.id, 'nome': m.nome} for m in moradores]
        except Exception:
            return []
        
    def alterar_status_ocorrencia(self, id_ocorrencia: int, novo_status: str) -> bool:
        try:
            ocorrencia = Ocorrencia.buscar_por_id(id_ocorrencia)
            if not ocorrencia:
                messagebox.showerror("Erro", "Ocorrência não encontrada.")
                return False

            ocorrencia.status = novo_status
            ocorrencia.salvar()

            if hasattr(self, "_tela_ocorrencia") and self._tela_ocorrencia:
                self._atualizar_lista_ocorrencias()

            messagebox.showinfo("Sucesso", f"Ocorrência marcada como {novo_status}.")
            return True

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível alterar o status: {e}")
            return False


