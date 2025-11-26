from tkinter import messagebox

from .abstract_controlador import AbstractControlador
from src.models.Morador import Morador
from typing import List, Optional, Tuple
from src.models.Contrato import Contrato
from ..views.tela_morador import TelaMoradores


class ControladorMorador(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self.tela_moradores = None
    
    def abre_tela(self, parent_view=None):
        self.moradores = Morador.buscar_com_contrato_ativo()

        self.tela_moradores = TelaMoradores(
                parent_view.content_frame,
                self._controlador_sistema,
                self
            )

        self.tela_moradores.atualizar_lista()

        self._controlador_sistema.tela_atual = self.tela_moradores
        self.tela_moradores.mostrar()
        

    def buscar_morador_por_id(self, morador_id: int) -> Optional['Morador']:
        return Morador.buscar_por_id(morador_id)
    
    def atualizar_lista_moradores(self):
        moradores = Morador.buscar_todos()
        if self.tela_moradores:
            self.tela_moradores.atualizar_tabela(moradores)

    def excluir_morador(self, morador_id):
        # 1. Verifica contrato ativo
        if Morador.tem_contrato_ativo(morador_id):
            messagebox.showwarning(
                "Ação Negada",
                "Não é possível excluir este morador pois ele possui um CONTRATO ATIVO.\n\n"
                "Encerre o contrato antes de tentar excluir."
            )
            return

        # 2. Confirmação
        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este morador permanentemente?"):
            if Morador.excluir(morador_id):
                messagebox.showinfo("Sucesso", "Morador excluído com sucesso.")
                # Atualiza a tela se ela estiver aberta
                if self.tela_moradores:
                    self.tela_moradores.atualizar_lista()
            else:
                messagebox.showerror("Erro", "Erro ao excluir morador.")

    def atualizar_morador_existente(self, morador_id, dados_novos):
        try:
            morador = Morador.buscar_por_id(morador_id)
            if not morador:
                messagebox.showerror("Erro", "Morador não encontrado.")
                return False

            morador.nome = dados_novos['nome']
            morador.email = dados_novos['email']
            morador.telefone = dados_novos['telefone']

            sucesso, mensagem = morador.atualizar()

            if sucesso:
                messagebox.showinfo("Sucesso", "Dados atualizados!")
                if self.tela_moradores:
                    self.tela_moradores.atualizar_lista()
                return True
            else:
                messagebox.showerror("Erro", mensagem)
                return False

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")
            return False

    def listar_todos_detalhado(self) -> List[dict]:
        try:
            usuario_logado = self._controlador_sistema.usuario_logado

            if usuario_logado and usuario_logado.tipo_usuario == 'administrador':
                todos_moradores = Morador.buscar_todos()
            else:
                todos_moradores = Morador.buscar_com_contrato_ativo()

            if not todos_moradores:
                return []

            lista_formatada = []

            contratos_ativos = Contrato.buscar_ativos() or []
            mapa_contratos = {c.morador_id: c for c in contratos_ativos}

            for m in todos_moradores:
                contrato = mapa_contratos.get(m.id)
                quarto_num = contrato.quarto.numero_quarto if contrato and contrato.quarto else "-"

                if usuario_logado.tipo_usuario == 'administrador' or quarto_num != "-":
                    lista_formatada.append({
                        'id': m.id,
                        'nome': m.nome,
                        'email': m.email,
                        'telefone': m.telefone,
                        'cpf': m.cpf,
                        'quarto_numero': quarto_num
                    })

            return lista_formatada

        except Exception as e:
            print(f"Erro ao listar detalhado: {e}")
            return []

    def listar_moradores_nao_alocados(self) -> List[dict]:
        try:
            moradores = Morador.buscar_nao_alocados()
            return [{'id': m.id, 'nome': m.nome, 'cpf': m.cpf} for m in moradores]
        except Exception as e:
            print(f"Erro ao listar moradores não alocados: {e}")
            return []

    def cadastrar_morador(self, dados: dict):
        from src.utils.validador import Validador
        
        cpf = dados["cpf"]

        if Morador.buscar_por_cpf(cpf):
            return False, "Já existe um morador cadastrado com este CPF."
        
        # Validar senha antes de criar o morador
        valida_senha, mensagem_senha = Validador.validar_senha(dados["senha"])
        if not valida_senha:
            return False, mensagem_senha

        novo = Morador(
            cpf=dados["cpf"],
            nome=dados["nome"],
            email=dados["email"],
            telefone=dados["telefone"],
            senhaCriptografada=dados["senha"]
        )

        novo.salvar()
        return True, "Morador cadastrado com sucesso!"

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
