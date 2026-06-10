"""Formulação formal do problema de busca no labirinto.

Modela a tupla <S, A, T, s0, G, c> exigida na seção 5.1 do enunciado:

    S  : conjunto de posições livres (não-parede) da grade
    A  : ações ortogonais {direita, esquerda, baixo, cima}
    T  : função de transição -> dado um estado, quais sucessores são válidos
    s0 : posição inicial (a célula 'A')
    G  : teste de objetivo -> alcançar a célula 'B'
    c  : custo de cada movimento -> custo de entrar na célula de destino

Um "estado" é simplesmente a posição (linha, coluna) do agente na grade.
"""

# Ações ortogonais representadas como deslocamentos (delta_linha, delta_coluna).
# A linha cresce para baixo, então "cima" subtrai da linha.
#
# A ORDEM aqui é a convenção de varredura da árvore de estados: é nela que os
# sucessores são gerados e, portanto, ela governa o desempate de todas as buscas
# (na DFS é o que mais aparece). Adotamos HORIZONTAL primeiro (direita, esquerda)
# e só então vertical (baixo, cima). Assim a DFS "corre reto até a parede" antes
# de desviar, o que torna a visualização bem mais intuitiva — em vez de
# serpentear de cima para baixo a cada coluna num corredor horizontal.
ACOES = {
    "direita": (0, 1),
    "esquerda": (0, -1),
    "baixo": (1, 0),
    "cima": (-1, 0),
}


class ProblemaLabirinto:
    """Problema de ir de uma posição inicial até um objetivo no labirinto."""

    def __init__(self, mapa, inicio=None, objetivo=None):
        # Permitimos sobrescrever início/objetivo para reutilizar o mesmo mapa
        # em subproblemas (útil na Parte III, ao calcular distâncias entre
        # pares de pontos de coleta).
        self.mapa = mapa
        self.inicio = inicio if inicio is not None else mapa.inicio
        self.objetivo = objetivo if objetivo is not None else mapa.objetivo

    def objetivo_atingido(self, estado) -> bool:
        """Teste de objetivo G: o agente chegou na célula-alvo?"""
        return estado == self.objetivo

    def sucessores(self, estado):
        """Função de transição T.

        Gera tuplas (acao, novo_estado, custo) para cada movimento que cai
        dentro da grade e não esbarra em parede.
        """
        linha, coluna = estado
        for acao, (delta_linha, delta_coluna) in ACOES.items():
            destino = (linha + delta_linha, coluna + delta_coluna)
            if self.mapa.dentro(destino) and not self.mapa.eh_parede(destino):
                yield acao, destino, self.mapa.custo_entrada(destino)

    def heuristica(self, estado) -> int:
        """Distância de Manhattan do estado até o objetivo (seção 5.2).

        É admissível (nunca superestima o custo real): ela conta o número
        mínimo de passos ignorando paredes, e como o menor custo possível por
        passo é 1, esse valor nunca passa do custo verdadeiro do caminho.
        Logo, garante que o A* encontre o caminho ótimo.
        """
        linha, coluna = estado
        linha_objetivo, coluna_objetivo = self.objetivo
        return abs(linha - linha_objetivo) + abs(coluna - coluna_objetivo)
