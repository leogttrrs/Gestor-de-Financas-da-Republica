from .abstract_controlador import AbstractControlador
from src.models.Morador import Morador
from typing import List, Optional, Tuple

class ControladorMorador(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
    
    def abre_tela(self, parent_view=None):
        pass

    def buscar_morador_por_id(self, morador_id: int) -> Optional['Morador']:
        return Morador.buscar_por_id(morador_id)

    def listar_moradores_nao_alocados(self) -> List[dict]:
        try:
            moradores = Morador.buscar_nao_alocados()
            return [{'id': m.id, 'nome': m.nome, 'cpf': m.cpf} for m in moradores]
        except Exception as e:
            print(f"Erro ao listar moradores não alocados: {e}")
            return []

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

    def abrir_tela_mudar_senha(self, tela_perfil):
        tela_perfil._limpar_conteudo()
        tela_perfil.mostrar_formulario_mudar_senha()

    def atualizar_perfil(self, tela_perfil, dados):
        try:
            usuario_logado = self._controlador_sistema.usuario_logado
            if not usuario_logado:
                tela_perfil.mostrar_mensagem_erro("Usuário não está logado")
                return
            
            morador = Morador.buscar_por_cpf(usuario_logado.cpf)
            if morador:
                morador.nome = dados['nome']
                morador.email = dados['email']
                morador.telefone = dados['telefone']
                
                valido, mensagem = morador.validar_dados()
                if not valido:
                    tela_perfil.mostrar_mensagem_erro(mensagem)
                    return
                
                sucesso, mensagem = morador.atualizar()
                if sucesso:
                    usuario_logado.nome = dados['nome']
                    usuario_logado.email = dados['email']
                    usuario_logado.telefone = dados['telefone']
                    
                    tela_perfil.mostrar_mensagem_sucesso("Perfil atualizado com sucesso!")
                    self.abrir_tela_perfil(tela_perfil)
                else:
                    tela_perfil.mostrar_mensagem_erro(f"Erro ao atualizar perfil: {mensagem}")
            else:
                tela_perfil.mostrar_mensagem_erro("Morador não encontrado")
                
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
            
            morador = Morador.buscar_por_cpf(usuario_logado.cpf)
            if not morador:
                tela_perfil.mostrar_mensagem_erro("Morador não encontrado")
                return
            
            if not morador.verificar_senha(senha_atual):
                tela_perfil.mostrar_mensagem_erro("Senha atual incorreta")
                return
            
            sucesso, mensagem = Morador.alterar_senha(usuario_logado.cpf, senha_nova)
            
            if sucesso:
                tela_perfil.mostrar_mensagem_sucesso("Senha alterada com sucesso!")
                self.abrir_tela_perfil(tela_perfil)
            else:
                tela_perfil.mostrar_mensagem_erro(f"Erro ao alterar senha: {mensagem}")
                
        except Exception as e:
            tela_perfil.mostrar_mensagem_erro(f"Erro ao alterar senha: {str(e)}")


