"""Representação da solução e função de custo da Parte III.

Uma solução candidata é a ORDEM de visitação dos pontos de coleta (seção 6.1):
    ordem = [C3, C1, C4, C2]  ->  A -> C3 -> C1 -> C4 -> C2 -> B

O custo total (seção 6.2) é:
    C(s) = d(A, ordem[0]) + Σ d(ordem[i], ordem[i+1]) + d(ordem[-1], B)
usando as distâncias pré-calculadas (menor caminho real entre os pontos).
"""


def custo_rota(ordem, distancias, inicio, objetivo):
    """Custo total de sair de `inicio`, visitar os pontos na `ordem` e ir a `objetivo`."""
    if not ordem:                       # nenhum ponto de coleta: vai direto A -> B
        return distancias[(inicio, objetivo)]

    total = distancias[(inicio, ordem[0])]
    # zip(ordem, ordem[1:]) percorre os pares consecutivos da ordem.
    for atual, proximo in zip(ordem, ordem[1:]):
        total += distancias[(atual, proximo)]
    total += distancias[(ordem[-1], objetivo)]
    return total
