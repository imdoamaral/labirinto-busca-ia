# Parte IV — Análise da Busca Online (seção 7.5)

Agente online com **replanning A\*** (Opção A): mapa interno começa todo
desconhecido ('?'), percepção de raio 1, e a cada passo roda A* assumindo o
desconhecido como livre, anda um passo e replaneja. Reproduzir com
`python experimentos_online.py <mapa>`.

## Premissas
O agente conhece o **tamanho** do labirinto e as posições de **início** e
**objetivo**, mas **não** conhece as paredes. Como percebe os vizinhos antes de
agir, nunca entra numa parede; mas pode descobrir paredes à frente e ter de
replanejar.

## Métricas (seção 7.4)

| Mapa | Sucesso | Movimentos | Custo real | Reveladas | Revisitadas | Replanej. | Ótimo offline | Razão |
|------|:-------:|:----------:|:----------:|:---------:|:-----------:|:---------:|:-------------:|:-----:|
| `exemplo.txt`          | sim | 10 | 10 | 34 | 0 | 10 | 10 | **1.00** |
| `online_armadilha.txt` | sim | 20 | 20 | 50 | 3 | 20 | 14 | **1.43** |

A **razão online/offline** é a métrica central: 1.00 significa que o agente foi
tão bom quanto teria sido com o mapa completo; 1.43 significa que pagou 43% a
mais por não conhecer o ambiente.

---

## 1. O agente online tomou decisões subótimas? Por quê?

Depende do mapa. No `exemplo.txt`, **não** (razão 1.00): a suposição de que o
desconhecido é livre coincidiu com a realidade. No `online_armadilha.txt`,
**sim** (razão 1.43): o objetivo ficava logo abaixo do início, então o A*
otimista desceu reto por uma coluna que terminava em **beco sem saída**; só ao
chegar ao fim o agente percebeu a parede e teve de voltar e contornar. A
subotimalidade vem justamente de **agir com base numa suposição otimista** antes
de conhecer os obstáculos.

## 2. Quais informações faltavam ao agente?

A **localização das paredes** além do seu campo de percepção (raio 1). Ele sabia
o tamanho do mapa e onde estavam início e objetivo, mas descobria os obstáculos
só ao chegar perto deles — por isso apostou num caminho que não existia.

## 3. O mapa interno convergiu para o mapa real?

Apenas **parcialmente**, na região explorada. No `online_armadilha.txt` foram
reveladas 50 das 56 células; no `exemplo.txt`, 34 de 77. Células fora da
trajetória permanecem '?' (ver o mapa interno final). Ou seja, o agente constrói
um modelo **suficiente para chegar ao objetivo**, não um mapa completo.

## 4. O agente revisitou muitas células?

Poucas, e só quando precisou voltar: 0 revisitas no `exemplo.txt` e 3 no
`online_armadilha.txt` (a subida de volta pelo beco). Com replanning A* e
percepção de vizinhos, as revisitas se concentram nos **backtrackings** ao
descobrir um caminho sem saída.

## 5. Como melhorar a exploração?

- **Aumentar o raio de percepção** (r > 1): revela mais a cada passo e reduz
  apostas em becos.
- **Suposição menos otimista** para o desconhecido (atribuir um custo extra a
  células '?'), desencorajando entrar em regiões não confirmadas.
- **Memória de becos**: marcar caminhos sem saída para não tentá-los de novo.
- Usar algoritmos de replanejamento incremental (ex.: D\* Lite) ou LRTA\*, mais
  eficientes que recalcular o A* do zero a cada passo.

## 6. O que diferencia busca online de busca clássica?

A **busca clássica planeja uma vez com o mapa completo** e segue o caminho ótimo.
A **busca online intercala perceber → planejar → agir**, descobrindo o mapa
enquanto se move; por isso pode tomar decisões subótimas (razão ≥ 1) e replaneja
várias vezes (aqui, um replanejamento por passo). A razão online/offline mede
exatamente esse "preço de não conhecer o ambiente".
