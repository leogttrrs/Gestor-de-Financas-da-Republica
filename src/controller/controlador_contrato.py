from .abstract_controlador import AbstractControlador
from src.models.Contrato import Contrato
from src.models.Divida import Divida
from src.models.Quarto import Quarto
from src.models.Morador import Morador
from src.views.tela_contrato import TelaContrato
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal, InvalidOperation


class ControladorContrato(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self._tela_contrato = None

    def abre_tela(self, parent_view=None):
        if parent_view is None:
            return
        
        self._atualizar_status_contratos()
        
        self._tela_contrato = TelaContrato(self)
        
        self._tela_contrato.inicializar_componentes(parent_view.content_frame)
        
        self._atualizar_lista_contratos()

    
    def _parse_data(self, data_str: str) -> Optional[date]:
        formatos = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']
        for fmt in formatos:
            try:
                return datetime.strptime(data_str, fmt).date()
            except ValueError:
                continue
        return None

    def _periodos_se_sobrepoem(self,
                               inicio_a: Optional[date],
                               fim_a: Optional[date],
                               inicio_b: Optional[date],
                               fim_b: Optional[date]) -> bool:
        if not inicio_a or not inicio_b:
            return False
        fim_a = fim_a or date.max
        fim_b = fim_b or date.max
        return inicio_a <= fim_b and inicio_b <= fim_a

    def _atualizar_status_contratos(self):
        hoje = date.today()
        contratos = Contrato.buscar_todos()
        
        for contrato in contratos:
            if contrato.status == 'ativo':
                if contrato.data_fim and contrato.data_fim <= hoje:
                    contrato.status = 'finalizado'
                    contrato.salvar()
            
            elif contrato.status == 'agendado':
                data_inicio = contrato.data_inicio
                if data_inicio and data_inicio <= hoje and contrato.quarto:
                    contratos_ativos = [
                        c for c in Contrato.buscar_por_quarto(contrato.quarto.id)
                        if c.id != contrato.id and c.status == 'ativo'
                    ]
                    conflito = any(
                        self._periodos_se_sobrepoem(
                            data_inicio,
                            contrato.data_fim,
                            c.data_inicio,
                            c.data_fim
                        ) for c in contratos_ativos
                    )
                    if not conflito:
                        contrato.status = 'ativo'
                        contrato.salvar()
    
    def _atualizar_lista_contratos(self):
        if self._tela_contrato is None:
            return
        
        contratos = self.listar_contratos(filtro_status='ativo')
        contratos_agendados = self.listar_contratos(filtro_status='agendado')
        contratos = contratos + contratos_agendados
        
        contratos_dict = []
        for contrato in contratos:
            contratos_dict.append({
                'id': contrato.id,
                'morador_nome': contrato.morador.nome if contrato.morador else 'N/A',
                'quarto_numero': contrato.quarto.numero_quarto if contrato.quarto else 'N/A',
                'valor_aluguel': float(contrato.valor_aluguel),
                'data_inicio': contrato.data_inicio.strftime('%d/%m/%Y') if contrato.data_inicio else '-',
                'data_fim': contrato.data_fim.strftime('%d/%m/%Y') if contrato.data_fim else '-',
                'status': contrato.status
            })
        
        self._tela_contrato.exibir_contratos(contratos_dict)

    def listar_contratos(self, filtro_status: Optional[str] = None, 
                         filtro_data: Optional[str] = None,
                         ordenar_por: str = 'data_inicio') -> List[Contrato]:
        contratos = Contrato.buscar_todos()
        
        if filtro_status:
            contratos = [c for c in contratos if c.status == filtro_status]
        
        if filtro_data:
            hoje = date.today()
            
            if filtro_data == 'maior_que_hoje':
                contratos = [c for c in contratos if c.data_fim and c.data_fim > hoje]
            elif filtro_data == 'menor_ou_igual_hoje':
                contratos = [c for c in contratos if c.data_fim and c.data_fim <= hoje]
            elif filtro_data == 'menor_que_hoje':
                contratos = [c for c in contratos if c.data_fim and c.data_fim < hoje]
        
        if ordenar_por == 'data_inicio':
            contratos.sort(key=lambda c: c.data_inicio if c.data_inicio else date.min, reverse=True)
        
        return contratos

    def listar_contratos_ativos(self) -> List[Contrato]:
        return self.listar_contratos(filtro_status='ativo')

    def verificar_morador_pode_ter_contrato(self, morador_id: int, quarto_id: int) -> bool:
        contrato_ativo = Contrato.buscar_contrato_ativo_morador(morador_id)
        if contrato_ativo:
            return False
        
        return self._verificar_disponibilidade_quarto(quarto_id)

    def _verificar_disponibilidade_quarto(self, quarto_id: int, morador_id: Optional[int] = None) -> bool:
        try:
            quarto = Quarto.buscar_por_id(quarto_id)
            if not quarto:
                return False
            
            return quarto.obter_vagas_disponiveis() > 0
            
        except Exception:
            return False

    def criar_contrato(self, morador_id: int, quarto_id: int, valor_aluguel: float = 0.0, 
                      data_inicio: Optional[date] = None) -> Optional[Contrato]:
        try:
            if not self.verificar_morador_pode_ter_contrato(morador_id, quarto_id):
                return None
            
            morador = Morador.buscar_por_id(morador_id)
            quarto = Quarto.buscar_por_id(quarto_id)
            
            if not morador or not quarto:
                return None
            
            contrato = Contrato(
                morador=morador,
                quarto=quarto,
                valor_aluguel=Decimal(str(valor_aluguel)),
                data_inicio=data_inicio if data_inicio else date.today(),
                status='ativo'
            )
            
            contrato_salvo = contrato.salvar()
            
            return contrato_salvo
            
        except Exception:
            return None

    def atualizar_contrato(self, contrato_id: int, **kwargs) -> Optional[Contrato]:
        try:
            contrato = Contrato.buscar_por_id(contrato_id)
            if not contrato:
                return None
            
            if 'valor_aluguel' in kwargs:
                contrato.valor_aluguel = Decimal(str(kwargs['valor_aluguel']))
            if 'data_inicio' in kwargs:
                contrato.data_inicio = kwargs['data_inicio']
            if 'data_fim' in kwargs:
                contrato.data_fim = kwargs['data_fim']
            if 'status' in kwargs:
                contrato.status = kwargs['status']
            
            return contrato.salvar()
            
        except Exception:
            return None

    def finalizar_contrato(self, contrato_id: int) -> bool:
        try:
            contrato = Contrato.buscar_por_id(contrato_id)
            
            if self._morador_possui_divida_ativa(contrato.morador.id):
                if self._tela_contrato:
                    self._tela_contrato.mostrar_erro(
                        "Não foi possível efetuar a operação! O morador possui pendências de dívida"
                    )
                return False
            
            contrato.finalizar()

            if self._tela_contrato:
                self._atualizar_lista_contratos()
                self._tela_contrato.mostrar_sucesso("Contrato encerrado com sucesso!")
            
            return True
            
        except Exception as e:
            if self._tela_contrato:
                self._tela_contrato.mostrar_erro(f"Erro ao finalizar contrato: {str(e)}")
            return False
    
    def _morador_possui_divida_ativa(self, morador_id: int) -> bool:
        try:
            dividas = Divida.buscar_por_morador(morador_id)
            return any(d.status == 'pendente' for d in dividas)
        except Exception:
            return False

    def excluir_contrato(self, contrato_id: int) -> bool:
        try:
            contrato = Contrato.buscar_por_id(contrato_id)

            contrato.excluir()
            if self._tela_contrato:
                self._atualizar_lista_contratos()
            return True

        except Exception as e:
            if self._tela_contrato:
                self._tela_contrato.mostrar_erro(f"Erro ao excluir contrato: {str(e)}")
            return False

    def listar_moradores(self) -> List[dict]:
        try:
            moradores = Morador.buscar_todos()
            return [{'id': m.id, 'nome': m.nome, 'cpf': m.cpf} for m in moradores]
        except Exception:
            return []

    def listar_quartos(self) -> List[dict]:
        try:
            quartos = Quarto.buscar_todos()
            return [{
                'id': q.id,
                'numero': q.numero_quarto,
                'tamanho': q.tamanho,
                'vagas_disponiveis': q.obter_vagas_disponiveis(),
                'status': q.status
            } for q in quartos]
        except Exception:
            return []

    def criar_contrato_interface(self, dados: dict) -> None:
        if not self._tela_contrato:
            return

        try:
            campos_obrigatorios = ('morador_id', 'quarto_id', 'valor_aluguel', 'data_inicio', 'data_fim')
            if not dados or any(not dados.get(campo) for campo in campos_obrigatorios):
                self._tela_contrato.mostrar_erro_modal("Preencha todos os campos!")
                return

            morador_id = int(dados.get('morador_id'))
            quarto_id = int(dados.get('quarto_id'))
            valor_aluguel_bruto = str(dados.get('valor_aluguel')).strip()
            data_inicio_str = str(dados.get('data_inicio')).strip()
            data_fim_str = str(dados.get('data_fim')).strip()

            try:
                valor_aluguel = Decimal(valor_aluguel_bruto.replace(',', '.'))
                if valor_aluguel <= 0:
                    raise InvalidOperation()
            except (InvalidOperation, TypeError, ValueError):
                self._tela_contrato.mostrar_erro_modal("Valor de aluguel inválido!")
                return

            data_inicio = self._parse_data(data_inicio_str)
            data_fim = self._parse_data(data_fim_str)

            if not data_inicio or not data_fim:
                self._tela_contrato.mostrar_erro_modal("Data de início e/ou fim inválida! Utilize o formato DD/MM/AAAA.")
                return

            if data_inicio < date.today():
                self._tela_contrato.mostrar_erro_modal(
                    "Data de início inválida! Data de início deve ser igual ou posterior ao dia de hoje."
                )
                return
            elif data_inicio == date.today():
                status_contrato = 'ativo'
            else:
                status_contrato = 'agendado'

            if data_fim <= data_inicio:
                self._tela_contrato.mostrar_erro_modal(
                    "Data de fim inválida! A data de fim deve ser posterior à data de início do contrato."
                )
                return

            if data_fim <= date.today():
                self._tela_contrato.mostrar_erro_modal(
                    "Data de fim inválida! Informe uma data posterior ao dia de hoje."
                )
                return

            morador = Morador.buscar_por_id(morador_id)

            if self._morador_possui_divida_ativa(morador_id):
                self._tela_contrato.mostrar_erro_modal(
                    "Não foi possível efetuar a operação! O morador possui pendências de dívida."
                )
                return

            if Contrato.existe_contrato_vigente_para_morador(morador_id, data_inicio):
                self._tela_contrato.mostrar_erro_modal("Não foi possível efetuar a operação! \n O morador possui contrato ativo/agendado no período do novo contrato.")
                return

            quarto = Quarto.buscar_por_id(quarto_id)

            if Contrato.existe_contrato_vigente_para_quarto(quarto_id, data_inicio):
                self._tela_contrato.mostrar_erro_modal("Não foi possível efetuar a operação! \n O quarto possui contrato ativo/agendado no período do novo contrato.")
                return

            contrato = Contrato(
                morador=morador,
                quarto=quarto,
                valor_aluguel=valor_aluguel,
                data_inicio=data_inicio,
                data_fim=data_fim,
                status=status_contrato
            )

            contrato.salvar()
            self._atualizar_lista_contratos()
            self._tela_contrato.fechar_modal()
            self._tela_contrato.mostrar_sucesso("Contrato cadastrado com sucesso!")

        except Exception as e:
            self._tela_contrato.mostrar_erro_modal(f"Erro ao criar contrato: {str(e)}")
