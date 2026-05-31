# Agente Inteligente em Labirinto

Trabalho prático de Inteligência Artificial: um agente que resolve labirintos em
grade sob três condições — mapa conhecido, múltiplos pontos de coleta e mapa
desconhecido — usando busca clássica, busca local e busca online.

## Estrutura

```
core/                # base reutilizável
  mapa.py            # leitura da grade e legenda
  problema.py        # formulação formal <S, A, T, s0, G, c>
  metricas.py        # coleta e tabela de métricas
parte2_classica/
  buscas.py          # BFS, DFS, UCS, Gulosa, A*
parte3_local/
  distancias.py      # matriz d(X,Y) via A*
  custo.py           # representação da rota e função de custo C(s)
  vizinhanca.py      # vizinhança por inversão de trecho (2-opt)
  hill_climbing.py
  simulated_annealing.py
viz/
  render.py          # visualização no terminal
  graficos.py        # curva de convergência (matplotlib)
mapas/               # labirintos de teste (legenda: # parede, ' ' livre, ~ lama, A, B, C, ?)
experimentos.py      # Parte II: tabela comparativa das buscas clássicas
experimentos_local.py# Parte III: busca local + gráfico de convergência
docs/                # modelagem PEAS e análises (Partes II e III)
uso_ia.md            # declaração de uso de IA (obrigatório)
```

## Como rodar

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt  # matplotlib

.venv/bin/python experimentos.py              # Parte II (mapas/exemplo.txt)
.venv/bin/python experimentos.py mapas/X.txt  # Parte II em outro mapa
.venv/bin/python experimentos_local.py        # Parte III (mapas/coletas.txt)
```

## Cronograma

- **Semana 1** — Agente + busca clássica (BFS, DFS, UCS, Gulosa, A*). ✅
- **Semana 2** — Busca local com pontos de coleta (Hill-Climbing, Simulated Annealing). ✅
- **Semana 3** — Busca online (replanning com A*), visualização, relatório e defesa.
