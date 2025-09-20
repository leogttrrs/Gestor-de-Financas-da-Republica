import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

import database
from Quarto import Quarto
from JanelaQuarto import JanelaQuarto
from database_setup import conectar_db, criar_tabela_quartos


class GerenciadorQuartosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Quartos")

        self.conn = conectar_db()
        criar_tabela_quartos(self.conn)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.state('zoomed')
        self.root.bind('<Escape>', lambda event: self.toggle_fullscreen())
        self.configurar_estilos()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0)
        label_titulo = ttk.Label(main_frame, text="Gerenciar quartos", font=("Helvetica", 16, "bold"))
        label_titulo.pack(pady=(0, 20))
        list_container = ttk.Frame(main_frame)
        list_container.pack(pady=10)
        canvas = tk.Canvas(list_container, width=950, height=500)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        self.frame_lista = ttk.Frame(canvas, padding=(5, 5))
        self.frame_lista.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.frame_lista, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        btn_adicionar = ttk.Button(main_frame, text="Adicionar Quarto", command=self.adicionar_quarto,
                                   style="Adicionar.TButton", padding=(10, 5))
        btn_adicionar.pack(pady=20)
        self.atualizar_lista_quartos()

    def on_closing(self):
        if self.conn:
            self.conn.close()
        self.root.destroy()

    def atualizar_lista_quartos(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quartos ORDER BY numero")
        rows = cursor.fetchall()

        quartos_do_db = []
        moradores_map = {m.id: m for m in database.moradores_db}
        for row in rows:
            quarto = Quarto(id=row[0], numero=row[1], tamanho=row[2], capacidade=row[3], status=row[4])
            if row[5]:
                ids = [int(id_str) for id_str in row[5].split(',')]
                quarto.moradores = [moradores_map[mid] for mid in ids if mid in moradores_map]
            quartos_do_db.append(quarto)

        self.frame_lista.columnconfigure(0, weight=1, uniform="group1")
        headers = ["Número", "Tamanho (m²)", "Capacidade", "Status", "Moradores", "Ações"]
        for i, header in enumerate(headers):
            ttk.Label(self.frame_lista, text=header, font=("Helvetica", 10, "bold")).grid(row=0, column=i, sticky="w",
                                                                                          padx=5, pady=5)
        ttk.Separator(self.frame_lista, orient='horizontal').grid(row=1, columnspan=len(headers), sticky='ew',
                                                                  pady=(5, 10))

        for i, quarto in enumerate(quartos_do_db):
            current_row = i + 2
            moradores_nomes = ", ".join([m.nome for m in quarto.moradores]) if quarto.moradores else "Vazio"
            status_style = ""
            if quarto.status == "Disponível":
                status_style = "Status.Disponivel.TLabel"
            elif quarto.status == "Ocupado":
                status_style = "Status.Ocupado.TLabel"
            elif quarto.status == "Manutenção":
                status_style = "Status.Manutencao.TLabel"
            ttk.Label(self.frame_lista, text=quarto.numero).grid(row=current_row, column=0, sticky="w", padx=5)
            ttk.Label(self.frame_lista, text=f"{quarto.tamanho:.1f}").grid(row=current_row, column=1, sticky="w",
                                                                           padx=5)
            ttk.Label(self.frame_lista, text=quarto.capacidade).grid(row=current_row, column=2, sticky="w", padx=5)
            ttk.Label(self.frame_lista, text=quarto.status.upper(), style=status_style).grid(row=current_row, column=3,
                                                                                             sticky="w", padx=5, pady=2)
            ttk.Label(self.frame_lista, text=moradores_nomes, wraplength=200, justify="left").grid(row=current_row,
                                                                                                   column=4, sticky="w",
                                                                                                   padx=5)
            action_frame = ttk.Frame(self.frame_lista)
            action_frame.grid(row=current_row, column=5, sticky="w", padx=5)
            btn_editar = ttk.Button(action_frame, text="Editar", style="Editar.TButton",
                                    command=lambda q_id=quarto.id: self.editar_quarto(q_id))
            btn_editar.pack(side="left", padx=2)
            btn_excluir = ttk.Button(action_frame, text="Excluir", style="Excluir.TButton",
                                     command=lambda q_id=quarto.id: self.excluir_quarto(q_id))
            btn_excluir.pack(side="left", padx=2)

    def salvar_quarto(self, dados_quarto):
        moradores_str = ",".join(map(str, dados_quarto["moradores_ids"]))
        cursor = self.conn.cursor()

        try:
            if "id" in dados_quarto:
                query = """ UPDATE quartos SET numero=?, tamanho=?, capacidade=?, status=?, moradores_ids_str=?
                            WHERE id=? """
                params = (dados_quarto["numero"], dados_quarto["tamanho"], dados_quarto["capacidade"],
                          dados_quarto["status"], moradores_str, dados_quarto["id"])
            else:
                query = """ INSERT INTO quartos (numero, tamanho, capacidade, status, moradores_ids_str)
                            VALUES (?, ?, ?, ?, ?) """
                params = (dados_quarto["numero"], dados_quarto["tamanho"], dados_quarto["capacidade"],
                          dados_quarto["status"], moradores_str)

            cursor.execute(query, params)
            self.conn.commit()

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro de Validação", f"O quarto número {dados_quarto['numero']} já existe.")
            return

        self.atualizar_lista_quartos()

    def excluir_quarto(self, quarto_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT moradores_ids_str FROM quartos WHERE id=?", (quarto_id,))
        result = cursor.fetchone()

        if result and result[0]:
            messagebox.showerror("Ação Proibida", "Não é possível excluir um quarto que possui moradores.")
            return

        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este quarto?"):
            cursor.execute("DELETE FROM quartos WHERE id=?", (quarto_id,))
            self.conn.commit()
            self.atualizar_lista_quartos()

    def toggle_fullscreen(self):
        current_state = self.root.state()
        new_state = 'normal' if current_state == 'zoomed' else 'zoomed'
        self.root.state(new_state)

    def configurar_estilos(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure("Status.Disponivel.TLabel", background="#28a745", foreground="white", padding=(5, 2),
                        font=('Helvetica', 8, 'bold'))
        style.configure("Status.Ocupado.TLabel", background="#dc3545", foreground="white", padding=(5, 2),
                        font=('Helvetica', 8, 'bold'))
        style.configure("Status.Manutencao.TLabel", background="#ffc107", foreground="black", padding=(5, 2),
                        font=('Helvetica', 8, 'bold'))
        style.configure("Adicionar.TButton", foreground="white", background="#28a745", borderwidth=0,
                        font=('Helvetica', 10, 'bold'))
        style.configure("Editar.TButton", foreground="white", background="#007bff", borderwidth=0,
                        font=('Helvetica', 9))
        style.configure("Excluir.TButton", foreground="white", background="#dc3545", borderwidth=0,
                        font=('Helvetica', 9))
        style.map("Adicionar.TButton", background=[('active', '#218838')])
        style.map("Editar.TButton", background=[('active', '#0069d9')])
        style.map("Excluir.TButton", background=[('active', '#c82333')])

    def get_moradores_alocados_ids(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT moradores_ids_str FROM quartos")
        rows = cursor.fetchall()
        ids = set()
        for row in rows:
            if row[0]:
                ids.update(int(id_str) for id_str in row[0].split(','))
        return ids

    def adicionar_quarto(self):
        moradores_alocados = self.get_moradores_alocados_ids()
        moradores_disponiveis = [m for m in database.moradores_db if m.id not in moradores_alocados]
        JanelaQuarto(self.root, self.salvar_quarto, moradores_disponiveis)

    def editar_quarto(self, quarto_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quartos WHERE id=?", (quarto_id,))
        row = cursor.fetchone()
        if not row: return

        quarto_selecionado = Quarto(id=row[0], numero=row[1], tamanho=row[2], capacidade=row[3], status=row[4])
        moradores_map = {m.id: m for m in database.moradores_db}
        if row[5]:
            ids = [int(id_str) for id_str in row[5].split(',')]
            quarto_selecionado.moradores = [moradores_map[mid] for mid in ids if mid in moradores_map]

        moradores_alocados = self.get_moradores_alocados_ids()
        ids_moradores_neste_quarto = {m.id for m in quarto_selecionado.moradores}
        moradores_para_exibir = [
            m for m in database.moradores_db
            if m.id not in moradores_alocados or m.id in ids_moradores_neste_quarto
        ]
        JanelaQuarto(self.root, self.salvar_quarto, moradores_para_exibir, quarto_selecionado)
