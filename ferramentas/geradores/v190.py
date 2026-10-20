#!/usr/bin/env python3
"""Gera a v1.9.0 a partir da v1.8.0.
 - Tela: nome da composição como título grande; duração, dias úteis e HH em faixa de destaque.
 - Dados (base embutida, composições padrão, nomes antigos de parâmetros, atividades novas) em blocos
   <script type="application/json"> legíveis: uma atividade por linha; composições com um item por linha.
 - Índice e marcadores de seção no script; função validarDados() para os testes.
 A partir desta versão os dados se editam direto nos blocos JSON (não é mais preciso script gerador).
Uso: python3 v190.py v1.8.0.html v1.9.0.html
"""
import sys, json, re
src, dst = sys.argv[1:3]
t = open(src, encoding='utf-8').read()

def rep(old, new, count=1):
    global t
    n = t.count(old)
    assert n == count, (n, old[:120])
    t = t.replace(old, new)

j = lambda v: json.dumps(v, ensure_ascii=False)

# ---------------------------------------------------------------- 1) versão e novidades
rep("const APP_VERSION='1.8.0';", "const APP_VERSION='1.9.0';")
t = re.sub(r'<!-- Dimensionamento de Histograma · arquivo 1\.8\.0 · [^ ]+ ·', '<!-- Dimensionamento de Histograma · arquivo 1.9.0 · 20/10/2026 ·', t, count=1)
assert 'arquivo 1.9.0' in t
NOV = """ {v:'1.9.0',data:'20/10/2026',itens:[
  'O nome da composição volta a ter destaque, como título, e a duração, os dias úteis e o HH aparecem em números grandes numa faixa com a cor da disciplina.',
  'Organização interna do arquivo para manutenção mais segura (dados legíveis, índice e verificação automática). Nenhum cálculo mudou: as 38 composições padrão dão os mesmos resultados da 1.8.0.'
 ]},"""
rep("const NOVIDADES=[\n", "const NOVIDADES=[\n" + NOV + "\n")

# ---------------------------------------------------------------- 2) cabeçalho da composição
a = t.index("$('#ed').innerHTML=`<div class=\"card\"><div class=\"row\">\n <label class=\"grow\">Nome da composição")
b = t.index('</p>', a) + 4
old = t[a:b]
assert 'class="cstat"' in old and old.count('\n') == 4, old
NEW = ("$('#ed').innerHTML=`<div class=\"card\"><div class=\"chead\" style=\"--dc:${discCor(c.disc)}\"><div class=\"chead-r\">\n"
       " <input class=\"ctitle\" value=\"${esc(c.nome)}\" aria-label=\"Nome da composição\" title=\"Nome da composição — clique para editar\" onchange=\"upd('nome',this.value)\">\n"
       " </div><div class=\"chead-t\"><select class=\"cdisc\" aria-label=\"Disciplina\" style=\"color:${discCor(c.disc,1)}\" onchange=\"upd('disc',this.value)\">${discs.map(d=>`<option ${d===c.disc?'selected':''}>${esc(d)}</option>`).join('')}</select>\n"
       "  <button onclick=\"dupComp()\">Duplicar</button><button class=\"d\" onclick=\"delComp()\">Excluir</button></div>\n"
       " <div class=\"cstat\"><div><b>${fmt(k.dur)} h</b><span>Duração com a equipe atual</span></div><div><b>${k.days}</b><span>Dias úteis${temPrat()?' (sem praticabilidade)':''}</span></div><div><b>${fmt(mo,0)} h</b><span>Mão de obra (HH)</span></div></div></div>")
t = t[:a] + NEW + t[b:]
OLDCSS = (".cstat{display:flex;flex-wrap:wrap;gap:4px 16px;align-items:center;margin:2px 0 14px;font-size:13px;color:var(--gr)}.cstat b{color:var(--g1);font-size:14.5px}"
          ".dtag{display:inline-block;border:1px solid var(--dc);border-left-width:4px;border-radius:6px;padding:1px 8px;font-size:11.5px;font-weight:700;background:#fff}")
rep(OLDCSS,
    ".chead{margin:0 0 16px}.chead-r{display:flex;flex-wrap:wrap;gap:8px;align-items:center}"
    "input.ctitle{flex:1 1 100%;width:100%;min-width:0;font-size:21px;font-weight:700;letter-spacing:-.01em;color:var(--g1);border:1px solid transparent;border-radius:8px;padding:5px 8px;margin:0 0 0 -9px;background:transparent}"
    "input.ctitle:hover{border-color:var(--bd);background:#fff}input.ctitle:focus{border-color:var(--g3);background:#fff}"
    "select.cdisc{width:auto!important;max-width:240px;font-weight:700;font-size:12.5px;padding:5px 8px}.chead-t{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:4px}.chead-t button{padding:5px 12px;font-size:13px}"
    ".cstat{display:flex;flex-wrap:wrap;margin:10px 0 0;border:1px solid var(--bd);border-left:5px solid var(--dc);border-radius:10px;background:#fff;overflow:hidden}"
    ".cstat>div{flex:1 1 150px;padding:9px 16px;border-left:1px solid var(--bd);min-width:0}.cstat>div:first-child{border-left:0}"
    ".cstat b{display:block;font-size:23px;line-height:1.15;font-weight:700;letter-spacing:-.02em;color:var(--g1);font-variant-numeric:tabular-nums}.cstat span{font-size:12px;color:var(--gr)}"
    "@media (max-width:520px){input.ctitle{font-size:18px}.cstat>div{flex:1 1 33%;padding:8px 10px}.cstat b{font-size:19px}}")

rep('aria-label="Quantidade de ${esc(a.cod)}" value="${esc(a0.f)}"', 'aria-label="Fórmula de ${esc(a.cod)}" title="${esc(a0.f)}" value="${esc(a0.f)}"')
# ---------------------------------------------------------------- 3) dados em blocos JSON legíveis
L = t.split('\n')
def take(prefix):
    i = [k for k, l in enumerate(L) if l.startswith(prefix)]; assert len(i) == 1, prefix
    return i[0], json.loads(L[i[0]][len(prefix):].rstrip(';'))
i_db, DB = take('const DB=')
i_sd, SEED = take('const SEED=')
i_va, VANT = take('const VAR_ANT=')
i_an, NOVAS = take('const ACT_NOVAS=')
def bloco_base(D):
    s = '{"recursos":[\n' + ',\n'.join(j(r) for r in D['recursos']) + '\n],\n"base":[\n' + ',\n'.join(j(x) for x in D['base']) + '\n]}'
    assert set(D) == {'recursos', 'base'}
    return s
def bloco_comp(c):
    esc_ = [k for k in c if not isinstance(c[k], list)]
    lst = [k for k in c if isinstance(c[k], list)]
    head = '{' + ','.join(j(k) + ':' + j(c[k]) for k in esc_)
    parts = [j(k) + ':[' + ('\n  ' + ',\n  '.join(j(x) for x in c[k]) + '\n ]' if c[k] else ']') for k in lst]
    return head + ',\n ' + ',\n '.join(parts) + '}'
blocos = {
 'dados-base': ('Base de atividades embutida (cópia da base da nuvem v22 + atividades novas "só no app"). Uma atividade por linha: [código, disciplina, grupo, serviço, unidade, fonte, observação, {recurso: h por unidade}]. Quando a base da nuvem carrega, ela prevalece; daqui só valem as atividades listadas em dados-atividades-novas.', bloco_base(DB)),
 'dados-atividades-novas': ('Códigos das atividades novas que ainda não estão na base da nuvem (aparecem como "só no app").', '[\n' + ',\n'.join(j(x) for x in NOVAS) + '\n]'),
 'dados-composicoes': ('Composições padrão. Cada composição: params = entradas {k identificador, l descrição, u unidade, d valor padrão, o opções}; vars = parâmetros [identificador, fórmula ou valor, nome]; acts = atividades {cod, q fórmula}; notas = observações.', '[\n' + ',\n'.join(bloco_comp(c) for c in SEED) + '\n]'),
 'dados-nomes-antigos': ('Nomes de parâmetros de versões anteriores, para projetos salvos antes da 1.7.0.', j(VANT)),
}
html = ''
for bid, (desc, conteudo) in blocos.items():
    assert '</' not in conteudo and '<!--' not in conteudo, bid
    html += f'<!-- {desc} -->\n<script type="application/json" id="{bid}">\n{conteudo}\n</script>\n'
# confere que os blocos reproduzem os dados
assert json.loads(blocos['dados-base'][1]) == DB and json.loads(blocos['dados-composicoes'][1]) == SEED
assert json.loads(blocos['dados-atividades-novas'][1]) == NOVAS and json.loads(blocos['dados-nomes-antigos'][1]) == VANT
L[i_db] = "const DB=lerDados('dados-base');"
L[i_sd] = "const SEED=lerDados('dados-composicoes');"
L[i_va] = "const VAR_ANT=lerDados('dados-nomes-antigos');"
L[i_an] = "const ACT_NOVAS=lerDados('dados-atividades-novas');"
t = '\n'.join(L)

# ---------------------------------------------------------------- 4) índice e seções
INDICE = """/* ═══════════════════════════════════════════════════════════════════════════
   DIMENSIONAMENTO DE HISTOGRAMA — mapa do arquivo (procure por "§n")
   Dados editáveis: blocos <script type="application/json"> logo acima deste script
     dados-base · dados-atividades-novas · dados-composicoes · dados-nomes-antigos
   §1  Dados, versão, novidades e estado        §10 Tela Cronograma
   §2  Base de atividades e composições padrão  §11 Tela Histograma e curva S
   §3  Calendário (dias úteis, feriados, chuva) §12 Exportar e importar (.csv, .json)
   §4  Cálculo das composições (fórmulas)       §13 Nuvem: login, projetos, base global (Firebase)
   §5  Cronograma e histograma (cálculo)        §14 Biblioteca de composições
   §6  Interface: render, janelas, desfazer     §15 Início da sessão
   §7  Tela Parâmetros (calendário, INMET)      §16 Verificação dos dados (testes; não aparece na tela)
   §8  Telas Base de atividades e de recursos   §17 Copiar tabela
   §9  Tela Composições
   Regras do projeto, testes e fluxo de versões: CLAUDE.md na pasta "projeto".
   ═══════════════════════════════════════════════════════════════════════════ */
function lerDados(id){const e=document.getElementById(id);if(!e)throw Error('Bloco de dados "'+id+'" ausente');return JSON.parse(e.textContent)}"""
rep('<script>\nconst DB=lerDados', '<script>\n' + INDICE + "\n// ═══ §1 DADOS, VERSÃO, NOVIDADES E ESTADO ═══\nconst DB=lerDados")
t = t.replace('<script>\n' + INDICE, html + '<script>\n' + INDICE, 1)
SEC = [
 ('function baseFrom', '§2 BASE DE ATIVIDADES E COMPOSIÇÕES PADRÃO', 0),
 ('function nextMonday', '§3 CALENDÁRIO', 0),
 ('// ---------- cálculo', '§4 CÁLCULO DAS COMPOSIÇÕES', 1),
 ('let schedWarn', '§5 CRONOGRAMA E HISTOGRAMA (CÁLCULO)', 0),
 ('// ---------- UI', '§6 INTERFACE: RENDER, JANELAS, DESFAZER', 1),
 ('// Parâmetros', '§7 TELA PARÂMETROS', 1),
 ('// Base', '§8 TELAS BASE DE ATIVIDADES E BASE DE RECURSOS', 1),
 ('// Composições', '§9 TELA COMPOSIÇÕES', 1),
 ('// Cronograma', '§10 TELA CRONOGRAMA', 1),
 ('// Histograma', '§11 TELA HISTOGRAMA E CURVA S', 1),
 ('// export', '§12 EXPORTAR E IMPORTAR', 1),
 ('// Inicialização controlada pelo Firebase', '§13 NUVEM: LOGIN, PROJETOS E BASE GLOBAL', 0),
 ('// Biblioteca global de composições', '§14 BIBLIOTECA DE COMPOSIÇÕES', 0),
 ('async function bootstrapUser', '§15 INÍCIO DA SESSÃO', 0),
 ('// v1.5.1 — Copiar os dados', '§17 COPIAR TABELA', 0),
]
L = t.split('\n')
s0 = [k for k, l in enumerate(L) if l.startswith('<script>') and k + 1 < len(L) and L[k + 1].startswith('/* ═══')][0]
for pref, nome, exato in SEC:
    idx = [k for k in range(s0, len(L)) if (L[k] == pref if exato else L[k].startswith(pref))]
    assert len(idx) == 1, (pref, len(idx))
    L.insert(idx[0], f'// ═══ {nome} ═══')
t = '\n'.join(L)

# ---------------------------------------------------------------- 5) verificação dos dados (§16)
VALID = r"""// ═══ §16 VERIFICAÇÃO DOS DADOS (usada pelos testes; não aparece na tela) ═══
// Retorna a lista de problemas (vazia = tudo certo). Confere a base embutida e as composições padrão.
function validarDados(){const P=[],add=(onde,msg)=>P.push(onde+': '+msg);
 const recs=new Set(DB.recursos.map(r=>r[0])),cods=new Set();
 DB.base.forEach(x=>{const[cod,,,serv,un,,,r]=x;
  if(cods.has(cod))add(cod,'código repetido na base embutida');cods.add(cod);
  if(!serv)add(cod,'sem descrição');if(!un)add(cod,'sem unidade');
  const e=Object.entries(r||{});if(!e.length)add(cod,'sem recursos (soma 0 h)');
  e.forEach(([k,v])=>{if(!recs.has(k))add(cod,'recurso "'+k+'" fora da Base de recursos');if(!(typeof v==='number'&&isFinite(v)&&v>0))add(cod,'coeficiente inválido em '+k)})});
 ACT_NOVAS.forEach(c=>{if(!cods.has(c))add(c,'atividade nova sem cadastro na base embutida')});
 const ids=new Set();
 defaults().comps.forEach(c=>{if(ids.has(c.id))add(c.id,'composição com id repetido');ids.add(c.id);
  if(!c.nome)add(c.id,'composição sem nome');
  const L=compEval(c);
  Object.entries(L.varErr).forEach(([i,m])=>add(c.id,'parâmetro '+c.vars[i].k+': '+m));
  L.forEach(x=>{if(x.err)add(c.id,'fórmula de '+x.cod+': '+x.msg);if(!cods.has(x.cod))add(c.id,x.cod+' fora da base embutida')});
  (c.vars||[]).forEach(w=>{if(!w.l)add(c.id,'parâmetro '+w.k+' sem nome')});
  (c.inputs||[]).forEach(p=>{if(!p.l)add(c.id,'entrada '+p.k+' sem descrição')})});
 return P}"""
rep('// ═══ §17 COPIAR TABELA ═══', VALID + '\n// ═══ §17 COPIAR TABELA ═══')
open(dst, 'w', encoding='utf-8').write(t)
print('ok', len(t.encode()), 'linhas', t.count('\n') + 1)
