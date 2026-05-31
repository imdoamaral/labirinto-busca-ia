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

## 3. O que foi gerado/adaptado com apoio de IA

- Estrutura inicial de pastas e módulos (`core/`, `parte2_classica/`, `viz/`).
- Esqueleto comum das cinco buscas (diferindo apenas na estrutura de fronteira).

## 4. O que o grupo compreendeu e validou

> Preencher ao longo do desenvolvimento. Para cada parte, anotar o que cada
> integrante consegue explicar/defender sem consultar o código:

- [ ] Por que BFS encontra o caminho com menos passos e quando isso coincide
      com o menor custo.
- [ ] Por que DFS é rápida mas não garante a melhor solução.
- [ ] Como a UCS usa o custo acumulado g(n) e por que difere da BFS com a lama.
- [ ] Por que a Busca Gulosa pode ser subótima.
- [ ] Como o A* combina g(n)+h(n) e por que a heurística de Manhattan é admissível.
