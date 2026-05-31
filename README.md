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
  genetico.py        # bônus: Algoritmo Genético (OX + torneio + elitismo)
parte4_online/
  online.py          # agente online (replanning A*, mapa interno, percepção r=1)
viz/
  render.py          # visualização no terminal (com '@' do agente no modo online)
  graficos.py        # curva de convergência (matplotlib)
mapas/               # labirintos de teste (legenda: # parede, ' ' livre, ~ lama, A, B, C, ?)
experimentos.py        # Parte II: tabela comparativa das buscas clássicas
experimentos_local.py  # Parte III: busca local + gráfico de convergência
experimentos_online.py # Parte IV: busca online + razão online/offline
docs/                  # modelagem PEAS, análises (Partes II–IV) e relatorio.md (consolidado)
uso_ia.md              # declaração de uso de IA (obrigatório)
```

## Como rodar

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt  # matplotlib

.venv/bin/python experimentos.py                          # Parte II (mapas/exemplo.txt)
.venv/bin/python experimentos.py mapas/X.txt              # Parte II em outro mapa
.venv/bin/python experimentos_local.py                    # Parte III (mapas/coletas.txt)
.venv/bin/python experimentos_online.py mapas/X.txt       # Parte IV
.venv/bin/python experimentos_online.py mapas/X.txt --animar  # trajetória passo a passo
```

## Cronograma

- **Semana 1** — Agente + busca clássica (BFS, DFS, UCS, Gulosa, A*). ✅
- **Semana 2** — Busca local com pontos de coleta (Hill-Climbing, Simulated Annealing). ✅
- **Semana 3** — Busca online (replanning com A*), visualização e análises. ✅
  (Falta consolidar o relatório técnico final.)
