"""Busca online no labirinto desconhecido (Parte IV) — Replanning com A*.

Ciclo a cada passo (seção 7.2):
    perceber -> atualizar mapa interno -> planejar -> agir.

Premissas (declaradas para a defesa): o agente conhece o TAMANHO do labirinto e
as posições de início e objetivo, mas NÃO conhece as paredes. O mapa interno
começa todo desconhecido ('?') e é revelado conforme ele se move (percepção de
raio 1: a célula atual e seus 4 vizinhos ortogonais).

Estratégia (Opção A do enunciado): a cada passo o agente roda A* sobre o mapa
interno assumindo que o desconhecido é livre ("free-space assumption"), executa
APENAS o primeiro passo do plano e replaneja. Como ele percebe os vizinhos antes
de agir, nunca anda para dentro de uma parede; porém pode descobrir paredes mais
à frente e ter de replanejar, o que pode tornar o trajeto real mais caro que o
ótimo calculado com o mapa completo (daí a razão online/offline ≥ 1).
"""
from dataclasses import dataclass, field

from core.mapa import Mapa, PAREDE, DESCONHECIDO
from core.problema import ACOES
from parte2_classica.buscas import a_estrela
from viz.render import desenhar_mapa


class ProblemaOnline:
    """Planejamento sobre o mapa interno, tratando o desconhecido como livre.

    Tem a mesma interface que `ProblemaLabirinto` (inicio, objetivo_atingido,
    heuristica, sucessores e o atributo `mapa`), então é resolvido pelo mesmo
    A* da Parte II.
    """

    def __init__(self, mapa_interno, inicio, objetivo):
        self.mapa = mapa_interno
        self.inicio = inicio
        self.objetivo = objetivo

    def objetivo_atingido(self, estado):
        return estado == self.objetivo

    def heuristica(self, estado):
        linha, coluna = estado
        linha_obj, coluna_obj = self.objetivo
        return abs(linha - linha_obj) + abs(coluna - coluna_obj)

    def sucessores(self, estado):
        linha, coluna = estado
        for acao, (delta_linha, delta_coluna) in ACOES.items():
            destino = (linha + delta_linha, coluna + delta_coluna)
            if not self.mapa.dentro(destino):
                continue
            # Só paredes CONHECIDAS bloqueiam; o desconhecido ('?') é livre.
            if self.mapa.caractere(destino) == PAREDE:
                continue
            yield acao, destino, self.mapa.custo_entrada(destino)


@dataclass
class ResultadoOnline:
    sucesso: bool
    movimentos: int
    custo_real: float
    celulas_reveladas: int
    celulas_revisitadas: int
    replanejamentos: int
    trajetoria: list
    mapa_interno: Mapa
    frames: list = field(default_factory=list)


def _criar_mapa_interno(mapa_real):
    """Mapa interno do mesmo tamanho do real, porém todo desconhecido ('?')."""
    grade = [[DESCONHECIDO] * mapa_real.colunas for _ in range(mapa_real.linhas)]
    return Mapa(grade=grade, inicio=mapa_real.inicio,
                objetivo=mapa_real.objetivo, coletas=[])


def _revelar(mapa_real, mapa_interno, posicao, revelados):
    """Copia para o mapa interno a célula atual e seus 4 vizinhos (raio 1)."""
    linha, coluna = posicao
    vizinhanca = [posicao]
    vizinhanca += [(linha + dl, coluna + dc) for dl, dc in ACOES.values()]
    for celula in vizinhanca:
        if mapa_real.dentro(celula):
            l, c = celula
            mapa_interno.grade[l][c] = mapa_real.grade[l][c]
            revelados.add(celula)


def busca_online(mapa_real, registrar_frames=False):
    """Executa o agente online até alcançar o objetivo (ou falhar).

    Devolve um `ResultadoOnline` com as métricas da seção 7.4.
    """
    mapa_interno = _criar_mapa_interno(mapa_real)
    objetivo = mapa_real.objetivo
    posicao = mapa_real.inicio

    revelados = set()
    visitados = {posicao}
    trajetoria = [posicao]
    custo_real = 0
    revisitadas = 0
    replanejamentos = 0
    frames = []

    _revelar(mapa_real, mapa_interno, posicao, revelados)

    # Limite de segurança contra laços (não deve ser atingido em mapas válidos).
    limite = mapa_real.linhas * mapa_real.colunas * 4

    while posicao != objetivo and replanejamentos < limite:
        plano, _ = a_estrela(ProblemaOnline(mapa_interno, posicao, objetivo))
        replanejamentos += 1
        if not plano or len(plano) < 2:
            break                       # sem caminho mesmo assumindo tudo livre

        if registrar_frames:
            frames.append(desenhar_mapa(mapa_interno, trajetoria, agente=posicao))

        posicao = plano[1]              # executa apenas o próximo passo do plano
        custo_real += mapa_real.custo_entrada(posicao)
        if posicao in visitados:
            revisitadas += 1
        visitados.add(posicao)
        trajetoria.append(posicao)
        _revelar(mapa_real, mapa_interno, posicao, revelados)

    if registrar_frames:
        frames.append(desenhar_mapa(mapa_interno, trajetoria, agente=posicao))

    return ResultadoOnline(
        sucesso=(posicao == objetivo),
        movimentos=len(trajetoria) - 1,
        custo_real=custo_real,
        celulas_reveladas=len(revelados),
        celulas_revisitadas=revisitadas,
        replanejamentos=replanejamentos,
        trajetoria=trajetoria,
        mapa_interno=mapa_interno,
        frames=frames,
    )
