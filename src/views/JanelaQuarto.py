import tkinter as tk
from tkinter import ttk, messagebox


class JanelaQuarto(tk.Toplevel):
    def __init__(self, parent, callback_salvar, all_moradores, quarto=None):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()

        self.callback_salvar = callback_salvar
        self.quarto_original = quarto
        self.all_moradores = all_moradores

        self.title("Editar Quarto" if quarto else "Adicionar Quarto")

        frame = ttk.Frame(self, padding="15")
        frame.pack(expand=True, fill="both")

        dados_frame = ttk.LabelFrame(frame, text="Dados do Quarto", padding="10")
        dados_frame.pack(fill="x", expand=True)

        ttk.Label(dados_frame, text="Número:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.entry_numero = ttk.Entry(dados_frame)
        self.entry_numero.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(dados_frame, text="Tamanho (m²):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.entry_tamanho = ttk.Entry(dados_frame)
        self.entry_tamanho.grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(dados_frame, text="Capacidade:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.entry_capacidade = ttk.Entry(dados_frame)
        self.entry_capacidade.grid(row=2, column=1, sticky="ew", padx=5)

        ttk.Label(dados_frame, text="Status:").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        self.combo_status = ttk.Combobox(dados_frame, values=["Disponível", "Manutenção"], state="readonly")
        self.combo_status.grid(row=3, column=1, sticky="ew", padx=5)

        dados_frame.columnconfigure(1, weight=1)

        moradores_frame = ttk.LabelFrame(frame, text="Moradores", padding="10")
        moradores_frame.pack(fill="both", expand=True, pady=10)

        canvas = tk.Canvas(moradores_frame)
        scrollbar = ttk.Scrollbar(moradores_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.moradores_vars = []

        if self.all_moradores:
            for morador in self.all_moradores:
                var = tk.IntVar()
                cb = ttk.Checkbutton(scrollable_frame, text=morador.nome, variable=var)
                cb.pack(anchor="w", padx=5)
                self.moradores_vars.append((morador.id, var))
        else:
            ttk.Label(scrollable_frame, text="Nenhum morador disponível para seleção.").pack(padx=5, pady=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if quarto:
            self.entry_numero.insert(0, quarto.numero)
            self.entry_tamanho.insert(0, quarto.tamanho)
            self.entry_capacidade.insert(0, quarto.capacidade)
            if quarto.status != "Ocupado":
                self.combo_status.set(quarto.status)
            else:
                self.combo_status.set("Disponível")
            morador_ids_no_quarto = {m.id for m in quarto.moradores}
            for morador_id, var in self.moradores_vars:
                if morador_id in morador_ids_no_quarto:
                    var.set(1)
        else:
            self.combo_status.set("Disponível")

        btn_salvar = ttk.Button(frame, text="Salvar", command=self.salvar, style="Adicionar.TButton", padding=(10, 5))
        btn_salvar.pack(pady=10)

        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def salvar(self):
        try:
            numero = int(self.entry_numero.get())
            tamanho = float(self.entry_tamanho.get())
            capacidade = int(self.entry_capacidade.get())
            status_selecionado = self.combo_status.get()
            if not all([numero, tamanho, status_selecionado]):
                messagebox.showerror("Erro de Validação", "Todos os campos de dados devem ser preenchidos.",
                                     parent=self)
                return
        except ValueError:
            messagebox.showerror("Erro de Validação", "Os campos de dados devem ser numéricos.", parent=self)
            return

        selected_morador_ids = [morador_id for morador_id, var in self.moradores_vars if var.get() == 1]
        num_moradores = len(selected_morador_ids)

        if num_moradores > capacidade:
            messagebox.showerror("Erro de Capacidade",
                                 f"O número de moradores selecionados ({num_moradores}) excede a capacidade do quarto ({capacidade}).",
                                 parent=self)
            return
        if status_selecionado == "Manutenção" and num_moradores > 0:
            messagebox.showerror("Erro de Status",
                                 "Um quarto em manutenção não pode ter moradores",
                                 parent=self)
            return

        final_status = ""
        if num_moradores == capacidade and capacidade > 0:
            final_status = "Ocupado"
        else:
            final_status = status_selecionado

        dados_quarto = {"numero": numero, "tamanho": tamanho, "capacidade": capacidade, "status": final_status,
                        "moradores_ids": selected_morador_ids}
        if self.quarto_original:
            dados_quarto["id"] = self.quarto_original.id
        self.callback_salvar(dados_quarto)
        self.destroy()