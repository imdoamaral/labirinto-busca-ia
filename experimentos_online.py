"""Experimentos da Parte IV — busca online no labirinto desconhecido.

Roda o agente online (replanning com A*), coleta as métricas da seção 7.4 e
compara o trajeto real com o caminho ótimo calculado no mapa completo (offline).

Uso, a partir da raiz do projeto:
    python experimentos_online.py                 # mapas/exemplo.txt
    python experimentos_online.py mapas/X.txt
    python experimentos_online.py mapas/X.txt --animar   # trajetória passo a passo
"""
import sys
import time

from core import mapa as modulo_mapa
from core.problema import ProblemaLabirinto
from parte2_classica.buscas import a_estrela
from parte4_online.online import busca_online
from viz.render import imprimir_mapa


def animar(frames, intervalo=0.25):
    """Mostra a trajetória passo a passo no terminal (limpa a tela entre frames)."""
    for indice, quadro in enumerate(frames):
        print("\033[H\033[J", end="")          # move o cursor ao topo e limpa
        print(f"Passo {indice}/{len(frames) - 1}\n")
        print(quadro)
        time.sleep(intervalo)


def rodar(caminho_mapa, animacao=False):
    mapa_real = modulo_mapa.ler_de_arquivo(caminho_mapa)

    # Caminho ótimo offline (com o mapa completo), para comparação.
    _, metricas_offline = a_estrela(ProblemaLabirinto(mapa_real))
    custo_otimo = metricas_offline.custo

    resultado = busca_online(mapa_real, registrar_frames=animacao)

    if animacao:
        animar(resultado.frames)

    razao = resultado.custo_real / custo_otimo if custo_otimo else float("inf")

    print(f"Mapa: {caminho_mapa}")
    print(f"Início={mapa_real.inicio}  Objetivo={mapa_real.objetivo}\n")

    print("Métricas da busca online (seção 7.4):")
    print(f"  sucesso ................. {'sim' if resultado.sucesso else 'não'}")
    print(f"  movimentos .............. {resultado.movimentos}")
    print(f"  custo real percorrido ... {resultado.custo_real}")
    print(f"  células reveladas ....... {resultado.celulas_reveladas}")
    print(f"  células revisitadas ..... {resultado.celulas_revisitadas}")
    print(f"  replanejamentos ......... {resultado.replanejamentos}")
    print(f"  custo ótimo offline ..... {custo_otimo}")
    print(f"  razão online/offline .... {razao:.2f}")

    print("\nMapa interno final (? = não revelado, @ = agente, . = trajetória):\n")
    imprimir_mapa(resultado.mapa_interno, resultado.trajetoria,
                  agente=resultado.trajetoria[-1])


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--animar"]
    animacao = "--animar" in sys.argv
    caminho = args[0] if args else "mapas/exemplo.txt"
    rodar(caminho, animacao)
