import tkinter as tk
from tkinter import ttk
from typing import List, Tuple


class TabelasPadrao:
    @staticmethod
    def criar_tabela(parent, colunas: List[str], larguras: List[int], altura=15):
        """
        Cria uma tabela (Treeview) estilizada
        
        Args:
            parent: Widget pai
            colunas: Lista com nomes das colunas
            larguras: Lista com larguras das colunas
            altura: Altura da tabela em linhas
            
        Returns:
            tuple: (tree, scrollbar)
        """
        # Frame da tabela
        table_frame = tk.Frame(parent, bg="white")
        table_frame.pack(fill="both", expand=True, padx=40, pady=(0, 30))
        
        # Configurar estilo
        style = ttk.Style()
        style.configure("Padrao.Treeview",
                       background="white",
                       foreground="#333333",
                       fieldbackground="white",
                       font=("Arial", 10))
        style.configure("Padrao.Treeview.Heading",
                       background="#F5F5F5",
                       foreground="#666666",
                       font=("Arial", 10, "bold"))
        style.map("Padrao.Treeview",
                 background=[("selected", "#E3F2FD")])
        
        # Criar Treeview
        tree = ttk.Treeview(
            table_frame,
            columns=colunas,
            show="headings",
            style="Padrao.Treeview",
            height=altura
        )
        
        # Configurar cabeçalhos e larguras
        for i, col in enumerate(colunas):
            tree.heading(col, text=col)
            anchor = "w" if i < len(colunas) - 1 else "center"
            tree.column(col, width=larguras[i], anchor=anchor)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Empacotar
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return tree, scrollbar
    
    @staticmethod
    def configurar_tags_status(tree):
        """Configura tags de cores para status de contratos"""
        tree.tag_configure("ativo", foreground="#2ECC71")
        tree.tag_configure("finalizado", foreground="#95A5A6")
