from estruturas.lista import No

class Fila:
    def __init__(self):
        self.inicio = None
        self.fim = None

    def enfileirar(self, dado):
        novo_no = No(dado)

        if self.fim is None:
            self.inicio = novo_no
            self.fim = novo_no
        else:
            self.fim.proximo = novo_no
            self.fim = novo_no

    def desenfileirar(self):
        if self.esta_vazia():
            return None

        dado = self.inicio.dado
        self.inicio = self.inicio.proximo

        if self.inicio is None:
            self.fim = None

        return dado
   
    def esta_vazia(self):
        return self.inicio is None

    def consultar_inicio(self):
        if self.esta_vazia():
            return None

        return self.inicio.dado

    def tamanho(self):
        contador = 0
        atual = self.inicio

        while atual is not None:
            contador += 1
            atual = atual.proximo

        return contador