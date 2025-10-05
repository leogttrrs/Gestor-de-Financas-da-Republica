import tkinter as tk
from tkinter import ttk, messagebox
from .menu_lateral import MenuAdministrador, MenuMorador
from .aplicacao_spa import ComponenteBase


class TelaComMenuLateral(ComponenteBase):
    
    def __init__(self, container, controlador_sistema, usuario_logado, tipo_usuario="admin", on_logout=None):
        super().__init__(container, controlador_sistema)
        self.usuario_logado = usuario_logado
        self.tipo_usuario = tipo_usuario
        self.on_logout = on_logout
        self.menu_lateral = None
        self.content_frame = None
        self.secao_atual = "dashboard"
        self.criar_interface()
    
    def criar_interface(self):
        self.criar_frame()
        style = ttk.Style()
        style.configure("Perfil.TFrame", background="white")
        self.frame.configure(style="Perfil.TFrame")
        
        if self.tipo_usuario == "admin":
            self.menu_lateral = MenuAdministrador(
                self.frame, 
                self.usuario_logado, 
                callback_navegacao=self._navegar_secao
            )
        else:
            self.menu_lateral = MenuMorador(
                self.frame, 
                self.usuario_logado, 
                callback_navegacao=self._navegar_secao
            )
        
        self.menu_lateral.definir_callback_sair(self._fazer_logout)
        
        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self._mostrar_conteudo_inicial()
    
    def _navegar_secao(self, secao):
        self.secao_atual = secao
        self._limpar_conteudo()
        
        if secao == "perfil_admin":
            self.controlador_sistema.controlador_administrador.abrir_tela_perfil(self)
        elif secao == "moradores":
            self.controlador_sistema.controlador_morador.abrir_tela_perfil(self)
        elif secao == "quartos":
            self.controlador_sistema.controlador_quarto.abre_tela(self)
        else:
            self._mostrar_em_desenvolvimento(secao)
    
    def _limpar_conteudo(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def _mostrar_conteudo_inicial(self):
        self.controlador_sistema.controlador_administrador.abrir_tela_perfil(self)
    
    def _mostrar_dashboard(self):
        self._mostrar_em_desenvolvimento("Quartos")
    
    def _criar_card_info(self, parent, titulo, valor, cor):
        card = ttk.Frame(parent, relief="solid", borderwidth=1)
        card.pack(side="left", fill="x", expand=True, padx=5)
        
        header = tk.Frame(card, bg=cor, height=4)
        header.pack(fill="x")
        
        content = ttk.Frame(card)
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
        title_label = ttk.Label(content, text=titulo, font=("Arial", 10), foreground="#666666")
        title_label.pack()
        
        value_label = ttk.Label(content, text=valor, font=("Arial", 16, "bold"))
        value_label.pack(pady=(5, 0))
    
    def _mostrar_moradores(self):
        self._mostrar_em_desenvolvimento("Moradores")
    
    def _mostrar_quartos(self):
        self._mostrar_em_desenvolvimento("Quartos")
    
    def _mostrar_contratos(self):
        self._mostrar_em_desenvolvimento("Contratos")
    
    def _mostrar_dividas(self):
        self._mostrar_em_desenvolvimento("Dívidas")
    
    def _mostrar_ocorrencias(self):
        self._mostrar_em_desenvolvimento("Ocorrências")
    
    def _mostrar_alertas(self):
        self._mostrar_em_desenvolvimento("Alertas")
    
    def _mostrar_em_desenvolvimento(self, secao):
        style = ttk.Style()
        style.configure("ContentWhite.TFrame", background="white")
        style.configure("ContentWhite.TLabel", background="white")
        
        self.content_frame.configure(style="ContentWhite.TFrame")
        
        title_label = ttk.Label(self.content_frame, text=secao, font=("Arial", 18, "bold"), 
                              background="white")
        title_label.pack(pady=(0, 20))
        
        content_area = ttk.Frame(self.content_frame, relief="solid", borderwidth=1, 
                               style="ContentWhite.TFrame")
        content_area.pack(fill="both", expand=True)
        
        placeholder_label = ttk.Label(content_area, text=f"Seção {secao} em desenvolvimento", 
                                    font=("Arial", 14), foreground="#999999", background="white")
        placeholder_label.pack(expand=True)
    
    def _fazer_logout(self):
        if self.on_logout:
            self.on_logout()

    def mostrar_formulario_perfil_admin(self, dados_usuario):
        self._limpar_conteudo()
        
        style = ttk.Style()
        style.configure("PerfilWhite.TFrame", background="white")
        style.configure("PerfilWhite.TLabel", background="white")
        
        self.content_frame.configure(style="PerfilWhite.TFrame")
        
        header_frame = ttk.Frame(self.content_frame, style="PerfilWhite.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Meu Perfil", font=("Arial", 20, "bold"), 
                              background="white")
        title_label.pack(side="left")
        
        subtitle_label = ttk.Label(header_frame, text="Atualize suas informações pessoais.", 
                                 font=("Arial", 10), foreground="gray", background="white")
        subtitle_label.pack(side="left", padx=(10, 0))
        
        form_frame = ttk.Frame(self.content_frame, style="PerfilWhite.TFrame")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        row1_frame = ttk.Frame(form_frame, style="PerfilWhite.TFrame")
        row1_frame.pack(fill="x", pady=(0, 20))
        
        nome_frame = ttk.Frame(row1_frame, style="PerfilWhite.TFrame")
        nome_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Label(nome_frame, text="Nome", font=("Arial", 10, "bold"), background="white").pack(anchor="w")
        self.entry_nome = ttk.Entry(nome_frame, font=("Arial", 10))
        self.entry_nome.pack(fill="x", ipady=8)
        self.entry_nome.insert(0, dados_usuario.get('nome', ''))
        
        cpf_frame = ttk.Frame(row1_frame, style="PerfilWhite.TFrame")
        cpf_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        ttk.Label(cpf_frame, text="CPF", font=("Arial", 10, "bold"), background="white").pack(anchor="w")
        self.entry_cpf = ttk.Entry(cpf_frame, font=("Arial", 10))
        self.entry_cpf.pack(fill="x", ipady=8)
        self.entry_cpf.insert(0, dados_usuario.get('cpf', ''))
        self.entry_cpf.configure(state="readonly")
        
        email_frame = ttk.Frame(form_frame, style="PerfilWhite.TFrame")
        email_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(email_frame, text="E-mail", font=("Arial", 10, "bold"), background="white").pack(anchor="w")
        self.entry_email = ttk.Entry(email_frame, font=("Arial", 10))
        self.entry_email.pack(fill="x", ipady=8)
        self.entry_email.insert(0, dados_usuario.get('email', ''))
        
        telefone_frame = ttk.Frame(form_frame, style="PerfilWhite.TFrame")
        telefone_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(telefone_frame, text="Telefone", font=("Arial", 10, "bold"), background="white").pack(anchor="w")
        self.entry_telefone = ttk.Entry(telefone_frame, font=("Arial", 10))
        self.entry_telefone.pack(fill="x", ipady=8)
        self.entry_telefone.insert(0, dados_usuario.get('telefone', ''))
        
        security_frame = ttk.Frame(form_frame, style="PerfilWhite.TFrame")
        security_frame.pack(fill="x", pady=(20, 20))
        
        ttk.Label(security_frame, text="Segurança", font=("Arial", 12, "bold"), background="white").pack(anchor="w")
        
        btn_mudar_senha = ttk.Button(security_frame, text="Mudar Senha", 
                                   command=lambda: self.controlador_sistema.controlador_administrador.abrir_tela_mudar_senha(self))
        btn_mudar_senha.pack(anchor="w", pady=(10, 0))
        
        danger_frame = ttk.Frame(form_frame, style="PerfilWhite.TFrame")
        danger_frame.pack(fill="x", pady=(20, 20))
        
        ttk.Label(danger_frame, text="Atenção!", font=("Arial", 12, "bold"), foreground="#dc3545", background="white").pack(anchor="w")
        ttk.Label(danger_frame, text="Ações irreversíveis que afetam todo o sistema.", 
                 font=("Arial", 9), foreground="#6c757d", background="white").pack(anchor="w", pady=(2, 10))
        
        btn_excluir_perfil = ttk.Button(danger_frame, text="Excluir Perfil e Dados", 
                                      command=lambda: self.controlador_sistema.controlador_administrador.excluir_perfil_admin(self),
                                      style="Danger.TButton")
        btn_excluir_perfil.pack(anchor="w")
        
        buttons_frame = ttk.Frame(form_frame, style="PerfilWhite.TFrame")
        buttons_frame.pack(fill="x", pady=(30, 0))
        
        btn_cancelar = ttk.Button(buttons_frame, text="Cancelar", 
                                command=lambda: self.controlador_sistema.controlador_administrador.abrir_tela_perfil(self),
                                style="Danger.TButton")
        btn_cancelar.pack(side="right", padx=(10, 0))
        
        btn_salvar = ttk.Button(buttons_frame, text="Salvar Alterações", 
                              command=self._salvar_perfil)
        btn_salvar.pack(side="right")
        
        style = ttk.Style()
        style.configure("Perfil.TButton", padding=(20, 10))
        btn_salvar.configure(style="Perfil.TButton")

    # O morador pode visualizar seu próprio perfil, mas não pode excluir o perfil -> portanto refactor.
    def mostrar_formulario_perfil_morador(self, dados_usuario):
        self._limpar_conteudo()
        
        style = ttk.Style()
        style.configure("PerfilWhite.TFrame", background="white")
        style.configure("PerfilWhite.TLabel", background="white")
        
        self.content_frame.configure(style="PerfilWhite.TFrame")
        
        header_frame = ttk.Frame(self.content_frame, style="PerfilWhite.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Meu perfil - Morador", font=("Arial", 20, "bold"), 
                              background="white")
        title_label.pack(side="left")
        
        subtitle_label = ttk.Label(header_frame, text="Atualize suas informações pessoais.", 
                                 font=("Arial", 10), foreground="gray", background="white")
        subtitle_label.pack(side="left", padx=(10, 0))
        
        form_frame = ttk.Frame(self.content_frame, style="PerfilWhite.TFrame")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        row1_frame = ttk.Frame(form_frame, style="PerfilWhite.TFrame")
        row1_frame.pack(fill="x", pady=(0, 20))
        
        nome_frame = ttk.Frame(row1_frame, style="PerfilWhite.TFrame")
        nome_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Label(nome_frame, text="Nome", font=("Arial", 10, "bold"), background="white").pack(anchor="w")
        self.entry_nome = ttk.Entry(nome_frame, font=("Arial", 10))
        self.entry_nome.pack(fill="x", ipady=8)
        self.entry_nome.insert(0, dados_usuario.get('nome', ''))
        
        cpf_frame = ttk.Frame(row1_frame, style="PerfilWhite.TFrame")
        cpf_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        ttk.Label(cpf_frame, text="CPF", font=("Arial", 10, "bold"), background="white").pack(anchor="w")
        self.entry_cpf = ttk.Entry(cpf_frame, font=("Arial", 10))
        self.entry_cpf.pack(fill="x", ipady=8)
        self.entry_cpf.insert(0, dados_usuario.get('cpf', ''))
        self.entry_cpf.configure(state="readonly")
        
        email_frame = ttk.Frame(form_frame, style="PerfilWhite.TFrame")
        email_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(email_frame, text="E-mail", font=("Arial", 10, "bold"), background="white").pack(anchor="w")
        self.entry_email = ttk.Entry(email_frame, font=("Arial", 10))
        self.entry_email.pack(fill="x", ipady=8)
        self.entry_email.insert(0, dados_usuario.get('email', ''))
        
        telefone_frame = ttk.Frame(form_frame, style="PerfilWhite.TFrame")
        telefone_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(telefone_frame, text="Telefone", font=("Arial", 10, "bold"), background="white").pack(anchor="w")
        self.entry_telefone = ttk.Entry(telefone_frame, font=("Arial", 10))
        self.entry_telefone.pack(fill="x", ipady=8)
        self.entry_telefone.insert(0, dados_usuario.get('telefone', ''))
        
        security_frame = ttk.Frame(form_frame, style="PerfilWhite.TFrame")
        security_frame.pack(fill="x", pady=(20, 20))
        
        ttk.Label(security_frame, text="Segurança", font=("Arial", 12, "bold"), background="white").pack(anchor="w")
        
        btn_mudar_senha = ttk.Button(security_frame, text="Mudar Senha", 
                                   command=lambda: self.controlador_sistema.controlador_morador.abrir_tela_mudar_senha(self))
        btn_mudar_senha.pack(anchor="w", pady=(10, 0))
        
        danger_frame = ttk.Frame(form_frame, style="PerfilWhite.TFrame")
        danger_frame.pack(fill="x", pady=(20, 20))
        
        ttk.Label(danger_frame, text="Atenção!", font=("Arial", 12, "bold"), foreground="#dc3545", background="white").pack(anchor="w")
        ttk.Label(danger_frame, text="Ações irreversíveis que afetam todo o sistema.", 
                 font=("Arial", 9), foreground="#6c757d", background="white").pack(anchor="w", pady=(2, 10))
        
        btn_excluir_perfil = ttk.Button(danger_frame, text="Excluir Perfil e Dados", 
                                      command=lambda: self.controlador_sistema.controlador_morador.excluir_perfil_morador(self),
                                      style="Danger.TButton")
        btn_excluir_perfil.pack(anchor="w")
        
        buttons_frame = ttk.Frame(form_frame, style="PerfilWhite.TFrame")
        buttons_frame.pack(fill="x", pady=(30, 0))
        
        btn_cancelar = ttk.Button(buttons_frame, text="Cancelar", 
                                command=lambda: self.controlador_sistema.controlador_morador.abrir_tela_perfil(self),
                                style="Danger.TButton")
        btn_cancelar.pack(side="right", padx=(10, 0))
        
        btn_salvar = ttk.Button(buttons_frame, text="Salvar Alterações", 
                              command=self._salvar_perfil)
        btn_salvar.pack(side="right")
        
        style = ttk.Style()
        style.configure("Perfil.TButton", padding=(20, 10))
        btn_salvar.configure(style="Perfil.TButton")

    def _salvar_perfil(self):
        dados = {
            'nome': self.entry_nome.get().strip(),
            'email': self.entry_email.get().strip(),
            'telefone': self.entry_telefone.get().strip()
        }
        self.controlador_sistema.controlador_morador.atualizar_perfil(self, dados)

    def mostrar_mensagem_sucesso(self, mensagem):
        messagebox.showinfo("Sucesso", mensagem)

    def mostrar_mensagem_erro(self, mensagem):
        messagebox.showerror("Erro", mensagem)


class TelaPerfilAdministrador(TelaComMenuLateral):
    def __init__(self, container, controlador_sistema, usuario_logado, on_logout=None):
        super().__init__(container, controlador_sistema, usuario_logado, "admin", on_logout)


class TelaPerfilMorador(TelaComMenuLateral):    
    def __init__(self, container, controlador_sistema, usuario_logado, on_logout=None):
        super().__init__(container, controlador_sistema, usuario_logado, "morador", on_logout)