import tkinter as tk
from tkinter import ttk, messagebox
from .components import ContainersPadrao, IconesPadrao, TextosPadrao, FormularioPadrao
from src.utils.validador import Validador


class TelaCadastroAdministrador(FormularioPadrao):

    def __init__(self, container, controlador_sistema, on_voltar=None, on_cadastro_success=None, embedded: bool = False):
        super().__init__(container, "Cadastro de Administrador")
        self.controlador_sistema = controlador_sistema
        self.on_voltar = on_voltar
        self.on_cadastro_success = on_cadastro_success
        self.embedded = embedded
        self.cancelado = True  # Inicialmente cancelado
        self.resultado = None
        
        # Só criar interface se for embedded
        if self.embedded:
            self.criar_interface()
    
    def criar_interface(self):
        """Cria interface usando componentes padronizados"""
        # Se estiver em modo embutido (embedded), renderiza dentro do container
        if self.embedded:
            container = self.container if hasattr(self, 'container') else self.parent
            
            # Criar frame principal embutido
            self.embedded_frame = tk.Frame(container, bg="#f0f0f0")
            
            # Criar canvas para scroll
            canvas = tk.Canvas(self.embedded_frame, bg="#f0f0f0", highlightthickness=0)
            scrollbar = tk.Scrollbar(self.embedded_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
            
            # Configurar scroll
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Pack canvas e scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Container centralizado para o cartão
            container_centralizado = tk.Frame(scrollable_frame, bg="#f0f0f0")
            container_centralizado.pack(fill="x", expand=True, padx=50, pady=30)
            
            # Criar cartão branco centralizado
            card = ContainersPadrao.cartao_branco(container_centralizado, largura=880, altura=650)
            card.pack(anchor="center")
            
            # Centralizar o conteúdo no canvas
            window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
            
            # Função para centralizar horizontalmente quando a janela redimensionar
            def centralizar_conteudo(event=None):
                canvas.update_idletasks()
                canvas_width = canvas.winfo_width()
                if canvas_width > 1:  # Evitar divisão por zero
                    # Centralizar horizontalmente
                    x_center = canvas_width // 2
                    canvas.coords(window_id, x_center, 0)
            
            canvas.bind("<Configure>", centralizar_conteudo)
            # Centralizar imediatamente após criação
            canvas.after_idle(centralizar_conteudo)
            
            # Bind mouse wheel para scroll
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        else:
            # Criar janela modal padronizada  
            janela = self.criar_janela_modal(largura=1000, altura=450)
            # Fundo e cartão padronizados
            card = ContainersPadrao.cartao_branco(janela, largura=1000, altura=450)

        # Cabeçalho padronizado
        IconesPadrao.icone_casa(card, tamanho=26)
        TextosPadrao.titulo_principal(card, "Cadastro de Administrador")
        TextosPadrao.subtitulo(card, "Gerencie sua república com facilidade.")

        # Container de campos padronizado
        fields_container = ContainersPadrao.container_campos(card, padding_x=30)

        # Linha 1: Nome e Email lado a lado
        linha1_frame = tk.Frame(fields_container, bg="white")
        linha1_frame.pack(fill="x", pady=5)
        
        nome_frame = tk.Frame(linha1_frame, bg="white")
        nome_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.adicionar_campo_nome(nome_frame, "Nome Completo:", "nome")
        
        email_frame = tk.Frame(linha1_frame, bg="white")
        email_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.adicionar_campo_email(email_frame, "E-mail:", "email")
        
        # Linha 2: CPF e Telefone lado a lado
        linha2_frame = tk.Frame(fields_container, bg="white")
        linha2_frame.pack(fill="x", pady=5)
        
        cpf_frame = tk.Frame(linha2_frame, bg="white")
        cpf_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.adicionar_campo_cpf(cpf_frame, "CPF:", "cpf")
        
        telefone_frame = tk.Frame(linha2_frame, bg="white")
        telefone_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.adicionar_campo_telefone(telefone_frame, "Telefone:", "telefone")
        
        # Linha 3: Senhas lado a lado
        linha3_frame = tk.Frame(fields_container, bg="white")
        linha3_frame.pack(fill="x", pady=5)
        
        senha_frame = tk.Frame(linha3_frame, bg="white")
        senha_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.adicionar_campo_senha_validada(senha_frame, "Senha:", "senha")
        
        conf_senha_frame = tk.Frame(linha3_frame, bg="white")
        conf_senha_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.adicionar_campo_senha_validada(conf_senha_frame, "Confirmar Senha:", "confirmar_senha")

        # Botões padronizados
        self.criar_botoes(card, "Cadastrar", "Cancelar")

        # Link para voltar ao login
        if self.on_voltar:
            link_frame = ttk.Frame(card, style="CartaoBranco.TFrame")
            link_frame.pack(pady=(10, 20))
            # In embedded mode, on_voltar should simply switch to the login view
            if self.embedded:
                TextosPadrao.link_azul(link_frame, "Já tem uma conta? Fazer login",
                                          lambda: self.on_voltar())
            else:
                # in modal mode, the base class logic already closes the modal
                TextosPadrao.link_azul(link_frame, "Já tem uma conta? Fazer login",
                                          lambda: self.on_voltar())

    def validar_campos(self):
        valores = self.obter_valores()
        
        nome = valores.get("nome", "").strip()
        if not nome:
            self.exibir_erro("O campo Nome é obrigatório")
            return ["nome"]
        
        nome_validado = Validador.validar_nome(nome)
        if isinstance(nome_validado, str) and ("inválido" in nome_validado.lower() or "deve ter" in nome_validado.lower()):
            self.exibir_erro(nome_validado)
            return ["nome"]
        
        email = valores.get("email", "").strip()
        if not email:
            self.exibir_erro("O campo E-mail é obrigatório")
            return ["email"]
        
        email_validado = Validador.validar_email(email)
        if isinstance(email_validado, str) and "inválido" in email_validado.lower():
            self.exibir_erro(email_validado)
            return ["email"]
        
        cpf = valores.get("cpf", "").strip()
        if not cpf:
            self.exibir_erro("O campo CPF é obrigatório")
            return ["cpf"]
        
        cpf_validado = Validador.validar_cpf(cpf)
        if isinstance(cpf_validado, str) and ("inválido" in cpf_validado.lower() or "erro" in cpf_validado.lower()):
            self.exibir_erro(cpf_validado)
            return ["cpf"]
        
        telefone = valores.get("telefone", "").strip()
        if not telefone:
            self.exibir_erro("O campo Telefone é obrigatório")
            return ["telefone"]
        
        telefone_validado = Validador.validar_telefone(telefone)
        if isinstance(telefone_validado, str) and "inválido" in telefone_validado.lower():
            self.exibir_erro(telefone_validado)
            return ["telefone"]
        
        senha = valores.get("senha", "").strip()
        confirmar_senha = valores.get("confirmar_senha", "").strip()
        
        if not senha:
            self.exibir_erro("O campo Senha é obrigatório")
            return ["senha"]
        
        if not confirmar_senha:
            self.exibir_erro("O campo Confirmar Senha é obrigatório")
            return ["confirmar_senha"]
        
        valida, mensagem = Validador.validar_senha(senha)
        if not valida:
            self.exibir_erro(mensagem)
            return ["senha"]
        
        if senha != confirmar_senha:
            self.exibir_erro("As senhas não coincidem")
            return ["senha", "confirmar_senha"]

        return []

    def executar(self):
        """Executa o modal e retorna os dados coletados"""
        # Se não estiver em modo embedded, criar janela modal
        if not self.embedded:
            import tkinter as tk
            
            # Criar janela modal
            self.janela = tk.Toplevel()
            self.janela.title("Cadastro de Administrador")
            self.janela.geometry("500x650")
            self.janela.resizable(False, False)
            self.janela.grab_set()  # Modal
            
            # Centralizar janela
            self.janela.update_idletasks()
            x = (self.janela.winfo_screenwidth() // 2) - (500 // 2)
            y = (self.janela.winfo_screenheight() // 2) - (650 // 2)
            self.janela.geometry(f"500x650+{x}+{y}")
            
            # Atualizar o container para ser a janela modal
            self.container = self.janela
            
            # Criar interface na janela modal
            self.criar_interface()
            
        # Aguardar fechamento da janela
        if hasattr(self, 'janela'):
            self.janela.wait_window()
        
        # Retornar dados coletados
        if hasattr(self, 'resultado') and not self.cancelado:
            return self.resultado, True  # dados, should_return_to_login
        else:
            return None, False  # cancelado ou erro

    def _confirmar(self):
        """Sobrescreve confirmação para processar cadastro"""
        campos_invalidos = self.validar_campos()

        if campos_invalidos:
            self.exibir_erro(f"Preencha os seguintes campos obrigatórios: {', '.join(campos_invalidos)}")
            return
        
        dados = self.obter_valores()

        if self.controlador_sistema:
            sucesso, mensagem = self.controlador_sistema.controlador_administrador.cadastrar_administrador(
                dados["cpf"], dados["nome"], dados["email"],
                dados["telefone"], dados["senha"]
            )
            
            if sucesso:
                self.exibir_sucesso("Administrador cadastrado com sucesso!")
                self.resultado = dados
                self.cancelado = False
                # No modo embedded, chamar callback
                if self.embedded and self.on_cadastro_success:
                    self.on_cadastro_success()
                elif hasattr(self, 'janela'):
                    self.janela.destroy()
                    if self.on_cadastro_success:
                        self.on_cadastro_success()
            else:
                self.exibir_erro(mensagem)
        else:
            self.exibir_erro("Sistema não disponível")
    
    def _cancelar(self):
        """Sobrescreve ação do botão cancelar para voltar ao login"""
        if self.embedded and self.on_voltar:
            # No modo SPA, chama callback para voltar ao login
            self.on_voltar()
        elif hasattr(self, 'janela'):
            # No modo modal, fecha a janela
            self.janela.destroy()
        else:
            # Fallback padrão
            super()._cancelar()

    def mostrar(self):
        """Mostra o componente no SPA"""
        if self.embedded and hasattr(self, 'embedded_frame'):
            self.embedded_frame.pack(fill="both", expand=True)
    
    def esconder(self):
        """Esconde o componente no SPA"""
        if self.embedded and hasattr(self, 'embedded_frame'):
            self.embedded_frame.pack_forget()
