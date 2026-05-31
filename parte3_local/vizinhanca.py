"""Definição da vizinhança para a busca local (seção 6.4).

Vizinhança escolhida: INVERSÃO DE UM TRECHO da ordem (movimento "2-opt"):
    [C1, C2, C3, C4, C5] -> [C1, C4, C3, C2, C5]

Justificativa: invertendo um trecho desfazemos "cruzamentos" da rota e
preservamos a maior parte da sequência de visitação, o que costuma ser mais
eficaz em problemas de ordenação (como este, parecido com o caixeiro-viajante)
do que a simples troca de dois pontos.
"""
import random


def vizinhos_por_inversao(ordem):
    """Gera todos os vizinhos invertendo cada trecho [i..j] da ordem.

    Usado pela subida de encosta, que examina toda a vizinhança a cada passo.
    """
    n = len(ordem)
    for i in range(n - 1):
        for j in range(i + 1, n):
            yield ordem[:i] + ordem[i:j + 1][::-1] + ordem[j + 1:]


def vizinho_aleatorio(ordem):
    """Devolve um único vizinho aleatório (inversão de um trecho sorteado).

    Usado pela têmpera simulada, que sorteia um vizinho por iteração.
    """
    i, j = sorted(random.sample(range(len(ordem)), 2))
    return ordem[:i] + ordem[i:j + 1][::-1] + ordem[j + 1:]
