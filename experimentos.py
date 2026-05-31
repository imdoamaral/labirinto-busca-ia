"""Roda as cinco buscas clássicas no mapa de exemplo e imprime a tabela
comparativa (modelo da seção 5.3 do enunciado).

Uso, a partir da raiz do projeto:
    python experimentos.py
    python experimentos.py mapas/outro_mapa.txt
    python experimentos.py mapas/outro_mapa.txt --animar   # exploração no terminal
"""
import sys

from core import mapa as modulo_mapa
from core.problema import ProblemaLabirinto
from parte2_classica.buscas import ALGORITMOS
from core.metricas import imprimir_tabela
from viz.render import imprimir_mapa, construir_quadros, animar_terminal


def animar_buscas(mapa) -> None:
    """Mostra, no terminal, a ordem de exploração de cada algoritmo, uma após a
    outra. Deixa ver as diferenças: BFS em camadas, DFS afundando, Gulosa indo
    reto ao objetivo, A* focado mas ótimo."""
    for nome, algoritmo in ALGORITMOS.items():
        traco = []
        caminho, _ = algoritmo(ProblemaLabirinto(mapa), traco)
        quadros = construir_quadros(traco, caminho)
        animar_terminal(mapa, quadros, titulo=f"{nome} — exploração")


def rodar(caminho_mapa: str, animacao: bool = False) -> None:
    mapa = modulo_mapa.ler_de_arquivo(caminho_mapa)
    problema = ProblemaLabirinto(mapa)

    print(f"Mapa: {caminho_mapa}  (início={mapa.inicio}, objetivo={mapa.objetivo})\n")
    imprimir_mapa(mapa)
    print()

    resultados = {}
    caminho_a_estrela = None
    for nome, algoritmo in ALGORITMOS.items():
        caminho, metricas = algoritmo(problema)
        resultados[nome] = metricas
        if nome == "A*":
            caminho_a_estrela = caminho

    imprimir_tabela(resultados)

    if caminho_a_estrela:
        print("\nCaminho encontrado pelo A*:\n")
        imprimir_mapa(mapa, caminho_a_estrela)

    if animacao:
        animar_buscas(mapa)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--animar"]
    animacao = "--animar" in sys.argv
    caminho = args[0] if args else "mapas/exemplo.txt"
    rodar(caminho, animacao)
