import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Callable
from src.models.Morador import Morador


class MenuLateral:
    def __init__(self, parent, titulo_republica="República", tipo_usuario="Administrador"):
        self.parent = parent
        self.titulo_republica = titulo_republica
        self.tipo_usuario = tipo_usuario
        self.frame = None
        self.opcoes_menu = []
        self.callback_sair = None
        self.criar_menu()
    
    def criar_menu(self):
        self.frame = ttk.Frame(self.parent, width=200, style="MenuBackground.TFrame")
        self.frame.pack(side="left", fill="y")
        self.frame.pack_propagate(False)
        
        header_frame = ttk.Frame(self.frame, style="MenuHeader.TFrame")
        header_frame.pack(fill="x", pady=(0, 1))
        
        style = ttk.Style()
        style.configure("MenuBackground.TFrame", background="#f0f0f0")
        style.configure("MenuHeader.TFrame", background="#4A90E2")
        style.configure("MenuTitle.TLabel", background="#4A90E2", foreground="white", font=("Arial", 12, "bold"))
        style.configure("MenuSubtitle.TLabel", background="#4A90E2", foreground="white", font=("Arial", 9))
        
        title_label = ttk.Label(header_frame, text=self.titulo_republica, style="MenuTitle.TLabel")
        title_label.pack(pady=(15, 5))
        
        subtitle_label = ttk.Label(header_frame, text=self.tipo_usuario, style="MenuSubtitle.TLabel")
        subtitle_label.pack(pady=(0, 15))
        
        self.menu_container = ttk.Frame(self.frame, style="MenuBackground.TFrame")
        self.menu_container.pack(fill="both", expand=True, padx=0, pady=0)
    
    def definir_opcoes_menu(self, opcoes: List[Tuple[str, Callable]]):
        self.opcoes_menu = opcoes
        self._criar_botoes_menu()
    
    def _criar_botoes_menu(self):
        for widget in self.menu_container.winfo_children():
            widget.destroy()
        
        style = ttk.Style()
        style.configure("MenuButton.TButton", 
                       background="#f0f0f0", 
                       relief="flat",
                       borderwidth=0)
        style.map("MenuButton.TButton",
                 background=[("active", "#e0e0e0")])
        
        for texto, callback in self.opcoes_menu:
            btn = ttk.Button(self.menu_container, text=texto, command=callback, style="MenuButton.TButton")
            btn.pack(fill="x", padx=10, pady=2)
    
    def definir_callback_sair(self, callback: Callable):
        self.callback_sair = callback
    
    def _sair(self):
        if self.callback_sair:
            self.callback_sair()
    
    def destacar_opcao(self, indice: int):
        botoes = [widget for widget in self.menu_container.winfo_children() if isinstance(widget, ttk.Button)]
        
        for btn in botoes:
            btn.configure(style="TButton")
        
        if 0 <= indice < len(botoes):
            style = ttk.Style()
            style.configure("Selected.TButton", background="#E3F2FD")
            botoes[indice].configure(style="Selected.TButton")
    
    def esconder(self):
        if self.frame:
            self.frame.pack_forget()
    
    def mostrar(self):
        if self.frame:
            self.frame.pack(side="left", fill="y")


class MenuAdministrador(MenuLateral):
    def __init__(self, parent, usuario_logado=None, callback_navegacao=None):
        self.usuario_logado = usuario_logado
        self.callback_navegacao = callback_navegacao
        super().__init__(parent, "República", "Administrador")
        self._definir_opcoes_admin()
    
    def _definir_opcoes_admin(self):
        opcoes = [
            ("👁 Visão Geral", lambda: self._navegar("dashboard")),
            ("👥 Moradores", lambda: self._navegar("moradores")),
            ("🏠Republica", lambda: self._navegar("republica")),
            ("🛏 Quartos", lambda: self._navegar("quartos")),
            ("📋 Contratos", lambda: self._navegar("contratos")),
            ("💰 Dívidas", lambda: self._navegar("dividas")),
            ("⚠️ Ocorrências", lambda: self._navegar("ocorrencias")),
            ("🔔 Alertas", lambda: self._navegar("alertas")),
            ("🧑 Meu Perfil", lambda: self._navegar("perfil_admin")),
            ("🚪 Sair", lambda: self._sair())
        ]
        self.definir_opcoes_menu(opcoes)
    
    def _navegar(self, secao):
        if self.callback_navegacao:
            self.callback_navegacao(secao)


class MenuMorador(MenuLateral):
    def __init__(self, parent, usuario_logado=None, callback_navegacao=None):
        self.usuario_logado = usuario_logado
        self.callback_navegacao = callback_navegacao
        super().__init__(parent, "República", "Morador")
        self._definir_opcoes_morador()

    def _definir_opcoes_morador(self):
        tem_contrato_ativo = Morador.tem_contrato_ativo(self.usuario_logado.id) if self.usuario_logado else False

        if tem_contrato_ativo:
            opcoes = [
                ("🏠 Visão Geral", lambda: self._navegar("dashboard")),
                ("👥 Moradores", lambda: self._navegar("moradores")),
                ("🛏 Quartos", lambda: self._navegar("quartos")),
                ("💰 Dívidas", lambda: self._navegar("dividas")),
                ("⚠️ Ocorrências", lambda: self._navegar("ocorrencias")),
                ("🔔 Alertas", lambda: self._navegar("alertas")),
                ("🧑 Meu Perfil", lambda: self._navegar("perfil_morador")),
                ("🚪 Sair", lambda: self._sair())
            ]
        else:
            opcoes = [
                ("💰 Dívidas", lambda: self._navegar("dividas")),
                ("🧑 Meu Perfil", lambda: self._navegar("perfil_morador")),
                ("🚪 Sair", lambda: self._sair())
            ]
            self._atualizar_subtitulo_acesso_limitado()

        self.definir_opcoes_menu(opcoes)

    def _atualizar_subtitulo_acesso_limitado(self):
        for widget in self.frame.winfo_children():
            if isinstance(widget, ttk.Frame) and hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label) and "Morador" in child.cget("text"):
                        child.configure(text="Morador", foreground="white")
                        break

    def _navegar(self, secao):
        if self.callback_navegacao:
            self.callback_navegacao(secao)