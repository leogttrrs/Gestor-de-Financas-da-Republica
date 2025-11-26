from .abstract_controlador import AbstractControlador
from src.models.Administrador import Administrador
from src.models.Republica import Republica
from typing import Tuple, Optional
from tkinter import messagebox


class ControladorAdministrador(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)

    def cadastrar_administrador(self, cpf: str, nome: str, email: str, telefone: str, senha: str) -> Tuple[bool, str]:
        try:
            from src.utils.validador import Validador
            
            if Administrador.existe_algum(tipo_usuario='administrador'):
                return False, "Já existe um administrador no sistema. Não é possível criar outro."
            
            # Validar senha antes de criar o administrador
            valida_senha, mensagem_senha = Validador.validar_senha(senha)
            if not valida_senha:
                return False, mensagem_senha
            
            admin_para_salvar = Administrador(cpf=cpf, nome=nome, email=email, telefone=telefone,
                                              senhaCriptografada=None)

            admin_para_salvar.senhaCriptografada = admin_para_salvar.hash_senha(senha)

            valido, mensagem = admin_para_salvar.validar_dados()
            if not valido:
                return False, mensagem

            sucesso, mensagem = Administrador.salvar_usuario(admin_para_salvar)

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
            from src.utils.validador import Validador
            
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
                # Validar senha antes de atualizar
                valida_senha, mensagem_senha = Validador.validar_senha(senha)
                if not valida_senha:
                    return False, mensagem_senha
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
        tela_perfil._limpar_conteudo()
        tela_perfil.mostrar_formulario_mudar_senha()

    def excluir_perfil_admin(self, tela_perfil):
        resposta = messagebox.askyesno(
            "⚠️ RESETAR SISTEMA INTEIRO",
            "ATENÇÃO MUITO CUIDADO!\n\n"
            "Esta ação irá:\n"
            "• Excluir seu perfil de administrador\n"
            "• Apagar TODOS os dados (Moradores, Contratos, Dívidas, Alertas)\n"
            "• O sistema voltará ao estado inicial (zero)\n\n"
            "Tem certeza absoluta que deseja continuar?",
            icon='warning'
        )

        if not resposta:
            return

        try:
            usuario_logado = self._controlador_sistema.usuario_logado
            if not usuario_logado:
                tela_perfil.mostrar_mensagem_erro("Usuário não está logado")
                return
            sucesso = Administrador.limpar_banco_dados()

            if sucesso:
                messagebox.showinfo("Sistema Resetado",
                                    "Todos os dados foram excluídos com sucesso.\nO sistema será reiniciado.")

                self._controlador_sistema.usuario_logado = None
                if hasattr(tela_perfil, 'on_logout') and tela_perfil.on_logout:
                    tela_perfil.on_logout()
            else:
                tela_perfil.mostrar_mensagem_erro("Ocorreu um erro técnico ao tentar limpar o banco de dados.")

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

    def alterar_senha(self, tela_perfil, senha_atual, senha_nova, confirmar_senha):
        try:
            usuario_logado = self._controlador_sistema.usuario_logado
            if not usuario_logado:
                tela_perfil.mostrar_mensagem_erro("Usuário não está logado")
                return
            
            if not senha_atual or not senha_nova or not confirmar_senha:
                tela_perfil.mostrar_mensagem_erro("Todos os campos são obrigatórios")
                return
            
            if senha_nova != confirmar_senha:
                tela_perfil.mostrar_mensagem_erro("A nova senha e a confirmação não coincidem")
                return
            
            if len(senha_nova) < 6:
                tela_perfil.mostrar_mensagem_erro("A nova senha deve ter pelo menos 6 caracteres")
                return
            
            admin = Administrador.buscar_por_cpf(usuario_logado.cpf)
            if not admin:
                tela_perfil.mostrar_mensagem_erro("Administrador não encontrado")
                return
            
            if not admin.verificar_senha(senha_atual):
                tela_perfil.mostrar_mensagem_erro("Senha atual incorreta")
                return
            
            sucesso, mensagem = Administrador.alterar_senha(usuario_logado.cpf, senha_nova)
            
            if sucesso:
                tela_perfil.mostrar_mensagem_sucesso("Senha alterada com sucesso!")
                self.abrir_tela_perfil(tela_perfil)
            else:
                tela_perfil.mostrar_mensagem_erro(f"Erro ao alterar senha: {mensagem}")
                
        except Exception as e:
            tela_perfil.mostrar_mensagem_erro(f"Erro ao alterar senha: {str(e)}")