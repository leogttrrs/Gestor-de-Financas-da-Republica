import tkinter as tk
from tkinter import ttk


class EstilosApp:    
    @staticmethod
    def configurar_estilos():
        style = ttk.Style()
        
        style.theme_use('clam')
        
        cores = {
            'primary': '#007bff',
            'primary_hover': '#0056b3',
            'success': '#28a745',
            'danger': '#dc3545',
            'light': '#f8f9fa',
            'dark': '#343a40',
            'white': '#ffffff',
            'gray': '#6c757d'
        }
        
        style.configure(
            'Primary.TButton',
            background=cores['primary'],
            foreground=cores['white'],
            font=('Arial', 12, 'bold'),
            padding=(20, 10),
            relief='flat'
        )
        
        style.map(
            'Primary.TButton',
            background=[('active', cores['primary_hover'])],
            relief=[('pressed', 'flat'), ('!pressed', 'flat')]
        )
        
        style.configure(
            'Custom.TEntry',
            fieldbackground=cores['white'],
            borderwidth=1,
            relief='solid',
            padding=10,
            font=('Arial', 12)
        )
        
        style.configure(
            'Card.TFrame',
            background=cores['white'],
            relief='raised',
            borderwidth=1
        )
        
        style.configure(
            'Title.TLabel',
            background=cores['white'],
            font=('Arial', 24, 'bold'),
            foreground=cores['dark']
        )
        
        style.configure(
            'Subtitle.TLabel',
            background=cores['white'],
            font=('Arial', 11),
            foreground=cores['gray']
        )
        
        style.configure(
            'Link.TLabel',
            background=cores['white'],
            font=('Arial', 10),
            foreground=cores['primary'],
            cursor='hand2'
        )
        
        return style, cores


class UtilsInterface:
    @staticmethod
    def centralizar_janela(janela, largura, altura):
        janela.update_idletasks()
        
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        
        x = (screen_width // 2) - (largura // 2)
        y = (screen_height // 2) - (altura // 2)
        
        janela.geometry(f'{largura}x{altura}+{x}+{y}')
    
    @staticmethod
    def criar_campo_com_placeholder(parent, placeholder, show=None, font=('Arial', 12)):
        container = ttk.Frame(parent)
        container.pack(fill='x', pady=(0, 15))
        
        var = tk.StringVar()
        
        entry = ttk.Entry(container, textvariable=var, font=font, style='Custom.TEntry')
        if show:
            entry.configure(show=show)
        entry.pack(fill='x', ipady=8)
        
        placeholder_label = ttk.Label(container, text=placeholder, 
                                    font=(font[0], font[1]-2), foreground='gray')
        placeholder_label.place(in_=entry, x=10, y=0, anchor='w')
        
        placeholder_ativo = True
        
        def on_focus_in(event):
            nonlocal placeholder_ativo
            if placeholder_ativo:
                placeholder_label.place_forget()
                placeholder_ativo = False
                if show:
                    entry.configure(show=show)
        
        def on_focus_out(event):
            nonlocal placeholder_ativo
            if not var.get():
                placeholder_label.place(in_=entry, x=10, y=0, anchor='w')
                placeholder_ativo = True
                if show:
                    entry.configure(show='')
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        if show:
            entry.configure(show='')
        
        return entry, var, container
    
    @staticmethod
    def criar_botao_primario(parent, texto, comando, **kwargs):
        btn = ttk.Button(parent, text=texto, command=comando, style='Primary.TButton', **kwargs)
        return btn
    
    @staticmethod
    def aplicar_efeito_hover(widget, cor_normal, cor_hover):
        def on_enter(event):
            widget.configure(background=cor_hover)
        
        def on_leave(event):
            widget.configure(background=cor_normal)
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)