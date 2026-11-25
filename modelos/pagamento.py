from datetime import datetime

class Pagamento:
    def __init__(self, prontuario, valor, forma_pagamento):
        self.prontuario = prontuario
        self.valor = valor
        self.forma_pagamento = forma_pagamento

        self.data_pagamento = None
        self.status = "Pendente"

    def confirmar_pagamento(self):
        if self.status == "Pendente":
            self.status = "Pago"
            self.data_pagamento = datetime.now()
            return True

        return False
