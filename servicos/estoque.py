from estruturas.lista import ListaEncadeada
from modelos.perda import Perda

class GerenciadorEstoque:
    def __init__(self):
        self.produtos = ListaEncadeada()

    def cadastrar_produto(self, produto):
        if self.buscar_produto(produto.codigo):
            return False

        self.produtos.adicionar(produto)
        return True

    def buscar_produto(self, codigo):
        return self.produtos.buscar_por(
            lambda produto: produto.codigo == codigo
        )

    def adicionar_lote(self, codigo, lote):
        produto = self.buscar_produto(codigo)

        if produto is None:
            return False

        lote.produto = produto
        produto.adicionar_lote(lote)
        return True

    def retirar_estoque(self, codigo, quantidade):
        produto = self.buscar_produto(codigo)

        if produto is None:
            return False

        return produto.retirar_estoque(quantidade)

    def ajustar_quantidade(self, codigo, lote, nova_quantidade):
        produto = self.buscar_produto(codigo)

        if produto is None or nova_quantidade < 0:
            return False

        if not produto.lotes.contem(lote):
            return False

        lote.quantidade = nova_quantidade
        return True

    def descartar_vencidos(self, codigo, data_atual):
        produto = self.buscar_produto(codigo)

        if produto is None:
            return False

        Perda.descartar_lotes_vencidos(produto, data_atual)
        return True

    def verificar_estoque_minimo(self, codigo):
        produto = self.buscar_produto(codigo)

        if produto is None:
            return None

        return produto.estoque_minimo()