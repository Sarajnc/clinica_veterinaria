from estruturas.lista import ListaEncadeada

class Tutor:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.animais = ListaEncadeada()

    def adicionar_animal(self, animal):
        self.animais.adicionar(animal)

    def buscar_animal(self, nome):
        return self.animais.buscar_por(
            lambda animal: animal.nome == nome
        )

    def remover_animal(self, nome):
        return self.animais.remover_por(
            lambda animal: animal.nome == nome
        )