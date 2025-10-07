from .abstract_controlador import AbstractControlador
from src.models.Administrador import Administrador
from src.models.Republica import Republica
from typing import Tuple, Optional


class ControladorAdministrador(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)

    def cadastrar_administrador(self, cpf: str, nome: str, email: str, telefone: str, senha: str) -> Tuple[bool, str]:
        try:
            if Administrador.existe_algum():
                return False, "Já existe um administrador no sistema. Não é possível criar outro."
            admin_para_salvar = Administrador(cpf=cpf, nome=nome, email=email, telefone=telefone,
                                              senhaCriptografada=None)

            admin_para_salvar.senhaCriptografada = admin_para_salvar.hash_senha(senha)

            valido, mensagem = admin_para_salvar.validar_dados()
            if not valido:
                return False, mensagem

            sucesso, mensagem = admin_para_salvar.salvar()

            if sucesso:
                try:
                    if not admin_para_salvar.id:
                        return False, "Erro crítico: O ID do administrador não foi definido após salvar."

                    nova_republica = Republica(
                        nome=f"República de {admin_para_salvar.nome}",
                        administrador_id=admin_para_salvar.id
                    )
                    nova_republica.salvar()
                    return True, "Administrador e República criados com sucesso!"
                except Exception as e_rep:
                    return False, f"Admin criado, mas falha ao criar república: {str(e_rep)}"
            else:
                return False, mensagem
                
        except Exception as e:
            return False, f"Erro ao cadastrar administrador: {str(e)}"

    def buscar_administrador_por_cpf(self, cpf: str) -> Optional[Administrador]:
        try:
            return Administrador.buscar_por_cpf(cpf)
        except Exception:
            return None

    def buscar_administrador_por_id(self, admin_id: int) -> Optional[Administrador]:
        try:
            return Administrador.buscar_por_id(admin_id)
        except Exception:
            return None

    def editar_administrador(self, admin_id: int, cpf: str, nome: str, email: str, telefone: str, senha: str = None) -> Tuple[bool, str]:
        try:
            admin = self.buscar_administrador_por_id(admin_id)
            if not admin:
                return False, "Administrador não encontrado"
            
            admin.cpf = cpf
            admin.nome = nome
            admin.email = email
            admin.telefone = telefone
            
            valido, mensagem = admin.validar_dados()
            if not valido:
                return False, mensagem
            
            if senha:
                admin.senhaCriptografada = admin.hash_senha(senha)
            
            sucesso, mensagem = admin.atualizar()
            if sucesso:
                return True, "Administrador atualizado com sucesso"
            else:
                return False, f"Erro ao atualizar administrador: {mensagem}"
                
        except Exception as e:
            return False, f"Erro ao editar administrador: {str(e)}"

    def excluir_administrador(self, cpf: str) -> Tuple[bool, str]:
        try:
            admin = self.buscar_administrador_por_cpf(cpf)
            if not admin:
                return False, "Administrador não encontrado"
            
            sucesso, mensagem = admin.excluir()
            if sucesso:
                return True, "Administrador excluído com sucesso"
            else:
                return False, f"Erro ao excluir administrador: {mensagem}"
                
        except Exception as e:
            return False, f"Erro ao excluir administrador: {str(e)}"

    def abre_tela(self):
        pass

    def abrir_tela_perfil(self, tela_perfil):
        if self._controlador_sistema.usuario_logado:
            dados_usuario = {
                'nome': self._controlador_sistema.usuario_logado.nome,
                'cpf': self._controlador_sistema.usuario_logado.cpf,
                'email': self._controlador_sistema.usuario_logado.email,
                'telefone': self._controlador_sistema.usuario_logado.telefone
            }
            tela_perfil._limpar_conteudo()
            tela_perfil.mostrar_formulario_perfil_admin(dados_usuario)

    def abrir_tela_mudar_senha(self, tela_perfil):
        from tkinter import messagebox
        messagebox.showinfo("Em desenvolvimento", "Funcionalidade de mudar senha em desenvolvimento.")

    def excluir_perfil_admin(self, tela_perfil):
        from tkinter import messagebox
        
        resposta = messagebox.askyesno(
            "Confirmar Exclusão", 
            "ATENÇÃO!\n\n"
            "Esta ação irá:\n"
            "• Excluir seu perfil de administrador\n"
            "• Apagar TODOS os dados da república\n"
            "• Remover todos os moradores, quartos e contratos\n"
            "• Esta ação é IRREVERSÍVEL!\n\n"
            "Tem certeza que deseja continuar?",
            icon='warning'
        )

        if not resposta:
            return
            
        try:
            usuario_logado = self._controlador_sistema.usuario_logado
            if not usuario_logado:
                tela_perfil.mostrar_mensagem_erro("Usuário não está logado")
                return
            
            admin = Administrador.buscar_por_cpf(usuario_logado.cpf)
            if not admin:
                tela_perfil.mostrar_mensagem_erro("Administrador não encontrado")
                return
            
            sucesso, mensagem = admin.excluir()
            
            if sucesso:
                messagebox.showinfo("Perfil Excluído", "Perfil excluído com sucesso. Retornando ao login...")
                self._controlador_sistema.usuario_logado = None
                if hasattr(tela_perfil, 'on_logout') and tela_perfil.on_logout:
                    tela_perfil.on_logout()
            else:
                tela_perfil.mostrar_mensagem_erro(f"Erro ao excluir perfil: {mensagem}")
                
        except Exception as e:
            tela_perfil.mostrar_mensagem_erro(f"Erro inesperado ao excluir perfil: {str(e)}")

    def atualizar_perfil(self, tela_perfil, dados):
        try:
            usuario_logado = self._controlador_sistema.usuario_logado
            if not usuario_logado:
                tela_perfil.mostrar_mensagem_erro("Usuário não está logado")
                return
            
            admin = Administrador.buscar_por_cpf(usuario_logado.cpf)
            if admin:
                admin.nome = dados['nome']
                admin.email = dados['email']
                admin.telefone = dados['telefone']
                
                valido, mensagem = admin.validar_dados()
                if not valido:
                    tela_perfil.mostrar_mensagem_erro(mensagem)
                    return
                
                sucesso, mensagem = admin.atualizar()
                if sucesso:
                    usuario_logado.nome = dados['nome']
                    usuario_logado.email = dados['email']
                    usuario_logado.telefone = dados['telefone']
                    
                    tela_perfil.mostrar_mensagem_sucesso("Perfil atualizado com sucesso!")
                    self.abrir_tela_perfil(tela_perfil)
                else:
                    tela_perfil.mostrar_mensagem_erro(f"Erro ao atualizar perfil: {mensagem}")
            else:
                tela_perfil.mostrar_mensagem_erro("Administrador não encontrado")
                
        except Exception as e:
            tela_perfil.mostrar_mensagem_erro(f"Erro ao atualizar perfil: {str(e)}")