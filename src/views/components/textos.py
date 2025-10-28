from tkinter import ttk


class TextosPadrao:
    @staticmethod
    def titulo_principal(parent, texto="Título", cor="#333333"):
        title_label = ttk.Label(parent, text=texto,
                               font=("Arial", 16, "bold"),
                               background="white",
                               foreground=cor)
        title_label.pack(pady=(0, 10))

        return title_label

    @staticmethod
    def subtitulo(parent, texto="Subtítulo", cor="gray"):
        subtitle_label = ttk.Label(parent, text=texto,
                                  font=("Arial", 11),
                                  foreground=cor,
                                  background="white")
        subtitle_label.pack(pady=(0, 30))

        return subtitle_label

    @staticmethod
    def link_azul(parent, texto="Link", comando=None, cor="#007bff"):
        link_label = ttk.Label(parent, text=texto,
                              font=("Arial", 10),
                              foreground=cor,
                              cursor="hand2",
                              background="white")
        link_label.pack()

        if comando:
            link_label.bind("<Button-1>", lambda e: comando())

        return link_label

    @staticmethod
    def texto_simples(parent, texto="Texto", fonte=("Arial", 10), cor="#333333", background="white"):
        text_label = ttk.Label(parent, text=texto,
                              font=fonte,
                              foreground=cor,
                              background=background)
        text_label.pack()

        return text_label

    @staticmethod
    def label_campo(parent, texto="Campo:", cor="#333333"):
        label_widget = ttk.Label(parent, text=texto,
                                font=("Arial", 10),
                                background="white",
                                foreground=cor)
        label_widget.pack(anchor="w", pady=(0, 5))

        return label_widget

    @staticmethod
    def titulo_secao(parent, texto="Seção", cor="#333333"):
        title_label = ttk.Label(parent, text=texto,
                               font=("Arial", 16, "bold"),
                               background="white",
                               foreground=cor)
        title_label.pack(pady=(10, 5))

        return title_label

    @staticmethod
    def texto_erro(parent, texto="Erro", cor="#dc3545"):
        error_label = ttk.Label(parent, text=texto,
                               font=("Arial", 9),
                               foreground=cor,
                               background="white")
        error_label.pack(pady=(5, 0))

        return error_label

    @staticmethod
    def texto_sucesso(parent, texto="Sucesso", cor="#28a745"):
        success_label = ttk.Label(parent, text=texto,
                                 font=("Arial", 9),
                                 foreground=cor,
                                 background="white")
        success_label.pack(pady=(5, 0))

        return success_label
