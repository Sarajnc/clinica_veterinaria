from datetime import datetime
from estruturas.lista import ListaEncadeada
from estruturas.pilha import Pilha

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

        self.historico_acoes = Pilha()

    def adicionar_item(self, item, tipo):
        if self.status != "Aberto":
            return False

        if tipo == "medicamento":
            self.medicamentos.adicionar(item)

        elif tipo == "procedimento":
            self.procedimentos.adicionar(item)

        else:
            return False

        self.historico_acoes.empilhar(("adicionou", item, tipo))
        return True

    def remover_item(self, item, tipo):
        if self.status != "Aberto":
            return False

        if tipo == "medicamento":
            removido = self.medicamentos.remover(item)

        elif tipo == "procedimento":
            removido = self.procedimentos.remover(item)

        else:
            return False

        if removido:
            self.historico_acoes.empilhar(("removeu", item, tipo))

        return removido

    def desfazer_ultima_acao(self):
        if self.status != "Aberto" or self.historico_acoes.esta_vazia():
            return False

        acao, item, tipo = self.historico_acoes.desempilhar()

        if tipo == "medicamento":
            lista = self.medicamentos
        else:
            lista = self.procedimentos

        if acao == "adicionou":
            return lista.remover(item)

        lista.adicionar(item)
        return True

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