# Dimensionamento de Histograma — instruções do projeto

App web da Volga Engenharia (Departamento de Instalação) que monta composições de serviço, cronograma e
histograma de recursos a partir de uma base de atividades com coeficientes (h por unidade).
Publicado pelo coordenador, Arthur, em https://dimensionamento-de-histograma.web.app (Firebase Hosting).
Quem pede e valida as mudanças: Osvaldo (planejamento). Os dois são administradores no app.

## Regras permanentes (não negociáveis)

1. **Um único arquivo.** Todo o app é o `index.html`: HTML, CSS, JS e dados. Sem dependência nova, sem
   etapa de compilação, sem arquivos auxiliares carregados em tempo de execução. A única dependência
   externa é o Firebase 10.14.1 (compat) por CDN.
2. **1 rodada = 1 versão = 1 index.html + 1 documento para o coordenador.** O documento lista só o que o
   usuário percebe; detalhe técnico vai para `docs/HISTORICO_TECNICO.md` (e a cópia em `versoes/`).
3. **Numeração X.Y.Z, sem sufixo.** X = exige converter projetos salvos; Y = funcionalidade nova;
   Z = correção sem funcionalidade nova. Atualizar em 3 lugares: comentário da 1ª linha, `APP_VERSION` e
   uma entrada nova no topo de `NOVIDADES` (linguagem de usuário). **Nunca apagar entradas antigas de
   NOVIDADES.**
4. **Nunca gravar na base compartilhada** (Firestore `base_global/catalogo`, recursos, biblioteca).
   Atividade nova entra no bloco `dados-base` e no bloco `dados-atividades-novas`; o app mostra "só no app"
   e o administrador usa "Incluir na base". Correções em atividades que já estão na nuvem são pedidas ao
   Arthur (a nuvem prevalece sobre a cópia embutida).
5. **Pendência ou erro de engenharia é decidido com o Osvaldo antes da versão sair.** O arquivo não carrega
   avisos de "revisão pendente" nem linhas de situação nas observações.
6. **Nenhum número muda sem ser declarado.** Rodar os testes; diferença de HH, duração ou dias em relação a
   `testes/referencia.json` só se estiver explicada no documento da versão — depois atualizar a referência.
7. Não digitar senhas nem criar contas. O Osvaldo faz login ele mesmo.
8. Respostas e documentos em português; análise profunda; perguntar antes quando a resposta muda o resultado.

## Estrutura

```
Volga Arthur/
  index.html                  original recebido (não mexer; = v1.0.0)
  projeto/                    ← cópia de trabalho do repositório Git (ver "Fluxo Git")
    index.html                última versão
    CLAUDE.md                 este arquivo
    README.md / LEIA-ME.md    para pessoas: o que é, como publicar e como testar
    testes/rodar.py           todos os testes num comando
    testes/referencia.json    HH, duração e dias de cada composição padrão (valores de referência)
    docs/                     histórico técnico e guia da pasta de versões
    ferramentas/              geradores antigos (1.5.0–1.9.0) e criar-repositorio.ps1
    .github/                  GitHub Actions (testes) e modelo de PR
  versoes/
    LEIA-ME.txt               qual arquivo publicar, como voltar
    HISTORICO_TECNICO.md      detalhes técnicos de cada versão
    vX.Y.Z/index.html         versões prontas para publicar + atalhos dos documentos + .json do projeto TESTE
    publicado-2026-10-19/     cópia exata do que estava no site antes da 1.5.0
```

## Mapa do index.html

- **Blocos de dados** (`<script type="application/json">`, logo antes do script principal):
  - `dados-base` — `{"recursos": [[nome, tipo]...], "base": [[código, disciplina, grupo, serviço, unidade,
    fonte, observação, {recurso: h/un}]...]}`. Uma atividade por linha. Cópia da base da nuvem v22 + novas.
  - `dados-atividades-novas` — códigos que ainda não estão na nuvem.
  - `dados-composicoes` — composições padrão: `id, nome, disc, crewDef`, `params` (entradas
    `{k, l, u, d, o?}`), `vars` (parâmetros `[identificador, fórmula, nome]`), `acts` (`{cod, q}`; `cod` pode
    ser `{by, map}` para escolha por entrada), `notas`.
  - `dados-nomes-antigos` — nomes de parâmetros de versões antigas (projetos salvos).
- **Script principal**: índice no topo; seções `§1` a `§18` (procure "═══ §"). Cálculo puro em §3–§5
  (`compEval`, `compCalc`, `schedule`, `histo`); telas em §6–§12; nuvem em §13–§15; `validarDados()` em §16;
  copiar tabela em §17; busca rápida Ctrl+K em §18 (`cmdkFontes` lista o que pode ser buscado — ação nova
  que o usuário repete deve entrar lá). Colar do Excel (`lerColagem`, `colarExcel`) fica em §9.
- Janelas: `uiDialog({title, msg, fields, buttons, wide, mono})` (campos `input`, `select` com `opts` ou
  `textarea`); atalhos `ask`, `askText`, `askForm`; avisos com `toast(msg, tipo)` (`alert()` já cai no `toast`). Não usar `prompt`/`confirm` do navegador.
- Fórmulas: avaliador próprio (`compileExpr`, sem `eval`); identificadores das entradas e parâmetros, mais
  `sqrt ceil floor max min PI` e `+ - * / ** ( ) < > ? :`.
- Disciplinas e cores: `DISC_COR` / `discKey()` (civil terracota, eletromecânica azul, instalações âmbar,
  demais cinza). A base usa "INST. ELÉTRICAS" e as composições "INSTALAÇÕES ELÉTRICAS".

## Como fazer uma versão

1. Conferir se o site mudou (o Arthur também publica). Se mudou, trazer as mudanças dele primeiro
   (commit no ramo `site-arthur`, citando-o).
2. Ramo novo `versao/X.Y.Z`. Editar `index.html` direto (dados nos blocos JSON; código nas seções).
3. `python testes/rodar.py index.html` → tem que dar `RESULTADO: OK` (ou só diferenças declaradas).
4. Se as diferenças forem intencionais: declarar no documento da versão e rodar com `--atualizar-referencia`.
5. Gerar o projeto TESTE: `python testes/rodar.py index.html --teste-json ../versoes/vX.Y.Z/TESTE_composicoes_civil_vX.Y.Z.json`.
6. Copiar para `versoes/vX.Y.Z/index.html`; documento da versão (Claude Docs) + atalho `.url` na pasta;
   atualizar `versoes/LEIA-ME.txt`, `versoes/HISTORICO_TECNICO.md` e `docs/HISTORICO_TECNICO.md`.
7. PR para `main`; merge com testes verdes; etiqueta anotada `vX.Y.Z`; Release com o `index.html` anexado.
   A sessão de IA abre o PR pela API; o merge, a etiqueta e a Release são feitos pelo Osvaldo no PowerShell
   (a sessão recebe 403 para enviar etiquetas e criar Releases) — entregar os comandos prontos.
8. Conferir em 1.366 px e 390 px (os testes já verificam rolagem lateral).

## Fluxo Git (repositório privado OsvaldoSantana/dimensionamento-de-histograma)

- O Git é só para o Osvaldo e para as sessões de IA. O Arthur não usa Git: ele recebe o `index.html`
  (anexo da Release ou da pasta `versoes`) e publica como sempre.
- `main` = sempre a última versão publicável, com testes passando. Não commitar direto em `main`.
- Cada rodada num ramo `versao/X.Y.Z` (ou `correcao/...`). Commits pequenos, mensagem em português com
  prefixo: `feat:` funcionalidade, `fix:` correção, `dados:` base/composições, `docs:` documentação,
  `test:` testes, `chore:` organização. Corpo explica o porquê e cita composições/códigos afetados.
- Abrir pedido de revisão (PR) para `main` com o modelo de `.github/pull_request_template.md`; o GitHub
  Actions roda `testes/rodar.py`. Merge só com testes verdes.
- Depois do merge: etiqueta anotada `vX.Y.Z` e Release com o `index.html` anexado e as novidades da versão.
- Mudanças que o Arthur publicar direto no site entram como commit próprio no ramo `site-arthur`,
  citando-o na mensagem, e são juntadas a `main` na rodada seguinte.
- Nunca commitar senhas, chaves ou dados de projetos de clientes. O `firebaseConfig` do index.html é
  público por natureza (identifica o projeto Firebase), não é segredo.

## Fontes de coeficientes

- SINAPI: conferir em https://buscadorsinapi.com.br/composicao/<código> (referência setembro/2026 usada na
  revisão de 20/10/2026). ORSE, GOINFRA, SICRO e DNIT não têm consulta aberta.
- Na base, "Aux. Pedreiro" = servente; equipamentos somam CHP + CHI quando a base já fez isso.
- A revisão completa da civil (fonte e situação de cada atividade) está no documento "Revisão da civil —
  fontes e quantidades (v1.7.0)"; o plano de evolução em "Plano de implantação — Dimensionamento de Histograma".

## Testes

`python testes/rodar.py <index.html>` abre o arquivo num Chromium com o Firebase simulado (nada vai para a
nuvem), percorre as abas, roda `validarDados()`, compara HH/duração/dias das 38 composições com a referência,
confere a tela Composições, a busca rápida (Ctrl+K), a leitura do Colar do Excel e a largura em 390 px.
Requisitos em `testes/requisitos.txt`.
