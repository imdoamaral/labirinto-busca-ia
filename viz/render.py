"""Visualização do labirinto no terminal.

Suficiente para inspecionar mapas e caminhos durante o desenvolvimento e para
a trajetória passo a passo do modo online. As figuras do relatório (curva de
convergência, heatmap de nós expandidos) serão feitas com matplotlib na Parte III.
"""

PASSO_CAMINHO = "."   # marca as células do caminho que não são A/B/C


def desenhar_mapa(mapa, caminho=None) -> str:
    """Devolve uma representação textual do mapa, opcionalmente com o caminho.

    As células do caminho viram '.', preservando 'A', 'B' e 'C' por cima para
    que continue legível onde o agente começa, termina e coleta.
    """
    no_caminho = set(caminho) if caminho else set()
    linhas_desenhadas = []
    for indice_linha, linha in enumerate(mapa.grade):
        celulas = []
        for indice_coluna, caractere in enumerate(linha):
            posicao = (indice_linha, indice_coluna)
            if posicao in no_caminho and caractere == " ":
                celulas.append(PASSO_CAMINHO)
            else:
                celulas.append(caractere)
        linhas_desenhadas.append("".join(celulas))
    return "\n".join(linhas_desenhadas)


def imprimir_mapa(mapa, caminho=None) -> None:
    print(desenhar_mapa(mapa, caminho))
