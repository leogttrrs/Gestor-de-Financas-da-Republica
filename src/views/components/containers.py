import tkinter as tk
from tkinter import ttk


class ContainersPadrao:
    @staticmethod
    def cartao_branco(parent_or_largura=None, largura=None, altura=None, padx=0, pady=0):
        parent = None
        first = parent_or_largura
        if first is not None and hasattr(first, 'winfo_exists'):
            parent = first
            w = largura
            h = altura
        else:
            parent = tk._default_root
            w = parent_or_largura if parent_or_largura is not None else largura
            h = altura

        if parent is None:
            parent = tk.Tk()

        card = tk.Frame(parent, bg="white", bd=0)

        try:
            card.configure(highlightbackground="#cfcfcf", highlightthickness=1)
        except Exception:
            card.configure(bd=1, relief="solid")

        if w or h:
            width_val = int(w) if w else None
            height_val = int(h) if h else None
            
            if width_val:
                card.configure(width=width_val)
            if height_val:
                card.configure(height=height_val)
            
            card.pack(pady=40, anchor="center")
            card.pack_propagate(False)
        else:
            card.pack(fill="both", expand=False, padx=padx, pady=pady)

        return card

    @staticmethod
    def fundo_cinza(parent, padding=0):
        frame = ttk.Frame(parent, style="FundoCinza.TFrame")
        frame.pack(fill="both", expand=True, padx=padding, pady=padding)
        return frame

    @staticmethod
    def container_campos(parent, padding_x=30):
        fields_frame = ttk.Frame(parent, style="ContainerCampos.TFrame")
        fields_frame.pack(padx=padding_x, fill="x")
        return fields_frame
