# Parte II — Análise da Busca Clássica (seção 5.4)

Respostas baseadas em dois mapas (reproduzir com `python experimentos.py <mapa>`).

## Mapa A — `mapas/exemplo.txt`
Labirinto com paredes, lama e múltiplas rotas; o caminho de menor custo também é
um dos de menos passos.

| Algoritmo | Sucesso | Custo | Passos | Explorados | Expandidos | Fronteira |
|-----------|:-------:|:-----:|:------:|:----------:|:----------:|:---------:|
| BFS       | sim     | 13    | 11     | 31         | 30         | 4         |
| DFS       | sim     | 31    | 25     | 26         | 25         | 6         |
| UCS       | sim     | 13    | 11     | 31         | 30         | 5         |
| Gulosa    | sim     | 13    | 11     | 12         | 11         | 5         |
| A*        | sim     | 13    | 11     | 31         | 30         | 5         |

## Mapa B — `mapas/armadilha_gulosa.txt`
Corredor reto até B cheio de lama (curto em passos, caro) com um desvio livre ao
lado (mais passos, barato). Isola o ponto fraco da Gulosa e da BFS.

| Algoritmo | Sucesso | Custo | Passos | Explorados | Expandidos | Fronteira |
|-----------|:-------:|:-----:|:------:|:----------:|:----------:|:---------:|
| BFS       | sim     | 19    | 7      | 15         | 14         | 2         |
| DFS       | sim     | 19    | 7      | 8          | 7          | 8         |
| UCS       | sim     | 9     | 9      | 15         | 14         | 4         |
| Gulosa    | sim     | 19    | 7      | 8          | 7          | 8         |
| A*        | sim     | 9     | 9      | 11         | 10         | 6         |

---

## 1. BFS encontrou o menor caminho? Em quais condições isso ocorre?

A BFS sempre encontra o caminho com o **menor número de passos** (11 no mapa A,
7 no mapa B). Mas ela só encontra o de **menor custo** quando todos os
movimentos custam o mesmo. No mapa A isso ocorre (BFS = UCS = 13), porque o
caminho mais curto em passos também é o mais barato. No mapa B **não** ocorre: a
BFS pega o corredor reto de lama (custo 19), enquanto o ótimo em custo é 9.
**Conclusão:** BFS é ótima em custo apenas com custos uniformes.

## 2. DFS encontrou solução rapidamente? A solução foi boa?

Sim, rapidamente: foi quem **menos explorou nós** (26 no mapa A, 8 no mapa B) e
usa pouca memória. Mas a qualidade não é garantida: no mapa A devolveu um
caminho de custo **31** (contra 13 do ótimo) — bem pior. No mapa B acertou 19
por acaso, num mapa pequeno. **Conclusão:** DFS é rápida e econômica em memória,
mas não garante boa solução.

## 3. UCS diferiu de BFS quando os custos variaram?

Sim — é exatamente o que o mapa B mostra: com a lama encarecendo o corredor
reto, a **UCS achou custo 9** (contornando) e a **BFS achou 19** (reto, menos
passos). No mapa A, sem essa armadilha, as duas coincidiram (13). **Conclusão:**
UCS e BFS divergem quando o caminho mais barato é mais longo em passos; a UCS
otimiza custo, a BFS otimiza passos.

## 4. A busca gulosa foi eficiente? Foi ótima?

Eficiente sim: explorou pouquíssimos nós (12 no mapa A, 8 no mapa B), pois corre
direto na direção do objetivo segundo h(n). Ótima **não**: no mapa B ela ignora
o custo e entra na lama (custo 19, contra 9 do ótimo). No mapa A ela foi ótima
por sorte. **Conclusão:** a Gulosa é rápida, mas pode ser subótima porque
desconsidera o custo já percorrido.

## 5. A* equilibrou qualidade da solução e eficiência?

Sim. Ele entrega o **custo ótimo** (9 no mapa B, igual à UCS) e, graças à
heurística, costuma **expandir menos nós** que a UCS para chegar lá (10 contra
14 no mapa B). No mapa A, pequeno, a vantagem de poda é menor e os números se
igualam à UCS. **Conclusão:** A* combina a otimalidade da UCS com a orientação
ao objetivo da Gulosa.

## 6. A heurística utilizada é admissível? Justifique.

Sim. A distância de Manhattan h(n) = |xₙ − x_B| + |yₙ − y_B| conta o número
**mínimo** de passos até B ignorando paredes e lama. Como o menor custo possível
por passo é 1, esse valor **nunca superestima** o custo real do caminho — que só
pode ser maior (por desvios em torno de paredes ou por células de lama, que
custam 3). Por nunca superestimar, ela é **admissível** e garante que o A*
encontre o caminho de custo ótimo.
