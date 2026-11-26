from estruturas.lista import ListaEncadeada

class Produto:
    def __init__(self, nome, codigo, preco_venda, quantidade_minima):
        self.nome = nome
        self.codigo = codigo
        self.preco_venda = preco_venda
        self.quantidade_minima = quantidade_minima

        self.lotes = ListaEncadeada()
        self.perdas = ListaEncadeada()

    def adicionar_lote(self, lote):
        self.lotes.adicionar(lote)
        return True

    def quantidade_em_estoque(self):
        total = 0
        atual = self.lotes.inicio

        while atual is not None:
            total += atual.dado.quantidade
            atual = atual.proximo

        return total

    def estoque_minimo(self):
        return self.quantidade_em_estoque() < self.quantidade_minima

    def retirar_estoque(self, quantidade):
        if quantidade <= 0 or self.quantidade_em_estoque() < quantidade:
            return False

        restante = quantidade
        atual = self.lotes.inicio

        while atual is not None and restante > 0:
            lote = atual.dado
            proximo = atual.proximo

            if lote.quantidade <= restante:
                restante -= lote.quantidade
                self.lotes.remover(lote)
            else:
                lote.quantidade -= restante
                restante = 0

            atual = proximo

        return True