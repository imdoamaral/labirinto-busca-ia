"""Leitura e representação do labirinto.

Legenda dos caracteres da grade:
    '#'  parede / obstáculo (intransponível)
    ' '  célula livre        -> custo de entrada CUSTO_LIVRE
    '~'  terreno custoso (lama) -> custo de entrada CUSTO_LAMA
    'A'  posição inicial do agente
    'B'  objetivo final
    'C'  ponto de coleta obrigatório
    '?'  célula desconhecida (usada só no mapa interno do modo online)

As células 'A', 'B' e 'C' são transponíveis e têm custo de entrada igual ao de
uma célula livre; elas só marcam posições especiais. O terreno '~' (lama) existe
para que os custos variem e a Busca de Custo Uniforme (UCS) possa diferir da
Busca em Largura (BFS), como pede a questão de análise 5.4.3 do enunciado.
"""
from dataclasses import dataclass

# Custo de ENTRAR em cada tipo de célula transponível.
CUSTO_LIVRE = 1
CUSTO_LAMA = 3

PAREDE = "#"
LAMA = "~"
DESCONHECIDO = "?"


@dataclass
class Mapa:
    """Grade do labirinto e as posições de interesse já localizadas.

    As posições são tuplas (linha, coluna), com a linha crescendo para baixo.
    """
    grade: list[list[str]]            # grade[linha][coluna] -> caractere
    inicio: tuple[int, int] | None    # posição de 'A'
    objetivo: tuple[int, int] | None  # posição de 'B'
    coletas: list[tuple[int, int]]    # posições de todos os 'C'

    @property
    def linhas(self) -> int:
        return len(self.grade)

    @property
    def colunas(self) -> int:
        return len(self.grade[0]) if self.grade else 0

    def caractere(self, posicao: tuple[int, int]) -> str:
        linha, coluna = posicao
        return self.grade[linha][coluna]

    def dentro(self, posicao: tuple[int, int]) -> bool:
        """Indica se a posição está dentro dos limites da grade."""
        linha, coluna = posicao
        return 0 <= linha < self.linhas and 0 <= coluna < self.colunas

    def eh_parede(self, posicao: tuple[int, int]) -> bool:
        """Parede e célula desconhecida são tratadas como intransponíveis."""
        return self.caractere(posicao) in (PAREDE, DESCONHECIDO)

    def custo_entrada(self, posicao: tuple[int, int]) -> int:
        """Custo de mover-se PARA esta célula (assume que não é parede)."""
        return CUSTO_LAMA if self.caractere(posicao) == LAMA else CUSTO_LIVRE


def ler_de_texto(texto: str) -> Mapa:
    """Constrói um Mapa a partir do conteúdo textual do labirinto.

    Os espaços são significativos (representam células livres), por isso só
    removemos a quebra de linha final de cada linha, nunca os espaços internos.
    """
    linhas_texto = texto.split("\n")
    # Descarta uma eventual última linha vazia deixada pela quebra final.
    if linhas_texto and linhas_texto[-1] == "":
        linhas_texto.pop()

    grade: list[list[str]] = []
    inicio = objetivo = None
    coletas: list[tuple[int, int]] = []

    for indice_linha, conteudo in enumerate(linhas_texto):
        celulas = list(conteudo)
        for indice_coluna, caractere in enumerate(celulas):
            posicao = (indice_linha, indice_coluna)
            if caractere == "A":
                inicio = posicao
            elif caractere == "B":
                objetivo = posicao
            elif caractere == "C":
                coletas.append(posicao)
        grade.append(celulas)

    return Mapa(grade=grade, inicio=inicio, objetivo=objetivo, coletas=coletas)


def ler_de_arquivo(caminho_arquivo: str) -> Mapa:
    """Lê um labirinto de um arquivo de texto."""
    with open(caminho_arquivo, encoding="utf-8") as arquivo:
        return ler_de_texto(arquivo.read())
