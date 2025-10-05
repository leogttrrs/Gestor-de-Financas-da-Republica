import tkinter as tk
from tkinter import ttk, messagebox
from .aplicacao_spa import ComponenteBase
from .tela_cadastro_base import TelaCadastroBase


class TelaMorador(ComponenteBase):
    def __init__(self, container, controlador_sistema, usuario_logado, on_logout=None):
        super().__init__(container, controlador_sistema)
        self.usuario_logado = usuario_logado
        self.on_logout = on_logout
        self.criar_interface()

    def criar_interface(self):
        self.criar_frame()
        
        header_frame = ttk.Frame(self.frame, relief="solid", borderwidth=1)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        title_label = ttk.Label(header_frame, text="Painel do Morador", 
                              font=("Arial", 16, "bold"))
        title_label.pack(side="left", padx=20, pady=15)
        
        user_frame = ttk.Frame(header_frame)
        user_frame.pack(side="right", padx=20, pady=15)
        
        # if usuario_logado == morador ...
        user_label = ttk.Label(user_frame, text=f"Bem-vindo, {self.usuario_logado.nome}", 
                             font=("Arial", 10))
        user_label.pack(side="left", padx=(0, 10))
        
        logout_btn = ttk.Button(user_frame, text="Sair", command=self._logout)
        logout_btn.pack(side="right")
        
        main_container = ttk.Frame(self.frame)
        main_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        left_panel = ttk.Frame(main_container, relief="solid", borderwidth=1)
        left_panel.pack(side="left", fill="y", padx=(0, 5))
        
        menu_label = ttk.Label(left_panel, text="Menu", font=("Arial", 12, "bold"))
        menu_label.pack(pady=(10, 5))
        
        self.criar_menu_opcoes(left_panel)
        
        self.content_frame = ttk.Frame(main_container, relief="solid", borderwidth=1)
        self.content_frame.pack(side="right", expand=True, fill="both", padx=(5, 0))
        
    def criar_card_info(self, parent, titulo, valor, lado):
        card = ttk.Frame(parent, relief="raised", borderwidth=2)
        card.pack(side=lado, padx=10, pady=5, fill="x", expand=True)
        
        title_label = ttk.Label(card, text=titulo, font=("Arial", 10, "bold"))
        title_label.pack(pady=(10, 5))
        
        value_label = ttk.Label(card, text=valor, font=("Arial", 12))
        value_label.pack(pady=(0, 10))

    # Os seguintes métodos já se encontram em tela_administrador.py -> refatorar para evitar duplicação
    def gerenciar_moradores(self):
        self.limpar_content_frame()
        
        title = ttk.Label(self.content_frame, text="Gerenciar Moradores", font=("Arial", 14, "bold"))
        title.pack(pady=20)
        
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        btn_adicionar = ttk.Button(btn_frame, text="Adicionar Morador", 
                                 command=self.adicionar_morador)
        btn_adicionar.pack(side="left", padx=5)
        
        btn_listar = ttk.Button(btn_frame, text="Listar Moradores", 
                              command=self.listar_moradores)
        btn_listar.pack(side="left", padx=5)
        
        self.moradores_frame = ttk.Frame(self.content_frame)
        self.moradores_frame.pack(expand=True, fill="both", padx=20, pady=20)

    def mostrar_configuracoes(self):
        self.limpar_content_frame()
        
        title = ttk.Label(self.content_frame, text="Configurações", font=("Arial", 14, "bold"))
        title.pack(pady=20)
        
        config_frame = ttk.Frame(self.content_frame)
        config_frame.pack(padx=20, pady=20, fill="x")
        
        ttk.Label(config_frame, text="Configurações do sistema:", font=("Arial", 12)).pack(anchor="w", pady=5)
        
        btn_backup = ttk.Button(config_frame, text="Fazer Backup", command=self.fazer_backup)
        btn_backup.pack(anchor="w", pady=5)
        
        btn_relatorio = ttk.Button(config_frame, text="Gerar Relatório", command=self.gerar_relatorio)
        btn_relatorio.pack(anchor="w", pady=5)
    
    def adicionar_morador(self):
        messagebox.showinfo("Em Desenvolvimento", "Cadastro de morador em desenvolvimento")
    
    def listar_moradores(self):
        for widget in self.moradores_frame.winfo_children():
            widget.destroy()
        
        lista_label = ttk.Label(self.moradores_frame, text="Lista de Moradores:", 
                              font=("Arial", 12, "bold"))
        lista_label.pack(anchor="w", pady=(0, 10))
        
        tree = ttk.Treeview(self.moradores_frame, columns=("CPF", "Email", "Telefone"), show="tree headings")
        tree.heading("#0", text="Nome")
        tree.heading("CPF", text="CPF")
        tree.heading("Email", text="Email")
        tree.heading("Telefone", text="Telefone")
        
        tree.column("#0", width=150)
        tree.column("CPF", width=120)
        tree.column("Email", width=180)
        tree.column("Telefone", width=120)
        
        tree.insert("", "end", text="João Silva", values=("123.456.789-00", "joao@email.com", "(11) 99999-9999"))
        tree.insert("", "end", text="Maria Santos", values=("987.654.321-00", "maria@email.com", "(11) 88888-8888"))
        
        tree.pack(expand=True, fill="both")
        
        scrollbar = ttk.Scrollbar(self.moradores_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
    
    def fazer_backup(self):
        messagebox.showinfo("Backup", "Backup realizado com sucesso!")
    
    def gerar_relatorio(self):
        messagebox.showinfo("Relatório", "Relatório gerado com sucesso!")
    
    def _logout(self):
        if self.on_logout:
            self.on_logout()
    
class TelaCadastroMorador(TelaCadastroBase):
    
    def get_titulo(self):
        return "Cadastrar Novo Morador"
    
    def get_subtitulo(self):
        return "Adicione um novo morador à república"
    
    def get_texto_botao(self):
        return "Cadastrar Morador"
    
    def criar_campos(self, parent):
        self.campos["nome"] = self._criar_campo(parent, "Nome completo")
        self.campos["cpf"] = self._criar_campo(parent, "CPF")
        self.campos["email"] = self._criar_campo(parent, "E-mail")
        self.campos["telefone"] = self._criar_campo(parent, "Telefone")
        
        self.campos["genero"] = ttk.Combobox(parent, font=("Arial", 12), 
                                           values=["Masculino", "Feminino"], state="readonly")
        self.campos["genero"].pack(pady=(0, 15), ipady=8, fill="x")
        self.campos["genero"].set("Selecione o gênero")
        
        self.campos["numero_quarto"] = self._criar_campo(parent, "Número do Quarto")
        self.campos["senha"] = self._criar_campo(parent, "Senha", show="*")
        self.campos["confirmar_senha"] = self._criar_campo(parent, "Confirmar senha", show="*")
    
    def validar_dados(self):
        nome = self.campos["nome"].get()
        cpf = self.campos["cpf"].get()
        email = self.campos["email"].get()
        telefone = self.campos["telefone"].get()
        genero = self.campos["genero"].get()
        numero_quarto = self.campos["numero_quarto"].get()
        senha = self.campos["senha"].get()
        confirmar_senha = self.campos["confirmar_senha"].get()
        
        placeholders = ["Nome completo", "CPF", "E-mail", "Telefone", "Número do Quarto", "Senha", "Confirmar senha"]
        
        if any(campo in placeholders for campo in [nome, cpf, email, telefone, numero_quarto, senha, confirmar_senha]):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return None
        
        if genero == "Selecione o gênero":
            messagebox.showerror("Erro", "Por favor, selecione o gênero")
            return None
        
        if senha != confirmar_senha:
            messagebox.showerror("Erro", "As senhas não coincidem")
            return None
        
        try:
            quarto_num = int(numero_quarto)
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
        return False, "Cadastro de morador ainda não implementado no backend"

    # Fim dos métodos duplicados -> refatorar para evitar duplicação