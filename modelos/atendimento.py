from animal import Animal
from datetime import datetime

class Atendimento:
    def __init__(self, animal, queixa, id):
        self.animal = animal
        self.queixa = queixa
        self.data_hora = datetime.now()
        self.id = id