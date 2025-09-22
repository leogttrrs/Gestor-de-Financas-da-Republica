# arquivo: src/views/tela_gerenciar_quartos.py

import tkinter as tk
from tkinter import ttk
from .aplicacao_spa import ComponenteBase
from ..models.Quarto import Quarto


class TelaQuarto(ComponenteBase):
    def __init__(self, container, controlador_sistema, on_back=None):
        super().__init__(container, controlador_sistema)
        self.on_back = on_back
        self.frame_lista = None

        self._configurar_estilos()

        self._criar_interface()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.configure("Status.Disponivel.TLabel", foreground="#28a745", font=('Arial', 9, 'bold'))
        style.configure("Status.Ocupado.TLabel", foreground="#dc3545", font=('Arial', 9, 'bold'))

        style.configure("Editar.TButton", foreground="white", background="#007bff", borderwidth=0, font=('Arial', 9))
        style.configure("Excluir.TButton", foreground="white", background="#dc3545", borderwidth=0, font=('Arial', 9))

        style.map("Editar.TButton", background=[('active', '#0069d9')])
        style.map("Excluir.TButton", background=[('active', '#c82333')])

    def _criar_interface(self):
        self.criar_frame()

        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill="x", pady=(0, 20))

        title_label = ttk.Label(header_frame, text="Gerenciar Quartos", font=("Arial", 20, "bold"))
        title_label.pack(side="left")

        btn_adicionar = ttk.Button(header_frame, text="+ Adicionar Quarto",
                                   command=self.controlador_sistema.controlador_quarto.abrir_tela_formulario)
        btn_adicionar.pack(side="right")

        list_container = ttk.Frame(self.frame)
        list_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(list_container)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)

        self.frame_lista = ttk.Frame(canvas, padding=(5, 5))
        self.frame_lista.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.frame_lista, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.atualizar_lista()

    def atualizar_lista(self):
        quartos = Quarto.buscar_todos()

        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        headers = ["Número", "Tamanho (m²)", "Status", "Morador", "Ações"]
        weights = [1, 1, 1, 3, 2]

        for i, header in enumerate(headers):
            self.frame_lista.columnconfigure(i, weight=weights[i])
            ttk.Label(self.frame_lista, text=header, font=("Arial", 10, "bold")).grid(row=0, column=i, sticky="w",
                                                                                      padx=5)

        for i, quarto in enumerate(quartos):
            row = i + 1
            moradores_str = ", ".join(quarto.moradores) if quarto.moradores else "Vazio"

            status_style = "Status.Ocupado.TLabel" if quarto.status == "Ocupado" else "Status.Disponivel.TLabel"

            ttk.Label(self.frame_lista, text=quarto.numero_quarto).grid(row=row, column=0, sticky="w", padx=5, pady=5)
            ttk.Label(self.frame_lista, text=quarto.tamanho).grid(row=row, column=1, sticky="w", padx=5, pady=5)
            ttk.Label(self.frame_lista, text=quarto.status, style=status_style).grid(row=row, column=2, sticky="w",
                                                                                     padx=5, pady=5)
            ttk.Label(self.frame_lista, text=moradores_str, wraplength=200).grid(row=row, column=3, sticky="w", padx=5,
                                                                                 pady=5)

            action_frame = ttk.Frame(self.frame_lista)
            action_frame.grid(row=row, column=4, sticky="w", padx=5)

            btn_editar = ttk.Button(action_frame, text="Editar", style="Editar.TButton",
                                    command=lambda
                                        q=quarto: self.controlador_sistema.controlador_quarto.abrir_tela_formulario(
                                        quarto_existente=q))
            btn_editar.pack(side="left")

            btn_excluir = ttk.Button(action_frame, text="Excluir", style="Excluir.TButton",
                                     command=lambda
                                         q_id=quarto.id: self.controlador_sistema.controlador_quarto.excluir_quarto(
                                         q_id))
            btn_excluir.pack(side="left", padx=5)