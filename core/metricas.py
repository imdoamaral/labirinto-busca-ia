"""Coleta e apresentação das métricas de execução das buscas.

Métricas obrigatórias (seção 5.3 do enunciado):
    - encontrou solução?      -> sucesso
    - custo do caminho        -> custo
    - tamanho do caminho      -> passos (número de movimentos)
    - número de nós explorados-> explorados
    - número de nós expandidos-> expandidos
    - tempo de execução       -> tempo (em segundos)
    - tamanho máximo da fronteira -> fronteira_max

Convenção adotada (e que defendemos no relatório):
    - "explorados": nós retirados da fronteira para serem examinados;
    - "expandidos": nós que de fato geraram sucessores (todos os explorados,
       exceto o objetivo, que encerra a busca sem ser expandido).
"""
from dataclasses import dataclass


@dataclass
class Metricas:
    sucesso: bool = False
    custo: float = 0.0
    passos: int = 0
    explorados: int = 0
    expandidos: int = 0
    tempo: float = 0.0       # segundos
    fronteira_max: int = 0


# --- Apresentação em tabela (modelo da seção 5.3) --------------------------

_COLUNAS = ("Algoritmo", "Sucesso", "Custo", "Passos",
            "Explorados", "Expandidos", "Tempo(ms)", "Fronteira")
_LARGURAS = (10, 8, 7, 8, 11, 11, 10, 10)


def _formatar_linha(valores) -> str:
    return "".join(str(valor).ljust(largura)
                   for valor, largura in zip(valores, _LARGURAS))


def imprimir_tabela(resultados: dict) -> None:
    """Imprime a tabela comparativa.

    `resultados` mapeia nome do algoritmo -> Metricas.
    """
    print(_formatar_linha(_COLUNAS))
    print("-" * sum(_LARGURAS))
    for nome, m in resultados.items():
        print(_formatar_linha((
            nome,
            "sim" if m.sucesso else "não",
            m.custo,
            m.passos,
            m.explorados,
            m.expandidos,
            f"{m.tempo * 1000:.3f}",
            m.fronteira_max,
        )))
