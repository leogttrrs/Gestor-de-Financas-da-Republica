from .abstract_controlador import AbstractControlador

class ControladorContrato(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)

    def abre_tela(self):
        pass
