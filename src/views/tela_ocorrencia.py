import tkinter as tk
from tkinter import ttk, messagebox


class TelaOcorrencias:
    def __init__(self, container, controlador):
        self._controlador_ocorrencia = controlador
        self.main_frame = None
        self.linhas_frame = None

    def inicializar_componentes(self, container):
        self.main_frame = ttk.Frame(container)
        self.main_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("White.TFrame", background="white")
        self.main_frame.configure(style="White.TFrame")

        top_header = tk.Frame(self.main_frame, bg="white")
        top_header.pack(fill="x", pady=(0, 15), padx=20)

        tk.Label(top_header, text="⚠️ Ocorrências", font=("Arial", 20, "bold"),
                 bg="white").pack(side="left", pady=10)

        usuario = self._controlador_ocorrencia._controlador_sistema.usuario_logado
        eh_admin = (usuario.tipo_usuario == 'administrador')

        if not eh_admin:
            tk.Button(top_header, text="+ Nova Ocorrência",
                      bg="#0d6efd", fg="white", font=("Arial", 10, "bold"), relief="flat",
                      command=lambda: self._controlador_ocorrencia.abrir_tela_formulario()).pack(side="right", pady=10)

        self.header_frame = tk.Frame(self.main_frame, bg="#f8f9fa", relief="solid", bd=1)
        self.header_frame.pack(fill="x", padx=20)

        self.header_frame.columnconfigure(0, weight=0, minsize=100)
        self.header_frame.columnconfigure(1, weight=0, minsize=150)
        self.header_frame.columnconfigure(2, weight=1)
        self.header_frame.columnconfigure(3, weight=0, minsize=120)
        self.header_frame.columnconfigure(4, weight=0, minsize=200)

        pad = 8
        font_head = ("Arial", 10, "bold")
        bg_head = "#f8f9fa"

        tk.Label(self.header_frame, text="Data", font=font_head, bg=bg_head).grid(row=0, column=0, sticky="w", padx=pad,
                                                                                  pady=pad)
        tk.Label(self.header_frame, text="Morador", font=font_head, bg=bg_head).grid(row=0, column=1, sticky="w",
                                                                                     padx=pad, pady=pad)
        tk.Label(self.header_frame, text="Título", font=font_head, bg=bg_head).grid(row=0, column=2, sticky="w",
                                                                                    padx=pad, pady=pad)
        tk.Label(self.header_frame, text="Status", font=font_head, bg=bg_head).grid(row=0, column=3, sticky="w",
                                                                                    padx=pad, pady=pad)
        tk.Label(self.header_frame, text="Ações", font=font_head, bg=bg_head).grid(row=0, column=4, sticky="e",
                                                                                   padx=pad, pady=pad)

        canvas_container = tk.Frame(self.main_frame, bg="white")
        canvas_container.pack(fill="both", expand=True, padx=20)

        self.canvas = tk.Canvas(canvas_container, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)

        self.linhas_frame = tk.Frame(self.canvas, bg="white")

        self.linhas_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.linhas_frame, anchor="nw", width=1000)

        def _on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas.find_all()[0], width=event.width)

        self.canvas.bind("<Configure>", _on_canvas_configure)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def atualizar_lista(self):
        if self._controlador_ocorrencia:
            self._controlador_ocorrencia._atualizar_lista_ocorrencias()

    def exibir_ocorrencias(self, lista_ocorrencias):
        if self.linhas_frame is None:
            return

        for widget in self.linhas_frame.winfo_children():
            widget.destroy()

        if not lista_ocorrencias:
            tk.Label(self.linhas_frame, text="Nenhuma ocorrência encontrada.", bg="white", fg="#666").pack(pady=20)
            return

        usuario = self._controlador_ocorrencia._controlador_sistema.usuario_logado
        eh_admin = (usuario.tipo_usuario == 'administrador')

        for o in lista_ocorrencias:
            row = tk.Frame(self.linhas_frame, bg="white")
            row.pack(fill="x", pady=0)

            row.columnconfigure(0, weight=0, minsize=100)
            row.columnconfigure(1, weight=0, minsize=150)
            row.columnconfigure(2, weight=1)
            row.columnconfigure(3, weight=0, minsize=120)
            row.columnconfigure(4, weight=0, minsize=200)

            data_fmt = str(o.data)
            try:
                from datetime import datetime
                data_fmt = datetime.strptime(str(o.data), "%Y-%m-%d").strftime("%d/%m/%Y")
            except:
                pass

            pad = 8

            tk.Label(row, text=data_fmt, bg="white").grid(row=0, column=0, sticky="w", padx=pad, pady=pad)

            nome = o.morador.nome if o.morador else "Desconhecido"
            tk.Label(row, text=nome, bg="white").grid(row=0, column=1, sticky="w", padx=pad, pady=pad)

            tk.Label(row, text=o.titulo, bg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky="w",
                                                                                      padx=pad, pady=pad)

            bg_status = "#d1e7dd" if o.status == "Finalizado" else "#fff3cd"
            fg_status = "#0f5132" if o.status == "Finalizado" else "#664d03"

            lbl_status = tk.Label(row, text=o.status, bg=bg_status, fg=fg_status,
                                  font=('Arial', 8, 'bold'), padx=8, pady=2)
            lbl_status.grid(row=0, column=3, sticky="w", padx=pad, pady=pad)

            acoes_frame = tk.Frame(row, bg="white")
            acoes_frame.grid(row=0, column=4, sticky="e", padx=pad, pady=pad)

            tk.Button(acoes_frame, text="👁", bg="#17a2b8", fg="white", bd=0, width=3, cursor="hand2",
                      command=lambda id=o.id: self._controlador_ocorrencia.abrir_tela_visualizacao(id)).pack(side="left", padx=2)

            if eh_admin:
                txt_status = "Reabrir" if o.status == "Finalizado" else "Finalizar"
                bg_btn_status = "#ffc107" if o.status == "Finalizado" else "#198754"

                tk.Button(acoes_frame, text="✓", bg=bg_btn_status, fg="white", bd=0, width=3, cursor="hand2",
                          command=lambda id=o.id: self._controlador_ocorrencia.alterar_status_ocorrencia(id)).pack(side="left",
                                                                                                                   padx=2)

                tk.Button(acoes_frame, text="🗑", bg="#dc3545", fg="white", bd=0, width=3, cursor="hand2",
                          command=lambda id=o.id: self._controlador_ocorrencia.excluir_ocorrencia(id)).pack(side="left", padx=2)
            else:
                tk.Button(acoes_frame, text="✏️", bg="#ffc107", fg="black", bd=0, width=3, cursor="hand2",
                          command=lambda obj=o: self._controlador_ocorrencia.abrir_tela_formulario(obj)).pack(side="left", padx=2)

                tk.Button(acoes_frame, text="🗑", bg="#dc3545", fg="white", bd=0, width=3, cursor="hand2",
                          command=lambda id=o.id: self._controlador_ocorrencia.excluir_ocorrencia(id)).pack(side="left", padx=2)

            tk.Frame(self.linhas_frame, height=1, bg="#e0e0e0").pack(fill="x")

    def mostrar_erro(self, msg):
        messagebox.showerror("Erro", msg)