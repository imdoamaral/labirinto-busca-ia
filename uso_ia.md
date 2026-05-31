# Uso de IA Generativa

Arquivo obrigatório (seção 10.1 do enunciado). Documenta de forma honesta como
ferramentas de IA generativa foram usadas como apoio, sem substituir o
entendimento do grupo. **O grupo não entrega solução que não compreende.**

## 1. Ferramentas utilizadas

- **Claude (Anthropic)** — apoio no planejamento, geração inicial de código e
  esclarecimento de algoritmos.

## 2. Principais prompts utilizados

- Análise do enunciado e proposta de planejamento das 3 semanas.
- Esclarecimento das diferenças práticas entre as estratégias (terminal vs.
  matplotlib; A* online vs. DFS online; papel do notebook; geração de mapas).
- Geração da fundação da Semana 1: leitura de mapas, formulação formal do
  problema, BFS/DFS/UCS/Gulosa/A* e coleta de métricas.
- Projeto de um mapa para evidenciar a subotimalidade da Busca Gulosa e a
  diferença entre BFS e UCS com custos variados.
- Redação das respostas das questões de análise da Parte II (seção 5.4) a partir
  dos números medidos nos experimentos.
- Parte III: matriz de distâncias (reaproveitando o A*), função de custo da rota,
  Hill-Climbing, Simulated Annealing, vizinhança por inversão de trecho, gráfico
  de convergência e análise de sensibilidade (temperatura/resfriamento).

## 3. O que foi gerado/adaptado com apoio de IA

- Estrutura inicial de pastas e módulos (`core/`, `parte2_classica/`, `viz/`).
- Esqueleto comum das cinco buscas (diferindo apenas na estrutura de fronteira).
- Mapa `mapas/armadilha_gulosa.txt` (corredor de lama + desvio livre) e o
  documento `docs/analise_parte2.md`. Os valores das tabelas foram obtidos
  executando `experimentos.py`, não inventados.

## 4. O que o grupo compreendeu e validou

> Preencher ao longo do desenvolvimento. Para cada parte, anotar o que cada
> integrante consegue explicar/defender sem consultar o código:

- [ ] Por que BFS encontra o caminho com menos passos e quando isso coincide
      com o menor custo.
- [ ] Por que DFS é rápida mas não garante a melhor solução.
- [ ] Como a UCS usa o custo acumulado g(n) e por que difere da BFS com a lama.
- [ ] Por que a Busca Gulosa pode ser subótima.
- [ ] Como o A* combina g(n)+h(n) e por que a heurística de Manhattan é admissível.
- [ ] Como a rota é representada e como C(s) usa as distâncias do A*.
- [ ] Por que o Hill-Climbing fica preso em mínimos locais.
- [ ] Como o Simulated Annealing aceita pioras (exp(−Δ/T)) para escapar deles.
- [ ] Efeito da temperatura inicial e da taxa de resfriamento na convergência.
