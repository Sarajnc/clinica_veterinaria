from estruturas.lista import ListaEncadeada

class NoArvore:
    def __init__(self, nome, codigo=None):
        self.nome = nome
        self.codigo = codigo
        self.estado = "Saudável"
        self.filhos = ListaEncadeada()

    def adicionar_filho(self, filho):
        self.filhos.adicionar(filho)

class Arvore:
    def __init__(self, raiz):
        self.raiz = raiz

    def exibir(self):
        self.exibir_no(self.raiz, 0)

    def exibir_no(self, no, nivel):
        espacos = "    " * nivel

        print(espacos + no.nome, end="")

        if no.codigo is not None:
            print(" [" + str(no.codigo) + "]", end="")

        print(" - " + no.estado)

        atual = no.filhos.inicio

        while atual is not None:
            self.exibir_no(atual.dado, nivel + 1)
            atual = atual.proximo

    def buscar_por_codigo(self, no, codigo):
        if no.codigo == codigo:
            return no

        atual = no.filhos.inicio

        while atual is not None:
            encontrado = self.buscar_por_codigo(atual.dado, codigo)

            if encontrado is not None:
                return encontrado

            atual = atual.proximo

        return None

    def marcar_alterado(self, codigo):
        no = self.buscar_por_codigo(self.raiz, codigo)

        if no is None:
            return False

        no.estado = "Alterado"
        return True