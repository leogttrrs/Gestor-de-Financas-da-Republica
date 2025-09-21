from abc import ABC, abstractmethod


class AbstractControlador(ABC):
    @abstractmethod
    def __init__(self, controlador_sistema) -> None:
        self._controlador_sistema = controlador_sistema

    def retornar(self):
        self._controlador_sistema.abre_tela()

    @abstractmethod
    def abre_tela(self):
        pass
