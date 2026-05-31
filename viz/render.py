"""Visualização do labirinto no terminal.

Suficiente para inspecionar mapas e caminhos durante o desenvolvimento e para
a trajetória passo a passo do modo online. As figuras do relatório (curva de
convergência, heatmap de nós expandidos) serão feitas com matplotlib na Parte III.
"""

PASSO_CAMINHO = "."   # marca as células do caminho que não são A/B/C
AGENTE = "@"          # posição atual do agente (usada no modo online)


def desenhar_mapa(mapa, caminho=None, agente=None) -> str:
    """Devolve uma representação textual do mapa.

    - `caminho`: células visitadas viram '.', preservando 'A', 'B' e 'C'.
    - `agente`: se informado, marca a posição atual com '@' (modo online).
    No modo online, as células ainda desconhecidas aparecem como '?'.
    """
    no_caminho = set(caminho) if caminho else set()
    linhas_desenhadas = []
    for indice_linha, linha in enumerate(mapa.grade):
        celulas = []
        for indice_coluna, caractere in enumerate(linha):
            posicao = (indice_linha, indice_coluna)
            if posicao == agente:
                celulas.append(AGENTE)
            elif posicao in no_caminho and caractere == " ":
                celulas.append(PASSO_CAMINHO)
            else:
                celulas.append(caractere)
        linhas_desenhadas.append("".join(celulas))
    return "\n".join(linhas_desenhadas)


def imprimir_mapa(mapa, caminho=None, agente=None) -> None:
    print(desenhar_mapa(mapa, caminho, agente))
