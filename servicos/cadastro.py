from estruturas.lista import ListaEncadeada
from modelos.tutor import Tutor
from modelos.animal import Animal

class Cadastro:
    def __init__(self):
        self.tutores = ListaEncadeada()
        self.animais = ListaEncadeada()

    def cadastrar(self, dado):
        if isinstance(dado, Tutor):
            if self.buscar(dado.cpf):
                return False

            self.tutores.adicionar(dado)
            return True

        elif isinstance(dado, Animal):
            tutor = self.buscar(dado.tutor.cpf)

            if tutor is None:
                return False

            if self.buscar(dado.tutor.cpf, dado.nome):
                return False

            dado.tutor = tutor
            tutor.adicionar_animal(dado)
            self.animais.adicionar(dado)
            return True

        return False

    def buscar(self, cpf, nome_animal=None):
        tutor = self.tutores.buscar_por(
            lambda tutor: tutor.cpf == cpf
        )

        if tutor is None:
            return None

        if nome_animal is None:
            return tutor

        return tutor.buscar_animal(nome_animal)

    def remover(self, cpf, nome_animal=None):
        tutor = self.buscar(cpf)

        if tutor is None:
            return False

        if nome_animal is None:
            atual = tutor.animais.inicio

            while atual is not None:
                self.animais.remover(atual.dado)
                atual = atual.proximo

            return self.tutores.remover(tutor)

        animal = tutor.buscar_animal(nome_animal)

        if animal is None:
            return False

        tutor.remover_animal(nome_animal)
        self.animais.remover(animal)
        return True