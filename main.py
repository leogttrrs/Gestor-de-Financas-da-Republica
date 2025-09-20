from controller.morador_controller import MoradorController
from view.morador_view import MoradorView

if __name__ == "__main__":
    view = None
    controller = MoradorController(view)
    view = MoradorView(controller)
    controller.view = view

    view.mainloop()
