from estruturas.arvore import Arvore, NoArvore

class Diagnostico:
    def __init__(self):
        animal = NoArvore("Animal")

        # Sistema digestório
        digestorio = NoArvore("Sistema digestório")
        digestorio.adicionar_filho(NoArvore("Estômago", "DIG01"))
        digestorio.adicionar_filho(NoArvore("Intestino", "DIG02"))

        # Sistema respiratório
        respiratorio = NoArvore("Sistema respiratório")
        respiratorio.adicionar_filho(NoArvore("Pulmões", "RES01"))
        respiratorio.adicionar_filho(NoArvore("Traqueia", "RES02"))

        # Pele
        pele = NoArvore("Pele")
        pele.adicionar_filho(NoArvore("Pelos", "PEL01"))
        pele.adicionar_filho(NoArvore("Unhas", "PEL02"))

        # Montagem da árvore
        animal.adicionar_filho(digestorio)
        animal.adicionar_filho(respiratorio)
        animal.adicionar_filho(pele)

        self.arvore = Arvore(animal)

    def exibir(self):
        self.arvore.exibir()

    def marcar_alterado(self, codigo):
        return self.arvore.marcar_alterado(codigo)