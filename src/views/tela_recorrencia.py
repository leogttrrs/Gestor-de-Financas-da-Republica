import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.models.Divida import Divida
from src.models.Morador import Morador


class TelaRecorrencia(tk.Toplevel):
    def __init__(self, parent, controlador, moradores: list[Morador], divida_existente: Divida = None):
        super().__init__(parent)
        self.controlador = controlador
        self.divida_existente = divida_existente
        self.moradores = moradores
        self.moradores_map = {m.nome: m.id for m in moradores}

        self.title("Adicionar Nova Dívida")
        self.geometry("400x400")
        self.transient(parent)
        self.grab_set()

        self.desc_var = tk.StringVar()
        self.valor_var = tk.StringVar()
        self.morador_var = tk.StringVar()
        self.vencimento_var = tk.StringVar()
        self.recorrencia_var = tk.StringVar()

        self.vencimento_var.trace_add('write', self._formatar_data)
        self._is_formatting = False

        self._criar_estilos()
        self._criar_formulario()


    def _formatar_data(self, *args):
        if self._is_formatting:
            return

        self._is_formatting = True

        texto_atual = self.vencimento_var.get()
        numeros = "".join(filter(str.isdigit, texto_atual))
        numeros = numeros[:8]

        formatado = ""
        if len(numeros) > 4:
            formatado = f"{numeros[:2]}/{numeros[2:4]}/{numeros[4:]}"
        elif len(numeros) > 2:
            formatado = f"{numeros[:2]}/{numeros[2:]}"
        else:
            formatado = numeros

        self.vencimento_var.set(formatado)
        self._is_formatting = False

    def _criar_estilos(self):
        style = ttk.Style()
        style.configure("Salvar.TButton", foreground="white", background="#28a745", borderwidth=0, font=('Arial', 10))
        style.map("Salvar.TButton", background=[('active', '#218838')])

    def _criar_formulario(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Descrição:", font=('Arial', 10, 'bold')).pack(anchor="w")
        ttk.Entry(frame, textvariable=self.desc_var, font=('Arial', 10)).pack(fill="x", pady=(0, 10), ipady=4)

        ttk.Label(frame, text="Valor", font=('Arial', 10, 'bold')).pack(anchor="w")
        ttk.Entry(frame, textvariable=self.valor_var, font=('Arial', 10)).pack(fill="x", pady=(0, 10), ipady=4)

        ttk.Label(frame, text="Morador:", font=('Arial', 10, 'bold')).pack(anchor="w")
        combo_moradores = ttk.Combobox(frame, textvariable=self.morador_var,
                                       values=list(self.moradores_map.keys()), state="readonly", font=('Arial', 10))
        combo_moradores.pack(fill="x", pady=(0, 10), ipady=4)

        ttk.Label(frame, text="Dia de vencimento:", font=('Arial', 10, 'bold')).pack(anchor="w")
        ttk.Entry(frame, textvariable=self.vencimento_var, font=('Arial', 10)).pack(fill="x", pady=(0, 20), ipady=4)

        ttk.Label(frame, text="Quantidade de recorrênica", font=('Arial', 10, 'bold')).pack(anchor="w")
        ttk.Entry(frame, textvariable=self.recorrencia_var, font=('Arial', 10)).pack(fill="x", pady=(0, 20), ipady=4)

        botoes_frame = ttk.Frame(frame)
        botoes_frame.pack(fill="x", side="bottom")

        btn_salvar = ttk.Button(botoes_frame, text="Salvar Dívidas", style="Salvar.TButton", command=self._salvar)
        btn_salvar.pack(side="right")

        btn_cancelar = ttk.Button(botoes_frame, text="Cancelar", command=self.destroy)
        btn_cancelar.pack(side="right", padx=10)

    def _salvar(self):
        try:
            nome_morador = self.morador_var.get()
            data_venc_str = int(self.vencimento_var.get())
            valor_str = self.valor_var.get()

            if not all([self.desc_var.get(), valor_str, nome_morador, data_venc_str]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios.", parent=self)
                return
            data_venc_db = data_venc_str
            valor_float = float(valor_str.replace(',', '.'))
            recorrencia_int = int(self.recorrencia_var.get())

            morador_id = self.moradores_map[nome_morador]

            morador = Morador.buscar_por_id(morador_id)

            dados = {
                "id": self.divida_existente.id if self.divida_existente else None,
                "descricao": self.desc_var.get(),
                "valor": valor_float,
                "morador": morador,
                "data_vencimento": data_venc_db,
                "recorrencia": recorrencia_int,
                "status": 'pendente'
            }

            if self.controlador.salvar_divida_recorrencia(dados):
                self.destroy()

        except ValueError:
            messagebox.showerror("Erro",
                                 "Formato de data ou valor inválido. Use DD/MM/AAAA e, para valor, use números (ex: 150,75).",
                                 parent=self)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self)