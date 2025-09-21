import tkinter as tk
from tkinter import messagebox
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(0, project_root)

from src.controller.controlador_sistema import ControladorSistema

def criar_janela_login():
    global janela
    janela = tk.Tk()
    janela.title("Tela de Login do Sistema")

    largura_janela = 300
    altura_janela = 150
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura_janela // 2)
    pos_y = (altura_tela // 2) - (altura_janela // 2)

    janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    label_titulo = tk.Label(janela, text="Sistema de Gestão", font=("Arial", 14, "bold"))
    label_titulo.pack(pady=20)

    botao_login_admin = tk.Button(
        janela, 
        text="Login Admin", 
        command=fazer_login_admin, 
        width=15,
        height=2,
        font=("Arial", 12)
    )
    botao_login_admin.pack(pady=20)

    janela.mainloop()

def fazer_login_admin():
    try:
        controlador = ControladorSistema()
        admin = controlador.fazer_login_primeiro_admin()
        
        if admin:
            messagebox.showinfo("Login Bem-sucedido", f"Bem-vindo, {admin.nome}!")
            janela.destroy()
            
            abrir_tela_principal(controlador, admin)
        else:
            messagebox.showerror("Erro", "Nenhum administrador encontrado no sistema.")
            
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}")

def abrir_tela_principal(controlador, usuario):
    try:
        from src.views.tela_perfil import TelaPerfilAdministrador
        
        janela_principal = tk.Tk()
        janela_principal.title("Sistema de Gestão Financeira")
        
        largura = 1200
        altura = 800
        largura_tela = janela_principal.winfo_screenwidth()
        altura_tela = janela_principal.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        janela_principal.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        
        tela_admin = TelaPerfilAdministrador(
            janela_principal,
            controlador,
            usuario,
            on_logout=lambda: fechar_sistema(janela_principal)
        )
        
        tela_admin.mostrar()
        
        janela_principal.mainloop()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir tela principal: {str(e)}")

def fechar_sistema(janela_principal):
    janela_principal.destroy()
    criar_janela_login()
        
if __name__ == "__main__":
    criar_janela_login()