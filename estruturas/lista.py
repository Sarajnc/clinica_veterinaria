class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

class ListaEncadeada:
    def __init__(self):
        self.inicio = None
        self.fim = None     
        self._tamanho = 0

    def adicionar(self, dado):
        novo_no = No(dado)

        if self.inicio is None:
            self.inicio = novo_no
            self.fim = novo_no
        else:
            self.fim.proximo = novo_no
            self.fim = novo_no

        self._tamanho += 1
        return True

    def buscar_por(self, criterio):
        atual = self.inicio

        while atual is not None:
            if criterio(atual.dado):
                return atual.dado 
            atual = atual.proximo

        return None

    def remover(self, dado):
        atual = self.inicio
        anterior = None

        while atual is not None and atual.dado != dado:
            anterior = atual
            atual = atual.proximo

        if atual is None:
            return False

        if anterior is None:
            self.inicio = atual.proximo
        else:
            anterior.proximo = atual.proximo

        if atual is self.fim:
            self.fim = anterior

        self._tamanho -= 1
        return True

    def remover_por(self, criterio):
        atual = self.inicio
        anterior = None

        while atual is not None and not criterio(atual.dado):
            anterior = atual
            atual = atual.proximo

        if atual is None:
            return False

        if anterior is None:
            self.inicio = atual.proximo
        else:
            anterior.proximo = atual.proximo

        if atual is self.fim:
            self.fim = anterior

        self._tamanho -= 1
        return True


    def contem(self, dado):
        atual = self.inicio

        while atual is not None:
            if atual.dado == dado:
                return True

            atual = atual.proximo

        return False

    def mostrar(self):
        atual = self.inicio

        while atual is not None:
            print(atual.dado)
            atual= atual.proximo

    def esta_vazia(self):
        return self.inicio is None

    def tamanho(self):
        return self._tamanho