from datetime import date

class Perda:
    def __init__(self, produto, lote, quantidade, data_descarte):
        self.produto = produto
        self.lote = lote
        self.quantidade = quantidade
        self.data_descarte = data_descarte

    @staticmethod
    def descartar_lotes_vencidos(produto, data_atual):
        atual = produto.lotes.inicio

        while atual is not None:
            lote = atual.dado
            proximo = atual.proximo

            if lote.data_validade < data_atual:
                perda = Perda(
                    produto,
                    lote,
                    lote.quantidade,
                    data_atual
                )

                produto.perdas.adicionar(perda)
                produto.lotes.remover(lote)

            atual = proximo