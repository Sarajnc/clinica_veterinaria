from datetime import date

from estruturas.lista import ListaEncadeada
from modelos.tutor import Tutor
from modelos.animal import Animal
from modelos.atendimento import Atendimento
from modelos.produto import Produto
from modelos.lote import Lote
from servicos.clinica import Clinica

clinica = Clinica(2)
historico = ListaEncadeada()
proximo_id = 1

def buscar_atendimento(numero):
    atual = historico.inicio
    while atual:
        if atual.dado.id_atendimento == numero:
            return atual.dado
        atual = atual.proximo
    return None

def listar_itens(lista):
    atual = lista.inicio
    numero = 1

    while atual:
        item = atual.dado
        print(f"{numero}. {item.nome} | Quantidade: {item.quantidade} | R$ {item.calcular_valor():.2f}")
        atual = atual.proximo
        numero += 1

def selecionar_item(lista):
    numero = int(input("Número do item: "))
    atual = lista.inicio
    posicao = 1

    while atual:
        if posicao == numero:
            return atual.dado
        atual = atual.proximo
        posicao += 1

    return None

def cadastro():
    print("\n1 - Cadastrar tutor")
    print("2 - Cadastrar animal")
    print("3 - Buscar tutor ou animal")
    print("4 - Remover tutor ou animal")

    opcao = input("Escolha: ")

    if opcao == "1":
        tutor = Tutor(
            input("Nome: "),
            input("CPF: "),
            input("Telefone: ")
        )
        print("Cadastro realizado!" if clinica.cadastro.cadastrar(tutor)
              else "CPF já cadastrado.")

    elif opcao == "2":
        cpf = input("CPF do tutor: ")
        tutor = clinica.cadastro.buscar(cpf)

        if tutor:
            animal = Animal(
                input("Nome: "),
                input("Espécie: "),
                input("Raça: "),
                int(input("Idade: ")),
                tutor
            )
            print("Animal cadastrado!" if clinica.cadastro.cadastrar(animal)
                  else "Não foi possível cadastrar.")
        else:
            print("Tutor não encontrado.")

    elif opcao == "3":
        cpf = input("CPF: ")
        nome = input("Nome do animal (ENTER para buscar tutor): ")
        resultado = clinica.cadastro.buscar(cpf, nome) if nome else clinica.cadastro.buscar(cpf)

        if resultado:
            print(vars(resultado))
        else:
            print("Cadastro não encontrado.")

    elif opcao == "4":
        cpf = input("CPF do tutor: ")
        nome = input("Nome do animal (ENTER para remover tutor): ")

        removido = clinica.cadastro.remover(cpf, nome) if nome else clinica.cadastro.remover(cpf)
        print("Cadastro removido!" if removido else "Cadastro não encontrado.")

def atendimento():
    global proximo_id

    print("\n1 - Registrar chegada")
    print("2 - Chamar próximo animal")
    print("3 - Listar atendimentos")

    opcao = input("Escolha: ")

    if opcao == "1":
        cpf = input("CPF do tutor: ")
        nome = input("Nome do animal: ")
        animal = clinica.cadastro.buscar(cpf, nome)

        if animal:
            queixa = input("Queixa: ")
            emergencia = input("É emergência? (s/n): ").lower() == "s"

            novo = Atendimento(animal, queixa, proximo_id, emergencia)
            clinica.receber_atendimento(novo)
            historico.adicionar(novo)
            proximo_id += 1
            print("Animal entrou na fila!")
        else:
            print("Animal não encontrado.")

    elif opcao == "2":
        veterinario = input("Veterinário responsável: ")
        chamado = clinica.chamar_proximo_animal(veterinario)

        if chamado:
            print(f"Atendendo: {chamado.animal.nome}")
            print(f"Prontuário: {chamado.prontuario.numero}")
        else:
            print("Nenhum paciente disponível ou consultórios ocupados.")

    elif opcao == "3":
        atual = historico.inicio
        while atual:
            a = atual.dado
            status = a.prontuario.status if a.prontuario else "Aguardando"
            print(f"#{a.id_atendimento} - {a.animal.nome} | {status}")
            atual = atual.proximo

def prontuario():
    numero = int(input("Número do atendimento: "))
    atendimento = buscar_atendimento(numero)

    if not atendimento or not atendimento.prontuario:
        print("Atendimento ou prontuário não encontrado.")
        return

    p = atendimento.prontuario

    print("\n1 - Exibir diagnóstico")
    print("2 - Marcar alteração")
    print("3 - Adicionar medicamento")
    print("4 - Adicionar procedimento")
    print("5 - Remover medicamento")
    print("6 - Remover procedimento")
    print("7 - Consultar prontuário")
    print("8 - Desfazer última ação")

    opcao = input("Escolha: ")

    if opcao == "1":
        p.exibir_diagnostico()

    elif opcao == "2":
        p.exibir_diagnostico()
        codigo = input("Código da estrutura: ")
        print("Alteração registrada!" if p.marcar_alteracao(codigo)
              else "Código inválido ou prontuário fechado.")

    elif opcao == "3":
        codigo = input("Código do produto: ")
        quantidade = int(input("Quantidade: "))
        print("Medicamento adicionado!" if clinica.adicionar_medicamento(
            atendimento, codigo, quantidade) else "Não foi possível adicionar.")

    elif opcao == "4":
        nome = input("Procedimento: ")
        valor = float(input("Valor: "))
        print("Procedimento adicionado!" if clinica.adicionar_procedimento(
            atendimento, nome, valor) else "Não foi possível adicionar.")

    elif opcao in ("5", "6"):
        lista = p.medicamentos if opcao == "5" else p.procedimentos
        tipo = "medicamento" if opcao == "5" else "procedimento"

        listar_itens(lista)
        item = selecionar_item(lista)

        if item:
            print("Item removido!" if p.remover_item(item, tipo)
                  else "Não foi possível remover.")
        else:
            print("Item não encontrado.")

    elif opcao == "8":
        print("Ação desfeita!" if p.desfazer_ultima_acao()
              else "Nada para desfazer ou prontuário fechado.")

    elif opcao == "7":
        print(f"\nProntuário: {p.numero}")
        print(f"Animal: {p.nome_animal}")
        print(f"Tutor: {p.nome_tutor}")
        print(f"Veterinário: {p.veterinario}")
        print(f"Status: {p.status}")

        print("\nMedicamentos:")
        listar_itens(p.medicamentos)

        print("\nProcedimentos:")
        listar_itens(p.procedimentos)

def estoque():
    print("\n1 - Cadastrar produto")
    print("2 - Adicionar lote")
    print("3 - Consultar estoque")
    print("4 - Ajustar quantidade de lote")
    print("5 - Descartar vencidos")

    opcao = input("Escolha: ")

    if opcao == "1":
        produto = Produto(
            input("Nome: "),
            input("Código: "),
            float(input("Preço de venda: ")),
            int(input("Estoque mínimo: "))
        )
        print("Produto cadastrado!" if clinica.estoque.cadastrar_produto(produto)
              else "Código já existente.")

    elif opcao == "2":
        codigo = input("Código do produto: ")
        produto = clinica.estoque.buscar_produto(codigo)

        if produto:
            lote = Lote(
                produto,
                input("Fornecedor: "),
                float(input("Preço de compra: ")),
                date.today(),
                date.fromisoformat(input("Validade (AAAA-MM-DD): ")),
                int(input("Quantidade: "))
            )
            clinica.estoque.adicionar_lote(codigo, lote)
            print("Lote cadastrado!")
        else:
            print("Produto não encontrado.")

    elif opcao == "3":
        atual = clinica.estoque.produtos.inicio

        while atual:
            p = atual.dado
            quantidade = p.quantidade_em_estoque()
            print(f"\n{p.nome} | Código: {p.codigo} | Estoque: {quantidade}")

            if clinica.estoque.verificar_estoque_minimo(p.codigo):
                print("ALERTA: estoque abaixo do mínimo!")

            lote_atual = p.lotes.inicio
            while lote_atual:
                l = lote_atual.dado
                print(f"  Lote: {l.fornecedor} | Qtd: {l.quantidade} | Validade: {l.data_validade}")
                lote_atual = lote_atual.proximo

            perda = p.perdas.inicio
            while perda:
                print(f"  PERDA: {perda.dado.quantidade} unidades descartadas")
                perda = perda.proximo

            atual = atual.proximo

    elif opcao == "4":
        codigo = input("Código do produto: ")
        produto = clinica.estoque.buscar_produto(codigo)

        if produto:
            atual = produto.lotes.inicio
            numero = 1

            while atual:
                l = atual.dado
                print(f"{numero} - {l.fornecedor} | Quantidade: {l.quantidade}")
                atual = atual.proximo
                numero += 1

            lote = selecionar_item(produto.lotes)
            if lote:
                quantidade = int(input("Nova quantidade: "))
                print("Estoque ajustado!" if clinica.estoque.ajustar_quantidade(
                    codigo, lote, quantidade) else "Não foi possível ajustar.")
        else:
            print("Produto não encontrado.")

    elif opcao == "5":
        codigo = input("Código do produto: ")
        print("Verificação concluída!" if clinica.estoque.descartar_vencidos(
            codigo, date.today()) else "Produto não encontrado.")

def pagamento():
    numero = int(input("Número do atendimento: "))
    atendimento = buscar_atendimento(numero)

    if not atendimento:
        print("Atendimento não encontrado.")
        return

    forma = input("Pagamento (PIX, Cartão ou Dinheiro): ")
    parcelas = 1

    if forma == "Cartão":
        parcelas = int(input("Número de parcelas: "))

    if input("Confirmar alta, fechamento e pagamento? (s/n): ").lower() == "s":
        if clinica.finalizar_atendimento(atendimento, forma, parcelas):
            print("Alta registrada, prontuário fechado e pagamento confirmado!")
        else:
            print("Não foi possível finalizar. Verifique os itens e o estoque.")

def relatorio():
    print("\n========== PAGAMENTOS ==========")
    atual = clinica.pagamentos.inicio
    total = 0

    while atual:
        p = atual.dado
        print(f"Prontuário {p.numero_prontuario} | {p.nome_pagador}")
        print(f"{p.forma_pagamento} | Total: R$ {p.valor_total:.2f}")
        total += p.valor_total
        atual = atual.proximo

    print(f"\nTotal recebido: R$ {total:.2f}")

def main():
    while True:
        print("""
========== CLÍNICA VETERINÁRIA ==========

1 - Tutores e animais
2 - Atendimento e fila
3 - Prontuário e diagnóstico
4 - Estoque
5 - Alta e pagamento
6 - Relatório de pagamentos
0 - Sair
""")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastro()
        elif opcao == "2":
            atendimento()
        elif opcao == "3":
            prontuario()
        elif opcao == "4":
            estoque()
        elif opcao == "5":
            pagamento()
        elif opcao == "6":
            relatorio()
        elif opcao == "0":
            print("Sistema encerrado!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()