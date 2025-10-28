import tkinter as tk
from tkinter import ttk


class BotoesPadrao:
    @staticmethod
    def botao_cinza(parent, texto="Botão", comando=None, side=None, padx=0, pady=10):
        btn = tk.Button(
            parent,
            text=texto,
            command=comando,
            bg="#B0B0B0",
            fg="#222222",
            font=("Arial", 11, "bold"),
            relief="flat",
            borderwidth=0,
            activebackground="#888888",
            activeforeground="#222222",
            cursor="hand2",
            padx=20,
            pady=10
        )
        if side:
            btn.pack(side=side, padx=padx, pady=pady)
        else:
            btn.pack(padx=padx, pady=pady)
        return btn
    @staticmethod
    def botao_azul(parent, texto="Botão", comando=None, side=None, padx=0, pady=10):
        btn = tk.Button(
            parent,
            text=texto,
            command=comando,
            bg="#4A90E2",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            borderwidth=0,
            activebackground="#357ABD",
            activeforeground="white",
            cursor="hand2",
            padx=20,
            pady=10
        )
        if side:
            btn.pack(side=side, padx=padx, pady=pady)
        else:
            btn.pack(padx=padx, pady=pady)
        return btn
    
    @staticmethod
    def botao_vermelho(parent, texto="Botão", comando=None, side=None, padx=0, pady=10):
        btn = tk.Button(
            parent,
            text=texto,
            command=comando,
            bg="#E74C3C",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            borderwidth=0,
            activebackground="#C0392B",
            activeforeground="white",
            cursor="hand2",
            padx=20,
            pady=10
        )
        if side:
            btn.pack(side=side, padx=padx, pady=pady)
        else:
            btn.pack(padx=padx, pady=pady)
        return btn

    @staticmethod
    def botao_verde(parent, texto="Botão", comando=None, side=None, padx=0, pady=10):
        btn = tk.Button(
            parent,
            text=texto,
            command=comando,
            bg="#2ECC71",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            borderwidth=0,
            activebackground="#27AE60",
            activeforeground="white",
            cursor="hand2",
            padx=20,
            pady=10
        )
        if side:
            btn.pack(side=side, padx=padx, pady=pady)
        else:
            btn.pack(padx=padx, pady=pady)
        return btn
    @staticmethod
    def botao_secundario(parent, texto="Botão", comando=None, largura=None, altura=8):
        style = ttk.Style()
        style.configure(
            "BotaoSecundario.TButton",
            background="white",
            foreground="#333333",
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        btn = ttk.Button(
            parent, text=texto, command=comando, style="BotaoSecundario.TButton"
        )
        if largura:
            btn.pack(ipady=altura, padx=(10, 10))
        else:
            btn.pack(fill="x", ipady=altura)
        return btn
