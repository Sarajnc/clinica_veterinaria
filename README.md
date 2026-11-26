# 🐾 Clínica Veterinária

Sistema em Python que simula o ciclo completo de um atendimento veterinário: cadastro de tutores e animais, fila de espera com prioridade para emergências, diagnóstico, prontuário, controle de estoque, alta e pagamento.

Todas as estruturas de dados (lista encadeada, fila, pilha e árvore) foram implementadas do zero, sem usar estruturas prontas do Python para resolver o problema. Apenas a biblioteca padrão é utilizada (`datetime`).

## 🚀 Como executar

Requisito: Python 3, sem dependências externas.

```bash
git clone https://github.com/Sarajnc/clinica_veterinaria.git
cd clinica_veterinaria
python3 main.py        # no Windows: py main.py
```

Menu principal: **1** Tutores e animais · **2** Atendimento e fila · **3** Prontuário e diagnóstico · **4** Estoque · **5** Alta e pagamento · **6** Relatório de pagamentos · **0** Sair

Os dados ficam apenas em memória e são perdidos ao encerrar o programa.

## 🗂️ Organização do código

```text
estruturas/   Estruturas genéricas, sem regras da clínica
  lista.py      No, ListaEncadeada
  fila.py       Fila
  pilha.py      Pilha
  arvore.py     NoArvore, Arvore
modelos/      Tutor, Animal, Atendimento, Prontuario, ItemProntuario,
              Pagamento, Produto, Lote, Perda
servicos/     Regras da clínica
  cadastro.py     Cadastro
  atendimento.py  GerenciadorAtendimentos
  diagnostico.py  Diagnostico
  estoque.py      GerenciadorEstoque
  clinica.py      Clinica (integra tudo)
main.py       Menu interativo
```

## 🧠 Combinações de estruturas

### 1. Atendimento com prioridade: Fila + Fila

- **Onde:** `GerenciadorAtendimentos` (`servicos/atendimento.py`), com `fila_emergencia` e `fila_normal`.
- **Métodos:** `adicionar_atendimento()` envia o atendimento para a fila correspondente. `proximo_atendimento()` retira da fila de emergência e, se ela estiver vazia, da fila normal. `Clinica.chamar_proximo_animal()` só chama alguém quando há consultório livre.
- **Por que:** cada fila preserva a ordem de chegada da sua categoria, e a prioridade vem da ordem em que as filas são consultadas. Tudo em O(1).
- **Desvantagem de uma fila só:** para uma emergência passar na frente, seria preciso percorrer a fila ou inserir no meio dela, O(n).

### 2. Tutores e animais: Lista de tutores + Lista de animais

- **Onde:** `Cadastro.tutores` é uma lista de `Tutor`, e cada `Tutor.animais` é outra lista.
- **Métodos:** `Cadastro.buscar(cpf, nome_animal)` localiza o tutor pelo CPF e depois chama `Tutor.buscar_animal()`, que percorre só os animais daquele tutor. `Tutor.adicionar_animal()` e `Tutor.remover_animal()` não têm limite de animais.
- **Por que:** a relação "um tutor, vários animais" fica na própria estrutura, e a busca do animal fica restrita ao tutor correto.
- **Desvantagem de uma lista só:** seria uma lista de animais com o CPF repetido, e toda busca teria que filtrar a lista inteira.

### 3. Estoque: Lista de produtos + Lista de lotes

- **Onde:** `GerenciadorEstoque.produtos` é uma lista de `Produto`, e cada `Produto` tem `lotes` e `perdas`, também listas.
- **Métodos:** `GerenciadorEstoque.retirar_estoque()` localiza o produto e chama `Produto.retirar_estoque()`, que consome os lotes a partir do início da lista. Como os lotes entram no fim, na ordem de compra, o primeiro é sempre o mais antigo. Antes da retirada, `Perda.descartar_lotes_vencidos()` remove os lotes vencidos e os registra em `Produto.perdas`.
- **Por que lista e não fila para os lotes:** lotes vencidos podem estar em qualquer posição, e o ajuste de inventário altera um lote específico. A lista permite remover ou alterar um lote do meio; uma fila só permite retirar do início.
- **Desvantagem de uma lista só para todos os lotes:** lotes de produtos diferentes ficariam misturados, e consultar ou retirar um produto exigiria percorrer todos os lotes da clínica.

### 4. Diagnóstico: Árvore + Lista de filhos

- **Onde:** `Arvore` e `NoArvore` (`estruturas/arvore.py`), montadas por `Diagnostico`. Cada `NoArvore` guarda seus filhos em uma `ListaEncadeada` (`NoArvore.filhos`).
- **O que a árvore representa:** o animal (raiz), seus sistemas (digestório, respiratório, pele) e seus órgãos ou estruturas (estômago, pulmões, unhas...). Cada nó tem estado **Saudável** ou **Alterado**, e os itens finais têm um código de identificação.
- **Métodos:** `Arvore.exibir()` percorre em pré-ordem, com indentação. `Arvore.marcar_alterado(codigo)` busca o nó pelo código, em profundidade, e muda o estado.
- **Por que:** a hierarquia animal → sistema → órgão é natural em uma árvore, e a lista de filhos permite que cada nó tenha de zero a N filhos.
- **Desvantagem de uma lista simples:** não representaria os níveis nem a relação entre sistemas e órgãos.

### 5. Prontuário: Listas + Pilha (desfazer)

- **Onde:** `Prontuario` mantém `medicamentos` e `procedimentos` (listas) e `historico_acoes` (pilha).
- **Métodos:** `adicionar_item()` e `remover_item()` empilham cada ação. `desfazer_ultima_acao()` desempilha a mais recente e faz o contrário: remove o item adicionado ou adiciona de volta o item removido. Só funciona com o prontuário aberto.
- **Por que:** a última ação feita é a primeira a ser desfeita (LIFO). Isso atende ao requisito de remover itens antes do fechamento, por exemplo quando o tutor não autoriza um procedimento.
- **Desvantagem de uma lista só:** o histórico ficaria misturado com os itens, e achar a última ação exigiria percorrer a lista inteira.

### 6. Finalização do atendimento

`Clinica.finalizar_atendimento()` usa várias estruturas na mesma operação: percorre os medicamentos do prontuário, confere o estoque de cada produto (combinação 3), baixa os medicamentos pelo lote mais antigo, registra o `Pagamento`, dá a alta e fecha o prontuário. Se o estoque for insuficiente, nada é baixado e o atendimento não é finalizado.

## ⏱️ Complexidade

| Operação | Custo |
|---|---|
| Inserir no fim da lista, enfileirar, desenfileirar, empilhar, desempilhar | O(1) |
| Buscar ou remover por critério na lista | O(n) |
| Buscar tutor e depois o animal | O(T + a) |
| Próximo atendimento (duas filas) | O(1) |
| Quantidade em estoque de um produto | O(L) |
| Retirar do estoque (produto + lotes) | O(P + L) |
| Desfazer última ação | O(n) se desfaz uma adição (remove da lista); O(1) se desfaz uma remoção |
| Exibir a árvore / marcar nó por código | O(N) |

T = tutores · a = animais do tutor · P = produtos · L = lotes do produto · n = itens da lista · N = nós da árvore

## 📜 Histórico de desenvolvimento

[Consultar histórico de commits](https://github.com/Sarajnc/clinica_veterinaria/commits/main)

---

**Projeto acadêmico — Estrutura de Dados | FATEC Rio Claro**
Desenvolvido por [Sarai Junco](https://github.com/Sarajnc).
