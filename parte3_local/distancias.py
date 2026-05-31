"""Matriz de distâncias entre os pontos relevantes do labirinto.

A função de custo da Parte III (seção 6.2) precisa de d(X, Y) = custo do menor
caminho entre dois pontos. O enunciado manda calcular esse menor caminho com
A* ou UCS — reaproveitamos o A* já implementado na Parte II.
"""
from core.problema import ProblemaLabirinto
from parte2_classica.buscas import a_estrela


def calcular_distancias(mapa, pontos):
    """Calcula o custo do menor caminho entre todos os pares de `pontos`.

    `pontos` é a lista de posições de interesse (início, pontos de coleta e
    objetivo). Devolve um dicionário (origem, destino) -> custo.

    Como o custo de entrar numa célula depende da célula de destino, calculamos
    cada par nos dois sentidos (não assumimos simetria). Levanta erro se algum
    par for inalcançável, para não mascarar um mapa mal formado.
    """
    distancias = {}
    for origem in pontos:
        for destino in pontos:
            if origem == destino:
                distancias[(origem, destino)] = 0
                continue
            problema = ProblemaLabirinto(mapa, inicio=origem, objetivo=destino)
            _caminho, metricas = a_estrela(problema)
            if not metricas.sucesso:
                raise ValueError(f"Não há caminho entre {origem} e {destino}.")
            distancias[(origem, destino)] = metricas.custo
    return distancias


def caminho_rota(mapa, ordem, inicio, objetivo):
    """Reconstrói o caminho célula a célula da rota inicio -> ordem -> objetivo.

    Enquanto `calcular_distancias` só guarda o CUSTO de cada trecho, aqui
    concatenamos os menores caminhos (A*) entre pontos consecutivos para poder
    DESENHAR a rota da Parte III. Cada trecho começa onde o anterior terminou,
    então descartamos o primeiro estado de cada trecho para não duplicar a
    junção.
    """
    pontos = [inicio] + list(ordem) + [objetivo]
    caminho = [inicio]
    for origem, destino in zip(pontos, pontos[1:]):
        trecho, _ = a_estrela(ProblemaLabirinto(mapa, inicio=origem, objetivo=destino))
        caminho.extend(trecho[1:])
    return caminho
