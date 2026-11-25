from estruturas.lista import No

class Pilha:
    def __init__(self):
        self.topo= None

    def empilhar(self, dado):
        novo_no = No(dado)

        novo_no.proximo = self.topo
        self.topo = novo_no

    def desempilhar(self):
        if self.esta_vazia():
            return None

        dado = self.topo.dado
        self.topo = self.topo.proximo

        return dado

    def consultar_topo(self):
        if self.esta_vazia():
            return None

        return self.topo.dado

    def esta_vazia(self):
        return self.topo is None