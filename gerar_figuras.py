"""Gera as figuras coloridas (PNG estático + GIF animado) das três partes.

Uso, a partir da raiz do projeto:
    python gerar_figuras.py            # gera tudo em docs/figuras/
    python gerar_figuras.py parte2     # só uma parte (parte2 | parte3 | parte4)

Os PNG são as figuras que entram no relatório (PDF não embeda animação); os GIF
servem para o repositório/README. A animação AO VIVO no terminal fica nos
experimentos (experimentos*.py com a opção --animar).
"""
import os
import sys
from itertools import permutations

from core import mapa as modulo_mapa
from core.problema import ProblemaLabirinto
from parte2_classica.buscas import ALGORITMOS
from parte3_local.distancias import calcular_distancias, caminho_rota
from parte3_local.custo import custo_rota
from parte4_online.online import busca_online
from viz.figuras import desenhar_percurso, animar_exploracao, animar_online

DIR_FIGURAS = "docs/figuras"

MAPAS_PARTE2 = ["mapas/exemplo.txt", "mapas/armadilha_gulosa.txt"]
MAPA_PARTE3 = "mapas/coletas.txt"
MAPA_PARTE4 = "mapas/online_armadilha.txt"


def _nome_base(caminho_mapa):
    return os.path.splitext(os.path.basename(caminho_mapa))[0]


def gerar_parte2():
    """Para cada mapa e cada algoritmo: PNG (percurso + exploração) e GIF."""
    saida = os.path.join(DIR_FIGURAS, "parte2")
    for caminho_mapa in MAPAS_PARTE2:
        mapa = modulo_mapa.ler_de_arquivo(caminho_mapa)
        base = _nome_base(caminho_mapa)
        for nome, algoritmo in ALGORITMOS.items():
            traco = []
            caminho, _ = algoritmo(ProblemaLabirinto(mapa), traco)
            rotulo = nome.replace("*", "estrela")     # 'A*' -> nome de arquivo
            titulo = f"{nome} — {base}"
            desenhar_percurso(mapa, caminho,
                              os.path.join(saida, f"{base}_{rotulo}.png"),
                              titulo=titulo, explorados=traco)
            animar_exploracao(mapa, traco, caminho,
                              os.path.join(saida, f"{base}_{rotulo}.gif"),
                              titulo=titulo)
            print(f"  Parte II: {base} / {nome}")


def gerar_parte3():
    """Rota ótima visitando todos os C: PNG e GIF traçando o percurso."""
    saida = os.path.join(DIR_FIGURAS, "parte3")
    mapa = modulo_mapa.ler_de_arquivo(MAPA_PARTE3)
    inicio, objetivo, coletas = mapa.inicio, mapa.objetivo, mapa.coletas

    distancias = calcular_distancias(mapa, [inicio] + coletas + [objetivo])
    # Ordem ótima por força bruta (poucos pontos), igual ao experimento da Parte III.
    ordem = min(permutations(coletas),
                key=lambda o: custo_rota(list(o), distancias, inicio, objetivo))
    custo = custo_rota(list(ordem), distancias, inicio, objetivo)

    caminho = caminho_rota(mapa, ordem, inicio, objetivo)
    titulo = f"Rota ótima das coletas (custo {custo})"
    desenhar_percurso(mapa, caminho, os.path.join(saida, "rota_otima.png"),
                      titulo=titulo)
    animar_exploracao(mapa, [], caminho, os.path.join(saida, "rota_otima.gif"),
                      titulo=titulo)
    print(f"  Parte III: rota ótima (custo {custo})")


def gerar_parte4():
    """Agente online: PNG do mapa interno final e GIF revelando o labirinto."""
    saida = os.path.join(DIR_FIGURAS, "parte4")
    mapa = modulo_mapa.ler_de_arquivo(MAPA_PARTE4)
    resultado = busca_online(mapa)
    desenhar_percurso(resultado.mapa_interno, resultado.trajetoria,
                      os.path.join(saida, "online_final.png"),
                      titulo="Busca online — mapa interno final")
    animar_online(mapa, resultado.trajetoria,
                  os.path.join(saida, "online.gif"), titulo="Busca online")
    print(f"  Parte IV: {resultado.movimentos} movimentos, "
          f"{resultado.replanejamentos} replanejamentos")


GERADORES = {"parte2": gerar_parte2, "parte3": gerar_parte3, "parte4": gerar_parte4}


def main(alvos):
    for alvo in alvos or list(GERADORES):
        if alvo not in GERADORES:
            print(f"Alvo desconhecido: {alvo}. Use um de: {', '.join(GERADORES)}")
            continue
        print(f"Gerando {alvo}...")
        GERADORES[alvo]()
    print(f"\nFiguras salvas em {DIR_FIGURAS}/")


if __name__ == "__main__":
    main(sys.argv[1:])
