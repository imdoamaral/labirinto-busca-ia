# Parte I — Projeto do Agente Inteligente

Rascunho da modelagem (Semana 1). O grupo deve revisar as justificativas e
ajustá-las ao que conseguir defender. Fonte primária: slide *Aula 02 - Agentes
Inteligentes*.

## 1. Modelagem PEAS

PEAS = (Performance, Environment, Actuators, Sensors).

### Performance (medida de desempenho)
Função sugerida no enunciado (todos os termos são penalizações):

J = −α·(custo do caminho) − β·(nós expandidos) − γ·(tempo de execução)
    − δ·(movimentos inválidos) − ε·(células revisitadas)

Os pesos α, β, γ, δ, ε ponderam a importância de cada fator e devem ser
justificados. Quanto maior J (menos penalidades), melhor o agente.

### Environment (ambiente)
Labirinto em grade, discreto, contendo: células livres, terreno custoso (lama),
paredes, posição inicial (A), objetivo (B), pontos de coleta (C) e, no modo
online, regiões desconhecidas (?).
Propriedades: **totalmente observável** na busca clássica e **parcialmente
observável** no modo online; **determinístico**, **estático**, **discreto** e
de **agente único**.

### Actuators (atuadores)
Movimentos ortogonais: A = {cima, baixo, esquerda, direita}.

### Sensors (sensores)
- Busca clássica: o agente percebe o mapa inteiro.
- Modo online: percebe apenas a vizinhança local (raio r = 1): as células
  (x−1,y), (x+1,y), (x,y−1), (x,y+1).

## 2. Classificação do agente

Mínimo exigido: **agente baseado em objetivos com modelo interno**.

Justificativa: o agente não age por reflexo — ele persegue o objetivo B e, no
modo online, mantém e atualiza um **modelo interno** do mapa (perceber →
atualizar mapa → planejar → agir). Pode-se argumentar que tende a um **agente
baseado em utilidade** quando passa a otimizar a função de desempenho J.

# Parte II — Formulação formal do problema

Problema = <S, A, T, s0, G, c> (seção 5.1):

- **S**: posições livres (não-parede) da grade. Estado = (linha, coluna).
- **A**: ações ortogonais {cima, baixo, esquerda, direita}.
- **T**: função de transição — de um estado, gera os vizinhos válidos (dentro
  da grade e sem parede). Ver `ProblemaLabirinto.sucessores`.
- **s0**: posição inicial (célula A).
- **G**: teste de objetivo — estado == posição de B.
- **c**: custo de cada movimento = custo de entrar na célula de destino
  (1 para livre, 3 para lama).

Heurística para as buscas informadas: distância de **Manhattan**
h(n) = |xₙ − x_B| + |yₙ − y_B|, **admissível** porque nunca superestima o custo
real (o menor custo por passo é 1).
