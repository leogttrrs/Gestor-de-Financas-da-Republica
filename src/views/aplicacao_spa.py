import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Callable, Any
from .tela_cadastro_base import TelaCadastroBase


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


class TelaLogin(ComponenteBase):
    
    def __init__(self, container, controlador_sistema, on_login_success=None, on_criar_perfil=None):
        super().__init__(container, controlador_sistema)
        self.on_login_success = on_login_success
        self.on_criar_perfil = on_criar_perfil
        self.criar_interface()
    
    def criar_interface(self):
        self.criar_frame()
        
        main_container = ttk.Frame(self.frame)
        main_container.pack(expand=True, fill="both")
        
        card = ttk.Frame(main_container, relief="raised", borderwidth=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=550)
        
        icon_frame = ttk.Frame(card)
        icon_frame.pack(pady=(40, 20))
        
        icon_label = ttk.Label(icon_frame, text="🏠", font=("Arial", 48))
        icon_label.pack()
        
        title_label = ttk.Label(card, text="Bem-vindo!", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(card, text="Acesse sua conta para gerenciar sua república.", 
                                 font=("Arial", 11), foreground="gray")
        subtitle_label.pack(pady=(0, 30))
        
        fields_frame = ttk.Frame(card)
        fields_frame.pack(padx=40, fill="x")
        
        self.entry_cpf = ttk.Entry(fields_frame, font=("Arial", 12), width=30)
        self.entry_cpf.pack(pady=(0, 15), ipady=8)
        self.entry_cpf.insert(0, "Seu CPF")
        self.entry_cpf.bind("<FocusIn>", self._limpar_placeholder_cpf)
        self.entry_cpf.bind("<FocusOut>", self._restaurar_placeholder_cpf)
        self.entry_cpf.configure(foreground="gray")
        
        self.entry_senha = ttk.Entry(fields_frame, font=("Arial", 12), width=30, show="*")
        self.entry_senha.pack(pady=(0, 10), ipady=8)
        self.entry_senha.insert(0, "Sua senha")
        self.entry_senha.bind("<FocusIn>", self._limpar_placeholder_senha)
        self.entry_senha.bind("<FocusOut>", self._restaurar_placeholder_senha)
        self.entry_senha.configure(foreground="gray", show="")
        
        esqueceu_label = ttk.Label(fields_frame, text="Esqueceu sua senha?", 
                                 font=("Arial", 10), foreground="#007bff", cursor="hand2")
        esqueceu_label.pack(anchor="w", pady=(0, 15))
        esqueceu_label.bind("<Button-1>", self._esqueceu_senha)
        
        self.btn_entrar = ttk.Button(fields_frame, text="Entrar", command=self._fazer_login)
        self.btn_entrar.pack(fill="x", ipady=10)
        
        style = ttk.Style()
        style.configure("Login.TButton", font=("Arial", 12, "bold"))
        self.btn_entrar.configure(style="Login.TButton")
        
        criar_frame = ttk.Frame(card)
        criar_frame.pack(pady=(20, 30))
        
        text_frame = ttk.Frame(criar_frame)
        text_frame.pack()
        
        criar_label = ttk.Label(text_frame, text="Crie seu perfil", 
                              font=("Arial", 10), foreground="#4A90E2", cursor="hand2")
        criar_label.pack(side="left")
        criar_label.bind("<Button-1>", self._criar_perfil)
        
        desc_label = ttk.Label(text_frame, text=" para administrar sua república", 
                             font=("Arial", 10), foreground="gray")
        desc_label.pack(side="left")
        
        self.frame.bind("<Return>", lambda e: self._fazer_login())
        self.frame.focus_set()
    
    def _limpar_placeholder_cpf(self, event):
        if self.entry_cpf.get() == "Seu CPF":
            self.entry_cpf.delete(0, tk.END)
            self.entry_cpf.configure(foreground="black")
    
    def _restaurar_placeholder_cpf(self, event):
        if not self.entry_cpf.get():
            self.entry_cpf.insert(0, "Seu CPF")
            self.entry_cpf.configure(foreground="gray")
    
    def _limpar_placeholder_senha(self, event):
        if self.entry_senha.get() == "Sua senha":
            self.entry_senha.delete(0, tk.END)
            self.entry_senha.configure(foreground="black", show="*")
    
    def _restaurar_placeholder_senha(self, event):
        if not self.entry_senha.get():
            self.entry_senha.insert(0, "Sua senha")
            self.entry_senha.configure(foreground="gray", show="")
    
    def _fazer_login(self):
        cpf = self.entry_cpf.get()
        senha = self.entry_senha.get()
        
        if cpf == "Seu CPF" or not cpf:
            messagebox.showerror("Erro", "Por favor, insira seu CPF")
            return
        
        if senha == "Sua senha" or not senha:
            messagebox.showerror("Erro", "Por favor, insira sua senha")
            return
        
        if self.controlador_sistema:
            usuario = self.controlador_sistema.fazer_login(cpf, senha)
            if usuario:
                if self.on_login_success:
                    self.on_login_success(usuario)
            else:
                messagebox.showerror("Erro", "CPF ou senha incorretos")
    
    def _esqueceu_senha(self, event):
        messagebox.showinfo("Esqueceu sua senha", "Funcionalidade em desenvolvimento")
    
    def _criar_perfil(self, event):
        if self.on_criar_perfil:
            self.on_criar_perfil()


class TelaCadastroAdministrador(TelaCadastroBase):
    
    def get_titulo(self):
        return "Crie seu Perfil de Administrador"
    
    def get_subtitulo(self):
        return "Gerencie sua república com facilidade."
    
    def get_texto_botao(self):
        return "Cadastrar"
    
    def criar_interface(self):
        self.criar_frame()
        
        main_container = ttk.Frame(self.frame)
        main_container.pack(expand=True, fill="both")
        
        card = ttk.Frame(main_container, relief="solid", borderwidth=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=500, height=650)
        card.configure(style="Card.TFrame")
        
        style = ttk.Style()
        style.configure("Card.TFrame", background="white")
        
        header_frame = ttk.Frame(card, style="Card.TFrame")
        header_frame.pack(fill="x", pady=(40, 0))
        
        icon_label = ttk.Label(header_frame, text="🏠", font=("Arial", 48), background="white")
        icon_label.pack()
        
        title_label = ttk.Label(header_frame, text=self.get_titulo(), font=("Arial", 20, "bold"), 
                              background="white", foreground="#333333")
        title_label.pack(pady=(20, 5))
        
        subtitle_label = ttk.Label(header_frame, text=self.get_subtitulo(), 
                                 font=("Arial", 11), background="white", foreground="#666666")
        subtitle_label.pack(pady=(0, 20))
        
        scroll_container = ttk.Frame(card, style="Card.TFrame")
        scroll_container.pack(fill="both", expand=True, padx=50, pady=(0, 20))
        
        self.fields_canvas = tk.Canvas(scroll_container, bg="white", highlightthickness=0)
        fields_scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=self.fields_canvas.yview)
        self.fields_canvas.configure(yscrollcommand=fields_scrollbar.set)
        
        fields_scrollbar.pack(side="right", fill="y")
        self.fields_canvas.pack(side="left", fill="both", expand=True)
        
        self.fields_frame = ttk.Frame(self.fields_canvas, style="Card.TFrame")
        self.fields_canvas_window = self.fields_canvas.create_window((0, 0), window=self.fields_frame, anchor="nw")
        
        self.criar_campos(self.fields_frame)
        
        self.fields_frame.bind("<Configure>", self._on_fields_configure)
        self.fields_canvas.bind("<Configure>", self._on_fields_canvas_configure)
        self.fields_canvas.bind_all("<MouseWheel>", self._on_fields_mousewheel)
        
        buttons_frame = ttk.Frame(card, style="Card.TFrame")
        buttons_frame.pack(fill="x", side="bottom", padx=50, pady=(0, 40))
        
        self.btn_cadastrar = ttk.Button(buttons_frame, text=self.get_texto_botao(), 
                                      command=self._cadastrar, style="Primary.TButton")
        self.btn_cadastrar.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_cancelar = ttk.Button(buttons_frame, text="Cancelar", command=self._voltar)
        btn_cancelar.pack(side="right")
        
        style.configure("Primary.TButton", background="#4A90E2", foreground="white", 
                       font=("Arial", 11, "bold"))
        style.map("Primary.TButton", background=[("active", "#357ABD")])
    
    def criar_campos(self, parent):
        nome_label = ttk.Label(parent, text="Nome Completo", font=("Arial", 10), 
                             background="white", foreground="#333333")
        nome_label.pack(anchor="w", pady=(0, 5))
        
        self.campos["nome"] = ttk.Entry(parent, font=("Arial", 11), width=40)
        self.campos["nome"].pack(fill="x", pady=(0, 15), ipady=8)
        self.campos["nome"].insert(0, "Digite seu nome completo")
        self.campos["nome"].configure(foreground="gray")
        self.campos["nome"].bind("<FocusIn>", lambda e: self._limpar_placeholder(self.campos["nome"], "Digite seu nome completo"))
        self.campos["nome"].bind("<FocusOut>", lambda e: self._restaurar_placeholder(self.campos["nome"], "Digite seu nome completo"))
        
        genero_label = ttk.Label(parent, text="Gênero", font=("Arial", 10), 
                               background="white", foreground="#333333")
        genero_label.pack(anchor="w", pady=(0, 5))
        
        self.campos["genero"] = ttk.Combobox(parent, font=("Arial", 11), 
                                           values=["Masculino", "Feminino"], state="readonly", width=37)
        self.campos["genero"].pack(fill="x", pady=(0, 15), ipady=8)
        self.campos["genero"].set("")
        
        cpf_label = ttk.Label(parent, text="CPF", font=("Arial", 10), 
                            background="white", foreground="#333333")
        cpf_label.pack(anchor="w", pady=(0, 5))
        
        self.campos["cpf"] = ttk.Entry(parent, font=("Arial", 11), width=40)
        self.campos["cpf"].pack(fill="x", pady=(0, 15), ipady=8)
        self.campos["cpf"].insert(0, "000.000.000-00")
        self.campos["cpf"].configure(foreground="gray")
        self.campos["cpf"].bind("<FocusIn>", lambda e: self._limpar_placeholder(self.campos["cpf"], "000.000.000-00"))
        self.campos["cpf"].bind("<FocusOut>", lambda e: self._restaurar_placeholder(self.campos["cpf"], "000.000.000-00"))
        
        email_label = ttk.Label(parent, text="E-mail", font=("Arial", 10), 
                              background="white", foreground="#333333")
        email_label.pack(anchor="w", pady=(0, 5))
        
        self.campos["email"] = ttk.Entry(parent, font=("Arial", 11), width=40)
        self.campos["email"].pack(fill="x", pady=(0, 15), ipady=8)
        self.campos["email"].insert(0, "seuemail@exemplo.com")
        self.campos["email"].configure(foreground="gray")
        self.campos["email"].bind("<FocusIn>", lambda e: self._limpar_placeholder(self.campos["email"], "seuemail@exemplo.com"))
        self.campos["email"].bind("<FocusOut>", lambda e: self._restaurar_placeholder(self.campos["email"], "seuemail@exemplo.com"))
        
        telefone_label = ttk.Label(parent, text="Telefone", font=("Arial", 10), 
                                 background="white", foreground="#333333")
        telefone_label.pack(anchor="w", pady=(0, 5))
        
        self.campos["telefone"] = ttk.Entry(parent, font=("Arial", 11), width=40)
        self.campos["telefone"].pack(fill="x", pady=(0, 15), ipady=8)
        self.campos["telefone"].insert(0, "(00) 00000-0000")
        self.campos["telefone"].configure(foreground="gray")
        self.campos["telefone"].bind("<FocusIn>", lambda e: self._limpar_placeholder(self.campos["telefone"], "(00) 00000-0000"))
        self.campos["telefone"].bind("<FocusOut>", lambda e: self._restaurar_placeholder(self.campos["telefone"], "(00) 00000-0000"))
        
        senha_label = ttk.Label(parent, text="Senha", font=("Arial", 10), 
                              background="white", foreground="#333333")
        senha_label.pack(anchor="w", pady=(0, 5))
        
        self.campos["senha"] = ttk.Entry(parent, font=("Arial", 11), width=40, show="")
        self.campos["senha"].pack(fill="x", pady=(0, 15), ipady=8)
        self.campos["senha"].insert(0, "Crie uma senha")
        self.campos["senha"].configure(foreground="gray")
        self.campos["senha"].bind("<FocusIn>", lambda e: self._limpar_placeholder_senha(self.campos["senha"], "Crie uma senha"))
        self.campos["senha"].bind("<FocusOut>", lambda e: self._restaurar_placeholder_senha(self.campos["senha"], "Crie uma senha"))
        
        confirmar_label = ttk.Label(parent, text="Confirmar Senha", font=("Arial", 10), 
                                  background="white", foreground="#333333")
        confirmar_label.pack(anchor="w", pady=(0, 5))
        
        self.campos["confirmar_senha"] = ttk.Entry(parent, font=("Arial", 11), width=40, show="")
        self.campos["confirmar_senha"].pack(fill="x", pady=(0, 15), ipady=8)
        self.campos["confirmar_senha"].insert(0, "Confirme sua senha")
        self.campos["confirmar_senha"].configure(foreground="gray")
        self.campos["confirmar_senha"].bind("<FocusIn>", lambda e: self._limpar_placeholder_senha(self.campos["confirmar_senha"], "Confirme sua senha"))
        self.campos["confirmar_senha"].bind("<FocusOut>", lambda e: self._restaurar_placeholder_senha(self.campos["confirmar_senha"], "Confirme sua senha"))
    
    def _limpar_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(foreground="black")
    
    def _restaurar_placeholder(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(foreground="gray")
    
    def _limpar_placeholder_senha(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(foreground="black", show="*")
    
    def _restaurar_placeholder_senha(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(foreground="gray", show="")
    
    def _on_fields_configure(self, event):
        self.fields_canvas.configure(scrollregion=self.fields_canvas.bbox("all"))
    
    def _on_fields_canvas_configure(self, event):
        canvas_width = event.width
        self.fields_canvas.itemconfig(self.fields_canvas_window, width=canvas_width)
    
    def _on_fields_mousewheel(self, event):
        self.fields_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def validar_dados(self):
        nome = self.campos["nome"].get()
        cpf = self.campos["cpf"].get()
        email = self.campos["email"].get()
        telefone = self.campos["telefone"].get()
        genero = self.campos["genero"].get()
        senha = self.campos["senha"].get()
        confirmar_senha = self.campos["confirmar_senha"].get()
        
        placeholders = ["Digite seu nome completo", "000.000.000-00", "seuemail@exemplo.com", 
                       "(00) 00000-0000", "Crie uma senha", "Confirme sua senha"]
        
        if any(campo in placeholders for campo in [nome, cpf, email, telefone, senha, confirmar_senha]):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return None
        
        if not genero:
            messagebox.showerror("Erro", "Por favor, selecione o gênero")
            return None
        
        if senha != confirmar_senha:
            messagebox.showerror("Erro", "As senhas não coincidem")
            return None
        
        return {
            "nome": nome,
            "cpf": cpf,
            "email": email,
            "telefone": telefone,
            "genero": genero.lower(),
            "senha": senha
        }
    
    def executar_cadastro(self, dados):
        if self.controlador_sistema:
            return self.controlador_sistema.controlador_administrador.cadastrar_administrador(
                dados["cpf"], dados["nome"], dados["email"], 
                dados["telefone"], dados["genero"], dados["senha"]
            )
        return False, "Sistema não disponível"


class TelaCadastroMoradorBase(TelaCadastroBase):
    
    def get_titulo(self):
        return "Criar Perfil de Morador"
    
    def get_subtitulo(self):
        return "Cadastre-se como morador da república"
    
    def get_texto_botao(self):
        return "Criar Conta de Morador"
    
    def criar_campos(self, parent):
        self.campos["nome"] = self._criar_campo(parent, "Nome completo")
        self.campos["cpf"] = self._criar_campo(parent, "CPF")
        self.campos["email"] = self._criar_campo(parent, "E-mail")
        self.campos["telefone"] = self._criar_campo(parent, "Telefone")
        
        self.campos["genero"] = ttk.Combobox(parent, font=("Arial", 12), 
                                           values=["Masculino", "Feminino"], state="readonly")
        self.campos["genero"].pack(pady=(0, 15), ipady=8, fill="x")
        self.campos["genero"].set("Selecione o gênero")
        
        self.campos["quarto"] = self._criar_campo(parent, "Número do Quarto")
        self.campos["senha"] = self._criar_campo(parent, "Senha", show="*")
        self.campos["confirmar_senha"] = self._criar_campo(parent, "Confirmar senha", show="*")
    
    def validar_dados(self):
        nome = self.campos["nome"].get()
        cpf = self.campos["cpf"].get()
        email = self.campos["email"].get()
        telefone = self.campos["telefone"].get()
        genero = self.campos["genero"].get()
        quarto = self.campos["quarto"].get()
        senha = self.campos["senha"].get()
        confirmar_senha = self.campos["confirmar_senha"].get()
        
        placeholders = ["Nome completo", "CPF", "E-mail", "Telefone", "Número do Quarto", "Senha", "Confirmar senha"]
        
        if any(campo in placeholders for campo in [nome, cpf, email, telefone, quarto, senha, confirmar_senha]):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return None
        
        if genero == "Selecione o gênero":
            messagebox.showerror("Erro", "Por favor, selecione o gênero")
            return None
        
        if senha != confirmar_senha:
            messagebox.showerror("Erro", "As senhas não coincidem")
            return None
        
        try:
            quarto_num = int(quarto)
        except ValueError:
            messagebox.showerror("Erro", "Número do quarto deve ser um número válido")
            return None
        
        return {
            "nome": nome,
            "cpf": cpf,
            "email": email,
            "telefone": telefone,
            "genero": genero.lower(),
            "numero_quarto": quarto_num,
            "senha": senha
        }
    
    def executar_cadastro(self, dados):
        return False, "Cadastro de morador em desenvolvimento"
    
    def __init__(self, container, controlador_sistema, on_voltar=None, on_cadastro_success=None):
        super().__init__(container, controlador_sistema)
        self.on_voltar = on_voltar
        self.on_cadastro_success = on_cadastro_success
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
        
        title_label = ttk.Label(card, text="Criar Perfil", font=("Arial", 24, "bold"))
        title_label.pack(pady=(20, 10))
        
        subtitle_label = ttk.Label(card, text="Cadastre-se como administrador", 
                                 font=("Arial", 11), foreground="gray")
        subtitle_label.pack(pady=(0, 30))
        
        fields_frame = ttk.Frame(card)
        fields_frame.pack(padx=40, fill="x")
        
        self.entry_nome = self._criar_campo(fields_frame, "Nome completo")
        self.entry_cpf = self._criar_campo(fields_frame, "CPF")
        self.entry_email = self._criar_campo(fields_frame, "Email")
        self.entry_telefone = self._criar_campo(fields_frame, "Telefone")
        
        self.combo_genero = ttk.Combobox(fields_frame, font=("Arial", 12), 
                                       values=["Masculino", "Feminino"], state="readonly")
        self.combo_genero.pack(pady=(0, 15), ipady=8, fill="x")
        self.combo_genero.set("Selecione o gênero")
        
        self.entry_senha = self._criar_campo(fields_frame, "Senha", show="*")
        self.entry_confirmar_senha = self._criar_campo(fields_frame, "Confirmar senha", show="*")
        
        self.btn_cadastrar = ttk.Button(fields_frame, text="Criar Conta", command=self._cadastrar)
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
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        email = self.entry_email.get()
        telefone = self.entry_telefone.get()
        genero = self.combo_genero.get()
        senha = self.entry_senha.get()
        confirmar_senha = self.entry_confirmar_senha.get()
        
        if any(campo in ["Nome completo", "CPF", "Email", "Telefone", "Senha", "Confirmar senha"] 
               for campo in [nome, cpf, email, telefone, senha, confirmar_senha]):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return
        
        if genero == "Selecione o gênero":
            messagebox.showerror("Erro", "Por favor, selecione o gênero")
            return
        
        if senha != confirmar_senha:
            messagebox.showerror("Erro", "As senhas não coincidem")
            return
        
        if self.controlador_sistema:
            sucesso, mensagem = self.controlador_sistema.controlador_administrador.cadastrar_administrador(
                cpf, nome, email, telefone, genero.lower(), senha
            )
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Administrador cadastrado com sucesso!")
                if self.on_cadastro_success:
                    self.on_cadastro_success()
            else:
                messagebox.showerror("Erro", mensagem)


class AplicacaoSPA:
    
    def __init__(self, controlador_sistema):
        self.controlador_sistema = controlador_sistema
        self.root = tk.Tk()
        self.componentes: Dict[str, ComponenteBase] = {}
        self.componente_atual = None
        
        self.configurar_janela()
        self.inicializar_componentes()
        self.mostrar_componente("login")
    
    def configurar_janela(self):
        self.root.title("Sistema de Gestão de República")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg="#f5f5f5")
        
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1000x700+{x}+{y}")
        
        self.container_principal = ttk.Frame(self.root)
        self.container_principal.pack(fill="both", expand=True)
        
        self._configurar_scroll()
    
    def _configurar_scroll(self):
        pass

    def _on_frame_configure(self, event):
        try:
            if hasattr(self, 'canvas'):
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        except:
            pass
    
    def _on_canvas_configure(self, event):
        try:
            if hasattr(self, 'canvas') and hasattr(self, 'canvas_window'):
                canvas_width = event.width
                self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        except:
            pass
    
    def _on_mousewheel(self, event):
        try:
            if hasattr(self, 'canvas'):
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except:
            pass
    
    def inicializar_componentes(self):
        self.componentes["login"] = TelaLogin(
            self.container_principal, 
            self.controlador_sistema,
            on_login_success=self._on_login_success,
            on_criar_perfil=lambda: self.mostrar_componente("cadastro_admin")
        )
        
        self.componentes["cadastro_admin"] = TelaCadastroAdministrador(
            self.container_principal,
            self.controlador_sistema,
            on_voltar=lambda: self.mostrar_componente("login"),
            on_cadastro_success=self._on_cadastro_admin_success
        )
    
    def _criar_tela_administrador(self, usuario):
        from .tela_perfil import TelaPerfilAdministrador
        
        tela_admin = TelaPerfilAdministrador(
            self.container_principal,
            self.controlador_sistema,
            usuario,
            on_logout=lambda: self.mostrar_componente("login")
        )
        self.componentes["perfil_admin"] = tela_admin
        return tela_admin
    
    def mostrar_componente(self, nome_componente):
        if self.componente_atual:
            self.componente_atual.esconder()
        
        if nome_componente in self.componentes:
            self.componente_atual = self.componentes[nome_componente]
            self.componente_atual.mostrar()
    
    def _on_login_success(self, usuario):
        tela_admin = self._criar_tela_administrador(usuario)
        self.mostrar_componente("perfil_admin")
    
    def _on_cadastro_admin_success(self):
        messagebox.showinfo("Sucesso", "Administrador cadastrado com sucesso! Faça login para continuar.")
        self.mostrar_componente("login")
    
    def executar(self):
        self.root.mainloop()


def iniciar_aplicacao_spa(controlador_sistema):
    app = AplicacaoSPA(controlador_sistema)
    app.executar()


if __name__ == "__main__":
    from src.controller.controlador_sistema import ControladorSistema
    controlador = ControladorSistema()
    iniciar_aplicacao_spa(controlador)