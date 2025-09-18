import tkinter as tk

def criar_janela_adm():
   
    # --- Configuração da Janela ---
    janela_adm = tk.Tk()
    janela_adm.title("Acesso Concedido")
    janela_adm.geometry("400x200") # Define o tamanho da janela

    # --- Centralizando a Janela na Tela ---
    largura_janela = 400
    altura_janela = 200
    largura_tela = janela_adm.winfo_screenwidth()
    altura_tela = janela_adm.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura_janela // 2)
    pos_y = (altura_tela // 2) - (altura_janela // 2)
    janela_adm.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    # --- Criação do Widget (Rótulo com a mensagem) ---
    label_mensagem = tk.Label(
        janela_adm,
        text="Você é um administrador",
        font=("Arial", 16, "bold") # Define a fonte, tamanho e estilo
    )
    # .pack() com expand=True centraliza o widget na janela
    label_mensagem.pack(expand=True)

    # --- Iniciar o Loop Principal da Interface ---
    janela_adm.mainloop()

