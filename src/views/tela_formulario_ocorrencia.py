import tkinter as tk
from tkinter import ttk, messagebox
from src.models.Ocorrencia import Ocorrencia


class TelaFormularioOcorrencia(tk.Toplevel):
    def __init__(self, parent, controlador_ocorrencia, ocorrencia_existente: Ocorrencia = None,
                 visualizar_apenas=False):
        super().__init__(parent)
        self._controlador_ocorrencia = controlador_ocorrencia
        self.ocorrencia_existente = ocorrencia_existente
        self.visualizar_apenas = visualizar_apenas

        usuario = getattr(self._controlador_ocorrencia._controlador_sistema, "usuario_logado", None)
        if not usuario and not visualizar_apenas:
            if not usuario:
                messagebox.showerror("Acesso Negado", "Nenhum usuário logado.", parent=parent)
                self.destroy()
                return
        self.usuario_logado = usuario

        if visualizar_apenas:
            titulo = "Visualizar Ocorrência"
        elif ocorrencia_existente:
            titulo = "Editar Ocorrência"
        else:
            titulo = "Registrar Ocorrência"

        self.title(titulo)
        self.geometry("500x450")
        self.configure(bg="white")
        self.transient(parent)
        self.titulo_var = tk.StringVar()
        self._criar_estilos()
        self._criar_formulario()
        self._carregar_dados()
        self.wait_visibility()
        self.grab_set()

    def _criar_estilos(self):
        style = ttk.Style()
        style.configure("Salvar.TButton", foreground="white", background="#007bff",
                        borderwidth=0, font=('Arial', 10, 'bold'))
        style.map("Salvar.TButton", background=[('active', '#0056b3')])
        style.configure("Form.TLabel", background="white", font=('Arial', 10, 'bold'))
        style.configure("Form.TFrame", background="white")

    def _criar_formulario(self):
        frame = ttk.Frame(self, padding=20, style="Form.TFrame")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Título:", style="Form.TLabel").pack(anchor="w")
        self.entry_titulo = ttk.Entry(frame, textvariable=self.titulo_var, font=('Arial', 10))
        self.entry_titulo.pack(fill="x", pady=(0, 10), ipady=4)

        ttk.Label(frame, text="Descrição Completa:", style="Form.TLabel").pack(anchor="w")

        desc_container = ttk.Frame(frame)
        desc_container.pack(fill="both", expand=True, pady=(0, 15))

        scrollbar = ttk.Scrollbar(desc_container)
        scrollbar.pack(side="right", fill="y")

        self.descricao_text = tk.Text(desc_container, height=10, wrap="word", font=('Arial', 10),
                                      yscrollcommand=scrollbar.set, relief="solid", bd=1)
        self.descricao_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.descricao_text.yview)

        botoes_frame = ttk.Frame(frame, style="Form.TFrame")
        botoes_frame.pack(fill="x", pady=(10, 0))

        if not self.visualizar_apenas:
            btn_salvar = ttk.Button(botoes_frame, text="Salvar Ocorrência",
                                    style="Salvar.TButton", command=self._salvar)
            btn_salvar.pack(side="right")
            btn_cancelar = ttk.Button(botoes_frame, text="Cancelar", command=self.destroy)
            btn_cancelar.pack(side="right", padx=10)
        else:
            btn_fechar = ttk.Button(botoes_frame, text="Fechar Visualização", command=self.destroy)
            btn_fechar.pack(side="right")

    def _carregar_dados(self):
        if self.ocorrencia_existente:
            self.titulo_var.set(self.ocorrencia_existente.titulo)
            self.descricao_text.insert("1.0", self.ocorrencia_existente.descricao)

            if self.visualizar_apenas:
                self.entry_titulo.configure(state='readonly')
                self.descricao_text.configure(state='disabled', bg="#f9f9f9")

    def _salvar(self):
        try:
            titulo = self.titulo_var.get().strip()
            descricao = self.descricao_text.get("1.0", "end").strip()

            if not titulo or not descricao:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios.", parent=self)
                return

            dados = {
                "titulo": titulo,
                "descricao": descricao,
                "morador": self.usuario_logado
            }

            if self.ocorrencia_existente:
                self.ocorrencia_existente.titulo = titulo
                self.ocorrencia_existente.descricao = descricao
                self.ocorrencia_existente.salvar()
            else:
                resultado = self._controlador_ocorrencia.cadastrar_ocorrencia(dados)
                if not isinstance(resultado, Ocorrencia):
                    messagebox.showerror("Erro", f"Falha ao salvar: {resultado}", parent=self)
                    return

            if getattr(self._controlador_ocorrencia, "_tela_ocorrencia", None):
                self._controlador_ocorrencia._tela_ocorrencia.atualizar_lista()

            messagebox.showinfo("Sucesso", "Ocorrência salva com sucesso!", parent=self)
            self.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self)