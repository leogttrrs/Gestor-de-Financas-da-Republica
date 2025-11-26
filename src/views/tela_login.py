from .tela_cadastro_base import ComponenteBase
from .components.botoes import BotoesPadrao
from .components.inputs import InputsPadrao
from .components.containers import ContainersPadrao
from .components.icones import IconesPadrao
from .components.textos import TextosPadrao
from tkinter import ttk, messagebox


class TelaLogin(ComponenteBase):
    def __init__(self, container, controlador_sistema, on_login_success=None, on_criar_perfil=None):
        super().__init__(container, controlador_sistema)
        self.on_login_success = on_login_success
        self.on_criar_perfil = on_criar_perfil
        self.criar_interface()

    def criar_interface(self):
        self.criar_frame()
        card = ContainersPadrao.cartao_branco(self.frame, largura=520, altura=520)
        
        IconesPadrao.icone_casa(card)

        TextosPadrao.titulo_principal(card, "Bem-vindo!")

        fields_frame = ContainersPadrao.container_campos(card)
        # Inputs padronizados
        self.entry_cpf = InputsPadrao.input_padrao(fields_frame, "Seu CPF", largura=30, altura=8)
        self.entry_senha = InputsPadrao.input_padrao(fields_frame, "Sua senha", largura=30, altura=8, tipo_senha=True)

        self.btn_entrar = BotoesPadrao.botao_azul(fields_frame, "Entrar", self._fazer_login, altura=10)

        # Container para links de cadastro usando componentes padronizados
        criar_frame = ttk.Frame(card, style="CartaoBranco.TFrame")
        criar_frame.pack(pady=(20, 30))

        text_frame = ttk.Frame(criar_frame, style="CartaoBranco.TFrame")
        text_frame.pack()

        TextosPadrao.link_azul(text_frame, "Crie seu perfil", self._criar_perfil, cor="#4A90E2")

        desc_label = ttk.Label(text_frame, text=" para administrar sua república", 
                             font=("Arial", 10), foreground="gray", background="white")
        desc_label.pack(side="left")

        self.frame.bind("<Return>", lambda e: self._fazer_login())
        self.frame.focus_set()

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

    def _esqueceu_senha(self):
        messagebox.showinfo("Esqueceu sua senha", "Funcionalidade em desenvolvimento")
    
    def _criar_perfil(self):
        if self.on_criar_perfil:
            self.on_criar_perfil()
