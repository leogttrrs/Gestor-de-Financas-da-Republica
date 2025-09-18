import tkinter as tk
from tkinter import messagebox
import tela_administrador
import tela_morador


# Função que será chamada quando o botão de login for pressionado
def fazer_login():
    """
    Verifica as credenciais inseridas pelo usuário.
    """
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    # Credenciais pré-definidas para validação
    # Em uma aplicação real, isso seria verificado contra um banco de dados
    if usuario == "admin" and senha == "admin":
        messagebox.showinfo("Login Bem-sucedido", f"Bem-vindo, {usuario}!")
        janela.destroy()
        tela_administrador.criar_janela_adm()
        
    elif usuario == "morador" and senha == "morador":
        messagebox.showinfo("Login Bem-sucedido", f"Bem-vindo, {usuario}!")
        janela.destroy()
        tela_morador.criar_janela_morador()
        
    else:
        messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")

# --- Configuração da Janela Principal ---
janela = tk.Tk()
janela.title("Tela de Login do Sistema")
janela.geometry("300x150") # Define o tamanho da janela (largura x altura)
janela.resizable(False, False) # Impede que a janela seja redimensionada

# --- Centralizando a Janela na Tela ---
largura_janela = 300
altura_janela = 150
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
pos_x = (largura_tela // 2) - (largura_janela // 2)
pos_y = (altura_tela // 2) - (altura_janela // 2)
janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")


# --- Criação dos Widgets (componentes da interface) ---

# Frame para organizar os widgets
frame_login = tk.Frame(janela)
frame_login.pack(pady=10) # Adiciona um espaçamento vertical

# Rótulo e campo de entrada para o usuário
label_usuario = tk.Label(frame_login, text="Usuário:")
label_usuario.grid(row=0, column=0, padx=5, pady=5, sticky="w") # Alinha à esquerda (west)

entry_usuario = tk.Entry(frame_login)
entry_usuario.grid(row=0, column=1, padx=5, pady=5)

# Rótulo e campo de entrada para a senha
label_senha = tk.Label(frame_login, text="Senha:")
label_senha.grid(row=1, column=0, padx=5, pady=5, sticky="w") # Alinha à esquerda

entry_senha = tk.Entry(frame_login, show="*") # O caractere '*' mascara a senha
entry_senha.grid(row=1, column=1, padx=5, pady=5)

# Botão de Login
botao_login = tk.Button(janela, text="Login", command=fazer_login, width=10)
botao_login.pack(pady=10)


# --- Iniciar o Loop Principal da Interface ---
# Mantém a janela aberta e aguardando interações do usuário
janela.mainloop()