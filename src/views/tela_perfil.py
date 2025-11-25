import tkinter as tk
from tkinter import ttk, messagebox
from .menu_lateral import MenuAdministrador, MenuMorador
from .aplicacao_spa import ComponenteBase
from src.utils.validador import Validador


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
        
        match secao:
            case "perfil_admin":
                if hasattr(self.controlador_sistema, 'controlador_administrador'):
                    self.controlador_sistema.controlador_administrador.abrir_tela_perfil(self)
                else:
                    self._mostrar_em_desenvolvimento('perfil_admin')
            case "perfil_morador":
                if hasattr(self.controlador_sistema, 'controlador_morador'):
                    self.controlador_sistema.controlador_morador.abrir_tela_perfil(self)
                else:
                    self._mostrar_em_desenvolvimento('perfil_morador')
            case "moradores":
                self.controlador_sistema.controlador_morador.abre_tela(self)
            case "quartos":
                self.controlador_sistema.controlador_quarto.abre_tela(self)
            case "contratos":
                self.controlador_sistema.controlador_contrato.abre_tela(self)
            case "dividas":
                self.controlador_sistema.controlador_divida.abre_tela(self)
            case "recorrencias":
                self.controlador_sistema.controlador_recorrencia.abre_tela(self)
            case "ocorrencias":
                self.controlador_sistema.controlador_ocorrencia.abre_tela(self)
            case _:
                self._mostrar_em_desenvolvimento(secao)
    
    def _limpar_conteudo(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def _mostrar_conteudo_inicial(self):
        if self.tipo_usuario == 'admin':
            if hasattr(self.controlador_sistema, 'controlador_administrador'):
                self.controlador_sistema.controlador_administrador.abrir_tela_perfil(self)
            else:
                self._mostrar_em_desenvolvimento('perfil_admin')
        else:
            if hasattr(self.controlador_sistema, 'controlador_morador'):
                self.controlador_sistema.controlador_morador.abrir_tela_perfil(self)
            else:
                self._mostrar_em_desenvolvimento('perfil_morador')
    
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

    def _salvar_perfil(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()
        
        nome_validado = Validador.validar_nome(nome)
        if isinstance(nome_validado, str) and ("inválido" in nome_validado.lower() or "deve ter" in nome_validado.lower()):
            self.mostrar_mensagem_erro(nome_validado)
            return
        
        email_validado = Validador.validar_email(email)
        if isinstance(email_validado, str) and "inválido" in email_validado.lower():
            self.mostrar_mensagem_erro(email_validado)
            return
        
        telefone_validado = Validador.validar_telefone(telefone)
        if isinstance(telefone_validado, str) and "inválido" in telefone_validado.lower():
            self.mostrar_mensagem_erro(telefone_validado)
            return
        
        dados = {
            'nome': nome_validado if isinstance(nome_validado, str) and "inválido" not in nome_validado.lower() else nome,
            'email': email_validado if isinstance(email_validado, str) and "inválido" not in email_validado.lower() else email,
            'telefone': telefone_validado if isinstance(telefone_validado, str) and "inválido" not in telefone_validado.lower() else telefone
        }
        
        if self.tipo_usuario == 'admin':
            self.controlador_sistema.controlador_administrador.atualizar_perfil(self, dados)
        else:
            self.controlador_sistema.controlador_morador.atualizar_perfil(self, dados)

    def mostrar_formulario_perfil_morador(self, dados_usuario):
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
                                   command=lambda: self.controlador_sistema.controlador_morador.abrir_tela_mudar_senha(self))
        btn_mudar_senha.pack(anchor="w", pady=(10, 0))
        
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

    def mostrar_mensagem_sucesso(self, mensagem):
        messagebox.showinfo("Sucesso", mensagem)

    def mostrar_mensagem_erro(self, mensagem):
        messagebox.showerror("Erro", mensagem)

    def mostrar_formulario_mudar_senha(self):
        self._limpar_conteudo()
        
        style = ttk.Style()
        style.configure("SenhaWhite.TFrame", background="white")
        style.configure("SenhaWhite.TLabel", background="white")
        
        self.content_frame.configure(style="SenhaWhite.TFrame")
        
        header_frame = ttk.Frame(self.content_frame, style="SenhaWhite.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Alterar Senha", font=("Arial", 20, "bold"), 
                              background="white")
        title_label.pack(side="left")
        
        subtitle_label = ttk.Label(header_frame, text="Atualize sua senha de acesso.", 
                                 font=("Arial", 10), foreground="gray", background="white")
        subtitle_label.pack(side="left", padx=(10, 0))
        
        form_frame = ttk.Frame(self.content_frame, style="SenhaWhite.TFrame")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        senha_atual_frame = ttk.Frame(form_frame, style="SenhaWhite.TFrame")
        senha_atual_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(senha_atual_frame, text="Senha Atual", font=("Arial", 10, "bold"), background="white").pack(anchor="w")
        self.entry_senha_atual = ttk.Entry(senha_atual_frame, font=("Arial", 10), show="*")
        self.entry_senha_atual.pack(fill="x", ipady=8)
        
        senha_nova_frame = ttk.Frame(form_frame, style="SenhaWhite.TFrame")
        senha_nova_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(senha_nova_frame, text="Nova Senha", font=("Arial", 10, "bold"), background="white").pack(anchor="w")
        self.entry_senha_nova = ttk.Entry(senha_nova_frame, font=("Arial", 10), show="*")
        self.entry_senha_nova.pack(fill="x", ipady=8)
        ttk.Label(senha_nova_frame, text="Mínimo de 6 caracteres", 
                 font=("Arial", 8), foreground="#6c757d", background="white").pack(anchor="w", pady=(2, 0))
        
        confirmar_senha_frame = ttk.Frame(form_frame, style="SenhaWhite.TFrame")
        confirmar_senha_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(confirmar_senha_frame, text="Confirmar Nova Senha", font=("Arial", 10, "bold"), background="white").pack(anchor="w")
        self.entry_confirmar_senha = ttk.Entry(confirmar_senha_frame, font=("Arial", 10), show="*")
        self.entry_confirmar_senha.pack(fill="x", ipady=8)
        
        info_frame = ttk.Frame(form_frame, style="SenhaWhite.TFrame")
        info_frame.pack(fill="x", pady=(10, 20))
        
        info_label = ttk.Label(info_frame, 
                             text="⚠️ Por segurança, você será redirecionado ao perfil após a alteração.",
                             font=("Arial", 9), foreground="#856404", background="#fff3cd",
                             padding=10, relief="solid", borderwidth=1)
        info_label.pack(fill="x")
        
        buttons_frame = ttk.Frame(form_frame, style="SenhaWhite.TFrame")
        buttons_frame.pack(fill="x", pady=(30, 0))
        
        if self.tipo_usuario == 'admin':
            btn_cancelar = ttk.Button(buttons_frame, text="Cancelar", 
                                    command=lambda: self.controlador_sistema.controlador_administrador.abrir_tela_perfil(self),
                                    style="Danger.TButton")
        else:
            btn_cancelar = ttk.Button(buttons_frame, text="Cancelar", 
                                    command=lambda: self.controlador_sistema.controlador_morador.abrir_tela_perfil(self),
                                    style="Danger.TButton")
        btn_cancelar.pack(side="right", padx=(10, 0))
        
        btn_salvar = ttk.Button(buttons_frame, text="Alterar Senha", 
                              command=self._alterar_senha)
        btn_salvar.pack(side="right")
        
        style = ttk.Style()
        style.configure("Senha.TButton", padding=(20, 10))
        btn_salvar.configure(style="Senha.TButton")

    def _alterar_senha(self):        
        senha_atual = self.entry_senha_atual.get().strip()
        senha_nova = self.entry_senha_nova.get().strip()
        confirmar_senha = self.entry_confirmar_senha.get().strip()
        
        if not senha_atual:
            self.mostrar_mensagem_erro("A senha atual é obrigatória")
            return
        
        if not senha_nova:
            self.mostrar_mensagem_erro("A nova senha é obrigatória")
            return
        
        if not confirmar_senha:
            self.mostrar_mensagem_erro("A confirmação de senha é obrigatória")
            return
        
        if senha_nova != confirmar_senha:
            self.mostrar_mensagem_erro("A nova senha e a confirmação não coincidem")
            return
        
        valida, mensagem = Validador.validar_senha(senha_nova)
        if not valida:
            self.mostrar_mensagem_erro(mensagem)
            return
        
        if self.tipo_usuario == 'admin':
            self.controlador_sistema.controlador_administrador.alterar_senha(
                self, senha_atual, senha_nova, confirmar_senha
            )
        else:
            self.controlador_sistema.controlador_morador.alterar_senha(
                self, senha_atual, senha_nova, confirmar_senha
            )


class TelaPerfilAdministrador(TelaComMenuLateral):
    def __init__(self, container, controlador_sistema, usuario_logado, on_logout=None):
        super().__init__(container, controlador_sistema, usuario_logado, "admin", on_logout)


class TelaPerfilMorador(TelaComMenuLateral):    
    def __init__(self, container, controlador_sistema, usuario_logado, on_logout=None):
        super().__init__(container, controlador_sistema, usuario_logado, "morador", on_logout)