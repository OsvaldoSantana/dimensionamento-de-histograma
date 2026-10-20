#!/usr/bin/env python3
"""Gera a v1.6.1 a partir da v1.6.0 (feita fora desta conversa), corrigindo o que a revisão encontrou.
 Mantém da 1.6.0: copiar tabela, seleção múltipla, logo que abre os projetos, composições revisadas pelo Osvaldo,
 atividades novas (agora com coeficientes), entradas só por quantidade, parâmetros recolhidos.
 Corrige: volta todas as disciplinas (composições padrão, filtros, busca de atividade), volta observações editáveis
 e avisos de auditoria, histórico de novidades, recursos fixos no código, atividades sem recurso, janela em m²,
 entrada "Portas" sem uso, observações desatualizadas.
Uso: python3 v161.py v160.html ../v16/v151.html v1.6.1.html
"""
import sys, json, re, difflib
src, ref, dst = sys.argv[1:4]
b = open(src, encoding='utf-8').read().split('\n')     # 1.6.0
a = open(ref, encoding='utf-8').read().split('\n')     # 1.5.1 (referência para desfazer trechos)

# ---------------------------------------------------------------- 1) desfazer trechos da 1.6.0 (por conteúdo, conferido)
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
def pick(pred):
    m = [o for o in ops if pred(o)]
    assert len(m) == 1, (len(m), [x[:5] for x in m])
    return m[0]
REVERT = [
 lambda o: o[0] == 'replace' and o[3] < len(b) and "g('terra').usar=false;" == b[o[3]].strip(),                       # malha volta (sem marcar)
 lambda o: o[0] == 'replace' and a[o[1]].lstrip().startswith('<label>Disciplina<select onchange="filt.disc'),          # filtro de disciplina na base
 lambda o: o[0] == 'replace' and '<th class="opt">Disciplina</th>' in a[o[1]] and 'table class="base"' in a[o[1]],     # coluna disciplina
 lambda o: o[0] == 'replace' and '<td class="opt">${esc(a.disc)}</td>' in a[o[1]] and "$('#brows').innerHTML" in a[o[1]],
 lambda o: o[0] == 'replace' and 'colspan="${adm?7:6}"' in a[o[1]],
 lambda o: o[0] == 'replace' and '<label>Disciplina<input id="na_d"' in a[o[1]],                                        # disciplina no cadastro de atividade
 lambda o: o[0] == 'replace' and "esc(c.disc)} · ${fmt(k.dur)} h" in a[o[1]],                                           # disciplina, horas e nº de atividades na lista
 lambda o: o[0] == 'delete' and 'n.startsWith("[BLOQUEADA]")' in a[o[1]],                                               # aviso de auditoria
 lambda o: o[0] == 'delete' and '<div class="notas">' in a[o[1]],                                                       # observações editáveis
 lambda o: o[0] == 'replace' and '<label>Disciplina<select id="pd"' in a[o[1]],                                         # disciplina na busca de atividade
 lambda o: o[0] == 'replace' and a[o[1]].startswith('let REC,TIPO,globalRecursos=[];'),                                 # sem recursos fixos no código
]
chosen = [pick(p) for p in REVERT]
# aplica de trás para frente para não deslocar índices
for tag, i1, i2, j1, j2 in sorted(chosen, key=lambda o: -o[3]):
    b[j1:j2] = a[i1:i2]
t = '\n'.join(b)

def rep(old, new, count=1):
    global t
    n = t.count(old)
    assert n == count, (n, old[:100])
    t = t.replace(old, new)

# ---------------------------------------------------------------- 2) novidades: histórico completo
an = '\n'.join(a)
old_hist = re.search(r"const NOVIDADES=\[\n(.*?)\n\];", an, re.S).group(1)          # 1.5.1 … 1.1.0
m = re.search(r"const NOVIDADES=\[\n(.*?)\n\];", t, re.S)
v160 = m.group(1).rstrip()
if not v160.endswith(','): v160 += ','
NOV161 = """ {v:'1.6.1',data:'20/10/2026',itens:[
  'Voltam todas as disciplinas: as composições padrão de eletromecânica e instalações elétricas (malha, SPDA, seccionadora, suportes, barramento, cabos, BT, HVAC, SDAI e CFTV), o filtro e a coluna de disciplina na Base de atividades e a escolha de disciplina ao incluir uma atividade na composição.',
  'Voltam as observações editáveis da composição (com "+ Observação") e os avisos "Composição não aprovada" e "Revisão técnica pendente".',
  'Atividades novas que estavam sem recurso (grauteamentos, telas, armação, fôrma e concreto do abrigo) recebem coeficientes provisórios de atividades equivalentes da base, indicados na fonte, para não entrarem com zero hora.',
  'Recursos novos que estavam fixos no arquivo foram trocados pelos da Base de recursos (Calceteiro → Pedreiro, Servente → Aux. Pedreiro, Guincho → Munck); nenhum recurso novo vai para a nuvem sem o administrador.',
  'A lista de composições volta a mostrar disciplina, horas e número de atividades, e o histórico completo de novidades volta a aparecer.'
 ]},"""
t = t.replace(m.group(0), "const NOVIDADES=[\n" + NOV161 + "\n" + v160 + "\n" + old_hist + "\n];", 1)
rep("const APP_VERSION='1.6.0-civil-dec32';", "const APP_VERSION='1.6.1';")
t = re.sub(r'<!-- Dimensionamento de Histograma · arquivo 1\.6\.0 · [^ ]+ ·', '<!-- Dimensionamento de Histograma · arquivo 1.6.1 · 20/10/2026 ·', t, count=1)
assert 'arquivo 1.6.1' in t

# ---------------------------------------------------------------- 3) base embutida: recursos e atividades novas
L = t.split('\n')
idb = [i for i, l in enumerate(L) if l.startswith('const DB=')][0]
D = json.loads(L[idb][len('const DB='):].rstrip(';'))
MAPREC = {'Calceteiro': 'Pedreiro', 'Servente': 'Aux. Pedreiro', 'Guincho Elétrico de Coluna': 'Munck'}
REMOVER = {'Cortadora de Piso'}
D['recursos'] = [r for r in D['recursos'] if r[0] not in MAPREC and r[0] not in REMOVER]
nomes = {r[0] for r in D['recursos']}
B = {x[0]: x for x in D['base']}
for x in D['base']:
    r = x[7]
    if any(k in MAPREC or k in REMOVER for k in r):
        novo = {}
        for k, v in r.items():
            if k in REMOVER: continue
            k2 = MAPREC.get(k, k)
            novo[k2] = round(novo.get(k2, 0) + v, 6)
        trocas = [f'{k} → {MAPREC[k]}' for k in r if k in MAPREC] + [f'{k} retirado' for k in r if k in REMOVER]
        x[7] = novo
        x[6] = (x[6] + ' | ' if x[6] else '') + 'Recursos ajustados à Base de recursos: ' + '; '.join(trocas) + '.'
    assert all(k in nomes for k in x[7]), (x[0], x[7])
# atividades sem recurso: coeficientes provisórios de atividades equivalentes da base
PROV = {'CIV-0134': 'MEC-0059', 'CIV-0135': 'MEC-0059', 'CIV-0136': 'CIV-0075', 'CIV-0137': 'CIV-0090',
        'CIV-0143': 'CIV-0085', 'CIV-0144': 'CIV-0084', 'CIV-0145': 'CIV-0062', 'CIV-0146': 'CIV-0077'}
for cod, eq in PROV.items():
    x = B[cod]; assert not x[7], cod
    x[7] = dict(B[eq][7])
    x[5] = (x[5] + ' — ' if x[5] else '') + f'coeficientes provisórios da {eq} ({B[eq][3][:60].strip()}) até aprovação'
# janela: a CIV-0141 é por m², a CIV-0046 de origem é por unidade (janela 1,00 × 1,20 m = 1,2 m²)
j = B['CIV-0141']; assert j[4] == 'm²'
j[7] = {k: round(v / 1.2, 6) for k, v in B['CIV-0046'][7].items()}
j[6] = (j[6] + ' | ' if j[6] else '') + 'Coeficiente da CIV-0046 (por unidade) dividido por 1,2 m² da janela padrão 1,00 × 1,20 m.'
L[idb] = 'const DB=' + json.dumps(D, ensure_ascii=False) + ';'

# ---------------------------------------------------------------- 4) composições padrão
isd = [i for i, l in enumerate(L) if l.startswith('const SEED=')][0]
SEED = json.loads(L[isd][len('const SEED='):].rstrip(';'))
la = an.split('\n')
SEED151 = {s['id']: s for s in json.loads([l for l in la if l.startswith('const SEED=')][0][len('const SEED='):].rstrip(';'))}
ids = [s['id'] for s in SEED]
assert 'malha' not in ids
out = [SEED151['malha']]
for s in SEED:
    out.append(s)
    if s['id'] == 'cerca':
        out += [SEED151[k] for k in ['spda', 'secc', 'supo', 'barr', 'cabos', 'bt', 'hvac', 'sdai', 'cftv']]
S = {s['id']: s for s in out}
# casa de comando: a entrada "Portas" não entra em nenhuma conta desde que as portas saíram da composição
cc = S['ccom']
usa = lambda c, k: any(re.search(r'\b%s\b' % re.escape(k), f) for f in [v[1] for v in c['vars']] + [x['q'] for x in c['acts'] if isinstance(x['q'], str)])
if not usa(cc, 'port'):
    cc['params'] = [p for p in cc['params'] if p['k'] != 'port']
# observações que citam códigos que não estão mais na composição
TROCA = {'CAN-005': 'CIV-02005', 'CAN-006': 'CIV-02006', 'CAN-007': 'CIV-02007', 'CAN-008': 'CIV-02008', 'CAN-009': 'CIV-02009',
         'CAN-010': 'CIV-02010', 'CAN-011': 'CIV-02011', 'CIV-0024': 'CIV-0147', 'CIV-0025': 'CIV-0148'}
for s in out:
    codes = {x['cod'] for x in s['acts'] if isinstance(x['cod'], str)}
    novas = []
    for n in s['notas']:
        for velho, novo in TROCA.items():
            if velho in n and velho not in codes and novo in codes: n = n.replace(velho, novo)
        novas.append(n)
    s['notas'] = novas
def nota(sid, velho, novo):
    s = S[sid]; achou = [n for n in s['notas'] if velho in n]
    assert achou, (sid, velho)
    s['notas'] = [n.replace(velho, novo) for n in s['notas']]
nota('limp', 'Limpeza mecanizada da camada vegetal (CIV-0001) e transporte do material removido para bota-fora (CIV-0114).',
     'Limpeza mecanizada da camada vegetal (CIV-0001), sem transporte para bota-fora (revisão de 19/10/2026).')
nota('ext', '(com a fôrma de 4,28 m², inclusa no CIV-0010)', '(fôrma de 4,28 m² na CIV-0145)')
# terraplanagem: observações que descreviam o modelo antigo (com corte, transporte e limpeza incluídos)
tr = S['terra']
fora = ('Com 1.630 m², o modelo dá corte', 'Corte para bota-fora:', 'ATENÇÃO: esta composição JÁ INCLUI CIV-0001')
n0 = len(tr['notas']); tr['notas'] = [n for n in tr['notas'] if not n.startswith(fora)]; assert n0 - len(tr['notas']) == 3
nota('terra', 'Novo: compactação do aterro (CIV-0103, rolo, camadas de 20 cm), que antes não era contada; bota-fora passa a incluir o corte, não só a raspagem.',
     'Compactação do aterro pela CIV-0103 (rolo, camadas de 20 cm). A limpeza do terreno é a composição separada "Limpeza do terreno".')
nota('terra', ', DMT de bota-fora e de empréstimo 10 km', '')
nota('eletro', ' Pilares (np): quantidades do Arthur por pilar, sem projeto de referência.', '')
nota('ext', 'Base v22: concreto pela CIV-0077 (0,69 m³ por abrigo) e fôrma pela CIV-0010 (4,28 m² por abrigo), ambos da lista do VO778-CV-229.',
     'Concreto pela CIV-0146 (0,69 m³ por abrigo) e fôrma pela CIV-0145 (4,28 m² por abrigo), da lista do VO778-CV-229; aço pela CIV-0143 (CA-60 Ø5) e CIV-0144 (CA-50 Ø8). Coeficientes provisórios até aprovação.')
for k in ('ccom', 'cmed'):
    nota(k, 'radier de 10 cm concretado pela CIV-0077 (m³)', 'radier de 10 cm concretado pela CIV-0142 (m³)')
# banco de dutos: a instalação dos dutos (ELE-0016) só tinha saído porque o projeto padrão era só civil
bd = S['banco']
assert not any(x['cod'] == 'ELE-0016' for x in bd['acts'])
bd['acts'].insert(2, {'cod': 'ELE-0016', 'q': 'L2*d2+L1*d1'})
bd['notas'] = [n for n in bd['notas'] if not n.startswith('Instalação elétrica de dutos ELE-0016 excluída')]
bd['notas'].append('Instalação dos dutos (ELE-0016) de volta: só tinha saído enquanto o projeto padrão era exclusivamente civil.')
L[isd] = 'const SEED=' + json.dumps(out, ensure_ascii=False) + ';'
t = '\n'.join(L)
rep(" g('terra').usar=false;g('malha').usar=false;g('malha').pred='';", " g('terra').usar=false;g('malha').usar=false;g('malha').pred='';")
# coluna de seleção estreita (o título "Selecionar" alargava a tabela e espremia o nome da atividade)
rep('<th class="ro-ok">Selecionar</th>', '<th class="ro-ok sel"><span class="sr">Selecionar</span></th>')
rep(".notas{margin:10px 0 6px}", "table.acts th.sel,table.acts td:has(>.act-select){width:1%;padding-left:8px;padding-right:4px}\n.notas{margin:10px 0 6px}")
open(dst, 'w', encoding='utf-8').write(t)
print('ok', len(t.encode()), 'SEED', len(out), 'DB', len(D['base']), 'rec', len(D['recursos']))
