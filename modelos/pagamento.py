from datetime import datetime

class Pagamento:
    def __init__(self, nome_pagador, prontuario, forma_pagamento,
                 valor_medicamentos, valor_procedimentos, parcelas=1):
        self.nome_pagador = nome_pagador
        self.numero_prontuario = prontuario.numero
        self.forma_pagamento = forma_pagamento
        self.parcelas = parcelas

        self.valor_medicamentos = valor_medicamentos
        self.valor_procedimentos = valor_procedimentos
        self.valor_total = valor_medicamentos + valor_procedimentos

        self.data_pagamento = None
        self.status = "Pendente"

    def confirmar_pagamento(self):
        if self.status == "Pendente":
            self.status = "Pago"
            self.data_pagamento = datetime.now()
            return True

        return False
