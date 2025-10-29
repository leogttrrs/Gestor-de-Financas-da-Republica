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

        headers = ("Morador", "Título", "Status", "Ações")
        widths = [180, 250, 120, 150]

        header_frame = tk.Frame(self.frame_lista, bg="white")
        header_frame.pack(fill="x", pady=(10, 5))
        for i, h in enumerate(headers):
            tk.Label(
                header_frame,
                text=h,
                bg="white",
                font=("Arial", 12, "bold"),
                padx=5,
                pady=5,
                width=int(widths[i]/10),  
                anchor="w"
            ).grid(row=0, column=i, sticky="w")

        canvas = tk.Canvas(self.frame_lista, bg="white", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.frame_lista, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.linhas_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0,0), window=self.linhas_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.linhas_frame.bind("<Configure>", on_frame_configure)

        self.atualizar_lista()



    def atualizar_lista(self, ocorrencias: Optional[List] = None):
        ocorrencias = Ocorrencia.buscar_todos()
        if ocorrencias is None:
            ocorrencias = self._controlador_ocorrencia.listar_ocorrencias()

        for widget in self.linhas_frame.winfo_children():
            widget.destroy()

        if not ocorrencias:
            tk.Label(self.linhas_frame, text="Nenhuma ocorrência", bg="white").pack()
            return

        for i, o in enumerate(ocorrencias):
            morador = o.morador.nome if o.morador else "Desconhecido"
            status = o.status if o.status else "Pendente"

            linha = tk.Frame(self.linhas_frame, bg="white")
            linha.pack(fill="x", pady=2)

            tk.Label(linha, text=morador, bg="white", width=25, anchor="w").pack(side="left")
            tk.Label(linha, text=o.titulo, bg="white", width=35, anchor="w").pack(side="left")
            tk.Label(linha, text=status, bg="white", width=15, anchor="w").pack(side="left")

            visualizar = tk.Label(linha, text="Visualizar", fg="blue", cursor="hand2", bg="white", font=("Arial", 10, "underline"))
            visualizar.pack(side="left", padx=5)
            visualizar.bind("<Button-1>", lambda e, ocorr=o: self._abrir_visualizar(ocorr))


    def _abrir_visualizar(self, ocorrencia):
        usuario_logado = self._controlador_ocorrencia._controlador_sistema.usuario_logado

        modal = tk.Toplevel(self.main_frame)
        modal.title("Visualizar Ocorrência")
        modal.geometry("600x360")
        modal.transient(self.main_frame)
        modal.grab_set()

        body = tk.Frame(modal, bg="white")
        body.pack(fill="both", expand=True, padx=30, pady=10)

        tk.Label(body, text="Morador", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(body, text=ocorrencia.morador.nome, bg="white").pack(anchor="w", pady=(0,6))

        tk.Label(body, text="Título", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(body, text=ocorrencia.titulo, bg="white").pack(anchor="w", pady=(0,6))

        tk.Label(body, text="Descrição", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        descricao_box = tk.Text(body, height=6, wrap="word")
        descricao_box.insert("1.0", ocorrencia.descricao)
        descricao_box.configure(state="disabled")
        descricao_box.pack(fill="both", expand=False, pady=(0,6))

        botoes_frame = tk.Frame(modal, bg="white")
        botoes_frame.pack(side="bottom", fill="x", padx=30, pady=20)


        ttk.Button(botoes_frame, text="Fechar", command=modal.destroy).pack(side="left")

        if usuario_logado and usuario_logado.tipo_usuario.lower() == "morador":
            ttk.Button(botoes_frame, text="Editar", command=lambda: self._abrir_formulario_editar(ocorrencia)).pack(side="right", padx=5)
            ttk.Button(botoes_frame, text="Excluir", command=lambda: self._excluir_ocorrencia(modal, ocorrencia)).pack(side="right", padx=5)

        modal.update() 

    def _abrir_excluir(self, ocorrencia):
        usuario_logado = self._controlador_ocorrencia._controlador_sistema.usuario_logado


        modal = tk.Toplevel(self.main_frame)
        modal.title("Visualizar Ocorrência")
        modal.geometry("600x360")
        modal.transient(self.main_frame)
        modal.grab_set()

        body = tk.Frame(modal, bg="white")
        body.pack(fill="both", expand=True, padx=30, pady=10)

        tk.Label(body, text="Morador", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(body, text=ocorrencia.morador.nome, bg="white").pack(anchor="w", pady=(0,6))

        tk.Label(body, text="Título", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(body, text=ocorrencia.titulo, bg="white").pack(anchor="w", pady=(0,6))

        tk.Label(body, text="Descrição", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        descricao_box = tk.Text(body, height=6, wrap="word")
        descricao_box.insert("1.0", ocorrencia.descricao)
        descricao_box.configure(state="disabled")
        descricao_box.pack(fill="both", expand=False, pady=(0,6))

        botoes_frame = tk.Frame(modal, bg="white")
        botoes_frame.pack(side="bottom", fill="x", padx=30, pady=20)

        ttk.Button(botoes_frame, text="Fechar", command=modal.destroy).pack(side="left")

        if usuario_logado and usuario_logado.tipo_usuario.lower() == "morador":
            ttk.Button(botoes_frame, text="Editar", command=lambda: self._abrir_formulario_editar(ocorrencia)).pack(side="right", padx=5)
            ttk.Button(botoes_frame, text="Excluir", command=lambda: self._excluir_ocorrencia(modal, ocorrencia)).pack(side="right", padx=5)

        modal.update()  

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

    def _abrir_formulario_editar(self, ocorrencia):
        TelaFormularioOcorrencia(
            parent=self.main_frame,
            controlador_ocorrencia=self._controlador_ocorrencia,
            ocorrencia_existente=ocorrencia
        ).grab_set()


    
    def _excluir_ocorrencia(self, modal, ocorrencia):
        sucesso = self._controlador_ocorrencia.excluir_ocorrencia(ocorrencia.id)
        if sucesso:
            messagebox.showinfo("Resultado", "Ocorrência excluída com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível excluir a ocorrência.")
        modal.destroy()
        self.atualizar_lista()


