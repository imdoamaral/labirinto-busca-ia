"""Roda as cinco buscas clássicas no mapa de exemplo e imprime a tabela
comparativa (modelo da seção 5.3 do enunciado).

Uso, a partir da raiz do projeto:
    python experimentos.py
    python experimentos.py mapas/outro_mapa.txt
"""
import sys

from core import mapa as modulo_mapa
from core.problema import ProblemaLabirinto
from parte2_classica.buscas import ALGORITMOS
from core.metricas import imprimir_tabela
from viz.render import imprimir_mapa


def rodar(caminho_mapa: str) -> None:
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


if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else "mapas/exemplo.txt"
    rodar(caminho)
