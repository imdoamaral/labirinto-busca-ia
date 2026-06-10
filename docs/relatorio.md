# Relatório Técnico — Agente Inteligente em Labirinto

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
move). 

A legenda dos mapas é: `#` parede, `` célula livre (custo 1), `~` lama (custo 3), `A` início, `B` objetivo, `C` ponto de coleta, `?` célula desconhecida (modo online). 

O terreno de lama foi acrescentado para que os custos variem e a comparação entre algoritmos sensíveis a custo (UCS, A*) e sensíveis a passos (BFS) fique evidente.

### 1.1 Diferenças em relação à implementação de referência
Comparando a nossa implementação da busca clássica com a de referência da disciplina, há quatro decisões conscientes em que divergimos — todas justificadas adiante na Parte II:

- **Custo variável (lama).** A referência trata todo movimento com **custo unitário** e qualquer caractere não-`A`/`B`/espaço como parede (a lama `~` viraria muro). Nós modelamos a lama com custo 3 (`custo_entrada`), o que é o que torna possível **UCS ≠ BFS** e a "armadilha gulosa" (seção 3.3).

- **Ordem de varredura dos vizinhos.** A referência expande na ordem vertical-primeiro (`cima, baixo, esquerda, direita`); nós adotamos **horizontal-primeiro** (`direita, esquerda, baixo, cima`) para que a DFS "corra reto até a parede" antes de desviar, deixando a visualização mais intuitiva em corredores horizontais.

- **A\* puro vs. ponderado.** A referência usa **Weighted A\*** (peso `w=2` por padrão, mais rápido porém **não-ótimo**); nós usamos **A\* puro** (`w=1`), garantindo otimalidade com a heurística admissível.

- **Arquitetura e métricas.** Separamos *problema* (`core/problema.py`) de *estratégia de busca* (`parte2_classica/buscas.py`) — o que permite reaproveitar `ProblemaLabirinto` nas Partes III e IV — e medimos também **custo, tempo e fronteira máxima**, além de nós explorados/expandidos.

## 2. Parte I - Projeto do agente

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
objetivo B e, no modo online, mantém e atualiza um modelo interno do mapa.

## 3. Parte II — Busca clássica

### 3.1 Formulação formal
Problema = ⟨S, A, T, s₀, G, c⟩:

- **S:** posições livres (estado = (linha, coluna));
- **A:** ações ortogonais;
- **T:** vizinhos válidos (dentro da grade e sem parede);
- **s₀:** célula A; 
- **G:** estado == B; 
- **c:** custo de entrar na célula de destino
(1 livre, 3 lama). 
- **Heurística das buscas informadas:** distância de Manhattan,

### 3.2 Resultados
2 mapas: `exemplo.txt` (o mapa do enunciado, de **custo uniforme** — todos os
algoritmos completos acham o ótimo) e `armadilha_gulosa.txt` (corredor reto de
lama, curto em passos e caro, com um desvio livre ao lado).

**Mapa `exemplo.txt`:**

```text
###########
#A   #    #
# ## # ## #
#    C   B#
# ##   #  #
#   C  #  #
###########
```

| Algoritmo | Sucesso | Custo | Passos | Expandidos | Tempo (ms) | Fronteira |
|-----------|:-------:|:-----:|:------:|:----------:|:----------:|:---------:|
| BFS       | sim | 10 | 10 | 26 | 0.076 | 5 |
| DFS       | sim | 10 | 10 | 10 | 0.033 | 8 |
| UCS       | sim | 10 | 10 | 26 | 0.081 | 5 |
| Gulosa    | sim | 10 | 10 | 10 | 0.033 | 8 |
| A*        | sim | 10 | 10 | 14 | 0.048 | 7 |

**Mapa `armadilha_gulosa.txt`:**

```text
##########
#A~~~~~~B#
#        #
##########
```

| Algoritmo | Sucesso | Custo | Passos | Expandidos | Tempo (ms) | Fronteira |
|-----------|:-------:|:-----:|:------:|:----------:|:----------:|:---------:|
| BFS       | sim | 19 | 7  | 13 | 0.049 | 3 |
| DFS       | sim | 19 | 7  | 7  | 0.025 | 8 |
| UCS       | sim | 9  | 9  | 14 | 0.050 | 4 |
| Gulosa    | sim | 19 | 7  | 7  | 0.028 | 8 |
| A*        | sim | 9  | 9  | 10 | 0.038 | 6 |

### 3.3 Análise (seção 5.4)
Nas figuras: hachura azul = **células exploradas**, linha vermelha = **caminho devolvido**, bege = **lama** (`~`). Cada item mostra o algoritmo nos dois mapas — `exemplo` (custo uniforme) à esquerda e `armadilha_gulosa` à direita.

**1. BFS encontrou o menor caminho? Em quais condições isso ocorre?** 

*Sim, encontrou.* Mas só é ótima em custo quando os movimentos custam o mesmo (custo uniforme): aí o caminho com menos passos também é o mais barato — coincide no `exemplo` (BFS = UCS = 10) e falha no `armadilha` (19 vs 9 do ótimo).

<p align="center">
  <img src="figuras/parte2/exemplo_BFS.png" width="49%" alt="BFS no mapa exemplo">
  <img src="figuras/parte2/armadilha_gulosa_BFS.png" width="49%" alt="BFS no mapa armadilha">
</p>

GIFs:
[(exemplo)](figuras/parte2/exemplo_BFS.gif) · [(armadilha)](figuras/parte2/armadilha_gulosa_BFS.gif)

**2. DFS encontrou solução rapidamente? A solução foi boa?** 

*Rápida sim, qualidade não garantida.* Com a convenção de varredura horizontal-primeiro (`direita → esquerda → baixo → cima`), a DFS **corre reto até a parede antes de desviar** — dá para ver isso nas figuras. Foi a busca que **expandiu menos nós** (10 e 7), pois mergulha num ramo até o fim antes de abrir outros. Mas a qualidade depende do ramo em que ela cai: no `exemplo` acabou caindo **por sorte** no caminho ótimo (10, igual a BFS/UCS/A\*); no `armadilha` entrou reto na lama e ficou **subótima** (19 vs 9 do ótimo). Ou seja, achar o ótimo no `exemplo` foi coincidência da ordem de expansão, não garantia do algoritmo.

<p align="center">
  <img src="figuras/parte2/exemplo_DFS.png" width="49%" alt="DFS no mapa exemplo">
  <img src="figuras/parte2/armadilha_gulosa_DFS.png" width="49%" alt="DFS no mapa armadilha">
</p>

GIFs:
[(exemplo)](figuras/parte2/exemplo_DFS.gif) · [(armadilha)](figuras/parte2/armadilha_gulosa_DFS.gif)

**3. UCS diferiu de BFS quando os custos variaram?** 

*Sim, divergiram.* Quando os custos variam, as duas divergem: com a lama, a UCS achou **9** (contornando) e a BFS achou **19** (reto).

<p align="center">
    <img src="figuras/parte2/armadilha_gulosa_UCS.png" width="49%" alt="UCS no mapa armadilha">
    <img src="figuras/parte2/armadilha_gulosa_BFS.png" width="49%" alt="UCS no mapa exemplo">
</p>

GIFs:
[(exemplo)](figuras/parte2/exemplo_UCS.gif) · [(armadilha)](figuras/parte2/armadilha_gulosa_UCS.gif)

**4. A busca gulosa foi eficiente? Foi ótima?** 

*Eficiente sim; ótima não.* Expande pouquíssimos nós (corre na direção de `h`), mas pode ser subótima: ignora o custo já gasto e entra na lama (19 vs 9).

<p align="center">
  <img src="figuras/parte2/exemplo_Gulosa.png" width="49%" alt="Gulosa no mapa exemplo">
  <img src="figuras/parte2/armadilha_gulosa_Gulosa.png" width="49%" alt="Gulosa no mapa armadilha">
</p>

GIFs:
[(exemplo)](figuras/parte2/exemplo_Gulosa.gif) · [(armadilha)](figuras/parte2/armadilha_gulosa_Gulosa.gif)

**5. A\* equilibrou qualidade da solução e eficiência?** 

*Sim, equilibrou.* Une otimalidade e eficiência: custo ótimo (9) expandindo menos nós que a UCS (10 vs 14).

<p align="center">
  <img src="figuras/parte2/exemplo_Aestrela.png" width="49%" alt="A* no mapa exemplo">
  <img src="figuras/parte2/armadilha_gulosa_Aestrela.png" width="49%" alt="A* no mapa armadilha">
</p>

GIFs:
[(exemplo)](figuras/parte2/exemplo_Aestrela.gif) · [(armadilha)](figuras/parte2/armadilha_gulosa_Aestrela.gif)

**6. A heurística utilizada é admissível? Justifique.**

*Sim, é admissível.* O menor custo por passo é 1, então ela nunca superestima o custo restante, o que **garante a otimalidade do A\***.

## 4. Parte III — Busca local

### 4.1 Modelagem

O agente parte de `A`, precisa passar por **todos** os pontos de coleta `C` e
terminar em `B`. O que muda o custo não é *como* andar entre dois pontos (isso é
problema da Parte II), mas em **que ordem** visitar os `C`. A busca local procura
essa ordem.

- **Representação (6.1):** uma solução é a *ordem de visita* dos `C` — por exemplo,
  `[C3, C1, C2, ...]`. A rota completa é sempre `A → (essa ordem) → B`.

- **Custo (6.2):** soma das distâncias da rota inteira, na ordem escolhida:

  `C(s) = d(A, C_primeiro) + d(C_primeiro, C_seguinte) + ... + d(C_último, B)`

  Cada distância `d(X, Y)` é o **menor caminho** entre dois pontos no labirinto,
  calculado pelo **A\*** da Parte II (já considerando a lama). Quanto menor a soma,
  melhor a ordem.

- **Vizinhança (6.4):** os métodos de busca local não saltam para qualquer ordem;
  a cada passo eles só conseguem ir de uma ordem para outra *parecida* — uma
  **vizinha**. Aqui, uma vizinha é obtida **invertendo um trecho** da ordem atual.
  Um *trecho* é um pedaço contínuo da sequência (das posições `i` até `j`);
  invertê-lo é lê-lo de trás para frente:

  ```text
  ordem atual:  [C1, C2, C3, C4, C5]
                      └── trecho ──┘
  vizinha:      [C1, C4, C3, C2, C5]   (C2..C4 invertido)
  ```

  **Por que inverter?** Numa rota, um cruzamento (dois caminhos que se cortam)
  quase sempre custa mais do que descruzá-los. Inverter um trecho é justamente o
  que "desfaz" esse cruzamento, mudando só um pedaço da ordem e preservando o
  resto. Esse movimento é o clássico **2-opt** de problemas de rota (caixeiro-
  viajante), mais eficaz aqui do que simplesmente trocar dois pontos de lugar.

  **Onde é usada:** cada algoritmo consulta essa vizinhança de um jeito —
  - o **Hill-Climbing** gera *todas* as vizinhas (inverte cada trecho possível) e
    pula para a melhor, enquanto houver melhora (`vizinhos_por_inversao`);
  - o **Simulated Annealing** sorteia *uma* vizinha por iteração e decide se aceita
    (`vizinho_aleatorio`).

### 4.2 Resultados (mapa `coletas.txt`, 8 pontos)
Ótimo global por força bruta (8! = 40320) = **32**. 30 execuções por método.

```text
###############
#A   C   ~    #
#  ~   C   ~  #
#   C   ~   C #
# ~   C   ~   #
#      ~   C  #
#   ~   C   ~ #
#    ~   C   B#
###############
```

As colunas **Melhor / Pior / Médio** são o custo da rota (menor = melhor) ao longo
das 30 execuções. Como os métodos usam aleatoriedade, cada rodada pode dar um
resultado diferente: *Melhor* é o potencial (acha o ótimo?), *Pior* é o risco
(quão ruim fica no pior caso) e *Médio*, o resultado típico. A fenda entre Melhor
e Pior mede a **confiabilidade** — se forem iguais, o método é consistente.

| Método | Melhor | Pior | Médio | Tempo méd. | Iter. méd. | Sucesso |
|--------|:------:|:----:|:-----:|:----------:|:----------:|:-------:|
| Hill-Climbing             | 32 | 38 | 33.1 | 0.18 ms | 4    | 73%  |
| Simulated Annealing       | 32 | 32 | 32.0 | 6.32 ms | 2297 | 100% |
| Algoritmo Genético (bônus)| 32 | 32 | 32.0 | 38.6 ms | 100  | 100% |

![Rota ótima das coletas](figuras/parte3/rota_otima.png)

*Rota de custo 32: de `A`, visita todos os `C` na ordem que minimiza o custo
total e termina em `B` — a permutação que os métodos procuram entre as 8! = 40320
possíveis.*

### 4.3 Análise (seção 6.6)

**1. Hill-Climbing ficou preso em mínimo local?**

*Sim.* Sucesso de só 73%: em parte das execuções parou num ótimo local (pior caso custo 38, contra 32 do ótimo), pois só aceita vizinhos melhores e não tem como sair de um vale.

**2. Simulated Annealing encontrou soluções melhores?**

*Sim.* Atingiu o ótimo (32) em 100% das execuções, porque aceita pioras com probabilidade exp(−Δ/T) e assim escapa dos mínimos locais que prendem o HC.

![Convergência da busca local](figuras/convergencia_local.png)

*Curva iteração × melhor custo de **uma única execução** (a primeira das 30), com
HC e SA partindo da **mesma ordem inicial** — é um confronto direto do
comportamento de cada método, não o melhor caso de nenhum. A partir do mesmo
ponto: o HC despenca e estaciona cedo (rápido, mas trava num mínimo local); o SA
desce em "degraus" — cada patamar é uma piora aceita — e fecha o ótimo (32) por
volta da iteração 770.*

**Sensibilidade do SA** (taxa de sucesso em atingir o ótimo):

| Temp. inicial | Resfr. 0.90 | Resfr. 0.99 | Resfr. 0.999 |
|:-------------:|:-----------:|:-----------:|:------------:|
| 1     | 53% | 100% | 100% |
| 10    | 67% | 100% | 100% |
| 100   | 70% | 100% | 100% |
| 1000  | 70% | 100% | 100% |

**3. Como a temperatura inicial influenciou os resultados?**

*Efeito secundário.* Só pesa quando o resfriamento é rápido: com 0.90, subir T₀ de 1 para 100 elevou o sucesso de 53% para 70%. Com resfriamento lento (0.99/0.999) o sucesso já é 100%, independentemente de T₀.

**4. Como a taxa de resfriamento afetou a convergência?**

*Foi o fator dominante.* Resfriamento rápido (0.90) → 53–70% de sucesso; lento (0.99/0.999) → 100%, ao custo de muito mais iterações (o SA chega a ~2297 em média).

**5. A busca local encontrou sempre a solução ótima?**

*Nem sempre.* O HC não; o SA sim, quando bem parametrizado. Em geral não há garantia de otimalidade — aqui só sabemos que 32 é o ótimo porque foi confirmado por força bruta sobre as 8! = 40320 permutações.

**6. Qual foi o compromisso entre tempo e qualidade?**

*Velocidade × qualidade.* O HC é ~35× mais rápido (0.18 ms) porém arrisca parar num ótimo local; o SA é lento (6.32 ms) mas atinge o ótimo. Um meio-termo barato é rodar HC com vários reinícios aleatórios.

**Bônus — Algoritmo Genético** (`parte3_local/genetico.py`): abordagem populacional (seleção por torneio, cruzamento por ordem OX, mutação por troca e elitismo). Atingiu o ótimo (32) em 100% das execuções, convergindo por volta da geração 7, mas é o mais caro em tempo (~38.6 ms) por avaliar a população inteira a cada geração.

![Convergência do Algoritmo Genético](figuras/convergencia_ga.png)

*Eixo X é a geração: o melhor custo cai nas primeiras gerações e estabiliza no ótimo (32) por volta da geração 7, mantido pelo elitismo.*

## 5. Parte IV — Busca online

### 5.1 Estratégia e premissas
**Replanning A\*** (Opção A): mapa interno começa todo `?`; a cada passo o agente
percebe a vizinhança (raio 1), atualiza o mapa, roda A* assumindo o desconhecido
como livre, anda **um** passo e replaneja. O agente conhece o tamanho do mapa e
as posições de início e objetivo, mas **não** as paredes.

### 5.2 Resultados

Os mapas abaixo são a verdade de campo (o agente *não* a enxerga de início — só
o tamanho e as posições de `A` e `B`).

**Mapa `exemplo.txt`** (mesmo da Parte II):

```text
###########
#A   #    #
# ## # ## #
#    C   B#
# ##   #  #
#   C  #  #
###########
```

**Mapa `online_armadilha.txt`:**

```text
#######
#A    #
# ### #
# ### #
# ### #
##### #
#     #
#B#####
```

| Mapa | Sucesso | Movimentos | Custo real | Reveladas | Revisitadas | Replanej. | Ótimo offline | Razão |
|------|:-------:|:----------:|:----------:|:---------:|:-----------:|:---------:|:-------------:|:-----:|
| `exemplo.txt`          | sim | 10 | 10 | 34 | 0 | 10 | 10 | **1.00** |
| `online_armadilha.txt` | sim | 20 | 20 | 50 | 3 | 20 | 14 | **1.43** |

A **razão** = `custo real ÷ ótimo offline`, onde o *ótimo offline* é o custo que a
busca clássica acharia com o mapa completo. Ela mede quanto o agente pagou a mais
por descobrir o labirinto enquanto andava: é sempre **≥ 1** (no melhor caso empata
com o ótimo, 1.00; no `armadilha`, contornar o beco custou 43% a mais, 1.43).

### 5.3 Análise (seção 7.5)

**1. O agente online tomou decisões subótimas? Por quê?**

*Sim, quando a suposição otimista falha.* A heurística do A\* é a distância de **Manhattan**, que avalia "reto para baixo" como o caminho mais curto (cada passo para baixo reduz o `h`, enquanto ir para o lado o *aumenta*); e a suposição otimista trata o beco — ainda cheio de `?` — como livre. 

A subotimalidade vem de **agir sobre uma suposição otimista** antes de conhecer os obstáculos — guiado por uma heurística que, sem essa informação, aponta direto para a armadilha.

![Mapa interno final da busca online](figuras/parte4/online_final.png)

*Mapa interno ao fim da execução no `armadilha`: a linha vermelha é a trajetória real — vê-se a descida otimista, o beco e o desvio que eleva a razão a 1.43. Passo a passo no GIF `docs/figuras/parte4/online.gif`.*

**2. Quais informações faltavam ao agente?**

*A localização das paredes* além do seu raio de percepção (raio 1). Ele conhecia o tamanho do mapa e as posições de `A` e `B`, mas só descobria os obstáculos ao chegar perto — por isso apostou num caminho que não existia.

**3. O mapa interno convergiu para o mapa real?**

*Só parcialmente*, na região explorada: 50 de 56 células reveladas no `armadilha` e 34 de 77 no `exemplo`. Células fora da trajetória permanecem `?` (ver figura acima). O agente constrói um modelo suficiente para chegar ao objetivo, não um mapa completo.

**4. O agente revisitou muitas células?**

*Poucas.* 0 revisitas no `exemplo` e 3 no `armadilha`, concentradas no backtracking ao descobrir o beco. Como percebe os vizinhos antes de agir, ele raramente refaz caminho fora dos retornos.

**5. Como melhorar a exploração?**

*Várias frentes:* aumentar o raio de percepção (revela mais por passo), supor o desconhecido de forma menos otimista e memorizar becos sem saída.

**6. O que diferencia busca online de busca clássica?**

*Quando a informação chega.* A clássica planeja **uma vez** com o mapa completo e segue o caminho ótimo; a online intercala **perceber → planejar → agir**, descobrindo o mapa enquanto se move. Por isso pode tomar decisões subótimas e paga a razão online/offline ≥ 1 — o "preço" de não conhecer o ambiente.

## 6. Conclusão comparativa

As três abordagens resolvem o mesmo domínio com compromissos distintos:

- **Busca clássica** (mapa conhecido): com informação completa, o **A\*** é a melhor escolha — ótimo e eficiente. BFS/UCS são ótimos em condições específicas (passos vs custo), DFS é barata mas fraca, e a Gulosa é rápida porém arriscada.

- **Busca local** (otimização da ordem de coleta): quando o espaço de soluções é grande demais para busca exaustiva, a busca local entrega boas soluções rapidamente. O **Simulated Annealing** supera o Hill-Climbing por escapar de mínimos locais, controlando o compromisso tempo × qualidade pela taxa de resfriamento. O **Algoritmo Genético** (bônus) também alcança o ótimo, com a
  abordagem populacional ao custo de mais tempo.

- **Busca online** (mapa desconhecido): sem informação completa, o agente paga um preço (razão ≥ 1) por descobrir o mapa enquanto age. O **replanning A\*** reaproveita a busca clássica e mantém esse preço baixo quando o ambiente é "benigno", mas sofre com becos não previstos. O fio condutor é o papel da **informação**: quanto mais o agente sabe de antemão, mais perto do ótimo ele chega — da otimalidade garantida da busca clássica, passando pela aproximação controlada da busca local, até o custo inevitável da exploração na busca online.
