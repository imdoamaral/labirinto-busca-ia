"""Gráficos do relatório (matplotlib).

A seção 6.5 do enunciado exige pelo menos o gráfico iteração × melhor custo.
Usamos o backend "Agg" para salvar a figura em arquivo sem abrir janela.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plotar_convergencia(historicos, caminho_saida, titulo="Convergência"):
    """Plota a curva iteração × melhor custo de cada método.

    `historicos` é um dicionário nome_do_metodo -> lista de custos por iteração.
    """
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    plt.figure(figsize=(8, 5))
    for nome, historico in historicos.items():
        plt.plot(historico, label=nome)
    plt.xlabel("Iteração")
    plt.ylabel("Melhor custo")
    plt.title(titulo)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=120)
    plt.close()
