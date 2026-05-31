# Parte III — Análise da Busca Local (seção 6.6)

Otimização da ordem de visitação dos pontos de coleta no mapa
`mapas/coletas.txt` (8 pontos de coleta). Reproduzir com
`python experimentos_local.py`.

## Configuração
- **Representação (6.1):** ordem (permutação) dos pontos de coleta;
  rota = A → ordem → B.
- **Custo (6.2):** C(s) = d(A, ordem[0]) + Σ d(ordem[i], ordem[i+1]) + d(ordem[-1], B),
  com d(X,Y) = custo do menor caminho calculado por **A\*** (reaproveitado da
  Parte II), considerando a lama (custo 3).
- **Vizinhança (6.4):** inversão de um trecho da ordem (movimento 2-opt).
  *Justificativa:* desfaz "cruzamentos" da rota preservando boa parte da
  sequência; costuma ser mais eficaz que a simples troca de dois pontos.
- **Execuções:** 30 reinícios aleatórios por método; ótimo global obtido por
  força bruta (8! = 40320 permutações) = **32**.

## Métricas (seção 6.5)

| Método | Melhor | Pior | Médio | Tempo méd. | Iter. méd. | Sucesso |
|--------|:------:|:----:|:-----:|:----------:|:----------:|:-------:|
| Hill-Climbing       | 32 | 38 | 33.1 | 0.18 ms | 4    | 73%  |
| Simulated Annealing | 32 | 32 | 32.0 | 6.32 ms | 2297 | 100% |

Curva de convergência (iteração × melhor custo): `docs/figuras/convergencia_local.png`.

### Sensibilidade do Simulated Annealing
Taxa de sucesso em atingir o ótimo (30 execuções por configuração):

| Temp. inicial | Resfr. 0.90 | Resfr. 0.99 | Resfr. 0.999 |
|:-------------:|:-----------:|:-----------:|:------------:|
| 1     | 53% | 100% | 100% |
| 10    | 67% | 100% | 100% |
| 100   | 70% | 100% | 100% |
| 1000  | 70% | 100% | 100% |

---

## 1. Hill-Climbing ficou preso em mínimo local?

Sim. Em 30 execuções, a taxa de sucesso foi de **73%** — em ~27% das vezes ele
parou num **mínimo local** (pior custo **38** contra o ótimo **32**). Como a
subida de encosta só aceita movimentos que melhoram, ela trava no primeiro
ponto sem vizinho melhor, e o resultado depende fortemente da ordem inicial
sorteada.

## 2. Simulated Annealing encontrou soluções melhores?

Sim. Atingiu o ótimo (32) em **100%** das execuções, contra 73% do
Hill-Climbing, e com custo médio melhor (32.0 vs 33.1). Por aceitar pioras com
probabilidade exp(−Δ/T), ele consegue sair dos mínimos locais que prendem o HC.

## 3. Como a temperatura inicial influenciou os resultados?

O efeito é secundário, e só aparece quando o resfriamento é rápido demais. Com
resfriamento 0.90, subir a temperatura inicial de 1 para 100 elevou o sucesso de
**53% para 70%**: temperatura inicial maior aceita mais pioras no começo,
favorecendo a exploração. Com resfriamento adequado (0.99 ou 0.999), a
temperatura inicial deixa de importar — todas as configurações chegaram a 100%.

## 4. Como a taxa de resfriamento afetou a convergência?

Foi o **fator dominante**. Resfriar rápido (0.90) encerra a busca em poucas
iterações (~110), sem tempo de explorar, e o sucesso cai para **53–70%**.
Resfriar devagar (0.99 ≈ 1150 iterações; 0.999 ≈ 11500) deu **100%** de sucesso,
ao custo de mais iterações e mais tempo. Ou seja: resfriamento lento melhora a
qualidade, mas tem preço em tempo de execução.

## 5. A busca local encontrou sempre a solução ótima?

O **Hill-Climbing não** (73%): ele é sensível a mínimos locais. O **Simulated
Annealing sim** neste problema, desde que bem parametrizado (resfriamento ≥ 0.99).
Vale lembrar que, em geral, a busca local **não garante** o ótimo global — aqui
pudemos confirmar a otimalidade só porque há poucos pontos e foi possível
calcular o ótimo por força bruta.

## 6. Qual foi o compromisso entre tempo e qualidade?

O Hill-Climbing é **muito rápido** (~0.18 ms, ~4 iterações) mas tem qualidade
inferior (73%). O Simulated Annealing é **~35× mais lento** (~6.3 ms, ~2300
iterações) e entrega qualidade máxima (100%). O resfriamento controla esse
compromisso: mais lento = melhor qualidade e mais tempo. Uma estratégia prática
e barata é **Hill-Climbing com vários reinícios aleatórios**, que se aproxima da
qualidade do SA usando pouco tempo por execução.
