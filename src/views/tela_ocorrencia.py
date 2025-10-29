import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from .components.textos import TextosPadrao
from .components.botoes import BotoesPadrao
from .components.tabelas import TabelasPadrao
from .components.modais import ModaisPadrao
from ..models.Ocorrencia import Ocorrencia
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
                width=int(widths[i] / 10),
                anchor="w"
            ).grid(row=0, column=i, sticky="w")

        canvas = tk.Canvas(self.frame_lista, bg="white", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.frame_lista, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.linhas_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=self.linhas_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.linhas_frame.bind("<Configure>", on_frame_configure)

        self.atualizar_lista()

    def atualizar_lista(self, ocorrencias: Optional[List] = None):
        usuario_logado = self._controlador_ocorrencia._controlador_sistema.usuario_logado

        ocorrencias = Ocorrencia.buscar_todos()
        if ocorrencias is None:
            ocorrencias = self._controlador_ocorrencia.listar_ocorrencias()

        if usuario_logado:
            if usuario_logado.tipo_usuario.lower() == "morador":
                cpf_logado = usuario_logado.cpf
                ocorrencias = [
                    o for o in ocorrencias
                    if o.morador and o.morador.cpf == cpf_logado
                ]
            elif usuario_logado.tipo_usuario.lower() == "administrador":
                pass
        else:
            ocorrencias = []

        for widget in self.linhas_frame.winfo_children():
            widget.destroy()

        if not ocorrencias and usuario_logado.tipo_usuario.lower() == "morador":
            tk.Label(self.linhas_frame, text="Você não possui ocorrências.", bg="white").pack(pady=10)
            return
        
        elif not ocorrencias and usuario_logado.tipo_usuario.lower() == "administrador":
            tk.Label(self.linhas_frame, text="Não há ocorrências cadastradas.", bg="white").pack(pady=10)
            return
        
        for i, o in enumerate(ocorrencias):
            morador = o.morador.nome if o.morador else "Desconhecido"
            status = o.status if o.status else "Pendente"

            linha = tk.Frame(self.linhas_frame, bg="white")
            linha.pack(fill="x", pady=2)

            tk.Label(linha, text=morador, bg="white", width=25, anchor="w").pack(side="left")
            tk.Label(linha, text=o.titulo, bg="white", width=35, anchor="w").pack(side="left")
            tk.Label(linha, text=status, bg="white", width=15, anchor="w").pack(side="left")

            visualizar = tk.Label(
                linha,
                text="Visualizar",
                fg="blue",
                cursor="hand2",
                bg="white",
                font=("Arial", 10, "underline")
            )
            visualizar.pack(side="left", padx=5)
            visualizar.bind("<Button-1>", lambda e, ocorr=o: self._abrir_visualizar(ocorr))

    def _abrir_visualizar(self, ocorrencia):
        usuario_logado = self._controlador_ocorrencia._controlador_sistema.usuario_logado

        modal = tk.Toplevel(self.main_frame)
        modal.title("Visualizar Ocorrência")
        modal.geometry("600x400")
        modal.transient(self.main_frame)
        modal.grab_set()
        modal.configure(bg="#f5f5f5")

        card = tk.Frame(modal, bg="white", relief="solid", bd=1)
        card.pack(padx=30, pady=30, fill="both", expand=True)

        header = tk.Frame(card, bg="white")
        header.pack(fill="x", padx=20, pady=(20, 5))

        tk.Label(
            header,
            text=ocorrencia.titulo,
            bg="white",
            font=("Arial", 12, "bold"),
            anchor="w"
        ).pack(anchor="w")

        try:
            from datetime import datetime
            data_formatada = datetime.strptime(str(ocorrencia.data), "%Y-%m-%d").strftime("%d/%m/%Y")
        except Exception:
            data_formatada = str(ocorrencia.data)

        autor_data = f"{ocorrencia.morador.nome if ocorrencia.morador else 'Desconhecido'} - {data_formatada}"
        tk.Label(
            header,
            text=autor_data,
            bg="white",
            fg="#666666",
            font=("Arial", 10)
        ).pack(anchor="w")

        tk.Frame(card, height=1, bg="#e5e5e5").pack(fill="x", padx=20, pady=(5, 10))

        botoes_frame = tk.Frame(card, bg="white")
        botoes_frame.pack(side="bottom", fill="x", padx=20, pady=20)

        def criar_botao(texto, cor, comando):
            return tk.Button(
                botoes_frame,
                text=texto,
                bg=cor,
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                activebackground=cor,
                activeforeground="white",
                padx=15,
                pady=6,
                cursor="hand2",
                command=comando
            )

        if usuario_logado and usuario_logado.tipo_usuario.lower() == "morador":
            criar_botao("Editar", "#0d6efd", lambda: self._abrir_formulario_editar(ocorrencia)).pack(side="right", padx=5)
            criar_botao("Excluir", "#dc3545", lambda: self._excluir_ocorrencia(modal, ocorrencia)).pack(side="right", padx=5)

        elif usuario_logado and usuario_logado.tipo_usuario.lower() == "administrador":
            criar_botao("Editar", "#0d6efd", lambda: self._abrir_formulario_editar(ocorrencia)).pack(side="right", padx=5)
            criar_botao("Excluir", "#dc3545", lambda: self._excluir_ocorrencia(modal, ocorrencia)).pack(side="right", padx=5)
            criar_botao("Gerar Alerta", "#ffc107", lambda: self._abrir_modal_alerta()).pack(side="right", padx=5)

            if ocorrencia.status == "Pendente":
                criar_botao("Marcar como Finalizado", "#198754",
                            lambda: self._alterar_status_ocorrencia(modal, ocorrencia, "Finalizado")).pack(side="right", padx=5)
            elif ocorrencia.status == "Finalizado":
                criar_botao("Marcar como Pendente", "#198754",
                            lambda: self._alterar_status_ocorrencia(modal, ocorrencia, "Pendente")).pack(side="right", padx=5)

        from tkinter import font as tkfont
        import math

        descr_text = str(ocorrencia.descricao or "")
        wrap_pixels = 520
        fonte = tkfont.Font(family="Arial", size=10)
        linha_altura = fonte.metrics("linespace")

        def estimate_visual_lines(text, font_obj, wrap_px):
            total_lines = 0
            avg_char_width = max(1, font_obj.measure("abcdefghijklmnopqrstuvwxyz") / 26.0)

            for original_line in text.splitlines() or [""]:
                words = original_line.split(" ")
                cur_width = 0
                cur_line_count = 1
                for word in words:
                    word_w = font_obj.measure(word + " ")
                    if word_w > wrap_px:
                        chars_per_line = max(1, int(wrap_px / avg_char_width))
                        if cur_width > 0:
                            cur_line_count += 1
                            cur_width = 0
                        needed = math.ceil(len(word) / chars_per_line)
                        cur_line_count += (needed - 1)
                        cur_width = 0
                    else:
                        if cur_width + word_w <= wrap_px:
                            cur_width += word_w
                        else:
                            cur_line_count += 1
                            cur_width = word_w
                total_lines += cur_line_count
            return total_lines

        num_visual_lines = estimate_visual_lines(descr_text, fonte, wrap_pixels)
        MAX_VISIBLE_LINES = 5

        if num_visual_lines > MAX_VISIBLE_LINES:
            scroll_container = tk.Frame(card, bg="#f8f9fa")
            scroll_container.pack(fill="both", expand=False, padx=20, pady=(0, 10))

            canvas = tk.Canvas(scroll_container, bg="#f8f9fa", highlightthickness=0)
            canvas.pack(side="left", fill="both", expand=True)

            scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")
            canvas.configure(yscrollcommand=scrollbar.set)

            inner_frame = tk.Frame(canvas, bg="#f8f9fa")
            window_id = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

            def _on_configure_inner(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
            inner_frame.bind("<Configure>", _on_configure_inner)

            def _on_canvas_configure(event):
                canvas.itemconfig(window_id, width=event.width)
            canvas.bind("<Configure>", _on_canvas_configure)

            descricao_label = tk.Label(
                inner_frame,
                text=descr_text,
                bg="#f8f9fa",
                justify="left",
                anchor="nw",
                wraplength=wrap_pixels,
                font=("Arial", 10)
            )
            descricao_label.pack(fill="x", padx=10, pady=10, anchor="w")

            canvas.config(height=linha_altura * MAX_VISIBLE_LINES + 20)
        else:
            descricao_frame = tk.Frame(card, bg="#f8f9fa")
            descricao_frame.pack(fill="x", padx=20, pady=(0, 10))
            descricao_label = tk.Label(
                descricao_frame,
                text=descr_text,
                bg="#f8f9fa",
                justify="left",
                anchor="nw",
                wraplength=wrap_pixels,
                font=("Arial", 10)
            )
            descricao_label.pack(fill="x", padx=10, pady=10, anchor="w")

        rodape_info = tk.Frame(card, bg="white")
        rodape_info.pack(fill="x", padx=20, pady=(0, 10))
        tk.Label(
            rodape_info,
            text=f"Status atual: {ocorrencia.status}",
            bg="white",
            fg="#444",
            font=("Arial", 10, "italic")
        ).pack(anchor="w")

        modal.update()


    def _finalizar_ocorrencia(self, modal, ocorrencia):
        """Altera o status de 'Pendente' para 'Finalizado'."""
        confirm = messagebox.askyesno("Confirmar", "Deseja marcar esta ocorrência como finalizada?")
        if not confirm:
            return

        sucesso = self._controlador_ocorrencia.alterar_status_ocorrencia(ocorrencia.id, "Finalizado")

        if sucesso:
            messagebox.showinfo("Sucesso", "Ocorrência marcada como finalizada!")
            modal.destroy()
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", "Não foi possível atualizar o status da ocorrência.")

    def _gerar_alerta(self):
        """Exibe um modal informando que está em desenvolvimento."""
        alerta_modal = tk.Toplevel(self.main_frame)
        alerta_modal.title("Gerar Alerta")
        alerta_modal.geometry("300x150")
        alerta_modal.transient(self.main_frame)
        alerta_modal.grab_set()

        tk.Label(
            alerta_modal,
            text="Em desenvolvimento...",
            bg="white",
            font=("Arial", 11, "italic")
        ).pack(expand=True, fill="both", padx=20, pady=40)

        ttk.Button(alerta_modal, text="Fechar", command=alerta_modal.destroy).pack(pady=10)

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

    def _excluir_ocorrencia(self, modal_visualizar, ocorrencia):
        """Exibe um modal de confirmação antes de excluir a ocorrência."""
        def confirmar_exclusao():
            sucesso = self._controlador_ocorrencia.excluir_ocorrencia(ocorrencia.id)
            if sucesso:
                messagebox.showinfo("Resultado", "Ocorrência excluída com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível excluir a ocorrência.")
            confirm_modal.destroy()
            modal_visualizar.destroy()
            self.atualizar_lista()

        confirm_modal = tk.Toplevel(self.main_frame)
        confirm_modal.title("Confirmação")
        confirm_modal.geometry("350x150")
        confirm_modal.transient(self.main_frame)
        confirm_modal.grab_set()
        confirm_modal.configure(bg="white")

        tk.Label(
            confirm_modal,
            text="Deseja realmente excluir esta ocorrência?",
            bg="white",
            font=("Arial", 11),
            wraplength=300,
            justify="center"
        ).pack(expand=True, fill="both", padx=20, pady=20)

        botoes_frame = tk.Frame(confirm_modal, bg="white")
        botoes_frame.pack(pady=10)

        tk.Button(
            botoes_frame,
            text="Não",
            bg="#6c757d",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2",
            command=confirm_modal.destroy
        ).pack(side="left", padx=10)

        tk.Button(
            botoes_frame,
            text="Sim",
            bg="#198754",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2",
            command=confirmar_exclusao
        ).pack(side="right", padx=10)


    def _alterar_status_ocorrencia(self, modal, ocorrencia, novo_status):
        sucesso = self._controlador_ocorrencia.alterar_status_ocorrencia(ocorrencia.id, novo_status)
        if sucesso:
            modal.destroy()
            self.atualizar_lista()

    def _abrir_modal_alerta(self):
        alerta = tk.Toplevel(self.main_frame)
        alerta.title("Gerar Alerta")
        alerta.geometry("300x150")
        alerta.transient(self.main_frame)
        alerta.grab_set()

        frame = tk.Frame(alerta, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(frame, text="Em desenvolvimento...", bg="white", font=("Arial", 11)).pack(expand=True)
        ttk.Button(frame, text="Fechar", command=alerta.destroy).pack(pady=10)
