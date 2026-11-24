from estruturas.fila import Fila

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