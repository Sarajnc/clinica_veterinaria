from estruturas.lista import ListaEncadeada
from servicos.cadastro import Cadastro
from servicos.atendimento import GerenciadorAtendimentos
from servicos.estoque import GerenciadorEstoque
from modelos.prontuario import Prontuario
from modelos.item_prontuario import ItemProntuario
from modelos.pagamento import Pagamento
from datetime import date

class Clinica:
    def __init__(self, quantidade_consultorios):
        self.cadastro = Cadastro()
        self.atendimentos = GerenciadorAtendimentos()
        self.estoque = GerenciadorEstoque()

        self.quantidade_consultorios = quantidade_consultorios
        self.consultorios_ocupados = 0

        self.pagamentos = ListaEncadeada()
        self.atendimentos_em_andamento = ListaEncadeada()
        self.prontuarios = ListaEncadeada()

        self.proximo_numero_prontuario = 1

    def receber_atendimento(self, atendimento):
        self.atendimentos.adicionar_atendimento(atendimento)
        atendimento.status = "Aguardando"
        return True

    def chamar_proximo_animal(self, veterinario):
        if self.consultorios_ocupados >= self.quantidade_consultorios:
            return None

        atendimento = self.atendimentos.proximo_atendimento()

        if atendimento is None:
            return None

        prontuario = Prontuario(
            self.proximo_numero_prontuario,
            atendimento.animal.nome,
            atendimento.animal.tutor.nome,
            veterinario
        )

        atendimento.prontuario = prontuario
        atendimento.status = "Em andamento"

        self.prontuarios.adicionar(prontuario)
        self.atendimentos_em_andamento.adicionar(atendimento)

        self.proximo_numero_prontuario += 1
        self.consultorios_ocupados += 1

        return atendimento

    def finalizar_atendimento(self, atendimento, forma_pagamento, parcelas=1):
        if not self.atendimentos_em_andamento.contem(atendimento):
            return False

        prontuario = atendimento.prontuario

        if prontuario is None or prontuario.status != "Aberto":
            return False

        if forma_pagamento not in ("PIX", "Cartão", "Dinheiro"):
            return False

        if parcelas < 1:
            return False

        if forma_pagamento != "Cartão" and parcelas != 1:
            return False

        valor_medicamentos = self.calcular_valor_itens(
            prontuario.medicamentos
        )

        valor_procedimentos = self.calcular_valor_itens(
            prontuario.procedimentos
        )

        # Verifica se existe estoque suficiente antes de retirar.
        atual = prontuario.medicamentos.inicio

        while atual is not None:
            item = atual.dado

            if item.produto is None:
                return False

            self.estoque.descartar_vencidos(
                item.produto.codigo, date.today()
            )

            total_necessario = 0
            outro = prontuario.medicamentos.inicio

            while outro is not None:
                if outro.dado.produto is item.produto:
                    total_necessario += outro.dado.quantidade

                outro = outro.proximo

            if item.produto.quantidade_em_estoque() < total_necessario:
                return False

            atual = atual.proximo

        # Retira os medicamentos do estoque.
        atual = prontuario.medicamentos.inicio

        while atual is not None:
            item = atual.dado

            if not self.estoque.retirar_estoque(
                item.produto.codigo, item.quantidade
            ):
                return False

            atual = atual.proximo

        pagamento = Pagamento(
            atendimento.animal.tutor.nome,
            prontuario,
            forma_pagamento,
            valor_medicamentos,
            valor_procedimentos,
            parcelas
        )

        if not pagamento.confirmar_pagamento():
            return False

        if not prontuario.registrar_alta():
            return False

        if not prontuario.fechar_prontuario():
            return False

        self.pagamentos.adicionar(pagamento)
        self.atendimentos_em_andamento.remover(atendimento)

        atendimento.status = "Finalizado"
        self.consultorios_ocupados -= 1

        return True

    def adicionar_medicamento(self, atendimento, codigo, quantidade):
        if not self.atendimentos_em_andamento.contem(atendimento):
            return False

        produto = self.estoque.buscar_produto(codigo)

        if produto is None or quantidade <= 0:
            return False

        self.estoque.descartar_vencidos(codigo, date.today())

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

    def calcular_valor_itens(self, itens):
        total = 0
        atual = itens.inicio

        while atual is not None:
            total += atual.dado.calcular_valor()
            atual = atual.proximo

        return total