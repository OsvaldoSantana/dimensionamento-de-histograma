# Histórico técnico — Dimensionamento de Histograma

Uso interno. Para o coordenador, use o documento de cada versão (atalho na pasta da versão).
Restrição de todas as versões: arquivo único `index.html`, sem build e sem dependência externa nova. As únicas externas continuam sendo os 3 scripts do Firebase compat 10.14.1 (gstatic).

| Versão | Tamanho | SHA-256 (início) | Base |
|---|---|---|---|
| 1.0.0 | 135.910 bytes | adbc762dd1c9c06b | original publicado (cópia exata) |
| 1.1.0 | 185.601 bytes | 1683c820350d1a6f | 1.0.0 |
| 1.2.0 | 195.262 bytes | c853b7c840c3f323 | 1.1.0 |
| 1.3.0 | 240.546 bytes | 56ded03c0dee8a70 | 1.2.0 |
| 1.4.0 | 255.699 bytes | 9592c8f4e7190b89 | 1.3.0 |
| publicado-2026-10-19 | 146.303 bytes | 0ba9991dfb58e39a | 1.0.0 + mudanças do Arthur (o que estava no site; base v22) |
| 1.5.0 | 287.952 bytes | e004d3abca8cfbe4 | 1.4.0 + mudanças do Arthur portadas |
| 1.5.1 | 302.976 bytes | 1beeb26732d7f856 | 1.5.0 (feita fora desta linha: cópia de tabelas, auditoria) |
| 1.6.0 | 296.996 bytes | 46a2131bb89dd192 | 1.5.1 (feita fora desta linha: revisões de composições do Osvaldo, só civil) |
| 1.6.1 | 319.524 bytes | c4a65df4afdd19e5 | 1.6.0 + correções da revisão (gerada por `v161.py`) |
| 1.7.0 | 323.984 bytes | dec7533b02a30e88 | 1.6.1 + terraplanagem, parâmetros com nome, entradas compactas, revisão da civil (gerada por `v170.py`) |
| 1.8.0 | 325.128 bytes | 412102b1691b47ef | 1.7.0 + lista/tabela/cores, sem avisos, pendências decididas (gerada por `v180.py`) |
| 1.9.0 | 332.927 bytes | ce84cdb6b8f8e106 | 1.8.0 + cabeçalho em destaque, dados em blocos JSON, índice, validarDados, testes (gerada por `v190.py`; última gerada por script) |
| 1.10.0 | ver Release v1.10.0 | ver etiqueta | 1.9.0 + encadear composições no Cronograma (editada direto no repositório) |
| 1.11.0 | ver Release v1.11.0 | ver etiqueta | 1.10.0 + densidade e uso do espaço |
| 1.12.0 | ver Release v1.12.0 | ver etiqueta | 1.11.0 + busca rápida (Ctrl+K) e Colar do Excel |

---

## 1.12.0 — 20/10/2026 · Busca rápida (Ctrl+K) e Colar do Excel

- **§18 Busca rápida** (nova seção no fim do script): `#cmdk` (caixa `#cmdk-q` com `role=combobox`, lista `#cmdk-l` com `role=listbox` e `aria-activedescendant`). `cmdkFontes(q)` monta as fontes: Ações (Nova, Adicionar atividade da base, Colar do Excel, Duplicar, Encadear se `cronSel.size>1`, Desfazer/Refazer se houver pilha, Exportar .csv/.json, Abrir projeto, Novidades), Ir para (abas de `ABAS`), Composições do projeto (ponto `discCor`) e, com 2+ caracteres, atividades da base (`pickAct` na composição aberta). Sem projeto: só abas de base, Abrir projeto e Novidades; projeto só de leitura: sem ações de edição. `cmdkFiltra`: sem acento, por palavras (todas precisam aparecer em título+subtítulo+palavras-chave); nota 0 começa com a frase, 1 contém, 2 título contém todas, 3 só no subtítulo; grupos ordenados pela melhor nota; até 40 atividades da base e 60 itens por grupo. Teclas: ↑ ↓ PageUp/PageDown Enter Esc; clique; Ctrl/⌘+K abre e fecha (escuta em captura, também dentro de campos; ignorado com `#uidlg` ou `#syncdlg` abertos). `abrirComp(id)` limpa filtro de disciplina/busca da lista se esconderem a composição.
- `ABAS` vira constante global (antes lista local em `render()`); botão `.cmdk-btn` na barra das abas (lupa SVG inline + "Buscar Ctrl K" acima de 720 px).
- **Colar do Excel (§9)**: `numBR` (pt-BR: `1.234,5`→`1234.5`, `0,30`→`0.30`, `1.250`→`1250`; formato com ponto decimal mantido), `lerColagem(txt, comp)` (separador tab ou `;`; cabeçalho reconhecido por "Código/Cód." com coluna "Fórmula" ou, na falta, "Quantidade/Qtd"; sem cabeçalho, o código é a 1ª célula que existe na base ou tem forma `AAA-0000`, e a fórmula é a 1ª célula seguinte que compila em `compileExpr` e só usa identificadores da composição ou funções; sem fórmula → `1`, contada em `semQtd`; códigos fora da base em `fora`; linhas sem código em `sem`). `colarExcel(txt?)`: caixa com `textarea` quando chamado pelo botão; conferência (`uiDialog` `wide`+`mono`) com até 12 linhas, avisos e botões Cancelar / Substituir as atuais / Adicionar ao final. Evento `paste` no documento: só na aba Composições, fora de `input/textarea/select/contenteditable`, sem janela aberta, projeto editável e com pelo menos um código reconhecido.
- `uiDialog`: campo `type:'textarea'` (com `rows`), opções `wide` (700 px) e `mono` (mensagem em fonte monoespaçada com rolagem); `vals`, foco inicial e Tab circular incluem `textarea`.
- Testes (`testes/rodar.py`): itens 6 (Ctrl+K: abre com foco, "cronog"→Cronograma, nome→composição, `civ-0001`→atividade adicionada, Ctrl+Z, Esc) e 7 (`lerColagem` com e sem cabeçalho, vírgula decimal, milhar, código fora da base, quantidade vazia). Nenhum número muda (referência 1.9.0).

## 1.11.0 — 20/10/2026 · Densidade e uso do espaço

- `main` até 2.200 px (antes 1.680 px).
- `.kpis/.kpi` (Cronograma, Histograma, Parâmetros): faixa única com bordas internas, número 20 px e rótulo ao lado (`align-items:baseline`); fundo do cartão transparente (o fundo vermelho inline de "acima do limite" continua valendo).
- Lista lateral: `.side-top` com "+ Nova" e o filtro de disciplina numa linha; itens `.side .list .it` em uma linha (ponto `.dot` na cor da disciplina, nome com reticências e `title` completo, `.ok` ✓ se `usar`, setas só no hover/selecionado). Busca escondida abaixo de 900 px (lá a lista vira o seletor "Composição").
- Cabeçalho da composição: `.chead-t` (disciplina, Duplicar, Excluir) dentro de `.chead-r`, na linha do título; `select.cdisc` até 190 px; `.cstat` com número e rótulo lado a lado.
- "Dados de entrada" dentro de `.ins`; "Atividades (n)" dentro da `.tbl-bar`; `table.acts td` com padding 5×8.
- Cronograma: `.gtools` com escala (`.gz`) e legenda na mesma linha.
- Testes: referência 1.9.0 OK; 1.920, 1.366 e 390 px conferidos por captura; altura da tela Composições em 1.920 px de 2.232 para 1.885 px.

## 1.10.0 — 20/10/2026 · Encadear composições

Primeira versão feita direto no repositório (ramo `versao/1.10.0`, PR para `main`).

- Cronograma: coluna de seleção (`td.sel`, `cronSel` — fora do projeto, não salva, não entra no desfazer) com "selecionar todas" no cabeçalho; botão "Encadear selecionadas (n)", desabilitado com menos de 2.
- `encadear()`: ordem da lista; a 1ª mantém as predecessoras; da 2ª em diante `preds=[{id:anterior,t,lag}]` (substitui); todas `usar=true`; checagem de ciclo com `dependsOn(c,c.id)` em todas — se houver, desfaz e avisa; `syncLegacyPred`; toast. Ctrl+Z desfaz (histórico do render).
- `uiDialog`: campos com `opts` viram `<select>` (tipo de vínculo); `vals`, Tab e foco incluem select.
- CSS de `table.cron` com `nth-child` deslocado em 1 pela coluna nova (composição 4, predecessoras 9, início fixo 10).
- "Marcar todas"/"Limpar seleção" renomeados para "Usar todas"/"Não usar nenhuma" (agem só na coluna Usar).
- Testes: `testes/rodar.py` OK contra a referência da 1.9.0 (nenhum número de composição mudou); teste do recurso: 3 selecionadas com II +2 → "3II+2", "4II+2"; predecessora existente substituída; Ctrl+Z restaura; ciclo bloqueado; 390 px sem rolagem.

## 1.9.0 — 20/10/2026 · Cabeçalho em destaque e base de engenharia

Gerada por `v190.py v1.8.0.html v1.9.0.html`. **Última versão gerada por script:** daqui em diante edita-se `projeto/index.html` direto (ver `projeto/CLAUDE.md`).

### Interface
- Cabeçalho da composição: `input.ctitle` (21 px, 700, borda só no hover/foco) numa linha própria; `.chead-t` com disciplina (`select.cdisc` na cor da disciplina), Duplicar, Excluir; `.cstat` com 3 blocos (23 px) e `border-left` na cor da disciplina. 390 px: 18/19 px.
- Fórmula das atividades com `title` = fórmula completa.

### Dados e código
- `const DB/SEED/VAR_ANT/ACT_NOVAS` passam a `lerDados(id)` de blocos `<script type="application/json">`: `dados-base` (uma atividade por linha), `dados-atividades-novas`, `dados-composicoes` (um item de params/vars/acts/notas por linha), `dados-nomes-antigos`. Conferido: JSON dos blocos == dados da 1.8.0.
- Índice no topo do script e marcadores `// ═══ §1…§17 ═══`.
- `validarDados()` (§16): duplicados, descrição/unidade, recurso fora da Base de recursos, coeficiente ≤ 0 ou não numérico, atividade nova sem cadastro, id/nome de composição, erro de fórmula de parâmetro e de atividade, atividade fora da base embutida, parâmetro sem nome, entrada sem descrição. Resultado na 1.9.0: [].

### Pasta projeto
- `projeto/index.html` (= 1.9.0), `CLAUDE.md`, `LEIA-ME.md`, `testes/rodar.py` (Firebase simulado; abas; validarDados; HH/dur/dias × `referencia.json` com tolerância 0,05; tela Composições; 390 px; `--atualizar-referencia`; `--teste-json`), `testes/referencia.json` (38 composições, versão 1.9.0), `testes/requisitos.txt`, `ferramentas/geradores/v150…v190.py`.
- Teste de sanidade: alterando um coeficiente (CIV-0121) e um código (CIV-0023), o runner acusou 42 falhas nas composições afetadas. Com quebras de linha CRLF (Windows) o runner funciona.

### Testes
- `rodar.py` OK; `rev160.py` e `t190b.py` sem erros; HH idênticos à 1.8.0 nas 38 composições.

## 1.8.0 — 20/10/2026 · Lista com cores, tabela de atividades, sem avisos, pendências decididas

Gerada por `v180.py v1.7.0.html v1.8.0.html`.

### Interface
- `DISC_COR` (civil #B4561F / texto #9A4A1A, eletromecânica #1F5FA8, instalações #A86B12 / texto #8A560B, geral #6B7280); `discKey()` junta "INST. ELÉTRICAS" (base) e "INSTALAÇÕES ELÉTRICAS" (composições). Contraste do texto ≥ 4,8:1.
- Lista lateral: `--dc` na faixa esquerda, só nome + disciplina (+ "no cronograma"); busca `input.lbusca` filtra no DOM (`filtraLista`, sem render, mantém o foco) e reaplica `hidden` no render (`compBusca`). Saiu "Ordem da lista".
- Cabeçalho: `.kpis` da composição → `p.cstat` com `.dtag`. Removido o bloco do aviso [BLOQUEADA]/[REVISÃO TÉCNICA] do `rComp`.
- Tabela: regras antigas `table.acts td:nth-child(3){min-width:210px}` e `(5)`/`(8)` estavam deslocadas desde a coluna de seleção (1.6.0) — trocadas por larguras por coluna; cabeçalho "Fórmula"; recursos `td.rtx` em texto; barra `.tbl-bar` recebe o botão Copiar (`insertControls` usa a barra irmã anterior se existir). Em 1366 px a tabela cabe (973 px).
- Cronograma: barras com `discCor(c.disc)` e legenda por disciplina.

### Composições e base
- cant: nome sem "(layout Milhão 25 × 21,5 m)".
- Notas iniciadas por "[BLOQUEADA]", "[REVISÃO TÉCNICA]" ou "VALIDAÇÃO:" removidas em todas as 38 (inclui as 4 de drenagem que a 1.6.0 marcou como não aprovadas).
- disj/poste/bspda/pcf: CIV-0073 → CIV-0068 (101102 = tubulão completo com concreto).
- CIV-0149 (96619, m², 0,33905/0,12265) no lugar da CIV-0074 em disj (1,0), poste (0,6), bspda (1,2), pcf (np×1,1), cerca (2×1×0,6×port).
- trafoalv: var `tg=0.1245` (3,00 m³ / 24,1 m da lista VO778-CV-207); CIV-0134 = qtd×2×(C+L)×tg.
- ccom/cmed: CIV-0150 (91341, m², 0,5548789/0,1568136) = qtd×port×0,90×2,10, após a CIV-0141.
- ACT_NOVAS + CIV-0149, CIV-0150 (29 atividades só no app).

### Testes
- `t180.py`: nome, sem notas de situação, sem CIV-0073 na civil, graute 3,00, portas 3,78/1,89 m², magro em m², nenhuma atividade faltando, lista/busca/cores, tabela (larguras, Fórmula, copiar na barra), cronograma com 3 cores e legenda, 390 px sem rolagem.
- `rev160.py`, `t180b.py`: sem erros. HH 1.7.0→1.8.0: trafoalv 231,0→276,6; ccom 307,9→310,6; cmed 106,6→108,0; disj 45,0→42,5; poste 10,6→9,4; bspda 45,4→38,7; pcf 47,4→38,4.

## 1.7.0 — 20/10/2026 · Terraplanagem, parâmetros com nome, entradas compactas, revisão da civil

Gerada por `v170.py v1.6.1.html v1.7.0.html` (scratchpad `ver/`).

### Dados
- `SEED.vars` passa a `[k, f, nome]`; `defaults()` copia `l` para `{k,f,l}`. Nova `const VAR_ANT` com nomes de parâmetros de versões anteriores (terra, limp, cmed, pcf) para projetos salvos.
- `varLabel(c,w)`: `w.l` → nome da composição padrão de mesmo `id` → de mesmo `nome` → vazio ("Sem nome"). `nomeVar(i)` renomeia (grava `w.l`).
- `compEval` devolve também `out.env` (valores das variáveis) para mostrar "= valor" nas fórmulas.
- Base embutida, só atividades de `ACT_NOVAS`: CIV-0141 ← SINAPI 94572 por m² (0,46483/0,232415; desfaz o ÷1,2 da 1.6.1); CIV-0136 ← 107279 Q-636 (0,018582/0,0074328); CIV-0137 ← 97088 (0,0462942/0,0185177); CIV-0143 ← 92915 (0,1933/0,0316); CIV-0146 ← coeficientes da CIV-0142. Atividades da base v22 não foram alteradas (a nuvem prevalece); correções listadas no doc da revisão.

### Composições (civil sem drenagem: 21)
- terra: vars `ecorte=0.30, fh=1.25, corte=area*ecorte, aterro=corte/fh`; acts CIV-0121=corte, CIV-0103=aterro; notas reescritas.
- limp: vars removidas (esp, dbota sem uso); notas reescritas.
- CIV-0009 → CIV-0074 em todas as civis (drenagem mantém CIV-0009).
- cant: CIV-0056 → CIV-0133. trafocon: CIV-0075 → CIV-0110.
- cmed: + CIV-0004 (`qtd*6.35*P`) na posição 2; saem CIV-0067/0078/0014 (cint) e a var `cint`. pcf: sai var `A`.
- Notas: removidas as que começam com "VALIDAÇÃO:" e as "[BLOQUEADA]/[REVISÃO TÉCNICA] Auditoria 19/10/2026"; primeira nota = situação específica de 20/10/2026. Só trafoalv fica [BLOQUEADA]. brit/calc/eletro/ext/trafoalv com notas ajustadas.

### Interface
- Caixa "Dados de entrada" (`.din`): entradas em linha (`label.ci`: nome, campo 92 px, unidade), identificador no `title`.
- `details.mini` "Parâmetros (n)" (grade `.pars`: nome + [k] + ✎, fórmula, "= valor"; chips das entradas com ×, + Entrada, ajuda das fórmulas) e "Observações (n)". Estado aberto em `UIO` salvo em `localStorage['volga_hist_ui_open']` (try/catch). Erro de fórmula força Parâmetros aberto e em vermelho. `addNota` abre Observações.
- Removida a caixa "Auditoria técnica / parâmetros internos".

### Testes (Playwright, Chromium 1194)
- `t170.py`: terra 489/391,2; nenhum parâmetro sem nome nas 38 composições; CIV-0009 só na drenagem; coeficientes novos; cmed com 12 atividades; situações; recolher/abrir e persistência; erro de fórmula; renomear; nomes em projeto antigo; 390 px sem rolagem lateral.
- `rev160.py` (regressão geral) e `t170b.py` (seleção múltipla, desfazer, busca por disciplina, copiar tabela): sem erros de console.
- KPIs 1.6.1 → 1.7.0 (HH): terra 24,6→12,3; cmed 87,6→106,6; ccom 288,2→307,9; trafocon 359,4→375,6; trafoalv 217,2→231; eletro 250,7→261,8; canc 229,3→242,9; cant 704,9→717,1; demais variações < 5 HH.

## 1.6.1 — 20/10/2026 · Correções da revisão da 1.6.0

Gerada por `v161.py` sobre a 1.6.0, desfazendo trechos escolhidos por conteúdo com `difflib`: cada trecho é localizado de forma única na comparação com a 1.5.1 e conferido por `assert`.

- **Mantido da 1.5.1/1.6.0:**
  - copiar tabela (TSV + HTML; `MutationObserver`);
  - seleção múltipla de atividades (`excluirAtividadesSelecionadas`, com desfazer);
  - logo que abre "Todos os projetos";
  - "Auditoria técnica / parâmetros internos" recolhido;
  - entradas só por quantidade;
  - avisos `[BLOQUEADA]`/`[REVISÃO TÉCNICA]`;
  - revisões de composição do Osvaldo (terraplanagem e limpeza sem transporte; casas revisadas; pavimento de 8 cm; brita e calçada com espessura em m);
  - 26 atividades novas em `ACT_NOVAS` ("só no app").
- **Desfeito da 1.6.0 (regressões):**
  - filtro, coluna e campo de disciplina na Base de atividades e no cadastro;
  - `#pd` volta a ser `select` de disciplina na busca de atividade da composição (estava fixo em CIVIL: impedia incluir MEC/ELE);
  - disciplina, horas e nº de atividades na lista lateral;
  - aviso de auditoria e bloco de observações editáveis (`.notas`), que tinham sido apagados da tela;
  - `applyRecursos` sem os 4 recursos fixos no código.
- **Composições padrão:**
  - voltam malha, spda, secc, supo, barr, cabos, bt, hvac, sdai e cftv (da 1.5.1), nas posições originais (38 no total);
  - banco de dutos volta com ELE-0016;
  - observações desatualizadas corrigidas: terraplanagem (3 removidas, 2 ajustadas), limpeza, abrigo, casas (CIV-0142), eletrocentro e códigos CAN→CIV-020xx no canteiro.
- **Base embutida:**
  - recursos Calceteiro→Pedreiro, Servente→Aux. Pedreiro, Guincho Elétrico de Coluna→Munck; Cortadora de Piso retirada (CIV-0132 e CIV-0138 a CIV-0140; anotado na observação da atividade);
  - 8 atividades sem recurso recebem coeficientes provisórios, indicados na fonte:
    - CIV-0134 e CIV-0135 ← MEC-0059;
    - CIV-0136 ← CIV-0075;
    - CIV-0137 ← CIV-0090;
    - CIV-0143 ← CIV-0085;
    - CIV-0144 ← CIV-0084;
    - CIV-0145 ← CIV-0062;
    - CIV-0146 ← CIV-0077;
  - CIV-0141 (janela em m²) = CIV-0046 ÷ 1,2 m². **ERRADO** — a SINAPI 94572 já é por m²; desfeito na 1.7.0.
- **Achado corrigido na revisão:** a entrada "Portas" da casa de comando É usada (`vaos = port×0,90×2,10 + jan×1,00×1,20`, desconto de vãos). Continua.
- **Pendências:**
  - parede corta-fogo segue com comprimento e altura, e só pré-moldada (revisão do Osvaldo). O pedido de 19/10 era quantidade + tipo;
  - as 27 atividades "só no app" e os coeficientes provisórios precisam de aprovação do Arthur;
  - premissas sem uso em limpeza, terraplanagem e parede corta-fogo (inofensivas).
- **Testes:**
  - 38 composições sem erro e sem código fora da base;
  - recursos, impacto, observações, admin, CIV-0128;
  - seleção múltipla com desfazer;
  - busca por ELETROMECÂNICA;
  - copiar tabela (223 linhas da base);
  - aviso "não aprovada" na terraplanagem;
  - regressão da 1.4.0 ok;
  - 390 px sem rolagem lateral;
  - sem erros de console.

## 1.6.0 e 1.5.1 — revisão de 20/10/2026

Feitas fora desta linha de trabalho. Na revisão foram encontrados:

- app só civil (10 composições padrão retiradas e busca de atividade fixa em CIVIL);
- observações editáveis e aviso de auditoria apagados da tela;
- 8 atividades novas sem recurso, que entravam com 0 h (abrigo 59 → 22 h; eletrocentro 251 → 178 h);
- atividades duplicadas com outro código (GER→CIV-0130/0131, CAN→CIV-02005…02011, CIV-0024/0025→CIV-0147/0148);
- janela por m² com coeficiente por unidade;
- 4 recursos fixos no código;
- histórico de novidades apagado;
- `APP_VERSION` com sufixo fora do padrão X.Y.Z.

---

## 1.5.0 — 19/10/2026 · Barra verde, funções do Arthur, composições padrão revisadas

Gerada por `v150.py` a partir da 1.4.0 (todas as trocas são `replace` com contagem conferida).

- **Divergência encontrada:** o site não estava na linha 1.1–1.4; era o 1.0.0 com mudanças do Arthur (diff de 130 linhas). Tudo foi portado e adaptado às janelas do app (`ask`, `uiDialog`, `aviso` no lugar de `confirm`/`alert` com listas longas):
  - `applyRecursos()` + `globalRecursos` (REC/TIPO deixam de ser `const`); `ensureGlobal` grava `recursos` na criação e lê em `get` e `onSnapshot`.
  - Aba `recursos` → `rRecursos`, `recForm`, `recSave` (async), `recDel` (async), `commitRecursos` (transação com `version`, histórico com `previousRecursos`). Incluída nas listas sem projeto e de somente leitura.
  - `impactoAtividade`, `textoImpacto`, `diffAtividade`, `confirmarImpacto`/`respImpacto` em `delAct` e `saveAct`. Na 1.4.0, `editIdx` guarda o código: `old=globalBase[pos]`. Cancelar mantém o formulário em edição (no do Arthur, zerava `editIdx`). `usoAtividades` fica sem uso.
  - Notas editáveis: `setNota`, `rmNota` (corrigido `!c.notas[i]===undefined`, que era sempre falso), `addNota`.
  - `ADMINS` (arthur.araujo, osvaldo.junior); `canEditProject` aceita admin; `setReadOnly` liga `body.admin-other` e `#admin-banner`; `saveCloudProject` grava em `projectRef(currentOwnerId||uid, id)`; lista de projetos mostra "Abrir" para admin. **As regras do Firestore precisam permitir a escrita do admin em projetos de outros** (já valem no site).
- **Topo:** `header` volta a `var(--g1)` com borda `var(--g3)`; o logo usa `filter:brightness(0) invert(1)` (versão negativa), sem duplicar o SVG; botões, menu e status voltam às cores sobre fundo escuro.
- **Base embutida (`DB.base`) = base v22 da nuvem:** conferida por impressão digital (djb2) das 195 atividades, com zero diferenças. Mudanças da v22 em relação à embutida da 1.4.0:
  - CIV-0002: só textos.
  - CIV-0005: pedreiro 1,47 → 2.
  - **CIV-0010: virou fôrma de radier em m² (SINAPI 107283; carpinteiro 2,8, ajudante 0,51).**
  - CIV-0023: só textos.
  - CIV-0063 e CIV-0077: entra o vibrador.
  - `+ CIV-0128` (ORSE 4177).
- **Atividades só no app:** `ACT_NOVAS=['CIV-0128']`; `baseAll()` acrescenta (com cache por referência e tamanho) as atividades embutidas dessa lista que faltam em `globalBase`, marcadas `soApp`. Na Base de atividades, essas linhas aparecem com a etiqueta "só no app" e o botão `incluirNaBase(cod)` para o admin (`commitGlobalBase('incluir')`). As linhas novas ficam no fim, então os índices de `globalBase` usados por `actForm`/`delAct` não mudam.
- **SEED (38 composições):**
  - Substituídas mantendo o id: malha (malha2), terra, loc, poste, bspda, cpm (caixa2), canc (canal2), ext, cmed, pcf.
  - Novas: cant, limp, trafocon, trafoalv, eletro, disj, banco, ccom.
  - O nome perde o " — revisada".
  - `crewDef` passa a vir do SEED (terra, limp e malha = 2).
- **Ajuste à CIV-0010 v22** em canal2, caixa2, ccom2, cmed2 e ext2: concreto em `CIV-0077`; fôrma em `CIV-0010`:
  - caixa: `1.55*ext`;
  - casas: `P*0.10`;
  - abrigo: `4.28*n`;
  - canaleta: sem fôrma.
  - Drenagem não revisada (sarj, cd1, oleo) continua lançando m³ na CIV-0010 → pendência.
- **Testes** (`t150.py`, `t150b.py`, `t150c.py`, `t150r.py`):
  - todas as 38 composições avaliam sem erro e sem código fora da base;
  - CIV-0128 "só no app" → incluir;
  - recursos: renomear com janela, exclusão bloqueada para PTA, sem botões para não admin;
  - notas: incluir, editar e excluir;
  - janelas de impacto ao excluir e ao editar, com diff;
  - admin em projeto de outro: faixa verde e edição; não admin: somente leitura;
  - regressão da 1.4.0 ok;
  - 390 px sem rolagem lateral;
  - sem erros de console além dos do stub do Firebase.

---

## 1.4.0 — 19/10/2026 · Histograma, tabelas mensais, bases e status

Só interface; `histo()`, `schedule()` e o formato de dados não mudaram (histograma idêntico ao original nos dois modos; vínculos, calendário, segurança, INMET e menu reconferidos; desempenho igual: histograma ~72 ms no projeto grande).

- **Números:** `fmt()` troca o separador de milhar por U+202F (espaço fino inseparável); `fmtCsv()` (sem agrupamento) no CSV do cronograma; `fmtCoef()` (2–4 casas) nos coeficientes da base.
- **Histograma (`rHist`):** `hv` ganha `top` (8 | 12 | 0 = todas) e `res` (série isolada); `hv.tipo` padrão = 'Mão de obra'. Séries ordenadas pelo volume (Σ do período); acima de `top+1` as menores são somadas em `Outros` DEPOIS da agregação semanal/mensal (o total de cada coluna fica idêntico — testado em dia/semana/mês). Paleta de 12 tons distintos + ângulo áureo além de 12; cor ligada à posição em `ord` (estável ao isolar). Legenda = botões (`histPick(i)`, `.ro-ok`), com o pico de cada série. `hv.gran='mes'` (pico do mês, barra de 64 px, rótulo `mmm/aa`). KPIs: rótulo explícito, média por período, mês/semana do pico. Resumo por recurso ordenado por tipo e horas. Tooltip com `histColLabel()`.
- **Tabelas mensais (`mtab`):** sem fundo proporcional; `td.pk` (sublinhado) no máximo da linha só se a linha varia; coluna `Pico`; `tfoot` "Total no mesmo dia" = máx. diário de Σ ceil(recurso) do grupo no mês (`monthlyTotal`), testado ≤ soma e ≥ máximo da coluna.
- **Base de atividades:** colunas Código | Serviço (escopo `.tg` + observação em 2 linhas) | Disciplina | Un. | Recursos | Fonte | ações (só admin, `button.i`). `fonteHtml()` encurta URL http(s) para o domínio (href só http/https, escapado). `usoProjeto()` (via `usedCodes`) → marca `.inuse` e filtro `filt.uso`. Disciplina/Fonte ocultas ≤ 720 px.
- **Base de composições:** `libraryMeta` (Map por id, lido do `compJson`, sem gravar no documento) → nº de atividades, busca por código, prévia `<details>`; filtro `libraryDisc`; `libDate(updatedAt)`; selo "já no projeto" por `librarySourceId`.
- **Status (`statusRefresh`):** vazio sem projeto; "Somente leitura"; "Alterações não salvas…" ao agendar; "Salvando…"; "Salvo às HH:MM"; erro só no `catch` de `saveCloudProject` (`statusErr`). `reportError` não mexe mais no status. Snapshot da base global chama `statusRefresh()` em vez de "Projeto aberto/Selecione um projeto". `#cloudstatus:empty` oculto.

---

## 1.3.0 — 19/10/2026 · Identidade Volga, janelas do app, tabelas

Só interface; cálculos e formato de dados inalterados (histograma idêntico ao original; vínculos, calendário, segurança, INMET e menu reconferidos).

- **Número de versão:** o topo mostra só `v{globalVersion}` (contador da base global, numeração do sistema do Arthur) via `updVer()`; "Base global vN" saiu do `#cloudstatus`. `APP_VERSION` (1.3.0) continua como identificador do ARQUIVO: comentário da 1ª linha, Novidades ("arquivo 1.3.0") e pastas.
- **Identidade:** logo oficial inline (`<symbol>` `#vlg` em `<defs>`, cores fixas #003437/#2a451d e gradiente `#vlg-grad`; sem as classes `.cls-*` do SVG original, que vazariam para a página); `viewBox` ampliado para não cortar o símbolo; símbolo sozinho ≤ 860 px. Favicon e apple-touch-icon em data URI (PNG 180 px). Cabeçalho branco com filete #2a451d; `<title>` em sentence case; `theme-color`. Logo também no login.
- **Janelas do app:** `window.alert` → `toast()` (rodapé, `aria-live`, tipos ok/warn/err por heurística, 4,5/7/10 s, máx. 3). `confirm`/`prompt` → `uiDialog()` / `ask()` / `askText()` / `askForm()` (Promise; foco preso, Enter confirma, Esc/clique fora cancela, foco devolvido; variante `dng`). 18 pontos convertidos para `async`: renomear, restaurar preliminares, zerar praticabilidade, excluir atividade, excluir composição, nova entrada (formulário de 4 campos), importar JSON (2), importar do navegador, criar, duplicar e excluir projeto (digitar EXCLUIR), publicar e adicionar à biblioteca, excluir da biblioteca. Teste: nenhuma caixa nativa aberta.
- **Linha do tempo:** passo de rótulo de mês `stepM ∈ {1,2,3,6,12}` tal que `stepM × 30,44 × px/dia ≥ 46 px` (78 px no formato longo); formato curto `mmm/aa`; 1º mês parcial só rotulado se couber. Teste: 0 sobreposições em todas as escalas, a 1366 e 700 px.
- **Tabelas mensais** (`mtab()`): cabeçalho em 2 linhas (ano com `colspan` + mês abreviado), coluna de nomes `sticky`, zeros como "·", fundo `rgba(77,138,60, .08–.50)` proporcional ao máximo da tabela, divisória em janeiro.
- **Títulos:** `.card>h3` / `.desc` padronizados; seções do histograma passaram de h4 para h3 com descrição.

---

## 1.2.0 — 19/10/2026 · Proporções e responsividade

Só interface; nenhuma função de cálculo nem formato de dados alterado (histograma testado idêntico ao original; vínculos, calendário e segurança reconferidos).

**Auditoria antes/depois** (1920, 1366, 768 e 390 px): estouro horizontal da página em 768 e 390 → nenhum; cabeçalho 116 px (1366) e 245 px (390) → 56 e 59 px; editor de composições com 869 px numa tela de 390 → 366 px.

- **Cabeçalho:** `<h1>` com marca (3 barras em CSS) + nome do app (só "Histograma" ≤ 720 px; só a marca ≤ 520 px); `#projname` em destaque; ações em `<details id="projmenu">` (`menuGo`, fecha com clique fora e Esc; no celular, `position:fixed` dentro da tela); `#cloudstatus` vira ponto colorido ≤ 1100 px (`setStatus` grava `title` e classe `err`); botão de versão `.lnk`.
- **Abas:** `#nav` = `.tabs` (rolagem horizontal, máscara de fade no celular) + `.ur` (desfazer/refazer, só ícone ≤ 720 px); `setTab` traz a aba ativa para a área visível.
- **Composições:** `.grid` = `minmax(230px,290px) minmax(0,1fr)`; coluna `.side` sticky com rolagem própria; ≤ 900 px a lista some e aparece o seletor `.only-sm`; itens compactos (`.it-h`, setas `.ib` visíveis no hover/foco/toque).
- **Tabelas:** `.tbl` (rolagem horizontal própria) em atividades (`table.acts`), equipe e resumo do histograma; ações em linha com `button.i` (28 px; 38 px em `pointer:coarse`); código sem quebra; fórmula com largura 100%.
- **Cronograma:** `table.cron` com larguras fixas para ID/predecessoras/data; Equipe `td.eq` com 2 linhas (`-webkit-line-clamp`) e `title`; Disciplina vira subtítulo sob o nome ≤ 1500 px (`.dsc`/`.dsc2`); colunas `.opt` ocultas ≤ 720 px; ajuda em `<details class="help">`; largura dos rótulos do Gantt 240/140 px.
- **Parâmetros:** HTML inválido corrigido (label dentro de label nos dias da semana → `.fld`); meses em grade `.months`.
- **Escala geral:** `main` até 1680 px; paddings com `clamp()`; KPIs `clamp(18px,.9vw+10px,24px)`; ≤ 720 px: campos em duas colunas, KPIs em 2 colunas; `pointer:coarse`: controles com 40 px de altura mínima.
- Desempenho inalterado (histograma no projeto grande ~102 ms; cronograma ~65 ms).

---

## 1.1.0 — 19/10/2026

### Segurança e robustez (análise de 16/10)
- Avaliador de fórmulas próprio (`compileExpr`) no lugar de `new Function`; 178 fórmulas com resultado idêntico; mensagem de erro por fórmula.
- `esc()` escapa `'` e crase; `js()` para valores em `onclick`; IDs normalizados em `migrate`.
- `setParam` valida a jornada; edição da base por código (`editIdx` guarda o código); mensagens em PT (`FB_MSG`); aviso se o Firebase não carregar; login em `<form>`; modal com `role="dialog"` e Esc; `dupComp` remove `librarySourceId`; CSV com aspas e proteção contra fórmula; importação sem renomear o projeto.

### Interface
- `render()`: bloqueio sem projeto, título e renomear, `beforeunload`, desfazer/refazer (60 passos), preservação de rolagem e foco, somente leitura via `disabled` (`applyReadOnly`, classe `ro-ok`).
- `APP_VERSION`, `NOVIDADES`, `showNovidades` e botão de versão no cabeçalho.

### Histograma
- `hv.dist`: `unif` (padrão, idêntico ao original — testado dia a dia) | `ativ` (cada atividade ocupa sua janela de horas; carga = horas ÷ duração da atividade).
- Limite de efetivo (`hv.cap`), eixo Y com topo arredondado, curva S (`curvaS`).

### Calendário e praticabilidade
- `params.prat[12]` (0–90%): `capMes()` = horas produtivas × (1 − %); `spanFwd` consome horas produtivas por dia útil.
- `params.pratFonte`: origem dos percentuais (estação, anos, limiar, janela, fuso, data); apagada ao editar ou colar à mão.
- `folgas[].rec`: `''` | `'anual'` (MM-DD; ano 2000 = todos os anos; atravessa a virada do ano) | `'pascoa'` (`off`, `dur`). Páscoa por Meeus/Jones/Butcher. Feriados nacionais fixos (inclui 20/11) + Sexta-feira Santa; Carnaval e Corpus Christi opcionais. Edição de lançamentos.
- Campos de data gravam em `blur`/Enter: o Chrome dispara `change` a cada parte da data digitada e o redesenho tirava o foco.

### INMET (`zipList`, `zipRead`, `parseInmet`, `calcPratINMET`, `inmetCard`)
- Lê os ZIPs anuais direto pelo diretório central (`File.slice`, só a estação escolhida; `DecompressionStream('deflate-raw')`) ou os CSVs da estação. Formatos 2019+ (`2020/01/01;0000 UTC`) e anteriores (`2018-01-01;00:00`); UTF-8 ou Windows-1252; decimal com vírgula; vazio ou −9999 = sem dado. ZIP64 não suportado (mensagem pede o CSV).
- Leitura de hora H = chuva acumulada de H−1 a H. A janela (ini, fim] é aplicada em hora local (fuso fixo; horário de verão de anos ≤ 2018 não considerado). Dia válido = ≥ 75% das horas da janela com dado. p(dia do ano) = anos com chuva ≥ limiar ÷ anos válidos. Dias esperados no mês = Σp (29/02 com peso 0,25); % = esperados ÷ dias do mês (fev = 28,25).
- **Validação:** com UTC e falta = 0 (regras da planilha 23840008_PRA_001), os 12 percentuais coincidem com a coluna AK da planilha. Com hora local (UTC−3) e dias sem dado descartados: Jan 3,23 · Fev 2,36 · Mar 6,45 · Abr 5,28 · Mai 4,03 · Jun 5,83 · Jul 4,03 · Ago 1,08 · Set 0 · Out 0,65 · Nov 5,00 · Dez 2,42 (478 dias descartados).
- **Achados na planilha:** filtro 06–18 aplicado na hora UTC (equivale a 03–15 local); dados faltantes contados como chuva zero (A428: 2021 com 24%, 2022 com 71% e 2024 com 28% das horas sem dado); rodapé cita a estação A001, mas os dados são da A428.

### Cronograma
- `comp.preds = [{id, t:'TI'|'II'|'TT'|'IT', lag}]`; `migrate` converte `pred/lag`; `syncLegacyPred` mantém `pred/lag` = primeiro TI (compatibilidade ao voltar de versão).
- `schedule`: início = máximo das restrições (TI `nextW(addW(fim,1+lag))`; II `nextW(addW(ini,lag))`; TT `spanBack(addW(fim,lag))`; IT `spanBack(addW(ini,lag−1))`); nada antes do início do projeto; avisos de ciclo e de predecessora desmarcada (`schedWarn`).
- `parsePreds` aceita TI/II/TT/IT e FS/SS/FF/SF, com `+n`/`-n`; recusa ciclo (`dependsOn`); `moveTo` (coluna ID); escala `gz` (dia, semana, mês, ajuste); CSV com ID e predecessoras.

### Desempenho
- Histograma: uma `<path>` por série (antes um `<rect>` por barra), rótulos esparsos, dica única por posição do mouse (`histTip`), agrupamento por mês feito uma vez (`byMonth`), `capMes()` em vez de recalcular a jornada por dia, `content-visibility:auto` nos blocos abaixo da área visível (`.cv`).
- `captureView`/`restoreView` só tocam o que tinha rolagem ou foco.
- Medido (redesenho + layout, mediana): projeto grande — histograma 732 → 112 ms, cronograma 368 → 71 ms; projeto típico — histograma 59 → 24 ms, cronograma 37 → 29 ms. Elementos na tela do histograma: ~22 mil → ~5 mil.

### Retirado nesta rodada
- Estimativa de terraplanagem pelo arranjo (código guardado fora da versão, para quando as composições forem revisadas).

### Testes
- Navegador headless com Firebase simulado; `node --check`; todas as abas e modos; injeção por fórmula e por ID bloqueadas; somente leitura; tela sem projeto; vínculos TI/II/TT/IT/múltiplos conferidos com cálculo manual; feriados e repetição anual; importação INMET (ZIP com 2 estações, CSV formato antigo). Não testados: login e gravação reais no Firestore.

## Pendências e decisões em aberto
- Modo padrão do histograma (hoje Uniforme; os dois disponíveis).
- Critérios padrão da praticabilidade (5 mm, 06–18 h local) e revisão do estudo de praticabilidade atual.
- Regras de segurança do Firestore (fora do arquivo).
