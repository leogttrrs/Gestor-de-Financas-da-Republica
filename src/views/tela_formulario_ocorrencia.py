import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.models.Ocorrencia import Ocorrencia


class TelaFormularioOcorrencia(tk.Toplevel):
    def __init__(self, parent, controlador_ocorrencia, ocorrencia_existente: Ocorrencia = None):
        super().__init__(parent)
        self.controlador = controlador_ocorrencia
        self.ocorrencia_existente = ocorrencia_existente

        usuario = getattr(self.controlador._controlador_sistema, "usuario_logado", None)
        if not usuario:
            messagebox.showerror("Acesso Negado", "Nenhum usuário logado.", parent=parent)
            self.destroy()
            return

        self.usuario_logado = usuario

        self.title("Editar Ocorrência" if ocorrencia_existente else "Registrar Ocorrência")
        self.geometry("450x380")
        self.transient(parent)
        self.grab_set()

        # Variáveis
        self.titulo_var = tk.StringVar()
        self.descricao_var = tk.StringVar()

        # Estilos e Formulário
        self._criar_estilos()
        self._criar_formulario()

        # Carregar dados da ocorrência existente
        if ocorrencia_existente:
            self.titulo_var.set(ocorrencia_existente.titulo)
            self.descricao_text.insert("1.0", ocorrencia_existente.descricao)

    # ----------------------------
    # ESTILOS
    # ----------------------------
    def _criar_estilos(self):
        style = ttk.Style()
        style.configure("Salvar.TButton", foreground="white", background="#007bff",
                        borderwidth=0, font=('Arial', 10, 'bold'))
        style.map("Salvar.TButton", background=[('active', '#0056b3')])

    # ----------------------------
    # FORMULÁRIO
    # ----------------------------
    def _criar_formulario(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        # Título
        ttk.Label(frame, text="Título:", font=('Arial', 10, 'bold')).pack(anchor="w")
        ttk.Entry(frame, textvariable=self.titulo_var, font=('Arial', 10)).pack(fill="x", pady=(0, 10), ipady=4)

        # Descrição
        ttk.Label(frame, text="Descrição:", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.descricao_text = tk.Text(frame, height=8, wrap="word", font=('Arial', 10))
        self.descricao_text.pack(fill="both", expand=True, pady=(0, 15))

        # Botões
        botoes_frame = ttk.Frame(frame)
        botoes_frame.pack(fill="x")

        btn_salvar = ttk.Button(botoes_frame, text="Salvar Ocorrência",
                                style="Salvar.TButton", command=self._salvar)
        btn_salvar.pack(side="right")

        btn_cancelar = ttk.Button(botoes_frame, text="Cancelar", command=self.destroy)
        btn_cancelar.pack(side="right", padx=10)

    # ----------------------------
    # SALVAR
    # ----------------------------
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

            # EDITAR
            if self.ocorrencia_existente:
                self.ocorrencia_existente.titulo = titulo
                self.ocorrencia_existente.descricao = descricao
                self.ocorrencia_existente.salvar()

            else:
                # NOVA OCORRÊNCIA
                resultado = self.controlador.cadastrar_ocorrencia(dados)

                if not isinstance(resultado, Ocorrencia):
                    messagebox.showerror("Erro", f"Falha ao salvar: {resultado}", parent=self)
                    return

            # Atualiza a lista da tela de ocorrências, se existir
            if getattr(self.controlador, "_tela_ocorrencia", None):
                self.controlador._tela_ocorrencia.atualizar_lista()

            messagebox.showinfo("Sucesso", "Ocorrência salva com sucesso!", parent=self)
            self.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self)
