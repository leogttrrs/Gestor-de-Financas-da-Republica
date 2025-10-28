import tkinter as tk
from tkinter import ttk


class InputsPadrao:
    @staticmethod
    def campo_texto(parent, label="Campo:", placeholder="", pady_label=5, pady_entry=8):
        """Cria um campo de texto com label"""
        tk.Label(
            parent, 
            text=label, 
            font=("Arial", 10), 
            bg="white", 
            fg="#333333"
        ).pack(anchor="w", pady=(15, pady_label))
        
        entry = ttk.Entry(parent, font=("Arial", 10))
        entry.pack(fill="x", ipady=pady_entry)
        
        if placeholder:
            entry.insert(0, placeholder)
        
        return entry
    
    @staticmethod
    def combobox(parent, label="Selecione:", valores=None, pady_label=5, pady_combo=8):
        """Cria um combobox com label"""
        tk.Label(
            parent, 
            text=label, 
            font=("Arial", 10), 
            bg="white", 
            fg="#333333"
        ).pack(anchor="w", pady=(15, pady_label))
        
        combo = ttk.Combobox(parent, font=("Arial", 10), state="readonly")
        combo.pack(fill="x", ipady=pady_combo)
        
        if valores:
            combo['values'] = valores
        
        return combo
    
    @staticmethod
    def input_padrao(parent, placeholder="", largura=30, altura=6, tipo_senha=False):
        """Input simples com placeholder (mantido para compatibilidade)"""
        entry = ttk.Entry(parent, font=("Arial", 10), width=largura)
        entry.pack(pady=(0, 15), ipady=altura, fill="x")

        if placeholder:
            entry.insert(0, placeholder)
            entry.configure(foreground="gray")

            def limpar_placeholder(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.configure(foreground="black")
                    if tipo_senha:
                        entry.configure(show="*")

            def restaurar_placeholder(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.configure(foreground="gray")
                    if tipo_senha:
                        entry.configure(show="")

            entry.bind("<FocusIn>", limpar_placeholder)
            entry.bind("<FocusOut>", restaurar_placeholder)

        if tipo_senha:
            entry.configure(show="*")

        return entry
