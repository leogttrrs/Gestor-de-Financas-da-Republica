import tkinter as tk
import tela_login

def criar_janela_administrador():

    # --- Configuração da Janela ---
    janela_administrador = tk.Tk()
    janela_administrador.title("Acesso Concedido")
    janela_administrador.geometry("400x200") # Define o tamanho da janela

    # --- Centralizando a Janela na Tela ---
    largura_janela = 400
    altura_janela = 200
    largura_tela = janela_administrador.winfo_screenwidth()
    altura_tela = janela_administrador.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura_janela // 2)
    pos_y = (altura_tela // 2) - (altura_janela // 2)
    janela_administrador.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    # --- Criação do Widget (Rótulo com a mensagem) ---
    label_mensagem = tk.Label(
        janela_administrador,
        text="Você é um administrador",
        font=("Arial", 16, "bold") # Define a fonte, tamanho e estilo
    )
    # .pack() com expand=True centraliza o widget na janela
    label_mensagem.pack(expand=True)

    #Botão de Gerenciar Usuários
    botao_gerenciar = tk.Button(janela_administrador, text="Gerenciar Usuários", command=lambda: print("Função de Gerenciar Usuários não implementada."), width=20)
    botao_gerenciar.pack(pady=10)

    # Botão de Logoff
    botao_logoff = tk.Button(janela_administrador, text="Sair", command=lambda: [janela_administrador.destroy(), tela_login.criar_janela_login()], width=10)
    botao_logoff.pack(pady=10)

    # --- Iniciar o Loop Principal da Interface ---
    janela_administrador.mainloop()

