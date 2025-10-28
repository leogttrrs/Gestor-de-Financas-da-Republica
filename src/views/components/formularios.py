import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.validador import Validador
from ..estilos import EstilosApp
from .containers import ContainersPadrao
from .textos import TextosPadrao
from .icones import IconesPadrao
from .botoes import BotoesPadrao


class FormularioPadrao:
    """
    Classe para criar formulários funcionais que retornam dados como o PySimpleGUI
    """

    def __init__(self, parent, titulo="Formulário"):
        self.parent = parent
        self.titulo = titulo
        self.resultado = None
        self.cancelado = False
        self.campos = {}
        self.janela = None
        # embedded_frame will be set by forms that support embedded mode
        self.embedded_frame = None

    def configurar_estilos_validacao(self):
        """Configura os estilos para campos válidos e inválidos"""
        EstilosApp.configurar_estilos_validacao()

    def criar_janela_modal(self, largura=500, altura=600):
        """Cria uma janela modal centralizada com scroll"""
        # Configurar estilos globais primeiro
        EstilosApp.configurar_estilos_globais()
        
        self.janela = tk.Toplevel(self.parent)
        self.janela.title(self.titulo)
        self.janela.geometry(f"{largura}x{altura}")
        self.janela.resizable(True, True)
        self.janela.configure(bg="#f5f5f5")

        # Configurar estilos de validação
        self.configurar_estilos_validacao()

        # Centralizar janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")

        # Tornar modal
        self.janela.transient(self.parent)
        self.janela.grab_set()

        # Adicionar canvas e scrollbar para scroll
        canvas = tk.Canvas(self.janela, bg="#f5f5f5")
        scrollbar = ttk.Scrollbar(self.janela, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        return self.scrollable_frame

    def mostrar(self):
        """Exibe o formulário. Para formulários embutidos usa `embedded_frame`,
        caso contrário reexibe a janela modal."""
        if getattr(self, 'embedded_frame', None) is not None:
            # pack the embedded frame centered
            self.embedded_frame.pack(pady=40, anchor="center")
        elif self.janela:
            try:
                self.janela.deiconify()
            except Exception:
                pass

    def esconder(self):
        """Esconde o formulário embutido ou a janela modal."""
        if getattr(self, 'embedded_frame', None) is not None:
            try:
                self.embedded_frame.pack_forget()
            except Exception:
                pass
        elif self.janela:
            try:
                self.janela.withdraw()
            except Exception:
                pass

    def adicionar_campo_texto(self, container, label, chave, valor_inicial="", obrigatorio=True):
        """Adiciona um campo de texto ao formulário"""
        # Label
        TextosPadrao.label_campo(container, label)

        # Campo com estilo sem bordas
        style = ttk.Style()
        style.configure("InputTexto.TEntry",
                       fieldbackground="white",
                       borderwidth=0,
                       relief="solid",
                       font=("Arial", 11),
                       focuscolor="none")

        entry = ttk.Entry(container, font=("Arial", 11), width=40, style="InputTexto.TEntry")
        entry.pack(fill="x", pady=(0, 15), ipady=8)

        if valor_inicial:
            entry.insert(0, valor_inicial)

        self.campos[chave] = {
            'widget': entry,
            'obrigatorio': obrigatorio,
            'tipo': 'texto'
        }

        return entry

    def adicionar_campo_senha(self, container, label, chave, valor_inicial="", obrigatorio=True):
        """Adiciona um campo de senha ao formulário"""
        # Label
        TextosPadrao.label_campo(container, label)

        # Campo com estilo sem bordas
        style = ttk.Style()
        style.configure("InputSenha.TEntry",
                       fieldbackground="white",
                       borderwidth=0,
                       relief="solid",
                       font=("Arial", 11),
                       focuscolor="none")

        entry = ttk.Entry(container, font=("Arial", 11), width=40, show="*", style="InputSenha.TEntry")
        entry.pack(fill="x", pady=(0, 15), ipady=8)

        if valor_inicial:
            entry.insert(0, valor_inicial)

        self.campos[chave] = {
            'widget': entry,
            'obrigatorio': obrigatorio,
            'tipo': 'senha'
        }

        return entry

    def adicionar_combobox(self, container, label, chave, opcoes, valor_inicial="", obrigatorio=True):
        """Adiciona um combobox ao formulário"""
        # Label
        TextosPadrao.label_campo(container, label)

        # Configurar estilo sem bordas para combobox
        style = ttk.Style()
        style.configure("InputCombo.TCombobox",
                       fieldbackground="white",
                       borderwidth=0,
                       relief="flat",
                       font=("Arial", 11),
                       focuscolor="none")

        # Combobox
        combo = ttk.Combobox(container, values=opcoes, state="readonly", font=("Arial", 11), style="InputCombo.TCombobox")
        combo.pack(fill="x", pady=(0, 15), ipady=8)

        if valor_inicial:
            combo.set(valor_inicial)

        self.campos[chave] = {
            'widget': combo,
            'obrigatorio': obrigatorio,
            'tipo': 'combo'
        }

        return combo

    def adicionar_campo_cpf(self, container, label, chave, valor_inicial="", obrigatorio=True):
        """Adiciona um campo de CPF com validação automática"""
        # Label
        TextosPadrao.label_campo(container, label)

        # Campo com estilo sem bordas
        style = ttk.Style()
        style.configure("InputCPF.TEntry",
                       fieldbackground="white",
                       borderwidth=0,
                       relief="flat",
                       font=("Arial", 11),
                       focuscolor="none")

        entry = ttk.Entry(container, font=("Arial", 11), width=40, style="InputCPF.TEntry")
        entry.pack(fill="x", pady=(0, 15), ipady=8)

        if valor_inicial:
            entry.insert(0, valor_inicial)

        # Adicionar validação em tempo real
        def validar_cpf_focusout(event):
            valor = entry.get().strip()
            if valor and valor != "":
                resultado = Validador.validar_cpf(valor)
                if "inválido" in str(resultado) or "Erro" in str(resultado):
                    entry.configure(style="InputInvalido.TEntry")
                    # Criar tooltip ou mostrar erro visual
                else:
                    entry.configure(style="InputValido.TEntry")
                    # Formatar CPF se válido
                    if isinstance(resultado, str) and len(resultado) == 11:
                        cpf_formatado = f"{resultado[:3]}.{resultado[3:6]}.{resultado[6:9]}-{resultado[9:]}"
                        entry.delete(0, tk.END)
                        entry.insert(0, cpf_formatado)

        entry.bind("<FocusOut>", validar_cpf_focusout)

        self.campos[chave] = {
            'widget': entry,
            'obrigatorio': obrigatorio,
            'tipo': 'cpf',
            'validador': Validador.validar_cpf
        }

        return entry

    def adicionar_campo_email(self, container, label, chave, valor_inicial="", obrigatorio=True):
        """Adiciona um campo de email com validação automática"""
        # Label
        TextosPadrao.label_campo(container, label)

        # Campo com estilo sem bordas
        style = ttk.Style()
        style.configure("InputEmail.TEntry",
                       fieldbackground="white",
                       borderwidth=0,
                       relief="flat",
                       font=("Arial", 11),
                       focuscolor="none")

        entry = ttk.Entry(container, font=("Arial", 11), width=40, style="InputEmail.TEntry")
        entry.pack(fill="x", pady=(0, 15), ipady=8)

        if valor_inicial:
            entry.insert(0, valor_inicial)

        # Adicionar validação em tempo real
        def validar_email_focusout(event):
            valor = entry.get().strip()
            if valor and valor != "":
                resultado = Validador.validar_email(valor)
                if "inválido" in str(resultado):
                    entry.configure(style="InputInvalido.TEntry")
                else:
                    entry.configure(style="InputValido.TEntry")

        entry.bind("<FocusOut>", validar_email_focusout)

        self.campos[chave] = {
            'widget': entry,
            'obrigatorio': obrigatorio,
            'tipo': 'email',
            'validador': Validador.validar_email
        }

        return entry

    def adicionar_campo_telefone(self, container, label, chave, valor_inicial="", obrigatorio=True):
        """Adiciona um campo de telefone com validação automática"""
        # Label
        TextosPadrao.label_campo(container, label)

        # Campo
        entry = ttk.Entry(container, font=("Arial", 11), width=40)
        entry.pack(fill="x", pady=(0, 15), ipady=8)

        if valor_inicial:
            entry.insert(0, valor_inicial)

        # Adicionar validação em tempo real
        def validar_telefone_focusout(event):
            valor = entry.get().strip()
            if valor and valor != "":
                resultado = Validador.validar_telefone(valor)
                if "inválido" in str(resultado):
                    entry.configure(style="InputInvalido.TEntry")
                else:
                    entry.configure(style="InputValido.TEntry")
                    # Formatar telefone se válido
                    import re
                    telefone_limpo = re.sub(r'[^0-9]', '', valor)
                    if len(telefone_limpo) == 11:
                        telefone_formatado = f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
                        entry.delete(0, tk.END)
                        entry.insert(0, telefone_formatado)
                    elif len(telefone_limpo) == 10:
                        telefone_formatado = f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
                        entry.delete(0, tk.END)
                        entry.insert(0, telefone_formatado)

        entry.bind("<FocusOut>", validar_telefone_focusout)

        self.campos[chave] = {
            'widget': entry,
            'obrigatorio': obrigatorio,
            'tipo': 'telefone',
            'validador': Validador.validar_telefone
        }

        return entry

    def adicionar_campo_nome(self, container, label, chave, valor_inicial="", obrigatorio=True):
        """Adiciona um campo de nome com validação automática"""
        # Label
        TextosPadrao.label_campo(container, label)

        # Campo com estilo sem bordas
        style = ttk.Style()
        style.configure("InputNome.TEntry",
                       fieldbackground="white",
                       borderwidth=0,
                       relief="flat",
                       font=("Arial", 11),
                       focuscolor="none")

        entry = ttk.Entry(container, font=("Arial", 11), width=40, style="InputNome.TEntry")
        entry.pack(fill="x", pady=(0, 15), ipady=8)

        if valor_inicial:
            entry.insert(0, valor_inicial)

        # Adicionar validação em tempo real
        def validar_nome_focusout(event):
            valor = entry.get().strip()
            if valor and valor != "":
                resultado = Validador.validar_nome(valor)
                if "inválido" in str(resultado) or "deve ter" in str(resultado):
                    entry.configure(style="InputInvalido.TEntry")
                else:
                    entry.configure(style="InputValido.TEntry")
                    # Aplicar formatação Title Case
                    if isinstance(resultado, str):
                        entry.delete(0, tk.END)
                        entry.insert(0, resultado)

        entry.bind("<FocusOut>", validar_nome_focusout)

        self.campos[chave] = {
            'widget': entry,
            'obrigatorio': obrigatorio,
            'tipo': 'nome',
            'validador': Validador.validar_nome
        }

        return entry

    def adicionar_campo_data_nascimento(self, container, label, chave, valor_inicial="", obrigatorio=True):
        """Adiciona um campo de data de nascimento com validação automática"""
        # Label
        TextosPadrao.label_campo(container, label)

        # Campo
        entry = ttk.Entry(container, font=("Arial", 11), width=40)
        entry.pack(fill="x", pady=(0, 15), ipady=8)

        if valor_inicial:
            entry.insert(0, valor_inicial)

        # Adicionar validação em tempo real
        def validar_data_focusout(event):
            valor = entry.get().strip()
            if valor and valor != "":
                resultado = Validador.validar_data_nascimento(valor)
                if "inválido" in str(resultado) or "Formato" in str(resultado):
                    entry.configure(style="InputInvalido.TEntry")
                else:
                    entry.configure(style="InputValido.TEntry")
                    # Aplicar formatação de data
                    if isinstance(resultado, str) and "/" in resultado:
                        entry.delete(0, tk.END)
                        entry.insert(0, resultado)

        entry.bind("<FocusOut>", validar_data_focusout)

        self.campos[chave] = {
            'widget': entry,
            'obrigatorio': obrigatorio,
            'tipo': 'data_nascimento',
            'validador': Validador.validar_data_nascimento
        }

        return entry

    def adicionar_campo_senha_validada(self, container, label, chave, valor_inicial="", obrigatorio=True):
        """Adiciona um campo de senha com validação automática"""
        # Label
        TextosPadrao.label_campo(container, label)

        # Campo
        entry = ttk.Entry(container, font=("Arial", 11), width=40, show="*")
        entry.pack(fill="x", pady=(0, 15), ipady=8)

        if valor_inicial:
            entry.insert(0, valor_inicial)

        # Adicionar validação em tempo real
        def validar_senha_focusout(event):
            valor = entry.get().strip()
            if valor and valor != "":
                valida, mensagem = Validador.validar_senha(valor)
                if not valida:
                    entry.configure(style="InputInvalido.TEntry")
                else:
                    entry.configure(style="InputValido.TEntry")

        entry.bind("<FocusOut>", validar_senha_focusout)

        self.campos[chave] = {
            'widget': entry,
            'obrigatorio': obrigatorio,
            'tipo': 'senha_validada',
            'validador': Validador.validar_senha
        }

        return entry

    def adicionar_campo_preco(self, container, label, chave, valor_inicial="", obrigatorio=True):
        """Adiciona um campo de preço com validação automática"""
        # Label
        TextosPadrao.label_campo(container, label)

        # Campo
        entry = ttk.Entry(container, font=("Arial", 11), width=40)
        entry.pack(fill="x", pady=(0, 15), ipady=8)

        if valor_inicial:
            entry.insert(0, str(valor_inicial))

        # Adicionar validação em tempo real
        def validar_preco_focusout(event):
            valor = entry.get().strip()
            if valor and valor != "":
                resultado = Validador.validar_preco(valor)
                if "inválido" in str(resultado):
                    entry.configure(style="InputInvalido.TEntry")
                else:
                    entry.configure(style="InputValido.TEntry")
                    # Formatar preço
                    if isinstance(resultado, (int, float)):
                        entry.delete(0, tk.END)
                        entry.insert(0, f"R$ {resultado:.2f}")

        entry.bind("<FocusOut>", validar_preco_focusout)

        self.campos[chave] = {
            'widget': entry,
            'obrigatorio': obrigatorio,
            'tipo': 'preco',
            'validador': Validador.validar_preco
        }

        return entry

    def validar_campos(self):
        """Valida todos os campos obrigatórios"""
        campos_invalidos = []

        for chave, campo_info in self.campos.items():
            widget = campo_info['widget']
            obrigatorio = campo_info['obrigatorio']

            valor = widget.get().strip()

            if obrigatorio and not valor:
                campos_invalidos.append(chave)

        return campos_invalidos

    def obter_valores(self):
        """Obtém os valores de todos os campos"""
        valores = {}
        for chave, campo_info in self.campos.items():
            widget = campo_info['widget']
            valores[chave] = widget.get().strip()
        return valores

    def confirmar_acao(self, mensagem):
        """Exibe uma caixa de confirmação"""
        return messagebox.askyesno("Confirmação", mensagem)

    def exibir_erro(self, mensagem):
        """Exibe uma mensagem de erro"""
        messagebox.showerror("Erro", mensagem)

    def exibir_sucesso(self, mensagem):
        """Exibe uma mensagem de sucesso"""
        messagebox.showinfo("Sucesso", mensagem)

    def criar_botoes(self, container, texto_confirmar="Confirmar", texto_cancelar="Cancelar"):
        """Cria os botões de ação do formulário"""
        buttons_frame = ttk.Frame(container, style="CartaoBranco.TFrame")
        buttons_frame.pack(fill="x", side="bottom", padx=30, pady=(20, 30))

        # Container para os botões lado a lado
        botoes_container = tk.Frame(buttons_frame, bg="white")
        botoes_container.pack(fill="x")
        
        # Frame para botão cancelar (esquerda)
        cancelar_frame = tk.Frame(botoes_container, bg="white")
        cancelar_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Frame para botão confirmar (direita)  
        confirmar_frame = tk.Frame(botoes_container, bg="white")
        confirmar_frame.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # Botão cancelar (vermelho, à esquerda)
        btn_cancelar = BotoesPadrao.botao_vermelho(
            cancelar_frame,
            texto_cancelar,
            self._cancelar
        )

        # Botão confirmar (azul, à direita)
        btn_confirmar = BotoesPadrao.botao_azul(
            confirmar_frame,
            texto_confirmar,
            self._confirmar
        )

        return btn_confirmar, btn_cancelar

    def _confirmar(self):
        """Ação do botão confirmar"""
        campos_invalidos = self.validar_campos()

        if campos_invalidos:
            self.exibir_erro(f"Preencha os seguintes campos obrigatórios: {', '.join(campos_invalidos)}")
            return

        self.resultado = self.obter_valores()
        self.cancelado = False
        self.janela.destroy()

    def _cancelar(self):
        """Ação do botão cancelar"""
        valores = self.obter_valores()

        # Verificar se há dados preenchidos
        tem_dados = any(valor.strip() for valor in valores.values())

        if tem_dados:
            if not self.confirmar_acao("Há informações preenchidas. Deseja descartar?"):
                return

        self.resultado = None
        self.cancelado = True
        self.janela.destroy()

    def executar(self):
        """Executa o formulário e retorna o resultado"""
        if self.janela:
            self.janela.wait_window()
        return self.resultado, self.cancelado


class TelaCadastroMorador(FormularioPadrao):
    """
    Exemplo de uso do FormularioPadrao para cadastro de morador
    """

    def __init__(self, parent, controlador, dados_iniciais=None):
        super().__init__(parent, "Cadastro de Morador")
        self.controlador = controlador
        self.dados_iniciais = dados_iniciais or {}
        self.criar_interface()

    def criar_interface(self):
        """Cria a interface do formulário"""
        janela = self.criar_janela_modal(largura=500, altura=650)

        # Fundo e cartão
        main_container = ContainersPadrao.fundo_cinza(janela)
        card = ContainersPadrao.cartao_branco(main_container, largura=450, altura=600)

        # Cabeçalho
        IconesPadrao.icone_casa(card, tamanho=36)
        TextosPadrao.titulo_principal(card, "Cadastro de Morador")
        TextosPadrao.subtitulo(card, "Preencha os dados do morador")

        # Container dos campos
        fields_container = ContainersPadrao.container_campos(card, padding_x=30)

        # Campos do formulário com validação automática
        self.adicionar_campo_nome(
            fields_container,
            "Nome Completo:",
            "nome",
            self.dados_iniciais.get("nome", "")
        )

        self.adicionar_campo_cpf(
            fields_container,
            "CPF:",
            "cpf",
            self.dados_iniciais.get("cpf", "")
        )

        self.adicionar_campo_email(
            fields_container,
            "E-mail:",
            "email",
            self.dados_iniciais.get("email", "")
        )

        self.adicionar_campo_telefone(
            fields_container,
            "Telefone:",
            "telefone",
            self.dados_iniciais.get("telefone", "")
        )

        self.adicionar_campo_texto(
            fields_container,
            "Número do Quarto:",
            "numero_quarto",
            str(self.dados_iniciais.get("numero_quarto", ""))
        )

        if not self.dados_iniciais:  # Só para cadastro novo
            self.adicionar_campo_senha_validada(fields_container, "Senha:", "senha")
            self.adicionar_campo_senha_validada(fields_container, "Confirmar Senha:", "confirmar_senha")

        # Botões
        texto_acao = "Atualizar" if self.dados_iniciais else "Cadastrar"
        self.criar_botoes(card, texto_acao, "Cancelar")

    def validar_campos(self):
        """Validação específica para morador"""
        campos_invalidos = super().validar_campos()

        valores = self.obter_valores()

        # Validação específica de senha para cadastro novo
        if not self.dados_iniciais:
            senha = valores.get("senha", "")
            confirmar_senha = valores.get("confirmar_senha", "")

            if senha != confirmar_senha:
                self.exibir_erro("As senhas não coincidem")
                return ["senha", "confirmar_senha"]

        # Validação de número do quarto
        numero_quarto = valores.get("numero_quarto", "")
        try:
            int(numero_quarto)
        except ValueError:
            if numero_quarto:  # Só valida se não estiver vazio
                campos_invalidos.append("numero_quarto")

        return campos_invalidos