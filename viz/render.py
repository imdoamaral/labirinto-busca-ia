"""Visualização do labirinto no terminal.

Suficiente para inspecionar mapas e caminhos durante o desenvolvimento, para a
trajetória passo a passo do modo online e para animar, em ASCII, a ORDEM de
exploração das buscas (sem nenhuma dependência externa). As versões coloridas
em PNG/GIF ficam em `viz/figuras.py` (matplotlib).
"""
import time

PASSO_CAMINHO = "."   # marca as células do caminho que não são A/B/C
EXPLORADO = "·"       # célula já explorada (retirada da fronteira)
AGENTE = "@"          # posição atual / último nó explorado


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


# --- Animação da exploração (compartilhada entre terminal e figuras) -------

def construir_quadros(ordem_exploracao, caminho):
    """Monta a sequência de quadros de uma busca para animação.

    Cada quadro é uma tupla (explorados, caminho_parcial). Primeiro a fronteira
    cresce — os nós aparecem na ordem em que foram explorados, com o caminho
    ainda vazio; depois, sobre o conjunto final de explorados, o caminho é
    traçado célula a célula. Nós reabertos (que não acrescentam célula nova) são
    ignorados, para a animação não ficar parada em quadros idênticos.

    Se `ordem_exploracao` vier vazia, sobra só o traçado do caminho — é o que a
    Parte III usa para animar a rota final, que não tem exploração espacial.
    """
    quadros = []
    explorados = []
    vistos = set()
    for estado in ordem_exploracao or []:
        if estado in vistos:
            continue
        vistos.add(estado)
        explorados = explorados + [estado]      # snapshot do acumulado
        quadros.append((explorados, []))

    for i in range(len(caminho or [])):
        quadros.append((explorados, caminho[:i + 1]))
    return quadros


def desenhar_exploracao(mapa, explorados=None, caminho=None, atual=None) -> str:
    """Desenho textual de um quadro de busca.

    As marcas entram sobre as células transponíveis "anônimas" — livre (' ') e
    lama ('~') —, com precedência caminho ('.') > posição atual ('@') >
    explorado ('·'). Assim dá para ver a busca avançar pela lama; a distinção do
    terreno fica preservada na versão colorida (PNG/GIF). Paredes e os marcos
    A/B/C são sempre mantidos.
    """
    no_caminho = set(caminho) if caminho else set()
    explorado = set(explorados) if explorados else set()
    linhas_desenhadas = []
    for indice_linha, linha in enumerate(mapa.grade):
        celulas = []
        for indice_coluna, caractere in enumerate(linha):
            posicao = (indice_linha, indice_coluna)
            anonima = caractere in (" ", "~")
            if anonima and posicao in no_caminho:
                celulas.append(PASSO_CAMINHO)
            elif anonima and posicao == atual:
                celulas.append(AGENTE)
            elif anonima and posicao in explorado:
                celulas.append(EXPLORADO)
            else:
                celulas.append(caractere)
        linhas_desenhadas.append("".join(celulas))
    return "\n".join(linhas_desenhadas)


def animar_terminal(mapa, quadros, intervalo=0.12, titulo="Exploração") -> None:
    """Roda a animação de `quadros` no terminal (limpa a tela entre quadros)."""
    for indice, (explorados, caminho_parcial) in enumerate(quadros):
        # Destaca o "agente": o último passo do caminho, ou o último nó explorado.
        atual = caminho_parcial[-1] if caminho_parcial else (
            explorados[-1] if explorados else None)
        print("\033[H\033[J", end="")               # cursor ao topo e limpa
        print(f"{titulo}  —  quadro {indice + 1}/{len(quadros)}\n")
        print(desenhar_exploracao(mapa, explorados, caminho_parcial, atual))
        time.sleep(intervalo)
