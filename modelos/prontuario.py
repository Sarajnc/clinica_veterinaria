from datetime import datetime
from estruturas.lista import ListaEncadeada

class Prontuario:
    def __init__(self, numero, nome_animal, nome_tutor, veterinario):
        self.numero = numero
        self.nome_animal = nome_animal
        self.nome_tutor = nome_tutor
        self.veterinario = veterinario

        self.data_hora = datetime.now()
        self.status = "Aberto"
        self.alta = False

        self.medicamentos = ListaEncadeada()
        self.procedimentos = ListaEncadeada()

    def adicionar_item(self, item, tipo):
        if self.status != "Aberto":
            return False

        if tipo == "medicamento":
            return self.medicamentos.adicionar(item)

        elif tipo == "procedimento":
            return self.procedimentos.adicionar(item)

        return False

    def remover_item(self, item, tipo):
        if self.status != "Aberto":
            return False
        
        if tipo == "medicamento":
            return self.medicamentos.remover(item)

        elif tipo == "procedimento":
            return self.procedimentos.remover(item)

        return False

    def registrar_alta(self):
        if self.status == "Aberto":
            self.alta = True
            return True

        return False

    def fechar_prontuario(self):
        if self.status == "Aberto" and self.alta:
            self.status = "Fechado"
            return True

        return False