from .abstract_controlador import AbstractControlador
from src.models.Morador import Morador
from src.utils.validador import Validador
from typing import Tuple, Optional
from tkinter import messagebox


class ControladorMorador(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
    
    def abre_tela(self):
        pass

    # morador pode cadastrar morador? ou adm chama esse método de morador?
    def cadastrar_morador(self, cpf: str, nome: str, email: str, telefone: str, genero: str, senha: str) -> Tuple[bool, str]:
        try:
            if Morador.existe_algum():
                return False, "Já existe um morador no sistema. Não é possível criar outro."

            valido, mensagem = Validador.validar_dados_usuario(cpf, nome, email, telefone, genero)
            if not valido:
                return False, mensagem
            
            senha_valida, msg_senha = Validador.validar_senha(senha)
            if not senha_valida:
                return False, msg_senha
            
            senha_hash = Validador.hash_senha(senha)

            morador_para_salvar = Morador(cpf=cpf, nome=nome, email=email, telefone=telefone,
                                              genero=genero, senhaCriptografada=senha_hash)
            sucesso, mensagem = morador_para_salvar.salvar()

            if sucesso:
                try:
                    if not morador_para_salvar.id:
                        return False, "Erro crítico: O ID do morador não foi definido após salvar."

                except Exception as e_rep:
                    return False, f"Morador criado, mas falha ao criar república: {str(e_rep)}"
            else:
                return False, mensagem
                
        except Exception as e:
            return False, f"Erro ao cadastrar morador: {str(e)}"
        
    def buscar_morador_por_cpf(self, cpf: str) -> Optional[Morador]:
        try:
            return Morador.buscar_por_cpf(cpf)
        except Exception:
            return None
        
    def buscar_morador_por_id(self, morador_id: int) -> Optional[Morador]:
        try:
            return Morador.buscar_por_id(morador_id)
        except Exception:
            return None
        
    def editar_morador(self, morador_id: int, cpf: str, nome: str, email: str, telefone: str, genero: str, senha: str = None) -> Tuple[bool, str]:
        try:
            morador = self.buscar_morador_por_id(morador_id)
            if not morador:
                return False, "Morador não encontrado"
            
            valido, mensagem = Validador.validar_dados_usuario(cpf, nome, email, telefone, genero)
            if not valido:
                return False, mensagem
            
            morador.cpf = cpf
            morador.nome = nome
            morador.email = email
            morador.telefone = telefone
            morador.genero = genero
            
            if senha:
                senha_valida, msg_senha = Validador.validar_senha(senha)
                if not senha_valida:
                    return False, msg_senha
                morador.senhaCriptografada = Validador.hash_senha(senha)
            
            sucesso, mensagem = morador.atualizar()
            if sucesso:
                return True, "Morador atualizado com sucesso"
            else:
                return False, f"Erro ao atualizar morador: {mensagem}"
                
        except Exception as e:
            return False, f"Erro ao editar morador: {str(e)}"

    def excluir_morador(self, cpf: str) -> Tuple[bool, str]:
        try:
            morador = self.buscar_morador_por_cpf(cpf)
            if not morador:
                return False, "Morador não encontrado"
            
            sucesso, mensagem = morador.excluir()
            if sucesso:
                return True, "Morador excluído com sucesso"
            else:
                return False, f"Erro ao excluir morador: {mensagem}"
                
        except Exception as e:
            return False, f"Erro ao excluir morador: {str(e)}"
        

    def abrir_tela_mudar_senha(self, tela_perfil):
        from tkinter import messagebox
        messagebox.showinfo("Em desenvolvimento", "Funcionalidade de mudar senha em desenvolvimento.")

    # revisar
    def excluir_perfil_morador(self, tela_perfil):
        from tkinter import messagebox
        
        resposta = messagebox.askyesno(
            "Confirmar Exclusão", 
            "ATENÇÃO!\n\n"
            "Esta ação irá:\n"
            "• Excluir o perfil de morador\n"
            "• Esta ação é IRREVERSÍVEL!\n\n"
            "Tem certeza que deseja continuar?",
            icon='warning'
        )

        if not resposta:
            return
            
        # refazer para mostrar o nome do morador a ser excluido ou lógica semelhante
        try:
            usuario_logado = self._controlador_sistema.usuario_logado
            if not usuario_logado:
                tela_perfil.mostrar_mensagem_erro("Usuário não está logado")
                return
            
            morador = Morador.buscar_por_cpf(usuario_logado.cpf)
            if not morador:
                tela_perfil.mostrar_mensagem_erro("Morador não encontrado")
                return
            
            sucesso, mensagem = morador.excluir()
            
            if sucesso:
                messagebox.showinfo("Perfil Excluído", "Perfil excluído com sucesso.")
            
            else:
                tela_perfil.mostrar_mensagem_erro(f"Erro ao excluir perfil: {mensagem}")
                
        except Exception as e:
            tela_perfil.mostrar_mensagem_erro(f"Erro inesperado ao excluir perfil: {str(e)}")

    def abrir_tela_perfil(self, tela_perfil):
        if self._controlador_sistema.usuario_logado:
            dados_usuario = {
                'nome': self._controlador_sistema.usuario_logado.nome,
                'cpf': self._controlador_sistema.usuario_logado.cpf,
                'email': self._controlador_sistema.usuario_logado.email,
                'telefone': self._controlador_sistema.usuario_logado.telefone
            }
            tela_perfil._limpar_conteudo()
            tela_perfil.mostrar_formulario_perfil_morador(dados_usuario)