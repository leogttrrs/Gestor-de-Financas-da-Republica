import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod


class ComponenteBase:
    
    def __init__(self, container, controlador_sistema=None):
        self.container = container
        self.controlador_sistema = controlador_sistema
        self.frame = None
    
    def criar_frame(self):
        if self.frame:
            self.frame.destroy()
        self.frame = ttk.Frame(self.container)
        return self.frame
    
    def mostrar(self):
        if self.frame:
            self.frame.pack(fill="both", expand=True)
    
    def esconder(self):
        if self.frame:
            self.frame.pack_forget()
    
    def destruir(self):
        if self.frame:
            self.frame.destroy()
            self.frame = None


class TelaCadastroBase(ComponenteBase, ABC):
    
    def __init__(self, container, controlador_sistema, on_voltar=None, on_cadastro_success=None):
        super().__init__(container, controlador_sistema)
        self.on_voltar = on_voltar
        self.on_cadastro_success = on_cadastro_success
        self.campos = {}
        self.criar_interface()
    
    def criar_interface(self):
        self.criar_frame()
        
        main_container = ttk.Frame(self.frame)
        main_container.pack(expand=True, fill="both")
        
        card = ttk.Frame(main_container, relief="raised", borderwidth=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=450, height=600)
        
        header_frame = ttk.Frame(card)
        header_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        voltar_btn = ttk.Label(header_frame, text="← Voltar", font=("Arial", 10), 
                             foreground="#007bff", cursor="hand2")
        voltar_btn.pack(anchor="w")
        voltar_btn.bind("<Button-1>", lambda e: self._voltar())
        
        title_label = ttk.Label(card, text=self.get_titulo(), font=("Arial", 24, "bold"))
        title_label.pack(pady=(20, 10))
        
        subtitle_label = ttk.Label(card, text=self.get_subtitulo(), 
                                 font=("Arial", 11), foreground="gray")
        subtitle_label.pack(pady=(0, 30))
        
        fields_frame = ttk.Frame(card)
        fields_frame.pack(padx=40, fill="x")
        
        self.criar_campos(fields_frame)
        
        self.btn_cadastrar = ttk.Button(fields_frame, text=self.get_texto_botao(), command=self._cadastrar)
        self.btn_cadastrar.pack(fill="x", ipady=10, pady=(20, 0))
        
        style = ttk.Style()
        style.configure("Cadastro.TButton", font=("Arial", 12, "bold"))
        self.btn_cadastrar.configure(style="Cadastro.TButton")
        
        login_frame = ttk.Frame(card)
        login_frame.pack(pady=(20, 30))
        
        login_label = ttk.Label(login_frame, text="Já tem uma conta? Fazer login", 
                              font=("Arial", 10), foreground="#007bff", cursor="hand2")
        login_label.pack()
        login_label.bind("<Button-1>", lambda e: self._voltar())
    
    @abstractmethod
    def get_titulo(self):
        pass
    
    @abstractmethod
    def get_subtitulo(self):
        pass
    
    @abstractmethod
    def get_texto_botao(self):
        pass
    
    @abstractmethod
    def criar_campos(self, parent):
        pass
    
    @abstractmethod
    def validar_dados(self):
        pass
    
    @abstractmethod
    def executar_cadastro(self, dados):
        pass
    
    def _criar_campo(self, parent, placeholder, show=None):
        entry = ttk.Entry(parent, font=("Arial", 12), width=30)
        if show:
            entry.configure(show=show)
        entry.pack(pady=(0, 15), ipady=8, fill="x")
        entry.insert(0, placeholder)
        entry.configure(foreground="gray")
        
        entry.bind("<FocusIn>", lambda e: self._limpar_placeholder(entry, placeholder, show))
        entry.bind("<FocusOut>", lambda e: self._restaurar_placeholder(entry, placeholder, show))
        
        return entry
    
    def _criar_combobox(self, parent, placeholder, values):
        combo = ttk.Combobox(parent, font=("Arial", 12), values=values, state="readonly")
        combo.pack(pady=(0, 15), ipady=8, fill="x")
        combo.set(placeholder)
        return combo
    
    def _limpar_placeholder(self, entry, placeholder, show=None):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(foreground="black")
            if show:
                entry.configure(show=show)
    
    def _restaurar_placeholder(self, entry, placeholder, show=None):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(foreground="gray")
            if show:
                entry.configure(show="")
    
    def _voltar(self):
        if self.on_voltar:
            self.on_voltar()
    
    def _cadastrar(self):
        dados = self.validar_dados()
        if dados:
            sucesso, mensagem = self.executar_cadastro(dados)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                if self.on_cadastro_success:
                    self.on_cadastro_success()
            else:
                messagebox.showerror("Erro", mensagem)
    
    def _validar_campo_vazio(self, valor, placeholder):
        return valor and valor != placeholder
    
    def _validar_campos_obrigatorios(self, campos_placeholders):
        for campo, placeholder in campos_placeholders.items():
            if not self._validar_campo_vazio(campo, placeholder):
                return False
        return True
    
    def _validar_senhas_coincidem(self, senha, confirmar_senha, placeholder_senha, placeholder_confirmar):
        if not self._validar_campo_vazio(senha, placeholder_senha):
            return False, "Por favor, insira a senha"
        
        if not self._validar_campo_vazio(confirmar_senha, placeholder_confirmar):
            return False, "Por favor, confirme a senha"
        
        if senha != confirmar_senha:
            return False, "As senhas não coincidem"
        
        return True, ""
    
    def _validar_numero(self, valor, nome_campo):
        try:
            return int(valor), ""
        except ValueError:
            return None, f"{nome_campo} deve ser um número válido"