
from datetime import date

from estruturas.lista import ListaEncadeada
from modelos.tutor import Tutor
from modelos.animal import Animal
from modelos.atendimento import Atendimento
from modelos.produto import Produto
from modelos.lote import Lote
from servicos.clinica import Clinica


# ============================================================
# CONFIGURAÇÕES
# ============================================================

clinica = Clinica(2)
historico = ListaEncadeada()
proximo_id = 1


# ============================================================
# FUNÇÕES VISUAIS
# ============================================================

def linha():
    print("=" * 58)


def titulo(nome):
    print("\n")
    linha()
    print(f"{nome.center(58)}")
    linha()


def secao(nome):
    print(f"\n--- {nome} ---")


def sucesso(mensagem):
    print(f"\n[OK] {mensagem}")


def erro(mensagem):
    print(f"\n[ERRO] {mensagem}")


def alerta(mensagem):
    print(f"\n[ATENÇÃO] {mensagem}")


def menu(titulo_menu, opcoes):
    titulo(titulo_menu)

    for numero, descricao in opcoes:
        print(f"  {numero} - {descricao}")

    linha()
    return input("Escolha uma opção: ").strip()


def confirmar(mensagem):
    return input(f"{mensagem} (s/n): ").strip().lower() == "s"


def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            erro("Digite um número inteiro válido.")


def ler_float(mensagem):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor < 0:
                erro("O valor não pode ser negativo.")
                continue
            return valor
        except ValueError:
            erro("Digite um valor numérico válido.")


def pausa():
    input("\nPressione ENTER para continuar...")


def mostrar_vazio(mensagem):
    print(f"\n{mensagem}")


# ============================================================
# BUSCAS E SELEÇÃO
# ============================================================

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

    if not atual:
        mostrar_vazio("Nenhum item cadastrado.")
        return

    while atual:
        item = atual.dado

        print(
            f"{numero}. {item.nome} | "
            f"Quantidade: {item.quantidade} | "
            f"R$ {item.calcular_valor():.2f}"
        )

        atual = atual.proximo
        numero += 1


def selecionar_item(lista):
    numero = ler_inteiro("Número do item: ")

    atual = lista.inicio
    posicao = 1

    while atual:
        if posicao == numero:
            return atual.dado

        atual = atual.proximo
        posicao += 1

    return None


# ============================================================
# APRESENTAÇÃO DE CADASTROS
# ============================================================

def exibir_tutor(tutor):
    titulo("DADOS DO TUTOR")

    print(f"Nome:     {tutor.nome}")
    print(f"CPF:      {tutor.cpf}")
    print(f"Telefone: {tutor.telefone}")

    linha()


def exibir_animal(animal):
    titulo("ANIMAL ENCONTRADO")

    print(f"Nome:     {animal.nome}")
    print(f"Espécie:  {animal.especie}")
    print(f"Raça:     {animal.raca}")
    print(f"Idade:    {animal.idade} anos")
    print(f"Tutor:    {animal.tutor.nome}")
    print(f"CPF:      {animal.tutor.cpf}")

    linha()


# ============================================================
# CADASTRO DE TUTORES E ANIMAIS
# ============================================================

def cadastro():
    opcao = menu("TUTORES E ANIMAIS", [
        ("1", "Cadastrar tutor"),
        ("2", "Cadastrar animal"),
        ("3", "Buscar tutor ou animal"),
        ("4", "Remover tutor ou animal"),
        ("0", "Voltar")
    ])

    if opcao == "1":
        titulo("CADASTRO DE TUTOR")

        tutor = Tutor(
            input("Nome completo: "),
            input("CPF: "),
            input("Telefone: ")
        )

        if clinica.cadastro.cadastrar(tutor):
            sucesso("Tutor cadastrado com sucesso!")
        else:
            erro("CPF já cadastrado.")

    elif opcao == "2":
        titulo("CADASTRO DE ANIMAL")

        cpf = input("CPF do tutor: ")
        tutor = clinica.cadastro.buscar(cpf)

        if tutor:
            animal = Animal(
                input("Nome do animal: "),
                input("Espécie: "),
                input("Raça: "),
                ler_inteiro("Idade: "),
                tutor
            )

            if clinica.cadastro.cadastrar(animal):
                sucesso("Animal cadastrado com sucesso!")
            else:
                erro("Não foi possível cadastrar o animal.")
        else:
            erro("Tutor não encontrado.")

    elif opcao == "3":
        titulo("CONSULTA DE CADASTRO")

        cpf = input("CPF: ").strip()
        nome = input("Nome do animal (ENTER para buscar tutor): ").strip()

        resultado = (
            clinica.cadastro.buscar(cpf, nome)
            if nome
            else clinica.cadastro.buscar(cpf)
        )

        if resultado:
            if isinstance(resultado, Animal):
                exibir_animal(resultado)
            else:
                exibir_tutor(resultado)
        else:
            erro("Cadastro não encontrado.")

    elif opcao == "4":
        titulo("REMOÇÃO DE CADASTRO")

        cpf = input("CPF do tutor: ").strip()
        nome = input("Nome do animal (ENTER para remover tutor): ").strip()

        if confirmar("Deseja realmente remover?"):
            removido = (
                clinica.cadastro.remover(cpf, nome)
                if nome
                else clinica.cadastro.remover(cpf)
            )

            if removido:
                sucesso("Cadastro removido!")
            else:
                erro("Cadastro não encontrado.")

    elif opcao != "0":
        erro("Opção inválida.")


# ============================================================
# ATENDIMENTOS E FILA
# ============================================================

def atendimento():
    global proximo_id

    opcao = menu("ATENDIMENTO E FILA", [
        ("1", "Registrar chegada"),
        ("2", "Chamar próximo animal"),
        ("3", "Listar atendimentos"),
        ("0", "Voltar")
    ])

    if opcao == "1":
        titulo("REGISTRO DE ATENDIMENTO")

        cpf = input("CPF do tutor: ")
        nome = input("Nome do animal: ")

        animal = clinica.cadastro.buscar(cpf, nome)

        if animal:
            queixa = input("Queixa principal: ")
            emergencia = confirmar("É uma emergência?")

            novo = Atendimento(
                animal,
                queixa,
                proximo_id,
                emergencia
            )

            clinica.receber_atendimento(novo)
            historico.adicionar(novo)

            proximo_id += 1

            sucesso(f"Atendimento #{novo.id_atendimento} registrado!")

            print(f"Animal: {animal.nome}")
            print(f"Tutor: {animal.tutor.nome}")
            print(f"Prioridade: {'EMERGÊNCIA' if emergencia else 'Normal'}")

        else:
            erro("Animal não encontrado.")

    elif opcao == "2":
        titulo("CHAMADA DE PACIENTE")

        veterinario = input("Veterinário responsável: ")

        chamado = clinica.chamar_proximo_animal(veterinario)

        if chamado:
            sucesso("Paciente encaminhado para atendimento!")

            print(f"Animal: {chamado.animal.nome}")
            print(f"Tutor: {chamado.animal.tutor.nome}")
            print(f"Veterinário: {veterinario}")
            print(f"Prontuário: {chamado.prontuario.numero}")

        else:
            alerta("Nenhum paciente disponível ou consultórios ocupados.")

    elif opcao == "3":
        titulo("HISTÓRICO DE ATENDIMENTOS")

        atual = historico.inicio

        if not atual:
            mostrar_vazio("Nenhum atendimento registrado.")
            return

        while atual:
            a = atual.dado
            status = a.prontuario.status if a.prontuario else "Aguardando"

            print(f"\nAtendimento #{a.id_atendimento}")
            print(f"Animal: {a.animal.nome}")
            print(f"Tutor: {a.animal.tutor.nome}")
            print(f"Queixa: {a.queixa}")
            print(f"Prioridade: {'Emergência' if a.emergencia else 'Normal'}")
            print(f"Status: {status}")

            atual = atual.proximo

    elif opcao != "0":
        erro("Opção inválida.")


# ============================================================
# PRONTUÁRIO E DIAGNÓSTICO
# ============================================================

def prontuario():
    titulo("PRONTUÁRIO E DIAGNÓSTICO")

    numero = ler_inteiro("Número do atendimento: ")
    atendimento_atual = buscar_atendimento(numero)

    if not atendimento_atual or not atendimento_atual.prontuario:
        erro("Atendimento ou prontuário não encontrado.")
        return

    p = atendimento_atual.prontuario

    opcao = menu("GERENCIAR PRONTUÁRIO", [
        ("1", "Exibir diagnóstico"),
        ("2", "Marcar alteração"),
        ("3", "Adicionar medicamento"),
        ("4", "Adicionar procedimento"),
        ("5", "Remover medicamento"),
        ("6", "Remover procedimento"),
        ("7", "Consultar prontuário"),
        ("8", "Desfazer última ação"),
        ("0", "Voltar")
    ])

    if opcao == "1":
        p.exibir_diagnostico()

    elif opcao == "2":
        p.exibir_diagnostico()

        codigo = input("Código da estrutura: ")

        if p.marcar_alteracao(codigo):
            sucesso("Alteração registrada!")
        else:
            erro("Código inválido ou prontuário fechado.")

    elif opcao == "3":
        codigo = input("Código do produto: ")
        quantidade = ler_inteiro("Quantidade: ")

        if clinica.adicionar_medicamento(
            atendimento_atual, codigo, quantidade
        ):
            sucesso("Medicamento adicionado!")
        else:
            erro("Não foi possível adicionar o medicamento.")

    elif opcao == "4":
        nome = input("Nome do procedimento: ")
        valor = ler_float("Valor: ")

        if clinica.adicionar_procedimento(
            atendimento_atual, nome, valor
        ):
            sucesso("Procedimento adicionado!")
        else:
            erro("Não foi possível adicionar o procedimento.")

    elif opcao in ("5", "6"):
        lista = p.medicamentos if opcao == "5" else p.procedimentos
        tipo = "medicamento" if opcao == "5" else "procedimento"

        secao("ITENS CADASTRADOS")
        listar_itens(lista)

        item = selecionar_item(lista)

        if item:
            if p.remover_item(item, tipo):
                sucesso("Item removido!")
            else:
                erro("Não foi possível remover.")
        else:
            erro("Item não encontrado.")

    elif opcao == "7":
        titulo("DADOS DO PRONTUÁRIO")

        print(f"Número:       {p.numero}")
        print(f"Animal:       {p.nome_animal}")
        print(f"Tutor:        {p.nome_tutor}")
        print(f"Veterinário:  {p.veterinario}")
        print(f"Status:       {p.status}")

        secao("MEDICAMENTOS")
        listar_itens(p.medicamentos)

        secao("PROCEDIMENTOS")
        listar_itens(p.procedimentos)

    elif opcao == "8":
        if p.desfazer_ultima_acao():
            sucesso("Última ação desfeita!")
        else:
            alerta("Nada para desfazer ou prontuário fechado.")

    elif opcao != "0":
        erro("Opção inválida.")


# ============================================================
# ESTOQUE
# ============================================================

def estoque():
    opcao = menu("CONTROLE DE ESTOQUE", [
        ("1", "Cadastrar produto"),
        ("2", "Adicionar lote"),
        ("3", "Consultar estoque"),
        ("4", "Ajustar quantidade de lote"),
        ("5", "Descartar vencidos"),
        ("0", "Voltar")
    ])

    if opcao == "1":
        titulo("CADASTRO DE PRODUTO")

        produto = Produto(
            input("Nome: "),
            input("Código: "),
            ler_float("Preço de venda: "),
            ler_inteiro("Estoque mínimo: ")
        )

        if clinica.estoque.cadastrar_produto(produto):
            sucesso("Produto cadastrado!")
        else:
            erro("Código já existente.")

    elif opcao == "2":
        titulo("ENTRADA DE LOTE")

        codigo = input("Código do produto: ")
        produto = clinica.estoque.buscar_produto(codigo)

        if produto:
            try:
                validade = date.fromisoformat(
                    input("Validade (AAAA-MM-DD): ")
                )

                lote = Lote(
                    produto,
                    input("Fornecedor: "),
                    ler_float("Preço de compra: "),
                    date.today(),
                    validade,
                    ler_inteiro("Quantidade: ")
                )

                clinica.estoque.adicionar_lote(codigo, lote)
                sucesso("Lote cadastrado!")

            except ValueError:
                erro("Data inválida. Utilize AAAA-MM-DD.")

        else:
            erro("Produto não encontrado.")

    elif opcao == "3":
        titulo("CONSULTA DE ESTOQUE")

        atual = clinica.estoque.produtos.inicio

        if not atual:
            mostrar_vazio("Nenhum produto cadastrado.")
            return

        while atual:
            p = atual.dado
            quantidade = p.quantidade_em_estoque()

            secao(p.nome)

            print(f"Código: {p.codigo}")
            print(f"Quantidade disponível: {quantidade}")
            print(f"Preço de venda: R$ {p.preco_venda:.2f}")

            if clinica.estoque.verificar_estoque_minimo(p.codigo):
                alerta("Estoque abaixo do mínimo!")

            print("\nLotes:")

            lote_atual = p.lotes.inicio

            if not lote_atual:
                print("  Nenhum lote disponível.")

            while lote_atual:
                l = lote_atual.dado

                print(f"  Fornecedor: {l.fornecedor}")
                print(f"  Quantidade: {l.quantidade}")
                print(f"  Validade: {l.data_validade}")

                if l.data_validade <= date.today():
                    alerta("Lote vencido ou com validade para hoje!")

                lote_atual = lote_atual.proximo

            perda = p.perdas.inicio

            if perda:
                print("\nHistórico de perdas:")

            while perda:
                print(
                    f"  {perda.dado.quantidade} unidades descartadas"
                )
                perda = perda.proximo

            atual = atual.proximo

    elif opcao == "4":
        titulo("AJUSTE DE LOTE")

        codigo = input("Código do produto: ")
        produto = clinica.estoque.buscar_produto(codigo)

        if produto:
            atual = produto.lotes.inicio
            numero = 1

            while atual:
                l = atual.dado

                print(
                    f"{numero} - {l.fornecedor} | "
                    f"Quantidade: {l.quantidade} | "
                    f"Validade: {l.data_validade}"
                )

                atual = atual.proximo
                numero += 1

            if produto.lotes.inicio:
                lote = selecionar_item(produto.lotes)

                if lote:
                    quantidade = ler_inteiro("Nova quantidade: ")

                    if clinica.estoque.ajustar_quantidade(
                        codigo, lote, quantidade
                    ):
                        sucesso("Estoque ajustado!")
                    else:
                        erro("Não foi possível ajustar.")
                else:
                    erro("Lote não encontrado.")
            else:
                alerta("Produto não possui lotes.")

        else:
            erro("Produto não encontrado.")

    elif opcao == "5":
        titulo("DESCARTE DE PRODUTOS VENCIDOS")

        codigo = input("Código do produto: ")

        if confirmar("Deseja realizar a verificação e o descarte?"):
            if clinica.estoque.descartar_vencidos(
                codigo, date.today()
            ):
                sucesso("Verificação concluída!")
            else:
                erro("Produto não encontrado.")

    elif opcao != "0":
        erro("Opção inválida.")


# ============================================================
# ALTA E PAGAMENTO
# ============================================================

def pagamento():
    titulo("ALTA E PAGAMENTO")

    numero = ler_inteiro("Número do atendimento: ")
    atendimento_atual = buscar_atendimento(numero)

    if not atendimento_atual:
        erro("Atendimento não encontrado.")
        return

    forma = input("Pagamento (PIX, Cartão ou Dinheiro): ").strip()
    parcelas = 1

    if forma.lower() == "cartão":
        parcelas = ler_inteiro("Número de parcelas: ")

        if parcelas < 1:
            erro("Informe pelo menos uma parcela.")
            return

    if confirmar("Confirmar alta, fechamento e pagamento?"):
        if clinica.finalizar_atendimento(
            atendimento_atual, forma, parcelas
        ):
            sucesso("Alta registrada, prontuário fechado e pagamento confirmado!")
        else:
            erro("Não foi possível finalizar. Verifique os itens e o estoque.")


# ============================================================
# RELATÓRIO FINANCEIRO
# ============================================================

def relatorio():
    titulo("RELATÓRIO DE PAGAMENTOS")

    atual = clinica.pagamentos.inicio
    total = 0
    quantidade = 0

    if not atual:
        mostrar_vazio("Nenhum pagamento registrado.")
        return

    while atual:
        p = atual.dado

        print(f"\nProntuário: {p.numero_prontuario}")
        print(f"Pagador: {p.nome_pagador}")
        print(f"Forma: {p.forma_pagamento}")
        print(f"Valor: R$ {p.valor_total:.2f}")

        total += p.valor_total
        quantidade += 1

        atual = atual.proximo

    linha()

    print(f"Quantidade de pagamentos: {quantidade}")
    print(f"TOTAL RECEBIDO: R$ {total:.2f}")

    linha()


# ============================================================
# MENU PRINCIPAL
# ============================================================

def main():
    while True:
        print("\n")
        linha()
        print("CLÍNICA VETERINÁRIA".center(58))
        print("SISTEMA DE GERENCIAMENTO".center(58))
        linha()

        print("\n  1 - Tutores e animais")
        print("  2 - Atendimento e fila")
        print("  3 - Prontuário e diagnóstico")
        print("  4 - Controle de estoque")
        print("  5 - Alta e pagamento")
        print("  6 - Relatório financeiro")

        print("\n  0 - Encerrar sistema")

        linha()

        opcao = input("Selecione uma opção: ").strip()

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
            print("\nAbrindo relatório financeiro...")
            relatorio()
            pausa()
        elif opcao == "0":
            if confirmar("Deseja realmente encerrar o sistema?"):
                print("\nSistema encerrado. Obrigada!")
                break
        else:
            erro("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()