import tkinter as tk
from typing import Dict, List, Optional
from .components.botoes import BotoesPadrao
from .components.textos import TextosPadrao
from .components.inputs import InputsPadrao
from .components.modais import ModaisPadrao
from .components.tabelas import TabelasPadrao


class TelaContrato:
    def __init__(self, controlador_contrato):
        self._controlador_contrato = controlador_contrato
        self.janela_modal = None
        self.tree = None
        self.main_frame = None
        
    def inicializar_componentes(self, parent):
        self.main_frame = tk.Frame(parent, bg="white")
        self.main_frame.pack(fill="both", expand=True)
        
        self._criar_cabecalho()
        
        self._criar_tabela()
        
        return self.main_frame
    
    def _criar_cabecalho(self):
        header_frame = tk.Frame(self.main_frame, bg="white")
        header_frame.pack(fill="x", padx=40, pady=(30, 20))
        
        titulo_frame = tk.Frame(header_frame, bg="white")
        titulo_frame.pack(side="left")
        
        TextosPadrao.titulo_principal(
            titulo_frame, 
            "Gerenciamento de Contratos"
        )
        TextosPadrao.subtitulo(
            titulo_frame, 
            "Visualize e gerencie os contratos de moradia.",
            cor="#666666"
        )
        
        botoes_frame = tk.Frame(header_frame, bg="white")
        botoes_frame.pack(side="right")
        
        BotoesPadrao.botao_cinza(
            botoes_frame,
            texto="Histórico",
            comando=self._abrir_historico_contratos,
            side="left"
        )
        
        BotoesPadrao.botao_azul(
            botoes_frame,
            texto="Adicionar Contrato",
            comando=self._abrir_modal_novo_contrato,
            side="left",
            padx=(10, 0)
        )
    
    def _criar_tabela(self):
        if hasattr(self, 'frame_lista') and self.frame_lista:
            self.frame_lista.destroy()
        self.frame_lista = tk.Frame(self.main_frame, bg="white")
        self.frame_lista.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        self.atualizar_lista()
    
    def atualizar_lista(self, contratos: Optional[List] = None):
        if contratos is None:
            contratos = self._controlador_contrato.listar_contratos()

        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        headers = ["Morador", "Início", "Fim", "Aluguel", "Status", "Ações"]
        weights = [2, 1, 1, 1, 1, 2]
        for i, header in enumerate(headers):
            self.frame_lista.columnconfigure(i, weight=weights[i])
            tk.Label(self.frame_lista, text=header, font=("Arial", 10, "bold"), bg="white").grid(row=0, column=i, sticky="w", padx=5)

            for i, contrato in enumerate(contratos):
                row = i + 1
                if hasattr(contrato, 'id'):
                    morador_nome = getattr(contrato, 'morador_nome', None) or (contrato.morador.nome if hasattr(contrato, 'morador') and contrato.morador else 'N/A')
                    data_inicio = contrato.data_inicio.strftime('%d/%m/%Y') if hasattr(contrato, 'data_inicio') and contrato.data_inicio else '-'
                    data_fim = contrato.data_fim.strftime('%d/%m/%Y') if hasattr(contrato, 'data_fim') and contrato.data_fim else '-'
                    valor_aluguel = float(getattr(contrato, 'valor_aluguel', 0))
                    status = getattr(contrato, 'status', '').capitalize()
                    status_raw = getattr(contrato, 'status', '').lower()
                    contrato_id = contrato.id
                else:
                    morador_nome = contrato.get('morador_nome', 'N/A')
                    data_inicio = contrato.get('data_inicio', '-')
                    data_fim = contrato.get('data_fim', '-')
                    valor_aluguel = float(contrato.get('valor_aluguel', 0))
                    status = contrato.get('status', '').capitalize()
                    status_raw = contrato.get('status', '').lower()
                    contrato_id = contrato.get('id')

                tk.Label(self.frame_lista, text=morador_nome, bg="white").grid(row=row, column=0, sticky="w", padx=5, pady=5)
                tk.Label(self.frame_lista, text=data_inicio, bg="white").grid(row=row, column=1, sticky="w", padx=5, pady=5)
                tk.Label(self.frame_lista, text=data_fim, bg="white").grid(row=row, column=2, sticky="w", padx=5, pady=5)
                tk.Label(self.frame_lista, text=f"R$ {valor_aluguel:.2f}", bg="white").grid(row=row, column=3, sticky="w", padx=5, pady=5)
                tk.Label(self.frame_lista, text=status, bg="white").grid(row=row, column=4, sticky="w", padx=5, pady=5)

                action_frame = tk.Frame(self.frame_lista, bg="white")
                action_frame.grid(row=row, column=5, sticky="w", padx=5)
                if status_raw == "ativo":
                    BotoesPadrao.botao_vermelho(action_frame, texto="Encerrar", comando=lambda cid=contrato_id: self._solicitar_rescisao(cid), side="left", padx=2, pady=2)
                elif status_raw == "agendado":
                    BotoesPadrao.botao_vermelho(action_frame, texto="Excluir", comando=lambda cid=contrato_id: self._solicitar_exclusao_agendado(cid), side="left", padx=2, pady=2)


    def _solicitar_exclusao_agendado(self, contrato_id: int):
        if self.confirmar_acao("Deseja realmente excluir este contrato agendado?"):
            if self._controlador_contrato.excluir_contrato(contrato_id):
                self.mostrar_sucesso("Contrato agendado foi excluído com sucesso!")
                self.atualizar_lista()

    def exibir_contratos(self, contratos=None):
        self.atualizar_lista(contratos)
    
    def _abrir_modal_novo_contrato(self):
        moradores_cadastrados = self._controlador_contrato.listar_moradores()
        if not moradores_cadastrados:
            self.mostrar_erro("Não há morador cadastrado")
            return

        quartos_cadastrados = self._controlador_contrato.listar_quartos()
        if not quartos_cadastrados:
            self.mostrar_erro("Não há quarto cadastrado!")
            return

        self._criar_modal_contrato(moradores_cadastrados, quartos_cadastrados)

    def _criar_modal_contrato(self, moradores: List[Dict], quartos: List[Dict]):
        self.janela_modal = ModaisPadrao.modal_formulario(
            titulo="Cadastrar contrato",
            largura=600,
            altura=580
        )
        
        ModaisPadrao.cabecalho_modal(self.janela_modal, "Cadastrar contrato")
        
        campos_frame = tk.Frame(self.janela_modal, bg="white")
        campos_frame.pack(fill="x", padx=40)
        
        self.combo_morador = InputsPadrao.combobox(
            campos_frame,
            label="Morador",
            valores=[m['nome'] for m in moradores]
        )
        self.moradores_dict = {m['nome']: m['id'] for m in moradores}
        
        self.combo_quarto = InputsPadrao.combobox(
            campos_frame,
            label="Quarto",
            valores=[f"Quarto {q['numero']}" for q in quartos]
        )
        self.quartos_dict = {f"Quarto {q['numero']}": q['id'] for q in quartos}
        
        self.entry_valor = InputsPadrao.campo_texto(
            campos_frame,
            label="Valor do Aluguel (R$)"
        )
        
        col1, col2 = ModaisPadrao.frame_duas_colunas(campos_frame)
        
        self.entry_data_inicio = InputsPadrao.campo_texto(
            col1,
            label="Data de Início (DD/MM/AAAA)"
        )
        
        self.entry_data_fim = InputsPadrao.campo_texto(
            col2,
            label="Data de Fim (DD/MM/AAAA)"
        )
        
        botoes_frame = tk.Frame(self.janela_modal, bg="white")
        botoes_frame.pack(side="bottom", fill="x", padx=40, pady=30)
        
        BotoesPadrao.botao_vermelho(
            botoes_frame,
            texto="Cancelar",
            comando=self._cancelar_modal,
            side="left"
        )
        
        BotoesPadrao.botao_azul(
            botoes_frame,
            texto="Salvar",
            comando=self._enviar_dados_para_controlador,
            side="right"
        )
    
    def _enviar_dados_para_controlador(self):
        morador_nome = self.combo_morador.get()
        quarto_nome = self.combo_quarto.get()
        valor = self.entry_valor.get()
        data_inicio = self.entry_data_inicio.get()
        data_fim = self.entry_data_fim.get()
        
        dados = {
            'morador_id': self.moradores_dict.get(morador_nome),
            'quarto_id': self.quartos_dict.get(quarto_nome),
            'valor_aluguel': valor,
            'data_inicio': data_inicio,
            'data_fim': data_fim
        }
        
        self._controlador_contrato.criar_contrato_interface(dados)
    
    
    def _solicitar_rescisao(self, contrato_id: int):
        if self.confirmar_acao("Deseja realmente rescindir este contrato?"):
            self._controlador_contrato.finalizar_contrato(contrato_id)
    
    def _abrir_historico_contratos(self):
        contratos_finalizados = self._controlador_contrato.listar_contratos(filtro_status='finalizado')
        self._criar_modal_historico(contratos_finalizados)
    
    def _cancelar_modal(self):
        if self.janela_modal:
            self.janela_modal.destroy()
            self.janela_modal = None
    
    def _criar_modal_historico(self, contratos: List):
        modal = ModaisPadrao.modal_formulario(
            titulo="Histórico de Contratos",
            largura=900,
            altura=600
        )
        ModaisPadrao.cabecalho_modal(modal, "Histórico de Contratos Finalizados")
        tabela_frame = tk.Frame(modal, bg="white")
        tabela_frame.pack(fill="both", expand=True, padx=40, pady=(20, 20))
        colunas = ("MORADOR", "QUARTO", "INÍCIO", "FIM", "ALUGUEL")
        larguras = [180, 100, 120, 120, 120]
        tree, scrollbar = TabelasPadrao.criar_tabela(
            tabela_frame,
            colunas,
            larguras,
            altura=15
        )
        if contratos:
            for contrato in contratos:
                tree.insert(
                    "", "end",
                    values=(
                        contrato.morador.nome if contrato.morador else 'N/A',
                        f"Quarto {contrato.quarto.numero_quarto}" if contrato.quarto else 'N/A',
                        contrato.data_inicio.strftime('%d/%m/%Y') if contrato.data_inicio else '-',
                        contrato.data_fim.strftime('%d/%m/%Y') if contrato.data_fim else '-',
                        f"R$ {float(contrato.valor_aluguel):.2f}"
                    )
                )
        else:
            tree.insert("", "end", values=("Nenhum contrato finalizado", "", "", "", ""))
        botoes_frame = tk.Frame(modal, bg="white")
        botoes_frame.pack(side="bottom", fill="x", padx=40, pady=30)
        BotoesPadrao.botao_azul(
            botoes_frame,
            texto="Fechar",
            comando=modal.destroy,
            side="right"
        )
    
    def fechar_modal(self):
        if self.janela_modal and self.janela_modal.winfo_exists():
            self.janela_modal.destroy()
            self.janela_modal = None
    
    def mostrar_erro_modal(self, mensagem: str):
        if self.janela_modal and self.janela_modal.winfo_exists():
            self._criar_dialog_customizado("Erro", mensagem, "#ef4444")
        else:
            self.mostrar_erro(mensagem)
    
    def _criar_dialog_customizado(self, titulo: str, mensagem: str, cor_fundo: str = "#3b82f6"):
        dialog = tk.Toplevel(self.janela_modal if self.janela_modal and self.janela_modal.winfo_exists() else None)
        dialog.title(titulo)
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        dialog.configure(bg="white")
        
        if self.janela_modal and self.janela_modal.winfo_exists():
            dialog.transient(self.janela_modal)
            dialog.grab_set()
            
            dialog.update_idletasks()
            x = self.janela_modal.winfo_x() + (self.janela_modal.winfo_width() // 2) - (dialog.winfo_width() // 2)
            y = self.janela_modal.winfo_y() + (self.janela_modal.winfo_height() // 2) - (dialog.winfo_height() // 2)
            dialog.geometry(f"+{x}+{y}")
        
        header = tk.Frame(dialog, bg=cor_fundo, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=titulo,
            font=("Arial", 14, "bold"),
            bg=cor_fundo,
            fg="white"
        ).pack(expand=True)
        
        tk.Label(
            dialog,
            text=mensagem,
            font=("Arial", 10),
            bg="white",
            fg="#333333",
            wraplength=300
        ).pack(pady=(20, 15))
        
        tk.Button(
            dialog,
            text="OK",
            command=dialog.destroy,
            bg=cor_fundo,
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=40,
            pady=10,
            cursor="hand2"
        ).pack(pady=(0, 20))
    
    def mostrar_sucesso(self, mensagem: str):
        self._criar_dialog_standalone("Sucesso", mensagem, "#10b981")
    
    def mostrar_erro(self, mensagem: str):
        self._criar_dialog_standalone("Erro", mensagem, "#ef4444")
    
    def mostrar_aviso(self, mensagem: str):
        self._criar_dialog_standalone("Aviso", mensagem, "#f59e0b")
    
    def confirmar_acao(self, mensagem: str) -> bool:
        return self._criar_dialog_confirmacao(mensagem)
    
    def _criar_dialog_standalone(self, titulo: str, mensagem: str, cor_fundo: str):
        dialog = tk.Toplevel()
        dialog.title(titulo)
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        dialog.configure(bg="white")
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        header = tk.Frame(dialog, bg=cor_fundo, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=titulo,
            font=("Arial", 14, "bold"),
            bg=cor_fundo,
            fg="white"
        ).pack(expand=True)
        
        tk.Label(
            dialog,
            text=mensagem,
            font=("Arial", 10),
            bg="white",
            fg="#333333",
            wraplength=300
        ).pack(pady=(20, 15))
        
        tk.Button(
            dialog,
            text="OK",
            command=dialog.destroy,
            bg=cor_fundo,
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=40,
            pady=10,
            cursor="hand2"
        ).pack(pady=(0, 20))
        
        dialog.wait_window()
    
    def _criar_dialog_confirmacao(self, mensagem: str) -> bool:
        resultado = [False]
        dialog = tk.Toplevel()
        dialog.title("Confirmar")
        dialog.geometry("400x160")
        dialog.resizable(False, False)
        dialog.configure(bg="white")
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        header = tk.Frame(dialog, bg="#3b82f6", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="Confirmar",
            font=("Arial", 14, "bold"),
            bg="#3b82f6",
            fg="white"
        ).pack(expand=True)
        
        tk.Label(
            dialog,
            text=mensagem,
            font=("Arial", 10),
            bg="white",
            fg="#333333",
            wraplength=350
        ).pack(pady=(20, 20))
        
        botoes_frame = tk.Frame(dialog, bg="white")
        botoes_frame.pack(pady=(0, 20))
        
        def confirmar():
            resultado[0] = True
            dialog.destroy()
        
        def cancelar():
            resultado[0] = False
            dialog.destroy()
        
        tk.Button(
            botoes_frame,
            text="Não",
            command=cancelar,
            bg="#6b7280",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=5)
        
        tk.Button(
            botoes_frame,
            text="Sim",
            command=confirmar,
            bg="#3b82f6",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=5)
        
        dialog.wait_window()
        return resultado[0]
    
    def mostrar(self):
        pass
