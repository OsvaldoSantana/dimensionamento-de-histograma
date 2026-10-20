#!/usr/bin/env python3
"""Gera a v1.8.0 a partir da v1.7.0.
 Tela: lista lateral só com nome e disciplina (cor por disciplina) + busca; cabeçalho compacto; tabela de
 atividades com larguras pelo conteúdo, coluna "Fórmula", recursos em texto e barra de seleção alinhada ao
 "Copiar tabela"; sem avisos de revisão; cores das disciplinas no cronograma.
 Composições (decisões de 20/10/2026): canteiro sem nome de obra; tubulão CIV-0073 → CIV-0068; graute da bacia
 em alvenaria 3,00 m³ (lista do projeto); magro de blocos/sapatas CIV-0149 (SINAPI 96619); porta das casas
 CIV-0150 (SINAPI 91341); linhas de situação removidas das observações.
Uso: python3 v180.py v1.7.0.html v1.8.0.html
"""
import sys, json, re
src, dst = sys.argv[1:3]
t = open(src, encoding='utf-8').read()

def rep(old, new, count=1):
    global t
    n = t.count(old)
    assert n == count, (n, old[:120])
    t = t.replace(old, new)

# ---------------------------------------------------------------- 1) versão e novidades
rep("const APP_VERSION='1.7.0';", "const APP_VERSION='1.8.0';")
t = re.sub(r'<!-- Dimensionamento de Histograma · arquivo 1\.7\.0 · [^ ]+ ·', '<!-- Dimensionamento de Histograma · arquivo 1.8.0 · 20/10/2026 ·', t, count=1)
assert 'arquivo 1.8.0' in t
NOV = """ {v:'1.8.0',data:'20/10/2026',itens:[
  'Lista de composições mais limpa: só o nome e a disciplina, com uma cor por disciplina (civil terracota, eletromecânica azul, instalações elétricas âmbar) e um campo para buscar pelo nome. A mesma cor aparece nas barras do cronograma, com legenda.',
  'Tabela de atividades reorganizada: código e unidade estreitos e o nome da atividade com o espaço que sobra; a coluna de entrada se chama "Fórmula"; os recursos aparecem em texto corrido; "Selecionar todas" e "Excluir selecionadas" ficam na mesma linha do "Copiar tabela".',
  'Duração, dias úteis e HH da composição em uma linha só, no lugar dos três cartões.',
  'Saem os avisos "Revisão técnica pendente" e "Composição não aprovada" e as linhas de situação nas observações. O canteiro deixa de ter o nome de uma obra no título.',
  'Bases com tubulão (disjuntor, poste, barramento/SPDA e parede corta-fogo): a escavação passa para a CIV-0068, porque a CIV-0073 é o tubulão completo e contava o concreto duas vezes.',
  'Bacia de trafo em alvenaria: graute de 3,00 m³ por base, como na lista de materiais do projeto (antes 0,658 m³).',
  'Atividades novas: lastro de concreto magro em blocos e sapatas (CIV-0149, SINAPI 96619) nas bases de disjuntor, poste, barramento/SPDA, corta-fogo e no portão da cerca; instalação de porta de alumínio veneziana (CIV-0150, SINAPI 91341) nas casas de comando e de medição.'
 ]},"""
rep("const NOVIDADES=[\n", "const NOVIDADES=[\n" + NOV + "\n")

# ---------------------------------------------------------------- 2) base embutida: atividades novas
L = t.split('\n')
idb = [i for i, l in enumerate(L) if l.startswith('const DB=')][0]
D = json.loads(L[idb][len('const DB='):].rstrip(';'))
cods = {x[0] for x in D['base']}
NOVAS = [
 ['CIV-0149', 'CIVIL', 'FUNDAÇÕES', 'LASTRO DE CONCRETO MAGRO EM BLOCOS E SAPATAS, E=5 CM', 'm²', 'SINAPI 96619',
  'LASTRO DE CONCRETO MAGRO, APLICADO EM BLOCOS DE COROAMENTO OU SAPATAS, ESPESSURA DE 5 CM. AF_01/2024 (96619). Por m² de fundo.',
  {'Pedreiro': 0.33905, 'Aux. Pedreiro': 0.12265}],
 ['CIV-0150', 'CIVIL', 'ESQUADRIAS', 'INSTALAÇÃO DE PORTA DE ALUMÍNIO DE ABRIR TIPO VENEZIANA', 'm²', 'SINAPI 91341',
  'PORTA EM ALUMÍNIO DE ABRIR TIPO VENEZIANA COM GUARNIÇÃO, FIXAÇÃO COM PARAFUSOS. AF_10/2025 (91341). Porta 0,90 × 2,10 m = 1,89 m².',
  {'Pedreiro': 0.5548789, 'Aux. Pedreiro': 0.1568136}],
]
for x in NOVAS:
    assert x[0] not in cods, x[0]
    D['base'].append(x)
L[idb] = 'const DB=' + json.dumps(D, ensure_ascii=False) + ';'
t = '\n'.join(L)
m = re.search(r'const ACT_NOVAS=(\[.*?\]);', t)
nov = json.loads(m.group(1)); nov += ['CIV-0149', 'CIV-0150']
t = t.replace(m.group(0), 'const ACT_NOVAS=' + json.dumps(nov, ensure_ascii=False) + ';', 1)

# ---------------------------------------------------------------- 3) composições padrão
L = t.split('\n')
isd = [i for i, l in enumerate(L) if l.startswith('const SEED=')][0]
SEED = json.loads(L[isd][len('const SEED='):].rstrip(';'))
S = {s['id']: s for s in SEED}
def act(sid, cod, n=1):
    a = [x for x in S[sid]['acts'] if x['cod'] == cod]
    assert len(a) == n, (sid, cod, len(a)); return a
def nota_rep(sid, velho, novo):
    s = S[sid]; achou = [n for n in s['notas'] if velho in n]
    assert len(achou) == 1, (sid, velho, len(achou))
    s['notas'] = [n.replace(velho, novo) for n in s['notas']]

# 3.1 nome sem obra
assert S['cant']['nome'] == 'Canteiro de obras padrão (layout Milhão 25 × 21,5 m)'
S['cant']['nome'] = 'Canteiro de obras padrão'
# 3.2 linhas de situação fora (todas as composições)
for s in SEED:
    s['notas'] = [n for n in s['notas'] if not n.startswith(('[BLOQUEADA]', '[REVISÃO TÉCNICA]', 'VALIDAÇÃO:'))]
# 3.3 tubulão: a CIV-0073 (SINAPI 101102) é o tubulão completo (escavação, armação e concreto) → escavação pela CIV-0068
for sid in ('disj', 'poste', 'bspda', 'pcf'):
    for a in act(sid, 'CIV-0073'): a['cod'] = 'CIV-0068'
    S[sid]['notas'].append('Escavação pela CIV-0068 (escavação mecanizada). A CIV-0073 (SINAPI 101102) é o tubulão completo, com armação e concreto, e somava a concretagem duas vezes com a CIV-0063.')
# 3.4 magro de blocos e sapatas: CIV-0074 (m³, pisos/radier) → CIV-0149 (m², SINAPI 96619, e = 5 cm)
MAG = {'disj': ('qtd*0.05', 'qtd*1.0'), 'poste': ('qtd*0.03', 'qtd*0.6'), 'bspda': ('qtd*0.06', 'qtd*1.2'),
       'pcf': ('np*0.055', 'np*1.1'), 'cerca': ('2*1*0.6*0.05*port', '2*1*0.6*port')}
for sid, (velho, novo) in MAG.items():
    a = act(sid, 'CIV-0074')[0]; assert a['q'] == velho, (sid, a['q'])
    a['cod'] = 'CIV-0149'; a['q'] = novo
S['disj']['notas'].append('Concreto magro pela CIV-0149 (blocos e sapatas, SINAPI 96619), em m² de fundo com 5 cm: 0,05 m³ = 1,0 m².')
# 3.5 graute da bacia em alvenaria: 3,00 m³ da lista do VO778-CV-207 (0,1245 m³ por metro de parede)
ta = S['trafoalv']
g = act('trafoalv', 'CIV-0134')[0]; assert g['q'] == 'qtd*2*(C+L)*0.0273', g['q']
g['q'] = 'qtd*2*(C+L)*tg'
i_al = [v[0] for v in ta['vars']].index('al')
ta['vars'].insert(i_al, ['tg', '0.1245', 'Graute por metro de parede (m³/m)'])
nota_rep('trafoalv', 'grauteadas (0,658 m³ conferido; a lista do projeto diz 3,00 m³)',
         'grauteadas (3,00 m³ da lista do projeto, 0,1245 m³ por metro de parede)')
# 3.6 portas das casas
for sid in ('ccom', 'cmed'):
    acts = S[sid]['acts']; i = [x['cod'] for x in acts].index('CIV-0141')
    acts.insert(i + 1, {'cod': 'CIV-0150', 'q': 'qtd*port*0.90*2.10'})
    nota_rep(sid, 'Portas: quantidade e vãos 0,90×2,10 m, instalação apenas conforme projeto.',
             'Portas 0,90 × 2,10 m: instalação pela CIV-0150 (porta de alumínio veneziana, SINAPI 91341, por m²) e desconto do vão na alvenaria e na pintura.')
L[isd] = 'const SEED=' + json.dumps(SEED, ensure_ascii=False) + ';'
t = '\n'.join(L)

# ---------------------------------------------------------------- 4) cores das disciplinas
rep("function setVar(i,v){cur().vars[i].f=v;render()}",
    "function setVar(i,v){cur().vars[i].f=v;render()}\n"
    "// v1.8.0: uma cor por disciplina (lista, etiqueta e cronograma). A base usa 'INST. ELÉTRICAS' e as composições 'INSTALAÇÕES ELÉTRICAS': as duas caem na mesma cor.\n"
    "const DISC_COR={civil:['#B4561F','#9A4A1A'],eletro:['#1F5FA8','#1F5FA8'],inst:['#A86B12','#8A560B'],geral:['#6B7280','#4B5563']};\n"
    "const semAc=s=>String(s||'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();\n"
    "function discKey(d){const s=semAc(d).trim();return s==='civil'?'civil':s.startsWith('eletromec')?'eletro':s.startsWith('inst')?'inst':'geral'}\n"
    "function discCor(d,txt){return DISC_COR[discKey(d)][txt?1:0]}\n"
    "let compBusca='';\n"
    "function filtraLista(v){compBusca=v;const q=semAc(v).trim();document.querySelectorAll('.list .it').forEach(e=>{e.hidden=!!q&&!semAc(e.dataset.n).includes(q)})}")

# ---------------------------------------------------------------- 5) lista lateral
OLD_SIDE = ("<div class=\"hint lhint\" style=\"margin:0 0 6px\">Ordem da lista</div><div class=\"list\">${visibleComps.map((c,i)=>{const k=compCalc(c);")
rep(OLD_SIDE, "<input class=\"lbusca ro-ok\" type=\"search\" placeholder=\"Buscar composição\" aria-label=\"Buscar composição pelo nome\" value=\"${esc(compBusca)}\" oninput=\"filtraLista(this.value)\"><div class=\"list\">${visibleComps.map((c,i)=>{const hid=compBusca&&!semAc(c.nome).includes(semAc(compBusca).trim());")
rep("return`<div class=\"it ${c.id===sel?'on':''}\" tabindex=\"0\" role=\"button\" aria-pressed=\"${c.id===sel}\"",
    "return`<div class=\"it ${c.id===sel?'on':''}\" ${hid?'hidden':''} data-n=\"${esc(c.nome)}\" style=\"--dc:${discCor(c.disc)}\" tabindex=\"0\" role=\"button\" aria-pressed=\"${c.id===sel}\"")
rep("<div class=\"it-h\"><b>${esc(c.nome)}</b>${order}</div><small>${esc(c.disc)} · ${fmt(k.dur)} h · ${c.acts.length} ativ.${c.usar?' · no cronograma':''}</small></div>",
    "<div class=\"it-h\"><b>${esc(c.nome)}</b>${order}</div><small class=\"dsc-l\" style=\"color:${discCor(c.disc,1)}\">${esc(c.disc)}${c.usar?' <span class=\"nc\" title=\"No cronograma\">· no cronograma</span>':''}</small></div>")

# ---------------------------------------------------------------- 6) cabeçalho compacto e sem avisos
rep("<div class=\"kpis\"><div class=\"kpi\"><b>${fmt(k.dur)} h</b><span>Duração total (equipe atual)</span></div><div class=\"kpi\"><b>${k.days}</b><span>Dias úteis${temPrat()?' (sem praticabilidade)':''}</span></div><div class=\"kpi\"><b>${fmt(mo,0)} h</b><span>HH de mão de obra</span></div></div>",
    "<p class=\"cstat\"><span class=\"dtag\" style=\"--dc:${discCor(c.disc)};color:${discCor(c.disc,1)}\">${esc(c.disc)}</span><span><b>${fmt(k.dur)} h</b> de duração com a equipe atual</span><span><b>${k.days}</b> dias úteis${temPrat()?' (sem praticabilidade)':''}</span><span><b>${fmt(mo,0)} h</b> de mão de obra (HH)</span></p>")
a = t.index('${c.notas&&c.notas.some(n=>n.startsWith("[BLOQUEADA]"))?')
b = t.index('</p>`:``)}', a) + len('</p>`:``)}')
assert b - a < 700, b - a
t = t[:a] + t[b:]
assert 'COMPOSIÇÃO NÃO APROVADA' not in t and 'REVISÃO TÉCNICA PENDENTE' not in t

# ---------------------------------------------------------------- 7) tabela de atividades
rep('<div class="row ro-ok" style="margin:7px 0 10px"><label class="dia chk"><input type="checkbox" onchange="marcarTodasAtividades(this.checked)" aria-label="Selecionar todas as atividades"> Selecionar todas</label><button type="button" class="d" onclick="excluirAtividadesSelecionadas()">Excluir selecionadas</button></div>',
    '<div class="tbl-bar ro-ok"><label class="dia chk"><input type="checkbox" onchange="marcarTodasAtividades(this.checked)" aria-label="Selecionar todas as atividades"> Selecionar todas</label><button type="button" class="d" onclick="excluirAtividadesSelecionadas()">Excluir selecionadas</button></div>')
rep('<th>Un.</th><th>Quantidade (valor ou fórmula)</th>', '<th>Un.</th><th>Fórmula</th>')
rep("<td>${Object.entries(a.r).map(([r,v])=>`<span class=\"chip\">${esc(r)}: ${fmt(v*l.q)}</span>`).join('')}</td>",
    "<td class=\"rtx\">${Object.entries(a.r).map(([r,v])=>`<span>${esc(r)} ${fmt(v*l.q)}</span>`).join(' · ')}</td>")
# o botão Copiar tabela entra na barra que já existe logo acima da tabela, se houver
rep("     tools.appendChild(button);\n     const parent=table.parentElement;\n     const anchor=parent?.matches('.scroll,.tbl')?parent:table;\n     anchor.before(tools);",
    "     tools.appendChild(button);\n     const parent=table.parentElement;\n     const anchor=parent?.matches('.scroll,.tbl')?parent:table;\n     const bar=anchor.previousElementSibling;\n     if(bar&&bar.classList.contains('tbl-bar')){button.classList.add('in-bar');bar.appendChild(button)}else anchor.before(tools);")
# larguras: as regras antigas por posição estavam deslocadas desde a coluna de seleção (código com 210 px mínimos)
rep("table.acts td:nth-child(2){white-space:nowrap}\ntable.acts td:nth-child(5){min-width:160px}table.acts td:nth-child(5) input{width:100%}",
    "table.acts th:nth-child(2),table.acts td:nth-child(2),table.acts th:nth-child(3),table.acts td:nth-child(3),table.acts th:nth-child(5),table.acts td:nth-child(5),table.acts th:nth-child(7),table.acts td:nth-child(7),table.acts th:nth-child(8),table.acts td:nth-child(8),table.acts td:nth-child(10){white-space:nowrap;width:1%}\n"
    "table.acts th:nth-child(4),table.acts td:nth-child(4){width:40%;min-width:240px}table.acts th:nth-child(6),table.acts td:nth-child(6){width:150px;min-width:115px}table.acts td:nth-child(6) input{width:100%}\n"
    "table.acts th:nth-child(9),table.acts td:nth-child(9){min-width:130px;max-width:230px}table.acts td.rtx{font-size:12px;color:var(--gr);line-height:1.45}table.acts td.rtx span{white-space:nowrap}table.acts td:nth-child(10) button.i{min-width:26px;width:26px;height:26px;padding:0}")
rep("table.acts td:nth-child(3){min-width:210px}table.acts td:nth-child(8){min-width:150px;max-width:280px}", "")

# ---------------------------------------------------------------- 8) cronograma com a cor da disciplina e legenda
rep("background:${i%2?'#4d8a3c':'#2f6a22'};border-radius:4px;color:#fff;", "background:${discCor(c.disc)};border-radius:4px;color:#fff;")
rep('<div class="card">${escala}<div class="gantt">',
    '<div class="card">${escala}<div class="legend">${[...new Set(U.map(c=>discKey(c.disc)))].map(k=>{const c0=U.find(c=>discKey(c.disc)===k);return`<span><i style="background:${discCor(c0.disc)}"></i>${esc(c0.disc)}</span>`}).join(\'\')}</div><div class="gantt">')

# ---------------------------------------------------------------- 9) CSS
CSS = (".list .it{border-left:4px solid var(--dc,transparent)!important}.list .it.on{border-left-color:var(--dc,var(--g2))!important}"
       ".list .it .dsc-l{font-weight:600;font-size:11.5px;letter-spacing:.01em}.list .it .nc{color:var(--gr);font-weight:500}"
       "input.lbusca{width:100%;margin:0 0 8px;padding:7px 10px}"
       ".cstat{display:flex;flex-wrap:wrap;gap:4px 16px;align-items:center;margin:2px 0 14px;font-size:13px;color:var(--gr)}.cstat b{color:var(--g1);font-size:14.5px}"
       ".dtag{display:inline-block;border:1px solid var(--dc);border-left-width:4px;border-radius:6px;padding:1px 8px;font-size:11.5px;font-weight:700;background:#fff}"
       ".tbl-bar{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:6px 0 8px}.tbl-bar .table-copy-btn.in-bar{margin-left:auto}\n")
rep(".notas{margin:4px 0 2px}", CSS + ".notas{margin:4px 0 2px}")
open(dst, 'w', encoding='utf-8').write(t)
print('ok', len(t.encode()), 'SEED', len(SEED), 'DB', len(D['base']))
