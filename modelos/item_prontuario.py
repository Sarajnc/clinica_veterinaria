class ItemProntuario:
    def __init__(self, nome, quantidade, valor_unitario, produto=None):
        self.nome = nome
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.produto = produto

    def calcular_valor(self):
        return self.quantidade * self.valor_unitario