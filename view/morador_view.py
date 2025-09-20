import tkinter as tk
from tkinter import messagebox

class MoradorView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Sistema de República - Morador")
        self.geometry("500x400")

        # Container para as telas
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dicionário de telas
        self.frames = {}

        for F in (MenuPrincipal, TelaOcorrencias, TelaContatos, TelaMoradores,
                  TelaAlertas, TelaDividas, TelaPagamento):
            frame = F(container, self, controller)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela(MenuPrincipal)

    def exibir_lista(self, itens, titulo="Lista"):
        janela = tk.Toplevel(self)
        janela.title(titulo)
        for item in itens:
            tk.Label(janela, text=str(item)).pack()

    def exibir_mensagem(self, mensagem, titulo="Informação"):
        """Mostra uma mensagem em uma janela popup."""
        messagebox.showinfo(titulo, mensagem)

    def mostrar_tela(self, tela):
        frame = self.frames[tela]
        frame.tkraise()


# ---------- TELAS ----------

class MenuPrincipal(tk.Frame):
    def __init__(self, parent, root, controller):
        super().__init__(parent)
        tk.Label(self, text="Menu Principal", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Gerenciar Ocorrências",
                  command=lambda: root.mostrar_tela(TelaOcorrencias)).pack(fill="x", pady=5)

        tk.Button(self, text="Visualizar Contatos e Quartos",
                  command=lambda: root.mostrar_tela(TelaContatos)).pack(fill="x", pady=5)

        tk.Button(self, text="Consultar Lista de Moradores",
                  command=lambda: root.mostrar_tela(TelaMoradores)).pack(fill="x", pady=5)

        tk.Button(self, text="Visualizar Alertas",
                  command=lambda: root.mostrar_tela(TelaAlertas)).pack(fill="x", pady=5)

        tk.Button(self, text="Consultar Histórico de Dívidas",
                  command=lambda: root.mostrar_tela(TelaDividas)).pack(fill="x", pady=5)

        tk.Button(self, text="Registrar Solicitação de Pagamento de Dívida",
                  command=lambda: root.mostrar_tela(TelaPagamento)).pack(fill="x", pady=5)

        tk.Button(self, text="Sair", command=root.quit).pack(fill="x", pady=20)


class TelaOcorrencias(tk.Frame):
    def __init__(self, parent, root, controller):
        super().__init__(parent)
        tk.Label(self, text="Gerenciar Ocorrências", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Button(self, text="Registrar Ocorrência Exemplo",
                  command=controller.gerenciar_ocorrencias).pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: root.mostrar_tela(MenuPrincipal)).pack(pady=10)


class TelaContatos(tk.Frame):
    def __init__(self, parent, root, controller):
        super().__init__(parent)
        tk.Label(self, text="Visualizar Contatos e Quartos", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Button(self, text="Mostrar Contatos",
                  command=controller.visualizar_contatos_e_quartos).pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: root.mostrar_tela(MenuPrincipal)).pack(pady=10)


class TelaMoradores(tk.Frame):
    def __init__(self, parent, root, controller):
        super().__init__(parent)
        tk.Label(self, text="Lista de Moradores", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Button(self, text="Mostrar Moradores",
                  command=controller.consultar_lista_moradores).pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: root.mostrar_tela(MenuPrincipal)).pack(pady=10)


class TelaAlertas(tk.Frame):
    def __init__(self, parent, root, controller):
        super().__init__(parent)
        tk.Label(self, text="Visualizar Alertas", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Button(self, text="Mostrar Alertas",
                  command=controller.visualizar_alertas).pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: root.mostrar_tela(MenuPrincipal)).pack(pady=10)


class TelaDividas(tk.Frame):
    def __init__(self, parent, root, controller):
        super().__init__(parent)
        tk.Label(self, text="Histórico de Dívidas", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Button(self, text="Mostrar Dívidas",
                  command=controller.consultar_historico_dividas).pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: root.mostrar_tela(MenuPrincipal)).pack(pady=10)


class TelaPagamento(tk.Frame):
    def __init__(self, parent, root, controller):
        super().__init__(parent)
        tk.Label(self, text="Solicitação de Pagamento", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Button(self, text="Registrar Pagamento",
                  command=controller.registrar_solicitacao_pagamento).pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: root.mostrar_tela(MenuPrincipal)).pack(pady=10)
