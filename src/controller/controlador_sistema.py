import atexit

from .controlador_administrador import ControladorAdministrador
from .controlador_morador import ControladorMorador
from .controlador_republica import ControladorRepublica
from .controlador_contrato import ControladorContrato
from .controlador_divida import ControladorDivida
from .controlador_pagamento import ControladorPagamento
from .controlador_ocorrencia import ControladorOcorrencia
from .controlador_alerta import ControladorAlerta
from .controlador_quarto import ControladorQuarto
from .controlador_recorrencia import ControladorRecorrencia
from src.models.Administrador import Administrador
from src.models.Morador import Morador



# from src.views.tela_sistema import TelaSistema 


class ControladorSistema:
    
    def __init__(self):
        self.__controlador_administrador = ControladorAdministrador(self)
        self.__controlador_morador = ControladorMorador(self)
        self.__controlador_republica = ControladorRepublica(self)
        self.__controlador_contrato = ControladorContrato(self)
        self.__controlador_divida = ControladorDivida(self)
        self.__controlador_pagamento = ControladorPagamento(self)
        self.__controlador_ocorrencia = ControladorOcorrencia(self)
        self.__controlador_alerta = ControladorAlerta(self)
        self.__controlador_quarto = ControladorQuarto(self)
        self.__controlador_recorrencia = ControladorRecorrencia(self)
        self.__usuario_logado = None
        self.__tela_atual = None
        
        # self.__tela_sistema = TelaSistema() Implementar
        
        atexit.register(self.salvar_todos_os_dados)
    
    @property
    def controlador_administrador(self) -> ControladorAdministrador:
        return self.__controlador_administrador

    @property
    def controlador_morador(self):
        return self.__controlador_morador

    @property
    def controlador_quarto(self) -> ControladorQuarto:
        return self.__controlador_quarto

    @property
    def controlador_contrato(self):
        return self.__controlador_contrato

    @property
    def controlador_divida(self):
        return self.__controlador_divida

    @property
    def controlador_ocorrencia(self) -> ControladorOcorrencia:
        return self.__controlador_ocorrencia
    
    @property
    def controlador_recorrencia(self) -> ControladorRecorrencia:
        return self.__controlador_controlador_recorrencia

    @property
    def tela_atual(self):
        return self.__tela_atual

    @tela_atual.setter
    def tela_atual(self, tela):
        self.__tela_atual = tela
    
    @property
    def usuario_logado(self):
        return self.__usuario_logado
    
    @usuario_logado.setter
    def usuario_logado(self, usuario):
        self.__usuario_logado = usuario
    
    def inicializa_sistema(self):
        self.abre_tela()
    
    def fazer_login(self, cpf: str = None, senha: str = None):
        if cpf and senha:
            admin = Administrador.buscar_por_cpf(cpf)
            if admin and admin.verificar_senha(senha):
                self.__usuario_logado = admin
                return admin
            
            morador = Morador.buscar_por_cpf(cpf)
            if morador and morador.verificar_senha(senha):
                self.__usuario_logado = morador
                return morador
            
            return None
        return None

    def gerenciar_administradores(self):
        self.__controlador_administrador.abre_tela()

    @staticmethod
    def encerra_sistema():
        exit(0)

    def abre_tela(self):
        if not self.__usuario_logado:
            self.fazer_login()
        else:
            if isinstance(self.__usuario_logado, Administrador):
                self.abre_painel_administrador()
            else:
                self.abre_painel_morador()

    def abre_painel_administrador(self):
        lista_opcoes = {
            1: self.gerenciar_administradores,
            2: self.gerenciar_moradores,
            3: self.gerenciar_republica,
            4: self.gerenciar_contratos,
            5: self.gerenciar_dividas,
            6: self.gerenciar_pagamentos,
            7: self.gerenciar_ocorrencias,
            8: self.gerenciar_alertas,
            9: self.gerenciar_quartos,
            10: self.gerenciar_recorrencias,
            0: self.encerra_sistema
        }
        
        for key, func in lista_opcoes.items():
            print(f"{key}: {func.__doc__}")

    def gerenciar_contratos(self):
        self.__controlador_contrato.abre_tela()

    def gerenciar_moradores(self):
        self.__controlador_morador.abre_tela()

    def gerenciar_republica(self):
        self.__controlador_republica.abre_tela()

    def gerenciar_dividas(self):
        self.__controlador_divida.abre_tela()

    def gerenciar_pagamentos(self):
        self.__controlador_pagamento.abre_tela()

    def gerenciar_ocorrencias(self):
        self.__controlador_ocorrencia.abre_tela()

    def gerenciar_alertas(self):
        self.__controlador_alerta.abre_tela()

    def gerenciar_quartos(self):
        self.__controlador_quarto.abre_tela()

    def gerenciar_recorrencias(self):
        self.__controlador_recorrencia.abre_tela()

    def salvar_todos_os_dados(self):
        pass