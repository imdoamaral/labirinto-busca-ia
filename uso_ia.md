# Uso de IA Generativa

Arquivo obrigatório (seção 10.1 do enunciado). Documenta de forma honesta como ferramentas de IA generativa foram usadas como apoio, sem substituir o entendimento do grupo.

## 1. Ferramentas utilizadas

- **Claude Code (Anthropic)** — assistente de programação agêntico operado via linha de comando (CLI oficial da Anthropic).
  - **Modelo:** Claude Opus 4.8 — o modelo de maior capacidade da Anthropic, da família Claude 4.X (a mais recente), voltado a tarefas de raciocínio e programação mais complexas.

## 2. Principais prompts utilizados

> Reproduzidos **literalmente** como digitados pelo grupo (grafia original
> preservada). Seleção dos prompts que conduziram o trabalho; omitidos os de
> rotina (commits/push, escolha do nome do repositório, dúvidas de ambiente).

**Planejamento e definições iniciais**

1. "Analise o arquivo 'Enunciado - Trabalho Prático.pdf' (na raiz do diretorio
   atual) e proponha um planejamento para a execuçao deste trabalho pratico. A
   divisao de tarefas/etapas pode seguir o proprio cronograma de 3 semanas
   proposto pelo enunciado na pagina 11. Tenha atençao especial a as regras de
   uso de IA generativa descritos na pagina 12. E ainda com relaçao ao codigo:
   utilize logica clara e minimalista, sempre que possivel use funçoes nativas e
   mantenha o estado padrao. Tenha em mente tambem que o objetivo desta atividade
   é o aprendizado, logo é razoavel assumir que os alunos que vao apresentar nao
   tem pleno dominio dos algoritmos que serao utilizados e precisarao de
   esclarecimentos (comentarios?) nas partes complicadas. A fonte primaria de
   pesquisa devera os slides de aula da pasta slides_aula, os slides estao
   nomeados por tema."
2. "Algumas duvidas antes de prosseguir: Qual a diferença de visualizaçao no
   terminal vs matplotlib? E qual a diferença pratica de usar A* ou DFS? E onde
   caberia o uso de um jupyter notebook? O professor cita essa possibilidade,
   creio que para analises, mas diga como vc pensou em fazer e caso se aplique os
   possiveis tradeoffs de usar notebook. Adicione a a memoria os criterios de
   penalizaçao, caso ja o tenha feito ou considere desncessario nesse momento,
   ignore. Como o professor propoe a geraçao de mapas/labirintos? Usaremos o que
   esta no slide? Ele se aplica a todos os problemas? Digo isso porque ele
   disponibilizou uma ferramenta externa 'criadora de labirintos' em
   https://www.asciiart.eu/ascii-maze-generator"
3. "Sim, pode começar a Semana 1 — inicialize o git também"

**Implementação (Semanas 1–3 e bônus)**

4. "prossiga com o item 1, depois o item 2."
5. "prossiga com a Semana 2"
6. "prossiga com a Semana 3"
7. "monte o relatorio.md reunindo as análises"
8. "implemente o bônus do Algoritmo Genético"

**Visualização e relatório**

9. "Com relaçao ao arquivo docs/relatorio.md: vc adicionou 2 graficos sem
   contexto proximo, adicione ao menos um pequeno texto antes/depois da imagem
   indicando o que esta acontecendo no grafico/como interpretar"
10. "como eu faço pra visualizar a animaçao dos agentes em cada busca e como eu
    gero uma imagem estatica do percurso pra poder colocar no relatorio final?
    Acredito que isso va ser bastante agregador no projeto"
11. "na figura 'gulosa - armadilha_gulosa' o texto acima menciona que a lama é
    bege e as celulas exploradas sao azuis, porem o corredor reto entre A e B
    esta totalmente cinza, com exceçao das celulas dos pontos de inicio e
    objetivo. / na figura 'a* - 'armadilha_gulosa' a celula imediatamente a a
    direita do ponto de inicio A esta na cor cinza - quando na verdade deveria
    estar na cor bege (lama)"
12. "em relatorio.md: tem como inserir os respectivos mapas (em arte ascii) mesmo
    antes das tabelas? O que vc acha da sugestao?"
13. "O relatorio diz: \"A Gulosa segue só a heurística e mergulha reto pela lama
    até B: explora pouquíssimas células (8)...\" - que heuristica é essa? Achei
    que a busca gulosa nao olhasse heuristica"

**Estudo para a defesa**

14. "Como vc sugere que eu aprenda os topicos necessarios descritos no final do
    documento uso_ia.md? Eu pensei em flashcard, repetiçao espaçada, pensei em
    ate mesmo escrever o pseudocodigo dos algoritmos de busca antes de sua
    implementaçao principal, para facilitar entendimento. O que vc sugere nesse
    caso? A apresentaçao sera daqui uma semana."

**Revisão final (consistência com o enunciado)**

15. "Estava revisando o relatorio final e observei que o exemplo de labirinto
    exemplo.txt do relatorio esta diferente do enunciado (abaixo): [mapa 11×7 do
    enunciado colado]"
16. "O problema é q eu nao sei como exatamente chegamos exemplos.txt atual, pois
    ele muda muita coisa. Conseguimos recuperar isso na memoria? Caso contrario
    acho que podemos concluir que foi mesmo um erro de extraçao e deveriamos
    tentar adicionar a lama (esse é o único diferencial relevante?) no mapa do
    enunciado."
17. "sim, pode aplicar e regenerar as figuras, mas antes, saiba que a ordem de
    exploraçao dos nos em uma arvore de estados é por padrao da esquerda para a
    direita, certifique-se de estar seguindo essa convençao"
18. "Em relatorio.md, a tabela da seçao 3.2 resultados nao segue o mesmo padrao
    do que é pedido no enunciado pagina 5, a coluna explorados q vc colocou nao
    existe no enunciado, e a coluna tempo do enunciado nao existe no relatorio."
19. "fronteira na tabela quer dizer o que na pratica?"
20. "Ainda no relatorio.md eu removi a seçao 3.4 de imagens e estive pensando em
    inserir as imagens de acordo com cada analise da seçao 3.3. O que acha?"
21. "em docs/figuras/parte2/armadilha_gulosa_BFS.gif a animaçao ta alihada com
    aquele conceito de ir da direita para a esquerda? E fiquei com outra duvida:
    se ela explora por niveis, ela nao deveria explorar o primeiro nivel (segunda
    linha) inteiro antes de passar ao segundo? Qual o criterio pra decidir se o
    nivel é vertical, horizontal, linha ou coluna?"
22. "nos exemplos png/gif do dfs ele coincidentemente passa pelos pontos de
    coleta, certo? Nao existe nenhuma interferencia deles no percurso"

## 3. Trechos de códigos sugeridos por IA

A implementação inicial de todas as partes foi gerada com apoio da IA e depois
**revisada, ajustada e testada pelo grupo**. As métricas das tabelas vêm sempre
da execução dos scripts, nunca inventadas. Principais blocos:

- **Núcleo (`core/`):** leitura de mapas (`mapa.py`), formulação formal do problema ⟨S, A, T, s₀, G, c⟩ (`problema.py`) e coleta de métricas (`metricas.py`).

- **Parte II (`parte2_classica/buscas.py`):** esqueleto comum das cinco buscas, diferindo apenas na estrutura da fronteira (fila FIFO, pilha LIFO ou heap).

- **Parte III (`parte3_local/`):** matriz de distâncias reaproveitando o A* (`distancias.py`), função de custo da rota (`custo.py`), Hill-Climbing, Simulated Annealing, vizinhança por inversão de trecho (`vizinhanca.py`) e o bônus de Algoritmo Genético (torneio, OX, elitismo — `genetico.py`).

- **Parte IV (`parte4_online/online.py`):** agente online com replanning A*, mapa interno, percepção de raio 1 e free-space assumption.

- **Visualização (`viz/`):** renderização no terminal (`render.py`), figuras de percurso/exploração em PNG/GIF (`figuras.py`) e gráficos de convergência (`graficos.py`).

- **Scripts e mapas:** `experimentos.py`, `experimentos_local.py`,
  `experimentos_online.py`, `gerar_figuras.py` e o mapa
  `mapas/armadilha_gulosa.txt` (corredor de lama + desvio livre).

## 4. Sugestões da IA não adotadas pelo grupo

- **Como reconciliar o `exemplo.txt`:** ao corrigir a divergência com o enunciado, a IA ofereceu opções (renomear o arquivo, manter o mapa próprio com uma nota explicativa, ou adicionar lama ao mapa do enunciado). O grupo **rejeitou todas** e optou por reproduzir o mapa do enunciado **puro** (custo uniforme), deixando a demonstração de custo variável só no `armadilha_gulosa.txt`.

- **Galeria de figuras separada:** o relatório reunia as figuras da Parte II numa seção própria (3.4). O grupo preferiu **distribuir cada figura junto da análise correspondente** (seção 3.3) e removeu a seção separada.

## 5. Erros cometidos pela IA (e como foram corrigidos)

- **Mapa de exemplo divergente do enunciado.** A IA criou `mapas/exemplo.txt` como um labirinto próprio (com lama e dimensões diferentes), em vez de reproduzir o exemplo do enunciado, e não houve conferência no momento da criação. *Correção:* na revisão final o mapa foi substituído pelo do enunciado (puro) e todas as tabelas e figuras foram regeradas.

- **DFS fora da convenção de exploração.** Por usar uma pilha LIFO empilhando os sucessores na ordem de geração, a DFS acabava explorando-os da **direita para a esquerda**, fora da convenção padrão (esquerda→direita: o primeiro sucessor gerado é o primeiro explorado). Isso alterava o caminho encontrado e mascarava a
subotimalidade esperada do algoritmo. *Correção:* empilhar os sucessores em ordem reversa, para que a pilha os desempilhe na ordem de geração.

- **Tabela de resultados fora do modelo do enunciado.** A tabela da Parte II trazia uma coluna "Explorados" inexistente no modelo da seção 5.3 e omitia a coluna "Tempo". *Correção:* removida "Explorados" e incluída "Tempo" em `relatorio.md` e `analise_parte2.md`.

- **Cores das figuras da Parte II.** As células de lama apareciam acinzentadas em vez de bege (um preenchimento translúcido misturava as cores), divergindo da legenda do texto. *Correção:* a renderização passou a usar hachura para marcar a  exploração, mantendo a lama visivelmente bege (`viz/figuras.py`).

## 6. Validação e preparação para a defesa

### 6.1 Como a solução foi validada
- As métricas de todas as tabelas vêm da execução dos scripts (`experimentos*.py`) — nunca inventadas — e foram **regeradas a cada alteração** de mapa ou algoritmo.

- **Parte II:** a heurística de Manhattan é admissível, então o custo do A* é o ótimo; conferido contra a UCS (mesmos custos).

- **Parte III:** o ótimo global (32) foi confirmado por **força bruta** sobre as 8! = 40320 permutações, e Hill-Climbing, Simulated Annealing e GA foram comparados a ele (30 execuções por método).

- **Parte IV:** o trajeto online é comparado ao caminho ótimo offline pela razão online/offline (1.00 quando coincide).

- **Revisão final:** o `exemplo.txt` foi conferido contra o enunciado e a ordem de exploração da DFS contra a convenção esquerda→direita.

### 6.2 Tópicos que cada integrante deve saber defender
> Cada integrante deve conseguir explicar/defender sem consultar material de apoio:

- [ ] Por que BFS encontra o caminho com menos passos e quando isso coincide com o menor custo.
- [ ] Por que DFS é rápida mas não garante a melhor solução.
- [ ] Como a UCS usa o custo acumulado g(n) e por que difere da BFS com a lama.
- [ ] Por que a Busca Gulosa pode ser subótima.
- [ ] Como o A* combina g(n)+h(n) e por que a heurística de Manhattan é admissível.
- [ ] Como a rota é representada e como C(s) usa as distâncias do A*.
- [ ] Por que o Hill-Climbing fica preso em mínimos locais.
- [ ] Como o Simulated Annealing aceita pioras (exp(−Δ/T)) para escapar deles.
- [ ] Efeito da temperatura inicial e da taxa de resfriamento na convergência.
- [ ] O ciclo perceber→atualizar→planejar→agir e a free-space assumption.
- [ ] Por que a razão online/offline pode ser > 1 (preço de não conhecer o mapa).
- [ ] Como o GA representa indivíduos e por que o cruzamento OX preserva permutações.