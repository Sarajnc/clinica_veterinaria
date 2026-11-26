# 🐾 Clínica Veterinária

Sistema em Python que simula o ciclo completo de um atendimento veterinário: cadastro de tutores e animais, fila de espera com prioridade para emergências, diagnóstico, prontuário, controle de estoque, alta e pagamento.

Todas as estruturas de dados (lista encadeada, fila, pilha e árvore) foram implementadas do zero, sem usar estruturas prontas do Python para resolver o problema. Apenas a biblioteca padrão é usada (`datetime`).

## Como executar

```bash
git clone https://github.com/Sarajnc/clinica_veterinaria.git
cd clinica_veterinaria
python3 main.py      # no Windows: py main.py
```

Os dados ficam apenas em memória e são perdidos ao encerrar o programa.

**Menu:** 1) Tutores e animais · 2) Atendimento e fila · 3) Prontuário e diagnóstico · 4) Estoque · 5) Alta e pagamento · 6) Relatório de pagamentos · 0) Sair

## Organização do código

```text
estruturas/   Estruturas genéricas, sem regra da clínica
  lista.py      No, ListaEncadeada
  fila.py       Fila
  pilha.py      Pilha
  arvore.py     NoArvore, Arvore
modelos/      Entidades: Tutor, Animal, Atendimento, Prontuario, ItemProntuario,
              Pagamento, Produto, Lote, Perda
servicos/     Regras da clínica
  cadastro.py     Cadastro
  atendimento.py  GerenciadorAtendimentos
  diagnostico.py  Diagnostico
  estoque.py      GerenciadorEstoque
  clinica.py      Clinica (integra tudo)
main.py       Menu interativo
```

## Combinações de estruturas

### 1. Atendimento com prioridade: Fila + Fila

- **Onde:** `GerenciadorAtendimentos` (`servicos/atendimento.py`) tem `fila_emergencia` e `fila_normal`, ambas `Fila`.
- **Métodos:** `adicionar_atendimento()` escolhe a fila conforme `atendimento.emergencia`; `proximo_atendimento()` desenfileira da emergência e, se estiver vazia, da normal. `Clinica.chamar_proximo_animal()` só chama se houver consultório livre.
- **Por que:** cada fila mantém a ordem de chegada da sua categoria, e a prioridade vem apenas da ordem de consulta entre as filas. Tudo em O(1).
- **Desvantagem de uma fila só:** para emergências passarem na frente, seria preciso inserir no meio da fila ou percorrê-la procurando a primeira emergência, custando O(n).

### 2. Tutores e animais: Lista de tutores + Lista de animais

- **Onde:** `Cadastro.tutores` é uma `ListaEncadeada` de `Tutor`, e cada `Tutor.animais` é outra `ListaEncadeada`.
- **Métodos:** `Cadastro.buscar(cpf, nome_animal)` localiza o tutor pelo CPF e depois chama `Tutor.buscar_animal()`, que percorre apenas os animais daquele tutor. `Tutor.adicionar_animal()` e `Tutor.remover_animal()` não têm limite de animais.
- **Por que:** a relação "um tutor, vários animais" fica na própria estrutura, e a busca procura só entre os animais do tutor certo.
- **Desvantagem de uma lista só:** seria uma lista de animais com o CPF repetido em cada um, e toda busca teria que filtrar a lista inteira (e mais de um tutor poderia ter um animal com o mesmo nome).

### 3. Estoque: Lista de produtos + Lista de lotes

- **Onde:** `GerenciadorEstoque.produtos` é uma `ListaEncadeada` de `Produto`, e cada `Produto` tem `lotes` e `perdas`, também listas.
- **Métodos:** `GerenciadorEstoque.retirar_estoque()` localiza o produto e chama `Produto.retirar_estoque()`, que consome os lotes a partir do primeiro da lista, o mais antigo (os lotes são inseridos no fim, na ordem de compra). Antes disso, `Perda.descartar_lotes_vencidos()` remove lotes vencidos e os registra em `Produto.perdas`.
- **Por que:** a retirada trabalha só com os lotes do produto pedido, e os lotes vencidos viram perda sem afetar os demais produtos.
- **Desvantagem de uma lista só:** lotes de produtos diferentes ficariam misturados, e consultar a quantidade ou retirar um produto exigiria percorrer todos os lotes da clínica.

### 4. Diagnóstico: Árvore + Lista de filhos

- **Onde:** cada `NoArvore` guarda seus filhos em uma `ListaEncadeada` (`NoArvore.filhos`).
- **Métodos:** `Arvore.exibir()` (percurso em pré-ordem, com indentação) e `Arvore.marcar_alterado(codigo)` (busca em profundidade pelo código). `Diagnostico` monta a árvore pré-definida.
- **Por que:** cada nó pode ter de zero a N filhos, e a lista permite isso sem definir um limite.

### 5. Prontuário: Listas + Pilha (desfazer)

- **Onde:** `Prontuario` mantém `medicamentos` e `procedimentos` (`ListaEncadeada`) e `historico_acoes` (`Pilha`).
- **Métodos:** `adicionar_item()` e `remover_item()` empilham cada ação feita; `desfazer_ultima_acao()` desempilha a mais recente e faz o contrário (remove o item adicionado ou adiciona de volta o item removido). Só funciona com o prontuário aberto.
- **Por que:** a última ação feita é sempre a primeira a ser desfeita (LIFO), e empilhar e desempilhar custa O(1). Isso atende ao requisito de adicionar ou remover itens antes do fechamento (por exemplo, quando o tutor não autoriza um procedimento).
- **Desvantagem de uma lista só:** o histórico ficaria misturado com os itens do prontuário, e achar a última ação exigiria percorrer a lista inteira, O(n).

### 6. Finalização do atendimento

`Clinica.finalizar_atendimento()` usa várias estruturas na mesma operação: percorre a lista de medicamentos do `Prontuario`, confere e baixa o estoque (combinação 3), cria o `Pagamento`, registra a alta e fecha o prontuário. Se o estoque não for suficiente, nada é baixado e o atendimento não é finalizado.

## Complexidade

| Operação                                             | Custo    |
| ---------------------------------------------------- | -------- |
| Inserir no fim da lista / enfileirar / desenfileirar | O(1)     |
| Buscar ou remover por critério na lista              | O(n)     |
| Buscar tutor por CPF e depois o animal               | O(T + a) |
| Próximo atendimento (duas filas)                     | O(1)     |
| Quantidade em estoque de um produto                  | O(L)     |
| Retirar do estoque (produto + lotes)                 | O(P + L) |
| Empilhar / desempilhar (histórico do prontuário)     | O(1)     |
| Exibir a árvore / marcar nó por código               | O(N)     |

T = tutores, a = animais do tutor, P = produtos, L = lotes do produto, N = nós da árvore.

## Entregas

- 📜 [Histórico de commits](https://github.com/Sarajnc/clinica_veterinaria/commits/main/)

---

_Projeto acadêmico — Estrutura de Dados · FATEC Rio Claro_
