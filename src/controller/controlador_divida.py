from tkinter import ttk, messagebox
from .abstract_controlador import AbstractControlador
from src.views.tela_dividas import TelaDividas
from src.views.tela_formulario_divida import TelaFormularioDivida
from src.views.tela_recorrencia import TelaRecorrencia
from src.models.Divida import Divida
from src.models.Morador import Morador
from src.models.Pagamento import Pagamento
from src.models.Historico import Historico
from datetime import datetime, date


class ControladorDivida(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self.tela_dividas = None
        self.moradores = []

    def abre_tela(self, parent_view=None):
        self.moradores = Morador.buscar_com_contrato_ativo()
        self.tela_dividas = TelaDividas(parent_view.content_frame, self._controlador_sistema, self.moradores)
        self._controlador_sistema.tela_atual = self.tela_dividas
        self.tela_dividas.mostrar()

    def carregar_dividas_na_view(self, container: ttk.Frame, tipo_usuario: str, ordenar_por: str,
                                 incluir_quitadas: bool, usuario_logado=None):
        if tipo_usuario == 'morador' and usuario_logado:
            dividas = Divida.buscar_por_morador_com_filtros(usuario_logado.id, incluir_quitadas)
        else:
            dividas = Divida.buscar_com_filtros(ordenar_por, incluir_quitadas)

        for widget in container.winfo_children():
            widget.destroy()

        if not dividas:
            ttk.Label(container, text="Nenhuma dívida encontrada para os filtros selecionados.", font=("Arial", 12),
                      style="Dividas.TLabel").pack(expand=True)
            return

        headers = ["Morador", "Descrição", "Valor", "Vencimento", "Status"]
        if tipo_usuario == 'administrador':
            headers.append("Ações")
        elif tipo_usuario == 'morador':
            headers.append("Ações")

        for i, header in enumerate(headers):
            container.columnconfigure(i, weight=(2 if header == "Descrição" else 1))
            ttk.Label(container, text=header, font=("Arial", 10, "bold"), style="Dividas.TLabel").grid(row=0, column=i,
                                                                                                       sticky="w",
                                                                                                       padx=5)

        for i, divida in enumerate(dividas):
            row = i + 1

            status_texto = divida.status.capitalize()
            status_style = f"Status.{status_texto}.TLabel"
            vencimento_style = "Dividas.TLabel"

            try:
                data_obj = datetime.strptime(divida.data_vencimento, '%Y-%m-%d')
                data_venc_formatada = data_obj.strftime('%d/%m/%Y')
            except (ValueError, TypeError):
                data_venc_formatada = divida.data_vencimento

            if divida.is_vencida:
                status_texto = "Vencida"
                status_style = "Status.Vencida.TLabel"
                vencimento_style = "Status.Vencida.TLabel"

            ttk.Label(container, text=divida.nome_morador, style="Dividas.TLabel").grid(row=row, column=0, sticky="w",
                                                                                        padx=5, pady=3)
            ttk.Label(container, text=divida.descricao, style="Dividas.TLabel").grid(row=row, column=1, sticky="w",
                                                                                     padx=5, pady=3)
            ttk.Label(container, text=f"R$ {divida.valor:.2f}", style="Dividas.TLabel").grid(row=row, column=2,
                                                                                             sticky="w", padx=5, pady=3)
            ttk.Label(container, text=data_venc_formatada, style=vencimento_style).grid(row=row, column=3, sticky="w",
                                                                                        padx=5, pady=3)
            ttk.Label(container, text=status_texto, style=status_style).grid(row=row, column=4, sticky="w", padx=5,
                                                                             pady=3)

            if tipo_usuario == 'administrador':
                action_frame = ttk.Frame(container, style="Dividas.TFrame")
                action_frame.grid(row=row, column=5, sticky="w", padx=5)

                btn_editar = ttk.Button(action_frame, text="Editar", style="Editar.TButton",
                                        command=lambda d=divida: self.abrir_tela_formulario_divida(divida_existente=d))
                btn_editar.pack(side="left")

                btn_excluir = ttk.Button(action_frame, text="Excluir", style="Excluir.TButton",
                                         command=lambda d_id=divida.id: self.excluir_divida(d_id))
                btn_excluir.pack(side="left", padx=5)

            elif tipo_usuario == 'morador' and divida.status == 'pendente':
                action_frame = ttk.Frame(container, style="Dividas.TFrame")
                action_frame.grid(row=row, column=5, sticky="w", padx=5)

                pagamentos_pendentes = Pagamento.buscar_por_divida_e_status(divida.id, 'pendente')

                if pagamentos_pendentes:
                    btn_texto = "Pagamento Solicitado"
                    btn_state = "disabled"
                else:
                    btn_texto = "Solicitar Pagamento"
                    btn_state = "normal"

                btn_pagamento = ttk.Button(
                    action_frame,
                    text=btn_texto,
                    style="Salvar.TButton",
                    command=lambda d=divida: self.solicitar_pagamento(d),
                    state=btn_state
                )
                btn_pagamento.pack(side="left")

    def solicitar_pagamento(self, divida: Divida):
        try:
            pagamentos_pendentes = Pagamento.buscar_por_divida_e_status(divida.id, 'pendente')

            if pagamentos_pendentes:
                messagebox.showinfo("Informação", "Já existe uma solicitação de pagamento pendente para esta dívida.")
                return

            novo_pagamento = Pagamento(
                divida=divida,
                valor=divida.valor,
                data_pagamento=date.today().strftime('%Y-%m-%d'),
                status='pendente'
            )
            novo_pagamento.salvar()

            Historico.registrar_evento(
                evento="Solicitação de Pagamento",
                morador_nome=divida.morador.nome,
                divida_descricao=divida.descricao,
                valor=divida.valor,
                detalhes="Morador solicitou registro de pagamento"
            )

            messagebox.showinfo("Sucesso", "Solicitação de pagamento registrada com sucesso!")
            self.tela_dividas.atualizar_todas_abas()

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível solicitar o pagamento: {e}")
                

    def abrir_tela_formulario_divida(self, divida_existente=None):
        root_window = self._controlador_sistema.tela_atual.frame.winfo_toplevel()
        moradores_ativos = Morador.buscar_com_contrato_ativo()
        TelaFormularioDivida(root_window, self, moradores_ativos, divida_existente)

    def salvar_divida(self, dados: dict):
        try:
            valor = dados.get("valor")
            if valor is None or valor <= 0:
                messagebox.showerror("Erro de Validação", "O valor da dívida deve ser maior que zero.")
                return False

            data_venc_str = dados.get("data_vencimento")
            if data_venc_str:
                try:
                    data_venc = datetime.strptime(data_venc_str, '%Y-%m-%d').date()
                    if data_venc < date.today():
                        messagebox.showerror("Erro de Validação",
                                             "A data de vencimento não pode ser anterior à data atual.")
                        return False
                except ValueError:
                    messagebox.showerror("Erro de Validação", "Formato de data de vencimento inválido.")
                    return False
            else:
                messagebox.showerror("Erro de Validação", "A data de vencimento é obrigatória.")
                return False

            morador_id_selecionado = dados['morador_id']
            morador_obj = Morador.buscar_por_id(morador_id_selecionado)
            if not morador_obj:
                messagebox.showerror("Erro", f"Morador com ID {morador_id_selecionado} não encontrado.")
                return False

            if not Morador.tem_contrato_ativo(morador_id_selecionado):
                messagebox.showerror("Erro", "Não é possível criar dívida para um morador sem contrato ativo.")
                return False

            divida_antiga = None
            if dados.get("id"):
                divida_antiga = Divida.buscar_por_id(dados["id"])

            divida_nova = Divida(
                id=dados.get("id"),
                morador=morador_obj,
                valor=dados["valor"],
                descricao=dados["descricao"],
                data_vencimento=dados["data_vencimento"],
                status=dados.get("status", 'pendente')
            )
            divida_nova.salvar()

            nome_morador_novo = divida_nova.morador.nome if divida_nova.morador else "Desconhecido"

            if divida_antiga:
                mudancas = []

                if divida_antiga.morador.id != divida_nova.morador.id:
                    mudancas.append(f"Morador alterado para '{nome_morador_novo}'")
                if divida_antiga.descricao != divida_nova.descricao:
                    mudancas.append(f"Descrição -> '{divida_nova.descricao}'")
                if divida_antiga.valor != divida_nova.valor:
                    mudancas.append(f"Valor -> R$ {divida_nova.valor:.2f}")
                if divida_antiga.data_vencimento != divida_nova.data_vencimento:
                    mudancas.append(f"Vencimento -> {divida_nova.data_vencimento}")

                if mudancas:
                    Historico.registrar_evento(
                        evento="Dívida Editada",
                        morador_nome=nome_morador_novo,
                        divida_descricao=divida_antiga.descricao,
                        valor=divida_nova.valor,
                        detalhes=", ".join(mudancas)
                    )
            else:
                Historico.registrar_evento(
                    evento="Dívida Criada",
                    morador_nome=nome_morador_novo,
                    divida_descricao=divida_nova.descricao,
                    valor=divida_nova.valor
                )

            if self.tela_dividas:
                self.tela_dividas.atualizar_todas_abas()
            return True

        except Exception as e:
            messagebox.showerror("Erro ao Salvar Dívida", f"Não foi possível salvar a dívida: {e}")
            return False
        
    def salvar_divida_recorrencia(self, dados: dict):
        hoje = datetime.today()
        dia_atual = int(hoje.day)
        mes_atual = int(hoje.month)
        ano_atual = int(hoje.year)
        dia_int = dados["data_vencimento"]
        recorrencias = dados["recorrencia"]

        try:
            if recorrencias < 1:
                messagebox.showerror("Erro", "O número de recorrências deve ser superior à 0.")
            elif dados["valor"] <= 0:
                messagebox.showerror("Erro", "O valor da dívida deve ser maior que zero.")
                return False
            elif dia_int < 1 or dia_int > 28:
                messagebox.showerror("Erro", "A data de vencimento deve estar entre 1 e 28.")
                return False

            morador = dados["morador"]
            if not Morador.tem_contrato_ativo(morador.id):
                messagebox.showerror("Erro", "Não é possível criar dívida para um morador sem contrato ativo.")
                return False

            data_base = datetime(ano_atual, mes_atual, dia_int)

            if dia_atual > dia_int:
                resposta = messagebox.askyesno(
                    "Confirmação",
                    "A data de vencimento é anterior ao dia atual.\n"
                    "A primeira dívida será criada para o próximo mês.\n"
                    "Deseja continuar?"
                )
                if resposta:
                    novo_mes = mes_atual + 1
                    novo_ano = ano_atual
                    if novo_mes > 12:
                        novo_mes = 1
                        novo_ano += 1
                        data_base = datetime(novo_ano, novo_mes, dia_int)
                    else:
                        data_base = datetime(ano_atual, novo_mes, dia_int)
                else:
                    return False
            for i in range(recorrencias):
                novo_mes = (data_base.month + i - 1) % 12 + 1
                novo_ano = data_base.year + ((data_base.month + i - 1) // 12)
                nova_data = datetime(novo_ano, novo_mes, data_base.day)
                nova_divida = Divida(
                    morador=dados["morador"],
                    descricao=f"{dados['descricao']} (Parcela {i + 1}/{recorrencias})",
                    valor=dados["valor"],
                    data_vencimento=nova_data.strftime('%Y-%m-%d'),
                    status="pendente"
                )
                nova_divida.salvar()

                nome_morador = Morador.buscar_por_id(nova_divida.morador.id).nome
                Historico.registrar_evento(
                    evento="Dívida Recorrente Criada",
                    morador_nome=nome_morador,
                    divida_descricao=nova_divida.descricao,
                    valor=nova_divida.valor
                )

            self.tela_dividas.atualizar_todas_abas()
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar as dívidas recorrentes: {e}")
            return False
        
    def abrir_tela_recorrencia(self, divida_existente=None):
        root_window = self._controlador_sistema.tela_atual.frame.winfo_toplevel()
        moradores_ativos = Morador.buscar_com_contrato_ativo()
        TelaRecorrencia(root_window, self, moradores_ativos, divida_existente)

    def excluir_divida(self, divida_id: int):
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta dívida?", icon='warning'):
            try:
                Divida.deletar(divida_id)
                self.tela_dividas.atualizar_lista()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir a dívida: {e}")

    def carregar_pagamentos_pendentes(self, container: ttk.Frame, usuario_logado=None):
        if usuario_logado and usuario_logado.tipo_usuario == 'morador':
            pagamentos = Pagamento.buscar_por_morador(usuario_logado.id)
        else:
            pagamentos = Pagamento.buscar_pendentes()

        for widget in container.winfo_children():
            widget.destroy()

        if not pagamentos:
            texto = "Nenhuma solicitação de pagamento pendente." if usuario_logado and usuario_logado.tipo_usuario == 'administrador' else "Nenhuma solicitação de pagamento para acompanhar."
            ttk.Label(container, text=texto, style="Dividas.TLabel").pack(expand=True)
            return

        headers = ["Morador", "Dívida", "Valor Pago", "Data", "Status"]
        if usuario_logado and usuario_logado.tipo_usuario == 'administrador':
            headers.append("Ações")

        for i, h in enumerate(headers):
            container.columnconfigure(i, weight=1)
            ttk.Label(container, text=h, style="Dividas.TLabel", font=('Arial', 10, 'bold')).grid(row=0, column=i,
                                                                                                  sticky='w', padx=5)

        for i, pag in enumerate(pagamentos):
            row = i + 1
            try:
                data_obj = datetime.strptime(pag.data_pagamento, '%Y-%m-%d')
                data_pag_formatada = data_obj.strftime('%d/%m/%Y')
            except (ValueError, TypeError):
                data_pag_formatada = pag.data_pagamento

            status_texto = pag.status.capitalize()
            status_style = f"Status.{status_texto}.TLabel"

            ttk.Label(container, text=pag.divida.morador.nome, style="Dividas.TLabel").grid(row=row, column=0,
                                                                                            sticky='w', padx=5, pady=4)
            ttk.Label(container, text=pag.divida.descricao, style="Dividas.TLabel").grid(row=row, column=1, sticky='w',
                                                                                         padx=5, pady=4)
            ttk.Label(container, text=f"R$ {pag.valor:.2f}", style="Dividas.TLabel").grid(row=row, column=2, sticky='w',
                                                                                          padx=5, pady=4)
            ttk.Label(container, text=data_pag_formatada, style="Dividas.TLabel").grid(row=row, column=3, sticky='w',
                                                                                       padx=5, pady=4)
            ttk.Label(container, text=status_texto, style=status_style).grid(row=row, column=4, sticky='w', padx=5,
                                                                             pady=4)

            if usuario_logado and usuario_logado.tipo_usuario == 'administrador' and pag.status == 'pendente':
                action_frame = ttk.Frame(container, style="Dividas.TFrame")
                action_frame.grid(row=row, column=5, sticky='w')
                btn_aceitar = ttk.Button(action_frame, text="Aceitar", style="Salvar.TButton",
                                         command=lambda p=pag: self.aceitar_pagamento(p))
                btn_aceitar.pack(side='left')
                btn_recusar = ttk.Button(action_frame, text="Recusar", style="Excluir.TButton",
                                         command=lambda p=pag: self.recusar_pagamento(p))
                btn_recusar.pack(side='left', padx=5)

    def aceitar_pagamento(self, pagamento: Pagamento):
        try:
            pagamento.atualizar_status('confirmado')
            if pagamento.divida:
                pagamento.divida.atualizar_status('quitada')
                Historico.registrar_evento(
                    evento="Pagamento Confirmado",
                    morador_nome=pagamento.divida.morador.nome,
                    divida_descricao=pagamento.divida.descricao,
                    valor=pagamento.valor,
                    detalhes="Administrador confirmou o pagamento"
                )

            messagebox.showinfo("Sucesso", "Pagamento confirmado e dívida quitada.")
            self.tela_dividas.atualizar_todas_abas()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível aceitar o pagamento: {e}")

    def recusar_pagamento(self, pagamento: Pagamento):
        try:
            pagamento.atualizar_status('cancelado')
            Historico.registrar_evento(
                evento="Pagamento Recusado",
                morador_nome=pagamento.divida.morador.nome,
                divida_descricao=pagamento.divida.descricao,
                valor=pagamento.valor,
                detalhes="Administrador recusou o pagamento"
            )
            messagebox.showinfo("Sucesso", "Pagamento recusado. A dívida continua pendente.")
            self.tela_dividas.atualizar_todas_abas()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível recusar o pagamento: {e}")

    def carregar_historico(self, container: ttk.Frame, usuario_logado=None):
        for widget in container.winfo_children():
            widget.destroy()

        if usuario_logado and usuario_logado.tipo_usuario == 'morador':
            eventos_historico = Historico.buscar_por_morador(usuario_logado.nome)
        else:
            eventos_historico = Historico.buscar_todos()

        if not eventos_historico:
            ttk.Label(container, text="Nenhum histórico para exibir.", style="Dividas.TLabel").pack(expand=True)
            return

        headers = ["Data/Hora", "Evento", "Morador", "Descrição da Dívida", "Valor", "Detalhes"]
        weights = [2, 2, 2, 3, 1, 4]

        for i, h in enumerate(headers):
            container.columnconfigure(i, weight=weights[i])
            ttk.Label(container, text=h, style="Dividas.TLabel", font=('Arial', 10, 'bold')).grid(row=0, column=i,
                                                                                                  sticky='w', padx=5)

        for i, evento in enumerate(eventos_historico):
            row = i + 1

            try:
                dt_obj = datetime.fromisoformat(evento.timestamp)
                timestamp_formatado = dt_obj.strftime('%d/%m/%Y %H:%M')
            except (ValueError, TypeError):
                timestamp_formatado = evento.timestamp

            valor_str = f"R$ {evento.valor:.2f}" if evento.valor is not None else ""

            ttk.Label(container, text=timestamp_formatado, style="Dividas.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=3)
            ttk.Label(container, text=evento.evento, style="Dividas.TLabel").grid(row=row, column=1, sticky='w', padx=5, pady=3)
            ttk.Label(container, text=evento.morador_nome or "", style="Dividas.TLabel").grid(row=row, column=2, sticky='w', padx=5, pady=3)
            ttk.Label(container, text=evento.divida_descricao or "", style="Dividas.TLabel").grid(row=row, column=3, sticky='w', padx=5, pady=3)
            ttk.Label(container, text=valor_str, style="Dividas.TLabel").grid(row=row, column=4, sticky='w', padx=5,
                                                                              pady=3)
            ttk.Label(container, text=evento.detalhes or "", style="Dividas.TLabel", wraplength=400,
                      justify='left').grid(row=row, column=5, sticky='w', padx=5, pady=3)

    def recarregar_abas_secundarias(self):
        if self.tela_dividas:
            usuario_logado = self._controlador_sistema.usuario_logado
            if self.tela_dividas.frame_avaliar_pagamentos:
                self.carregar_pagamentos_pendentes(self.tela_dividas.frame_avaliar_pagamentos, usuario_logado)
            if self.tela_dividas.frame_historico:
                self.carregar_historico(self.tela_dividas.frame_historico, usuario_logado)
