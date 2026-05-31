# Agente Inteligente em Labirinto

Trabalho prático de Inteligência Artificial: um agente que resolve labirintos em
grade sob três condições — mapa conhecido, múltiplos pontos de coleta e mapa
desconhecido — usando busca clássica, busca local e busca online.

## Estrutura

```
core/            # base reutilizável
  mapa.py        # leitura da grade e legenda
  problema.py    # formulação formal <S, A, T, s0, G, c>
  metricas.py    # coleta e tabela de métricas
parte2_classica/
  buscas.py      # BFS, DFS, UCS, Gulosa, A*
viz/
  render.py      # visualização no terminal
mapas/           # labirintos de teste (legenda: # parede, ' ' livre, ~ lama, A, B, C, ?)
experimentos.py  # roda as buscas e imprime a tabela comparativa
docs/modelagem.md# modelagem PEAS e formulação formal
uso_ia.md        # declaração de uso de IA (obrigatório)
```

## Como rodar

```bash
python experimentos.py              # usa mapas/exemplo.txt
python experimentos.py mapas/X.txt  # usa outro mapa
```

## Cronograma

- **Semana 1** — Agente + busca clássica (BFS, DFS, UCS, Gulosa, A*). ✅ em andamento
- **Semana 2** — Busca local com pontos de coleta (Hill-Climbing, Simulated Annealing).
- **Semana 3** — Busca online (replanning com A*), visualização, relatório e defesa.
