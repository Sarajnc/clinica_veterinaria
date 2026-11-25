class Perda:
    def __init__(self, produto, lote, quantidade, data_descarte):
        self.produto = produto
        self.lote = lote
        self.quantidade = quantidade
        self.data_descarte = data_descarte

    @staticmethod
    def descartar_lotes_vencidos(produto, data_atual):
        quantidade_lotes = produto.lotes.tamanho()

        for i in range(quantidade_lotes):
            lote = produto.lotes.desenfileirar()

            if lote.data_validade < data_atual:
                perda = Perda(
                    produto,
                    lote,
                    lote.quantidade,
                    data_atual
                )

                produto.perdas.adicionar(perda)

            else:
                produto.lotes.enfileirar(lote)