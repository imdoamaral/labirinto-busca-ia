"""Figuras coloridas do labirinto (matplotlib), para o relatório e o repositório.

A partir de um `Mapa` e dos dados que as buscas já produzem (ordem de exploração
e caminho final), gera:
  - `desenhar_percurso()` : PNG estático com terreno + células exploradas +
    caminho. É a figura que vai DENTRO do relatório (PDF não embeda animação);
  - `animar_exploracao()` : GIF mostrando a fronteira crescer na ordem de
    exploração e, no fim, o caminho ser traçado (bom para o README do repo).

Backend "Agg" (salva em arquivo, sem abrir janela), igual a `graficos.py`. Os
quadros da animação são montados por `viz.render.construir_quadros`, os mesmos
usados pela animação de terminal — as duas versões ficam sempre em sincronia.
"""
import os

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["hatch.linewidth"] = 0.8     # hachura fina das células exploradas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D

from core.mapa import PAREDE, LAMA, DESCONHECIDO
from viz.render import construir_quadros

# Terreno -> índice de cor. ' ', 'A', 'B' e 'C' caem no 0 (livre); os marcos
# A/B/C são desenhados por cima.
_CODIGO_TERRENO = {PAREDE: 1, LAMA: 2, DESCONHECIDO: 3}
_PALETA = ListedColormap(["#ffffff", "#3b3b3b", "#c8a165", "#d9d9d9"])
#                          livre      parede     lama       desconhecido

# Células exploradas: hachura azul POR CIMA do terreno (não o preenche), para a
# lama continuar visivelmente bege e ainda assim se ver que foi explorada — um
# preenchimento translúcido misturava as cores e deixava a lama acinzentada.
_COR_EXPLORADO = "#1f6fd6"                     # azul da hachura das exploradas
_HACHURA_EXPLORADO = "////"
_COR_CAMINHO = "#e8000b"                      # linha do caminho final
_COR_INICIO = "#1f9e3a"                       # marco 'A'
_COR_OBJETIVO = "#e8000b"                      # marco 'B'
_COR_COLETA = "#ff8c00"                        # marcos 'C'


def _xy(posicao):
    """(linha, coluna) -> (x, y) do matplotlib (x = coluna, y = linha)."""
    linha, coluna = posicao
    return coluna, linha


def _figsize(mapa, escala=0.5):
    """Tamanho da figura proporcional à grade, com um mínimo legível."""
    return (max(4.0, mapa.colunas * escala), max(3.0, mapa.linhas * escala))


def _matriz_terreno(mapa):
    """Grade de caracteres -> matriz de índices de cor da paleta."""
    return [[_CODIGO_TERRENO.get(c, 0) for c in linha] for linha in mapa.grade]


def _marcar_explorados(ax, explorados):
    """Hachura azul sobre cada célula explorada, sem preencher o terreno."""
    for linha, coluna in explorados or []:
        ax.add_patch(Rectangle(
            (coluna - 0.5, linha - 0.5), 1, 1, facecolor="none",
            edgecolor=_COR_EXPLORADO, hatch=_HACHURA_EXPLORADO,
            linewidth=0.0, zorder=2))


def _preparar_eixo(ax, mapa, titulo):
    """Desenha o terreno base e configura o eixo (sem ticks, grade fina)."""
    ax.imshow(_matriz_terreno(mapa), cmap=_PALETA, vmin=0, vmax=3)
    ax.set_title(titulo)
    ax.set_xticks([])
    ax.set_yticks([])
    # Linhas finas nas bordas das células, para leitura.
    ax.set_xticks([x - 0.5 for x in range(mapa.colunas + 1)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(mapa.linhas + 1)], minor=True)
    ax.grid(which="minor", color="#cccccc", linewidth=0.5)


def _marcar_pontos(ax, mapa):
    """Marca A (início), B (objetivo) e os C (coletas) por cima do terreno."""
    if mapa.inicio:
        x, y = _xy(mapa.inicio)
        ax.scatter([x], [y], c=_COR_INICIO, s=180, marker="o",
                   edgecolors="black", zorder=5, label="A (início)")
    if mapa.objetivo:
        x, y = _xy(mapa.objetivo)
        ax.scatter([x], [y], c=_COR_OBJETIVO, s=240, marker="*",
                   edgecolors="black", zorder=5, label="B (objetivo)")
    if mapa.coletas:
        xs = [c for _, c in mapa.coletas]
        ys = [l for l, _ in mapa.coletas]
        ax.scatter(xs, ys, c=_COR_COLETA, s=120, marker="s",
                   edgecolors="black", zorder=5, label="C (coleta)")


def _desenhar_caminho(ax, caminho):
    """Traça o caminho como uma linha sobre a grade."""
    if not caminho:
        return
    xs = [c for _, c in caminho]
    ys = [l for l, _ in caminho]
    ax.plot(xs, ys, color=_COR_CAMINHO, linewidth=2.5, zorder=4,
            solid_capstyle="round", solid_joinstyle="round")


def desenhar_percurso(mapa, caminho, caminho_saida, titulo="Percurso",
                      explorados=None):
    """Salva um PNG com o terreno, as células exploradas e o caminho final.

    `explorados` é opcional (lista/iterável de posições); quando informado,
    hachura o conjunto de nós que a busca explorou.
    """
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    fig, ax = plt.subplots(figsize=_figsize(mapa))
    _preparar_eixo(ax, mapa, titulo)
    _marcar_explorados(ax, explorados)
    _desenhar_caminho(ax, caminho)
    _marcar_pontos(ax, mapa)

    # Legenda: marcos A/B/C (automáticos) + exploração e caminho (proxies).
    handles, _ = ax.get_legend_handles_labels()
    if explorados:
        handles.append(Patch(facecolor="white", edgecolor=_COR_EXPLORADO,
                             hatch=_HACHURA_EXPLORADO, label="explorado"))
    if caminho:
        handles.append(Line2D([], [], color=_COR_CAMINHO, lw=2.5,
                              label="caminho"))
    ax.legend(handles=handles, loc="center left",
              bbox_to_anchor=(1.01, 0.5), fontsize=8)
    fig.tight_layout()
    fig.savefig(caminho_saida, dpi=130, bbox_inches="tight")
    plt.close(fig)


def animar_exploracao(mapa, ordem_exploracao, caminho, caminho_saida,
                      titulo="Exploração", fps=8, segundos_no_fim=1.5):
    """Salva um GIF animando a exploração e, no fim, o traçado do caminho.

    Reaproveita os mesmos quadros da animação de terminal. Se `ordem_exploracao`
    vier vazia, anima apenas o caminho (usado pela rota da Parte III).
    """
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    quadros = construir_quadros(ordem_exploracao, caminho)
    # Segura o último quadro por alguns instantes antes do GIF reiniciar.
    quadros += [quadros[-1]] * int(fps * segundos_no_fim)

    fig, ax = plt.subplots(figsize=_figsize(mapa))

    def desenhar(indice):
        explorados, caminho_parcial = quadros[indice]
        ax.clear()
        _preparar_eixo(ax, mapa, titulo)
        _marcar_explorados(ax, explorados)
        _desenhar_caminho(ax, caminho_parcial)
        _marcar_pontos(ax, mapa)

    animacao = FuncAnimation(fig, desenhar, frames=len(quadros),
                             interval=1000 / fps)
    animacao.save(caminho_saida, writer=PillowWriter(fps=fps))
    plt.close(fig)


def animar_online(mapa_real, trajetoria, caminho_saida,
                  titulo="Busca online", fps=4, segundos_no_fim=1.5):
    """Salva um GIF do agente online revelando o mapa e replanejando.

    Reconstrói, só a partir da `trajetoria`, o que o agente conhecia a cada
    passo: as células reveladas são a própria trajetória e seus vizinhos
    (percepção de raio 1). O que ainda não foi revelado aparece como '?'.
    """
    from core.mapa import Mapa
    from core.problema import ACOES

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    fig, ax = plt.subplots(figsize=_figsize(mapa_real))

    def revelados_ate(passo):
        """Conjunto de células conhecidas após `passo` movimentos."""
        conhecidas = set()
        for posicao in trajetoria[:passo + 1]:
            linha, coluna = posicao
            vizinhos = [posicao] + [(linha + dl, coluna + dc)
                                    for dl, dc in ACOES.values()]
            conhecidas.update(c for c in vizinhos if mapa_real.dentro(c))
        return conhecidas

    def mapa_conhecido(conhecidas):
        """Mapa interno: terreno real onde revelado, '?' no resto."""
        grade = [[mapa_real.grade[l][c] if (l, c) in conhecidas else DESCONHECIDO
                  for c in range(mapa_real.colunas)]
                 for l in range(mapa_real.linhas)]
        return Mapa(grade=grade, inicio=mapa_real.inicio,
                    objetivo=mapa_real.objetivo, coletas=[])

    quadros = list(range(len(trajetoria)))
    quadros += [quadros[-1]] * int(fps * segundos_no_fim)

    def desenhar(indice):
        passo = quadros[indice]
        mapa_passo = mapa_conhecido(revelados_ate(passo))
        ax.clear()
        _preparar_eixo(ax, mapa_passo, f"{titulo} — passo {passo}")
        _desenhar_caminho(ax, trajetoria[:passo + 1])
        _marcar_pontos(ax, mapa_passo)
        # Posição atual do agente.
        x, y = _xy(trajetoria[passo])
        ax.scatter([x], [y], c="black", s=90, marker="D", zorder=6)

    animacao = FuncAnimation(fig, desenhar, frames=len(quadros),
                             interval=1000 / fps)
    animacao.save(caminho_saida, writer=PillowWriter(fps=fps))
    plt.close(fig)
