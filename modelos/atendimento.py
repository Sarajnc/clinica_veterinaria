from datetime import datetime
from estruturas.fila import Fila

class Atendimento:
    def __init__(self, animal, queixa, id, emergencia):
        self.animal = animal
        self.queixa = queixa
        self.data_hora = datetime.now()
        self.id = id
        self.emergencia = emergencia

class GerenciadorAtendimentos:
    def __init__(self):
        self.fila_emergencia = Fila()
        self.fila_normal = Fila()

    def adicionar_atendimento(self, atendimento):
        if atendimento.emergencia:
            self.fila_emergencia.enfileirar(atendimento)
        else:
            self.fila_normal.enfileirar(atendimento)

    def proximo_atendimento(self):
        if not self.fila_emergencia.esta_vazia():
            return self.fila_emergencia.desenfileirar()

        elif not self.fila_normal.esta_vazia():
            return self.fila_normal.desenfileirar()

        else:
            return None