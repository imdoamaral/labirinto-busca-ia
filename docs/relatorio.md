# Relatório Técnico — Agente Inteligente em Labirinto

**Busca Clássica, Busca Local e Busca Online**
Linguagem: Python · Domínio: labirinto em grade discreta

Este relatório reúne a modelagem e os resultados das três partes do trabalho. As
análises detalhadas de cada parte estão em `docs/analise_parte2.md`,
`docs/analise_parte3.md` e `docs/analise_parte4.md`; aqui consolidamos tudo num
único documento, com a comparação final entre as abordagens.

> Reprodutibilidade: `python -m venv .venv && .venv/bin/pip install -r requirements.txt`,
> depois `experimentos.py` (Parte II), `experimentos_local.py` (Parte III) e
> `experimentos_online.py <mapa>` (Parte IV). O uso de IA generativa está
> declarado em `uso_ia.md`.

## Sumário
1. [Visão geral](#1-visão-geral)
2. [Parte I — Projeto do agente (PEAS)](#2-parte-i--projeto-do-agente)
3. [Parte II — Busca clássica](#3-parte-ii--busca-clássica)
4. [Parte III — Busca local com pontos de coleta](#4-parte-iii--busca-local)
5. [Parte IV — Busca online](#5-parte-iv--busca-online)
6. [Conclusão comparativa](#6-conclusão-comparativa)

---

## 1. Visão geral

O objetivo é um agente que resolve labirintos em grade sob três condições, no
mesmo domínio: **mapa conhecido** (A → B), **múltiplos pontos de coleta**
(visitar todos os C antes de B) e **mapa desconhecido** (explorar enquanto se
move). A legenda dos mapas é: `#` parede, ` ` célula livre (custo 1), `~` lama
(custo 3), `A` início, `B` objetivo, `C` ponto de coleta, `?` célula
desconhecida (modo online). O terreno de lama foi acrescentado para que os
custos variem e a comparação entre algoritmos sensíveis a custo (UCS, A*) e
sensíveis a passos (BFS) fique evidente.

## 2. Parte I — Projeto do agente

### 2.1 Modelagem PEAS
- **Performance:** J = −α·custo do caminho − β·nós expandidos − γ·tempo de
  execução − δ·movimentos inválidos − ε·células revisitadas. Todos os termos são
  penalizações; quanto maior J, melhor o agente.
- **Environment:** labirinto em grade, discreto, com células livres, lama,
  paredes, início, objetivo, pontos de coleta e regiões desconhecidas no modo
  online. É **totalmente observável** na busca clássica e **parcialmente
  observável** no modo online; **determinístico**, **estático**, **discreto** e
  de **agente único**.
- **Actuators:** movimentos ortogonais A = {cima, baixo, esquerda, direita}.
- **Sensors:** mapa inteiro (busca clássica) ou vizinhança local de raio 1
  (modo online).

### 2.2 Classificação do agente
**Agente baseado em objetivos com modelo interno** (mínimo exigido): persegue o
objetivo B e, no modo online, mantém e atualiza um modelo interno do mapa. Ao
otimizar a função J, aproxima-se de um **agente baseado em utilidade**.

## 3. Parte II — Busca clássica

### 3.1 Formulação formal
Problema = ⟨S, A, T, s₀, G, c⟩: **S** posições livres (estado = (linha, coluna));
**A** ações ortogonais; **T** vizinhos válidos (dentro da grade e sem parede);
**s₀** célula A; **G** estado == B; **c** custo de entrar na célula de destino
(1 livre, 3 lama). Heurística das buscas informadas: distância de **Manhattan**,
**admissível** (nunca superestima, pois o menor custo por passo é 1).

### 3.2 Resultados
Dois mapas: `exemplo.txt` (o caminho mais barato também é dos mais curtos) e
`armadilha_gulosa.txt` (corredor reto de lama, curto em passos e caro, com um
desvio livre ao lado).

**Mapa `exemplo.txt`:**

| Algoritmo | Sucesso | Custo | Passos | Explorados | Expandidos | Fronteira |
|-----------|:-------:|:-----:|:------:|:----------:|:----------:|:---------:|
| BFS       | sim | 13 | 11 | 31 | 30 | 4 |
| DFS       | sim | 31 | 25 | 26 | 25 | 6 |
| UCS       | sim | 13 | 11 | 31 | 30 | 5 |
| Gulosa    | sim | 13 | 11 | 12 | 11 | 5 |
| A*        | sim | 13 | 11 | 31 | 30 | 5 |

**Mapa `armadilha_gulosa.txt`:**

| Algoritmo | Sucesso | Custo | Passos | Explorados | Expandidos | Fronteira |
|-----------|:-------:|:-----:|:------:|:----------:|:----------:|:---------:|
| BFS       | sim | 19 | 7 | 15 | 14 | 2 |
| DFS       | sim | 19 | 7 | 8  | 7  | 8 |
| UCS       | sim | 9  | 9 | 15 | 14 | 4 |
| Gulosa    | sim | 19 | 7 | 8  | 7  | 8 |
| A*        | sim | 9  | 9 | 11 | 10 | 6 |

### 3.3 Análise (seção 5.4)
1. **BFS** sempre acha o caminho com menos passos; só é ótima em custo com
   custos uniformes (coincide no `exemplo`, falha no `armadilha`: 19 vs 9).
2. **DFS** é rápida e econômica em memória, mas a qualidade não é garantida
   (custo 31 vs 13 no `exemplo`).
3. **UCS ≠ BFS** quando os custos variam: com a lama, UCS achou 9 (contornando)
   e BFS achou 19 (reto).
4. **Gulosa** é eficiente (poucos nós) mas pode ser subótima: ignora o custo e
   entra na lama (19 vs 9).
5. **A\*** une otimalidade e eficiência: custo ótimo (9) expandindo menos nós
   que a UCS (10 vs 14).
6. A heurística de **Manhattan é admissível** (nunca superestima), garantindo a
   otimalidade do A*.

## 4. Parte III — Busca local

### 4.1 Modelagem
- **Representação (6.1):** permutação dos pontos de coleta; rota = A → ordem → B.
- **Custo (6.2):** C(s) = d(A, ordem[0]) + Σ d(ordem[i], ordem[i+1]) +
  d(ordem[-1], B), com d(X,Y) = menor caminho calculado por **A\*** (reaproveitado
  da Parte II), considerando a lama.
- **Vizinhança (6.4):** inversão de um trecho da ordem (2-opt) — desfaz
  "cruzamentos" preservando boa parte da sequência.

### 4.2 Resultados (mapa `coletas.txt`, 8 pontos)
Ótimo global por força bruta (8! = 40320) = **32**. 30 execuções por método.

| Método | Melhor | Pior | Médio | Tempo méd. | Iter. méd. | Sucesso |
|--------|:------:|:----:|:-----:|:----------:|:----------:|:-------:|
| Hill-Climbing             | 32 | 38 | 33.1 | 0.18 ms | 4    | 73%  |
| Simulated Annealing       | 32 | 32 | 32.0 | 6.32 ms | 2297 | 100% |
| Algoritmo Genético (bônus)| 32 | 32 | 32.0 | 38.6 ms | 100  | 100% |

![Convergência da busca local](figuras/convergencia_local.png)
![Convergência do Algoritmo Genético](figuras/convergencia_ga.png)

**Sensibilidade do SA (taxa de sucesso em atingir o ótimo):**

| Temp. inicial | Resfr. 0.90 | Resfr. 0.99 | Resfr. 0.999 |
|:-------------:|:-----------:|:-----------:|:------------:|
| 1     | 53% | 100% | 100% |
| 10    | 67% | 100% | 100% |
| 100   | 70% | 100% | 100% |
| 1000  | 70% | 100% | 100% |

### 4.3 Análise (seção 6.6)
1. **Hill-Climbing fica preso em mínimo local** (sucesso 73%; pior 38 vs ótimo 32).
2. **Simulated Annealing** encontra soluções melhores (100%), aceitando pioras
   com probabilidade exp(−Δ/T) para escapar dos mínimos.
3. **Temperatura inicial:** efeito secundário; só ajuda quando o resfriamento é
   rápido (com 0.90, subir T₀ de 1 para 100 elevou o sucesso de 53% para 70%).
4. **Taxa de resfriamento:** fator dominante; rápida (0.90) → 53–70%; lenta
   (0.99/0.999) → 100%, ao custo de mais iterações.
5. A busca local **não** encontrou sempre o ótimo (HC não; SA sim, se bem
   parametrizado). Em geral não há garantia — aqui confirmamos por força bruta.
6. **Compromisso tempo × qualidade:** HC é ~35× mais rápido porém pior; SA é
   lento e ótimo. Uma alternativa barata é HC com vários reinícios aleatórios.

**Bônus — Algoritmo Genético** (`parte3_local/genetico.py`): abordagem
populacional com seleção por torneio, cruzamento por ordem (OX), mutação por
troca e elitismo. Atingiu o ótimo (32) em 100% das execuções, convergindo por
volta da geração 7, mas é o mais caro em tempo (~38.6 ms) por avaliar a
população inteira a cada geração.

## 5. Parte IV — Busca online

### 5.1 Estratégia e premissas
**Replanning A\*** (Opção A): mapa interno começa todo `?`; a cada passo o agente
percebe a vizinhança (raio 1), atualiza o mapa, roda A* assumindo o desconhecido
como livre, anda **um** passo e replaneja. O agente conhece o tamanho do mapa e
as posições de início e objetivo, mas **não** as paredes.

### 5.2 Resultados

| Mapa | Sucesso | Movimentos | Custo real | Reveladas | Revisitadas | Replanej. | Ótimo offline | Razão |
|------|:-------:|:----------:|:----------:|:---------:|:-----------:|:---------:|:-------------:|:-----:|
| `exemplo.txt`          | sim | 11 | 13 | 37 | 0 | 11 | 13 | **1.00** |
| `online_armadilha.txt` | sim | 20 | 20 | 50 | 3 | 20 | 14 | **1.43** |

### 5.3 Análise (seção 7.5)
1. **Decisões subótimas** acontecem quando a suposição otimista falha: no
   `armadilha` o agente desceu reto num beco e teve de contornar (razão 1.43);
   no `exemplo` a suposição coincidiu (razão 1.00).
2. **Faltava** ao agente a localização das paredes além do raio de percepção.
3. O **mapa interno converge só parcialmente** (células fora da rota ficam `?`):
   o agente constrói um modelo suficiente para chegar, não completo.
4. **Revisitas** são poucas e concentradas nos backtrackings (0 e 3).
5. **Melhorar a exploração:** aumentar o raio de percepção, supor o desconhecido
   menos otimista, memorizar becos, usar replanejamento incremental (D* Lite).
6. **Diferença para a busca clássica:** a clássica planeja uma vez com o mapa
   completo; a online intercala perceber → planejar → agir, descobrindo o mapa e
   pagando a razão online/offline ≥ 1 pelo desconhecimento.

## 6. Conclusão comparativa

As três abordagens resolvem o mesmo domínio com compromissos distintos:

- **Busca clássica** (mapa conhecido): com informação completa, o **A\*** é a
  melhor escolha — ótimo e eficiente. BFS/UCS são ótimos em condições
  específicas (passos vs custo), DFS é barata mas fraca, e a Gulosa é rápida
  porém arriscada.
- **Busca local** (otimização da ordem de coleta): quando o espaço de soluções é
  grande demais para busca exaustiva, a busca local entrega boas soluções
  rapidamente. O **Simulated Annealing** supera o Hill-Climbing por escapar de
  mínimos locais, controlando o compromisso tempo × qualidade pela taxa de
  resfriamento. O **Algoritmo Genético** (bônus) também alcança o ótimo, com a
  abordagem populacional ao custo de mais tempo.
- **Busca online** (mapa desconhecido): sem informação completa, o agente paga um
  preço (razão ≥ 1) por descobrir o mapa enquanto age. O **replanning A\***
  reaproveita a busca clássica e mantém esse preço baixo quando o ambiente é
  "benigno", mas sofre com becos não previstos.

O fio condutor é o papel da **informação**: quanto mais o agente sabe de
antemão, mais perto do ótimo ele chega — da otimalidade garantida da busca
clássica, passando pela aproximação controlada da busca local, até o custo
inevitável da exploração na busca online.
