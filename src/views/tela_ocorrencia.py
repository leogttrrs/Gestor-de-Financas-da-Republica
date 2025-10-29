# tela_ocorrencias.py
import tkinter as tk
from tkinter import ttk
from typing import List, Optional
from .components.textos import TextosPadrao
from .components.botoes import BotoesPadrao
from .components.tabelas import TabelasPadrao
from .components.modais import ModaisPadrao
from ..models.Ocorrencia import Ocorrencia
from tkinter import messagebox
from .tela_formulario_ocorrencia import TelaFormularioOcorrencia


class TelaOcorrencias:
    def __init__(self, controlador_ocorrencia):
        self._controlador_ocorrencia = controlador_ocorrencia
        self.main_frame = None
        self.frame_lista = None
        self.tree = None

    def inicializar_componentes(self, parent):
        self.main_frame = tk.Frame(parent, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        self._criar_cabecalho()
        self._criar_tabela()

        return self.main_frame

    def _criar_cabecalho(self):
        header_frame = tk.Frame(self.main_frame, bg="white")
        header_frame.pack(fill="x", padx=40, pady=(20, 10))

        titulo_frame = tk.Frame(header_frame, bg="white")
        titulo_frame.pack(side="left")

        TextosPadrao.titulo_principal(titulo_frame, "Ocorrências")
        TextosPadrao.subtitulo(titulo_frame, "Registre e visualize ocorrências.", cor="#666666")

        botoes_frame = tk.Frame(header_frame, bg="white")
        botoes_frame.pack(side="right")

        usuario_logado = self._controlador_ocorrencia._controlador_sistema.usuario_logado
        if usuario_logado and usuario_logado.tipo_usuario == 'morador':
            btn_registrar = ttk.Button(
                botoes_frame,
                text="Registrar Ocorrência",
                command=self._abrir_formulario
            )
            btn_registrar.pack(side="right")

    def _criar_tabela(self):
        if self.frame_lista:
            self.frame_lista.destroy()

        self.frame_lista = tk.Frame(self.main_frame, bg="white")
        self.frame_lista.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        headers = ("ID", "Morador", "Título", "Status", "Ações")
        widths = [60, 200, 250, 120, 150]
        self.tree, scrollbar = TabelasPadrao.criar_tabela(
            self.frame_lista,
            headers,
            widths,
            altura=15
        )

        self.atualizar_lista()

    def atualizar_lista(self, ocorrencias: Optional[List] = None):
        ocorrencias = Ocorrencia.buscar_todos()
        if ocorrencias is None:
            ocorrencias = self._controlador_ocorrencia.listar_ocorrencias()

        # Limpa tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

        usuario_logado = self._controlador_ocorrencia._controlador_sistema.usuario_logado
        is_admin = usuario_logado and usuario_logado.tipo_usuario == "administrador"

        if not ocorrencias:
            self.tree.insert("", "end", values=("", "Nenhuma ocorrência", "", "", ""))
            return

        for o in ocorrencias:
            morador = o.morador.nome if o.morador else "Desconhecido"
            status = o.status if o.status else "Pendente"

            # Administrador pode visualizar e finalizar
            if is_admin and status.lower() == "pendente":
                acao = "Visualizar / Finalizar"
            else:
                acao = "Visualizar"

            self.tree.insert(
                "",
                "end",
                values=(
                    o.id,
                    morador,
                    o.titulo,
                    status,
                    acao
                )
            )

        self.tree.unbind("<Double-1>")
        self.tree.bind("<Double-1>", self._on_double_click)


    def _on_double_click(self, event):
        item = self.tree.selection()
        if not item:
            return

        values = self.tree.item(item, "values")
        ocorrencia_id = values[0]

        selecionada = self._controlador_ocorrencia.buscar_ocorrencia_por_id(ocorrencia_id)
        if selecionada:
            self._abrir_visualizar(selecionada)

    def _abrir_visualizar(self, ocorrencia):
        modal = ModaisPadrao.modal_formulario(titulo="Visualizar Ocorrência", largura=600, altura=360)
        ModaisPadrao.cabecalho_modal(modal, "Visualizar Ocorrência")

        body = tk.Frame(modal, bg="white")
        body.pack(fill="both", expand=True, padx=30, pady=10)

        tk.Label(body, text="Morador", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(body, text=ocorrencia.morador.nome, bg="white").pack(anchor="w", pady=(0, 6))

        tk.Label(body, text="Título", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(body, text=ocorrencia.titulo, bg="white").pack(anchor="w", pady=(0, 6))

        tk.Label(body, text="Descrição", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        descricao_box = tk.Text(body, height=6, wrap="word")
        descricao_box.insert("1.0", ocorrencia.descricao)
        descricao_box.configure(state="disabled")
        descricao_box.pack(fill="both", expand=False, pady=(0, 6))

        botoes_frame = tk.Frame(modal, bg="white")
        botoes_frame.pack(side="bottom", fill="x", padx=30, pady=20)

        BotoesPadrao.botao_cinza(botoes_frame, texto="Fechar", comando=modal.destroy, side="left")

        if ocorrencia.status.lower() == "pendente":
            def finalizar():
                ok, msg = self._controlador_ocorrencia.finalizar_ocorrencia(ocorrencia.id)
                ModaisPadrao.dialogo_mensagem(modal, "Resultado", msg)
                modal.destroy()
                self.atualizar_lista()

            BotoesPadrao.botao_vermelho(botoes_frame, texto="Finalizar", comando=finalizar, side="right")

    def _abrir_formulario(self):
        TelaFormularioOcorrencia(parent=self.main_frame, controlador_ocorrencia=self._controlador_ocorrencia).grab_set()

    def exibir_ocorrencias(self, lista):
        self.atualizar_lista(lista)

    def mostrar_erro_modal(self, msg: str):
        messagebox.showerror("Erro", msg)

    def mostrar_sucesso(self, msg: str):
        messagebox.showinfo("Sucesso", msg)

    def fechar_modal(self, modal):
        modal.destroy()
