"""Experimentos da Parte III — busca local com pontos de coleta.

Roda Hill-Climbing e Simulated Annealing em múltiplas execuções, coleta as
métricas da seção 6.5 e gera o gráfico de convergência iteração × melhor custo.

Uso, a partir da raiz do projeto:
    python experimentos_local.py
    python experimentos_local.py mapas/coletas.txt
"""
import sys
import time
import random
from itertools import permutations
from statistics import mean

from core import mapa as modulo_mapa
from parte3_local.distancias import calcular_distancias
from parte3_local.custo import custo_rota
from parte3_local.hill_climbing import hill_climbing
from parte3_local.simulated_annealing import simulated_annealing
from viz.graficos import plotar_convergencia

NUM_EXECUCOES = 30
SEMENTE = 42                 # fixa o acaso para os resultados serem reproduzíveis
FIGURA = "docs/figuras/convergencia_local.png"


def custo_otimo(coletas, distancias, inicio, objetivo):
    """Ótimo global por força bruta (viável porque há poucos pontos de coleta)."""
    return min(custo_rota(list(ordem), distancias, inicio, objetivo)
               for ordem in permutations(coletas))


def resumir(nome, custos, tempos, iteracoes, otimo):
    """Agrega as métricas da seção 6.5 de várias execuções."""
    sucessos = sum(1 for c in custos if c <= otimo)
    return {
        "metodo": nome,
        "melhor": min(custos),
        "pior": max(custos),
        "medio": mean(custos),
        "tempo_medio_ms": mean(tempos) * 1000,
        "iteracoes_medias": mean(iteracoes),
        "taxa_sucesso": sucessos / len(custos),
    }


def imprimir_resumo(linhas, otimo):
    print(f"\nÓtimo global (força bruta): {otimo}\n")
    cabecalho = ("Método", "Melhor", "Pior", "Médio", "Tempo(ms)",
                 "Iter.méd", "Sucesso")
    larguras = (20, 8, 8, 8, 11, 10, 9)

    def linha(valores):
        return "".join(str(v).ljust(w) for v, w in zip(valores, larguras))

    print(linha(cabecalho))
    print("-" * sum(larguras))
    for r in linhas:
        print(linha((
            r["metodo"], r["melhor"], r["pior"], f"{r['medio']:.1f}",
            f"{r['tempo_medio_ms']:.2f}", f"{r['iteracoes_medias']:.0f}",
            f"{r['taxa_sucesso'] * 100:.0f}%",
        )))


def rodar(caminho_mapa):
    random.seed(SEMENTE)
    mapa = modulo_mapa.ler_de_arquivo(caminho_mapa)
    inicio, objetivo, coletas = mapa.inicio, mapa.objetivo, mapa.coletas

    print(f"Mapa: {caminho_mapa}")
    print(f"Início={inicio}  Objetivo={objetivo}  Pontos de coleta={len(coletas)}")

    pontos = [inicio] + coletas + [objetivo]
    distancias = calcular_distancias(mapa, pontos)
    otimo = custo_otimo(coletas, distancias, inicio, objetivo)

    custos_hc, tempos_hc, iters_hc = [], [], []
    custos_sa, tempos_sa, iters_sa = [], [], []
    historico_hc = historico_sa = None

    for _ in range(NUM_EXECUCOES):
        ordem_inicial = random.sample(coletas, len(coletas))  # reinício aleatório

        t0 = time.perf_counter()
        _, custo_hc, hist_hc = hill_climbing(ordem_inicial, distancias, inicio, objetivo)
        tempos_hc.append(time.perf_counter() - t0)
        custos_hc.append(custo_hc)
        iters_hc.append(len(hist_hc) - 1)

        t0 = time.perf_counter()
        _, custo_sa, hist_sa = simulated_annealing(ordem_inicial, distancias, inicio, objetivo)
        tempos_sa.append(time.perf_counter() - t0)
        custos_sa.append(custo_sa)
        iters_sa.append(len(hist_sa) - 1)

        # Guarda a primeira execução como curva representativa do gráfico.
        if historico_hc is None:
            historico_hc, historico_sa = hist_hc, hist_sa

    resumo = [
        resumir("Hill-Climbing", custos_hc, tempos_hc, iters_hc, otimo),
        resumir("Simulated Annealing", custos_sa, tempos_sa, iters_sa, otimo),
    ]
    imprimir_resumo(resumo, otimo)

    plotar_convergencia(
        {"Hill-Climbing": historico_hc, "Simulated Annealing": historico_sa},
        FIGURA, titulo="Convergência da busca local (iteração × melhor custo)")
    print(f"\nGráfico de convergência salvo em: {FIGURA}")

    analise_sensibilidade(coletas, distancias, inicio, objetivo, otimo)


def analise_sensibilidade(coletas, distancias, inicio, objetivo, otimo):
    """Mede o efeito da temperatura inicial e da taxa de resfriamento no SA
    (questões 6.6.3 e 6.6.4)."""
    print("\nSensibilidade do Simulated Annealing (taxa de sucesso em atingir o ótimo):")
    cabecalho = ("Temp.inicial", "Taxa resfr.", "Médio", "Sucesso")
    larguras = (14, 13, 8, 9)

    def linha(valores):
        return "".join(str(v).ljust(w) for v, w in zip(valores, larguras))

    print(linha(cabecalho))
    print("-" * sum(larguras))
    for temp_inicial in (1.0, 10.0, 100.0, 1000.0):
        for taxa in (0.90, 0.99, 0.999):
            custos = []
            for _ in range(NUM_EXECUCOES):
                ordem_inicial = random.sample(coletas, len(coletas))
                _, custo, _ = simulated_annealing(
                    ordem_inicial, distancias, inicio, objetivo,
                    temp_inicial=temp_inicial, taxa_resfriamento=taxa)
                custos.append(custo)
            sucesso = sum(1 for c in custos if c <= otimo) / len(custos)
            print(linha((temp_inicial, taxa, f"{mean(custos):.1f}",
                         f"{sucesso * 100:.0f}%")))


if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else "mapas/coletas.txt"
    rodar(caminho)
