import tkinter as tk
from tkinter import ttk


class ModaisPadrao:
    @staticmethod
    def modal_formulario(titulo="Formulário", largura=600, altura=500):
        """Cria uma janela modal para formulários"""
        modal = tk.Toplevel()
        modal.title(titulo)
        modal.geometry(f"{largura}x{altura}")
        modal.resizable(False, False)
        modal.configure(bg="white")
        modal.transient()
        modal.grab_set()
        
        return modal
    
    @staticmethod
    def cabecalho_modal(parent, titulo="Título"):
        """Cria o cabeçalho de um modal"""
        tk.Label(
            parent,
            text=titulo,
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#333333"
        ).pack(pady=(30, 20))
    
    @staticmethod
    def frame_campos(parent, padx=40):
        """Cria o frame para campos do formulário"""
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="both", expand=True, padx=padx)
        return frame
    
    @staticmethod
    def frame_botoes(parent, padx=40, pady=(30, 30)):
        """Cria o frame para botões do modal"""
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", padx=padx, pady=pady)
        return frame
    
    @staticmethod
    def frame_duas_colunas(parent, pady=15):
        """Cria um frame com duas colunas"""
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", pady=(pady, 0))
        
        col1 = tk.Frame(frame, bg="white")
        col1.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        col2 = tk.Frame(frame, bg="white")
        col2.pack(side="left", fill="both", expand=True)
        
        return col1, col2
