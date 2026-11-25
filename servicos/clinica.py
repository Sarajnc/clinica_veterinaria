from estruturas.lista import ListaEncadeada
from servicos.cadastro import Cadastro
from servicos.atendimento import GerenciadorAtendimentos
from servicos.estoque import GerenciadorEstoque
from modelos.prontuario import Prontuario
from modelos.item_prontuario import ItemProntuario

class Clinica:
    def __init__(self, quantidade_consultorios):
        self.cadastro = Cadastro()
        self.atendimentos = GerenciadorAtendimentos()
        self.estoque = GerenciadorEstoque()

        self.quantidade_consultorios = quantidade_consultorios
        self.consultorios_ocupados = 0

        self.atendimentos_em_andamento = ListaEncadeada()
        self.prontuarios = ListaEncadeada()
        self.proximo_numero_prontuario = 1

    def receber_atendimento(self, atendimento):
        self.atendimentos.adicionar_atendimento(atendimento)
        return True

    def chamar_proximo_animal(self, veterinario):
        if self.consultorios_ocupados >= self.quantidade_consultorios:
            return None

        atendimento = self.atendimentos.proximo_atendimento()

        if atendimento is None:
            return None

        prontuario = Prontuario(
            self.proximo_numero_prontuario,
            atendimento.nome_animal,
            atendimento.nome_tutor,
            veterinario
        )

        atendimento.prontuario = prontuario

        self.prontuarios.adicionar(prontuario)
        self.atendimentos_em_andamento.adicionar(atendimento)

        self.proximo_numero_prontuario += 1
        self.consultorios_ocupados += 1

        return atendimento

    def liberar_consultorio(self, atendimento):
        if not self.atendimentos_em_andamento.remover(atendimento):
            return False

        self.consultorios_ocupados -= 1
        return True
    
    def finalizar_atendimento(self, atendimento):
        if not self.atendimentos_em_andamento.contem(atendimento):
            return False

        prontuario = atendimento.prontuario

        if prontuario is None:
            return False

        if not prontuario.registrar_alta():
            return False

        if not prontuario.fechar_prontuario():
            return False

        self.atendimentos_em_andamento.remover(atendimento)
        self.consultorios_ocupados -= 1

        return True
  
    def adicionar_medicamento(self, atendimento, codigo, quantidade):
        if not self.atendimentos_em_andamento.contem(atendimento):
            return False

        produto = self.estoque.buscar_produto(codigo)

        if produto is None or quantidade <= 0:
            return False

        if produto.quantidade_em_estoque() < quantidade:
            return False

        item = ItemProntuario(
            produto.nome,
            quantidade,
            produto.preco_venda,
            produto
        )

        return atendimento.prontuario.adicionar_item(
            item, "medicamento"
        )

    def adicionar_procedimento(self, atendimento, nome, valor):
        if not self.atendimentos_em_andamento.contem(atendimento):
            return False

        if valor < 0:
            return False

        item = ItemProntuario(nome, 1, valor)

        return atendimento.prontuario.adicionar_item(
            item, "procedimento"
        )