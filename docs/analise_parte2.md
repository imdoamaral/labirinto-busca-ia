# Parte II — Análise da Busca Clássica (seção 5.4)

Respostas baseadas em dois mapas (reproduzir com `python experimentos.py <mapa>`).

## Mapa A — `mapas/exemplo.txt`
O mapa de exemplo do enunciado: paredes e múltiplas rotas, **custo uniforme**
(sem lama). Como todo movimento custa o mesmo, o caminho de menor custo coincide
com o de menos passos e todos os algoritmos completos encontram o ótimo (10).

| Algoritmo | Sucesso | Custo | Passos | Expandidos | Tempo (ms) | Fronteira |
|-----------|:-------:|:-----:|:------:|:----------:|:----------:|:---------:|
| BFS       | sim     | 10    | 10     | 28         | 0.080      | 4         |
| DFS       | sim     | 18    | 18     | 22         | 0.061      | 7         |
| UCS       | sim     | 10    | 10     | 28         | 0.087      | 4         |
| Gulosa    | sim     | 10    | 10     | 10         | 0.035      | 9         |
| A*        | sim     | 10    | 10     | 14         | 0.050      | 7         |

## Mapa B — `mapas/armadilha_gulosa.txt`
Corredor reto até B cheio de lama (curto em passos, caro) com um desvio livre ao
lado (mais passos, barato). Isola o ponto fraco da Gulosa e da BFS.

| Algoritmo | Sucesso | Custo | Passos | Expandidos | Tempo (ms) | Fronteira |
|-----------|:-------:|:-----:|:------:|:----------:|:----------:|:---------:|
| BFS       | sim     | 19    | 7      | 14         | 0.050      | 2         |
| DFS       | sim     | 19    | 11     | 11         | 0.036      | 5         |
| UCS       | sim     | 9     | 9      | 14         | 0.049      | 4         |
| Gulosa    | sim     | 19    | 7      | 7          | 0.026      | 8         |
| A*        | sim     | 9     | 9      | 10         | 0.038      | 6         |

---

## 1. BFS encontrou o menor caminho? Em quais condições isso ocorre?

A BFS sempre encontra o caminho com o **menor número de passos** (10 no mapa A,
7 no mapa B). Mas ela só encontra o de **menor custo** quando todos os
movimentos custam o mesmo. No mapa A isso ocorre (BFS = UCS = 10), porque é um
mapa de custo uniforme. No mapa B **não** ocorre: a BFS pega o corredor reto de
lama (custo 19), enquanto o ótimo em custo é 9. **Conclusão:** BFS é ótima em
custo apenas com custos uniformes.

## 2. DFS encontrou solução rapidamente? A solução foi boa?

A DFS encontra uma solução logo e usa **pouca memória** (fronteira de só 7 e 5
nós), pois vai fundo em um ramo antes de abrir outros. Mas a **qualidade não é
garantida**: devolveu custo **18** no mapa A (contra 10 do ótimo) e **19** no
mapa B (contra 9) — subótima nos dois. E, por mergulhar em profundidade, ela
nem sempre expande pouco: no mapa A chegou a expandir 22 nós, mais que a Gulosa
(10) e o A* (14). **Conclusão:** DFS economiza memória, mas é a menos confiável
quanto à qualidade da solução.

## 3. UCS diferiu de BFS quando os custos variaram?

Sim — é exatamente o que o mapa B mostra: com a lama encarecendo o corredor
reto, a **UCS achou custo 9** (contornando) e a **BFS achou 19** (reto, menos
passos). No mapa A, de custo uniforme, as duas coincidiram (10). **Conclusão:**
UCS e BFS divergem quando o caminho mais barato é mais longo em passos; a UCS
otimiza custo, a BFS otimiza passos.

## 4. A busca gulosa foi eficiente? Foi ótima?

Eficiente sim: expandiu pouquíssimos nós (10 no mapa A, 7 no mapa B), pois corre
direto na direção do objetivo segundo h(n). Ótima **não**: no mapa B ela ignora
o custo e entra na lama (custo 19, contra 9 do ótimo). No mapa A ela foi ótima
por sorte (10, igual ao A*). **Conclusão:** a Gulosa é rápida, mas pode ser
subótima porque desconsidera o custo já percorrido.

## 5. A* equilibrou qualidade da solução e eficiência?

Sim. Ele entrega o **custo ótimo** (10 no mapa A, 9 no mapa B, igual à UCS) e,
graças à heurística, **expande bem menos nós** que a UCS para chegar lá: 14
contra 28 no mapa A e 10 contra 14 no mapa B. **Conclusão:** A* combina a
otimalidade da UCS com a orientação ao objetivo da Gulosa.

## 6. A heurística utilizada é admissível? Justifique.

Sim. A distância de Manhattan h(n) = |xₙ − x_B| + |yₙ − y_B| conta o número
**mínimo** de passos até B ignorando paredes e lama. Como o menor custo possível
por passo é 1, esse valor **nunca superestima** o custo real do caminho — que só
pode ser maior (por desvios em torno de paredes ou por células de lama, que
custam 3). Por nunca superestimar, ela é **admissível** e garante que o A*
encontre o caminho de custo ótimo.
