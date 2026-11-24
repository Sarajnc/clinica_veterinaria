from estruturas.lista import ListaEncadeada

class Produto:
    def __init__(self, nome, codigo, preco_venda, quantidade_minima):
        self.nome = nome
        self.codigo = codigo
        self.preco_venda = preco_venda
        self.quantidade_minima = quantidade_minima
        self.lotes = ListaEncadeada()

    def adicionar_lote(self, lote):
        self.lotes.adicionar(lote)

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
        
          