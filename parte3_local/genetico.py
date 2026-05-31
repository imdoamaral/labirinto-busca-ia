"""Algoritmo Genético (bônus, seção 6.3) para otimizar a ordem de coleta.

Trabalha sobre a mesma representação da busca local: um INDIVÍDUO é uma
permutação dos pontos de coleta, e seu "fitness" é o custo da rota C(s) (quanto
menor, melhor). A cada geração, evolui a população por seleção, cruzamento e
mutação, preservando o melhor indivíduo (elitismo).

Como cada indivíduo é uma permutação (cada ponto aparece uma só vez), os
operadores precisam preservar essa propriedade:
- cruzamento por ordem (OX): herda um trecho de um pai e completa com a ordem do
  outro pai, sem repetir pontos;
- mutação por troca: troca dois pontos de lugar.

Fonte primária: slide "Aula 05 - Algoritmos Genéticos".
"""
import random

from parte3_local.custo import custo_rota


def _selecao_torneio(populacao, custos, tamanho=3):
    """Sorteia `tamanho` indivíduos e devolve o de menor custo (seleção por torneio)."""
    competidores = random.sample(range(len(populacao)), tamanho)
    vencedor = min(competidores, key=lambda indice: custos[indice])
    return populacao[vencedor]


def _cruzamento_ordem(pai1, pai2):
    """Cruzamento por ordem (OX).

    Copia um trecho [i..j] do pai1 para o filho e preenche as posições restantes
    com os pontos do pai2, na ordem em que aparecem, pulando os já presentes.
    Isso gera um filho que continua sendo uma permutação válida.
    """
    n = len(pai1)
    i, j = sorted(random.sample(range(n), 2))

    filho = [None] * n
    filho[i:j + 1] = pai1[i:j + 1]                  # trecho herdado do pai1
    presentes = set(filho[i:j + 1])

    restantes = [ponto for ponto in pai2 if ponto not in presentes]
    indice = 0
    for posicao in range(n):
        if filho[posicao] is None:
            filho[posicao] = restantes[indice]
            indice += 1
    return filho


def _mutacao(individuo, taxa_mutacao):
    """Com probabilidade `taxa_mutacao`, troca dois pontos de lugar."""
    if random.random() < taxa_mutacao:
        i, j = random.sample(range(len(individuo)), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo


def algoritmo_genetico(coletas, distancias, inicio, objetivo,
                       tamanho_populacao=50, geracoes=100, taxa_mutacao=0.2):
    """Devolve (melhor_ordem, melhor_custo, historico_do_melhor_custo)."""
    def custo(ordem):
        return custo_rota(ordem, distancias, inicio, objetivo)

    # Com 0 ou 1 ponto de coleta não há o que permutar.
    if len(coletas) < 2:
        return list(coletas), custo(list(coletas)), [custo(list(coletas))]

    # População inicial: permutações aleatórias dos pontos de coleta.
    populacao = [random.sample(coletas, len(coletas)) for _ in range(tamanho_populacao)]
    custos = [custo(individuo) for individuo in populacao]

    melhor_indice = min(range(len(populacao)), key=lambda i: custos[i])
    melhor, melhor_custo = list(populacao[melhor_indice]), custos[melhor_indice]
    historico = [melhor_custo]

    for _ in range(geracoes):
        # Elitismo: o melhor indivíduo passa direto para a próxima geração.
        nova_populacao = [list(melhor)]
        while len(nova_populacao) < tamanho_populacao:
            pai1 = _selecao_torneio(populacao, custos)
            pai2 = _selecao_torneio(populacao, custos)
            filho = _mutacao(_cruzamento_ordem(pai1, pai2), taxa_mutacao)
            nova_populacao.append(filho)

        populacao = nova_populacao
        custos = [custo(individuo) for individuo in populacao]

        indice = min(range(len(populacao)), key=lambda i: custos[i])
        if custos[indice] < melhor_custo:
            melhor, melhor_custo = list(populacao[indice]), custos[indice]
        historico.append(melhor_custo)

    return melhor, melhor_custo, historico
