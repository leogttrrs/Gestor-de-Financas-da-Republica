from tkinter import ttk


class IconesPadrao:
    @staticmethod
    def icone_casa(parent, tamanho=48):
        icon_frame = ttk.Frame(parent)
        icon_label = ttk.Label(icon_frame, text="🏠", font=("Arial", tamanho), background="white")
        icon_label.pack()
        icon_frame.pack(pady=(40, 20))
        return icon_frame, icon_label
