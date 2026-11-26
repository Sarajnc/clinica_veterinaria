from datetime import datetime

class Atendimento:
    def __init__(self, animal, queixa, id_atendimento, emergencia):
        self.animal = animal
        self.queixa = queixa
        self.data_hora = datetime.now()
        self.id_atendimento = id_atendimento
        self.emergencia = emergencia
        self.status = "Aguardando"
        self.prontuario = None