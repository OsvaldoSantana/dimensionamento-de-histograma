#!/usr/bin/env python3
"""Gera a v1.7.0 a partir da v1.6.1.
 - Terraplanagem: corte = área × espessura média de corte; aterro compactado = corte ÷ fator de homogeneização.
 - Parâmetros com nome (SEED vars [k, f, nome]); valor calculado ao lado da fórmula.
 - Dados de entrada em linha compacta; Parâmetros e Observações recolhidos, com estado lembrado.
 - Revisão das fontes da civil (exceto drenagem): CIV-0009 → CIV-0074, CIV-0056 → CIV-0133, trafo em concreto
   CIV-0075 → CIV-0110, coeficientes SINAPI em CIV-0136/0137/0143/0146, CIV-0141 volta ao valor por m²,
   casa de medição com CIV-0004 e sem as atividades de canaleta zeradas, observações com situação específica.
Uso: python3 v170.py v1.6.1.html v1.7.0.html
"""
import sys, json, re
src, dst = sys.argv[1:3]
t = open(src, encoding='utf-8').read()

def rep(old, new, count=1):
    global t
    n = t.count(old)
    assert n == count, (n, old[:120])
    t = t.replace(old, new)

DATA = '20/10/2026'
# ---------------------------------------------------------------- 1) versão e novidades
rep("const APP_VERSION='1.6.1';", "const APP_VERSION='1.7.0';")
t = re.sub(r'<!-- Dimensionamento de Histograma · arquivo 1\.6\.1 · [^ ]+ ·', '<!-- Dimensionamento de Histograma · arquivo 1.7.0 · 20/10/2026 ·', t, count=1)
assert 'arquivo 1.7.0' in t
NOV = """ {v:'1.7.0',data:'20/10/2026',itens:[
  'Terraplanagem refeita: o corte passa a ser a área do terreno × a espessura média de corte (0,30 m, editável) e o aterro compactado é o corte dividido pelo fator de homogeneização (1,25). Com 1.630 m², o corte cai de 982 m³ para 489 m³, sem duas escavações.',
  'Os parâmetros das composições têm nome (ex.: "Espessura média de corte (m)" no lugar de "Parâmetro [ecorte]") e mostram o valor calculado ao lado da fórmula. O lápis ao lado do nome permite renomear.',
  'Dados de entrada em uma linha compacta. Parâmetros e Observações ficam recolhidos logo abaixo, com a quantidade de itens, e o app lembra se você os deixou abertos.',
  'Revisão das fontes da civil (exceto drenagem): concreto magro pela CIV-0074 (lastro de concreto magro), brita do canteiro pela CIV-0133, tela do fundo da bacia de trafo em concreto pela CIV-0110 (Q-196) e coeficientes da SINAPI nas telas Q-785 e Q-92, no aço Ø5 e no concreto do abrigo e na janela.',
  'Casa de medição: volta a armação das cintas (CIV-0004), que só existia na casa de comando, e saem as três atividades de canaleta interna que davam zero.',
  'Observações da civil reescritas: cada composição abre com uma linha de situação datada de 20/10/2026 que diz o que falta conferir; saíram as notas genéricas e as que descreviam modelos antigos.'
 ]},"""
rep("const NOVIDADES=[\n", "const NOVIDADES=[\n" + NOV + "\n")

# ---------------------------------------------------------------- 2) base embutida (só atividades novas, que não estão na base da nuvem)
L = t.split('\n')
idb = [i for i, l in enumerate(L) if l.startswith('const DB=')][0]
D = json.loads(L[idb][len('const DB='):].rstrip(';'))
B = {x[0]: x for x in D['base']}
nov = json.loads(re.search(r'const ACT_NOVAS=(\[.*?\]);', t).group(1))
def coef(cod, r, fonte, obs):
    assert cod in nov, cod
    x = B[cod]; x[7] = r; x[5] = fonte; x[6] = obs
coef('CIV-0141', {'Pedreiro': 0.46483, 'Aux. Pedreiro': 0.232415}, 'SINAPI 94572',
     'Coeficiente da SINAPI 94572, que já é por m² de janela (pedreiro 0,46483 h/m², servente 0,232415 h/m²). Uma janela 1,00 × 1,20 m = 1,20 m².')
coef('CIV-0136', {'Armador': 0.018582, 'Aux. Armador': 0.0074328}, 'SINAPI 107279 (tela Q-636, a mais próxima da Q-785)',
     'A SINAPI não tem tela Q-785; usada a 107279 (radier com tela Q-636), por kg. Massa da Q-785 conforme a lista do VO778-CV-215.')
coef('CIV-0137', {'Armador': 0.0462942, 'Aux. Armador': 0.0185177}, 'SINAPI 97088',
     'Armação com tela Q-92 (SINAPI 97088), por kg. Massa preliminar da escada conforme a lista do VO778-CV-205.')
coef('CIV-0143', {'Armador': 0.1933, 'Aux. Armador': 0.0316}, 'SINAPI 92915',
     'Montagem de aço CA-60 Ø5,0 mm (SINAPI 92915), por kg. 39,26 m × 0,154 kg/m ≈ 6,05 kg por abrigo.')
coef('CIV-0146', dict(B['CIV-0142'][7]), 'Coeficientes da CIV-0142 (SINAPI 97096) — provisórios até separar base e cobertura',
     '0,69 m³ por abrigo somando base e cobertura. Mesmos coeficientes da CIV-0142 (vibrador CHP + CHI = 0,102 h/m³).')
L[idb] = 'const DB=' + json.dumps(D, ensure_ascii=False) + ';'

# ---------------------------------------------------------------- 3) composições padrão
isd = [i for i, l in enumerate(L) if l.startswith('const SEED=')][0]
SEED = json.loads(L[isd][len('const SEED='):].rstrip(';'))
S = {s['id']: s for s in SEED}
DREN = {'sarj', 'td1', 'td2', 'mcana', 'mur', 'cd1', 'oleo'}
CIVIL = [s['id'] for s in SEED if s['disc'] == 'CIVIL' and s['id'] not in DREN]
assert len(CIVIL) == 21, CIVIL

def acts(sid): return S[sid]['acts']
def troca_cod(sid, velho, novo, n=None):
    k = 0
    for a in acts(sid):
        if a['cod'] == velho: a['cod'] = novo; k += 1
    assert k and (n is None or k == n), (sid, velho, k)
    return k
def nota_rep(sid, velho, novo):
    s = S[sid]; achou = [n for n in s['notas'] if velho in n]
    assert len(achou) == 1, (sid, velho, len(achou))
    s['notas'] = [n.replace(velho, novo) for n in s['notas']]
def nota_fora(sid, inicio):
    s = S[sid]; n0 = len(s['notas']); s['notas'] = [n for n in s['notas'] if not n.startswith(inicio)]
    assert n0 - len(s['notas']) == 1, (sid, inicio)

# 3.1 terraplanagem
tr = S['terra']
assert [a['cod'] for a in tr['acts']] == ['CIV-0121', 'CIV-0103']
tr['vars'] = [['ecorte', '0.30'], ['fh', '1.25'], ['corte', 'area*ecorte'], ['aterro', 'corte/fh']]
tr['acts'] = [{'cod': 'CIV-0121', 'q': 'corte'}, {'cod': 'CIV-0103', 'q': 'aterro'}]
tr['notas'] = [
 'Modelo (revisão de 20/10/2026): corte = área do terreno × espessura média de corte (0,30 m). O solo cortado é espalhado e compactado na própria área, sem transporte, empréstimo ou bota-fora.',
 'Aterro compactado = corte ÷ fator de homogeneização (1,25): cada 1 m³ cortado vira 0,80 m³ compactado.',
 'Com 1.630 m²: 489 m³ de corte com trator de esteiras (CIV-0121) e 391 m³ compactados com rolo em camadas de 20 cm (CIV-0103).',
 'Até a 1.6.1 o modelo de plataforma em terreno inclinado dava 982 m³ de corte (0,60 m de espessura média) e contava escavação duas vezes.',
 'Com levantamento planialtimétrico ou projeto de terraplenagem, use espessura média = volume de corte do projeto ÷ área.',
 'A limpeza da camada vegetal é a composição separada "Limpeza do terreno".']

# 3.2 limpeza
lp = S['limp']; lp['vars'] = []
lp['notas'] = [
 'Limpeza mecanizada da camada vegetal (CIV-0001) em toda a área do terreno, sem transporte para bota-fora.',
 'Use junto com a Terraplanagem quando a obra fizer as duas etapas, ou sozinha quando o terreno já vier terraplenado e só faltar limpar.']

# 3.3 canteiro: brita pela CIV-0133 (a CIV-0056 cita a SINAPI 102719, que é enchimento de dreno)
troca_cod('cant', 'CIV-0056', 'CIV-0133', 1)
nota_rep('cant', 'CIV-0056 — 16,8 m³ de brita', 'CIV-0133 — 16,8 m³ de brita nº 3')
S['cant']['notas'].append('A brita do pátio do canteiro passou da CIV-0056 (SINAPI 102719, enchimento de dreno) para a CIV-0133 (lastro de brita, SINAPI 100322).')

# 3.4 concreto magro: CIV-0009 cita a SINAPI 96622 (lastro de brita); a CIV-0074 é lastro de concreto magro (SINAPI 96620)
for sid in CIVIL:
    if any(a['cod'] == 'CIV-0009' for a in acts(sid)): troca_cod(sid, 'CIV-0009', 'CIV-0074')
assert not any(a['cod'] == 'CIV-0009' for sid in CIVIL for a in acts(sid))

# 3.5 trafo em concreto: tela do fundo Q-196 (5,1 kg/m² = 4 painéis Q-196), como na bacia em alvenaria
troca_cod('trafocon', 'CIV-0075', 'CIV-0110', 1)
S['trafocon']['notas'].append('Tela do fundo pela CIV-0110 (Q-196), como na bacia em alvenaria: a taxa de 5,1 kg/m² é a dos 4 painéis Q-196 (estava na CIV-0075, tela Q-503).')

# 3.6 casa de medição: armação das cintas (como na casa de comando) e sem canaleta interna
cm = S['cmed']
assert not any(a['cod'] == 'CIV-0004' for a in cm['acts'])
cm['acts'] = [a for a in cm['acts'] if 'cint' not in str(a['q'])]
assert len(cm['acts']) == 11
cm['acts'].insert(1, {'cod': 'CIV-0004', 'q': 'qtd*6.35*P'})
cm['vars'] = [v for v in cm['vars'] if v[0] != 'cint']
cm['notas'].append('Armação das cintas e vigas (CIV-0004, 6,35 kg por metro de perímetro), igual à casa de comando: tinha ficado de fora. Sem canaleta interna (as três atividades zeradas saíram).')

# 3.7 parede corta-fogo: área sem uso
pc = S['pcf']; pc['vars'] = [v for v in pc['vars'] if v[0] != 'A']

# 3.8 observações desatualizadas
nota_rep('eletro', 'Tela Q-785 mantida em massa preliminar de 1084,72 kg; horas de montagem pendentes de fundamentação.',
         'Tela Q-785: 1.084,72 kg (29,8 kg por m² de radier), com horas da SINAPI 107279 (tela Q-636, a mais próxima que a SINAPI tem).')
nota_rep('ext', 'aço pela CIV-0143 (CA-60 Ø5) e CIV-0144 (CA-50 Ø8). Coeficientes provisórios até aprovação.',
         'aço pela CIV-0143 (CA-60 Ø5, SINAPI 92915) e CIV-0144 (CA-50 Ø8). Concreto, fôrma e aço Ø8 com coeficientes provisórios.')
nota_fora('trafoalv', 'Grauteamento da canaleta 0,658 m³ preliminar versus 3,00 m³ da lista')
S['brit']['notas'] = ['Volume = área × espessura (0,10 m, a camada de 10 cm da CIV-0133). Se o projeto pedir outra espessura (ex.: 0,15 m), ajuste o parâmetro.']
S['calc']['notas'] = [n for n in S['calc']['notas'] if not n.startswith('[')]

# 3.9 notas genéricas fora e situação específica (primeira linha das observações)
SIT = {
 'cant': 'quantidades do layout do canteiro da SE Milhão; fontes GOINFRA e ORSE das atividades CIV-020xx não conferidas; largura da calçada (2,0 m no desenho, 1,0 m na especificação) a confirmar.',
 'terra': 'espessura média de corte de 0,30 m adotada sem levantamento planialtimétrico; compactação (CIV-0103) com fonte DNIT sem código.',
 'limp': 'coeficiente conferido (SINAPI 98525); falta só a validação do coordenador.',
 'loc': 'fonte ORSE 4177 não conferida nesta revisão (a ORSE não tem consulta aberta).',
 'trafocon': 'sem projeto de referência (geometria da composição do Arthur); aço Ø10 (CIV-0079) com ajudante cerca de 10 vezes acima da SINAPI 92884, correção pedida na base; junta (SICRO 307733) não conferida.',
 'trafoalv': None,
 'eletro': 'taxas de um único projeto (VO778-CV-215); tela Q-785 com coeficiente da Q-636; grauteamento com coeficientes provisórios (MEC-0059).',
 'disj': 'a escavação de tubulão (CIV-0073, SINAPI 101102) já pode incluir a concretagem: confirmar para não contar duas vezes com a CIV-0063.',
 'poste': 'escavação de tubulão (CIV-0073) pode incluir a concretagem; "gaveta" do poste (CIV-0072) sem fonte.',
 'bspda': 'escavação de tubulão (CIV-0073) pode incluir a concretagem; anéis Ø120 pela CIV-0017 (manilha DN300 de drenagem, SINAPI 92808) como aproximação; solo-cimento lançado como reaterro.',
 'canc': 'sem projeto de canaleta; cinta (SINAPI 93204) não conferida; tubo PVC de 1 m por metro de canaleta a confirmar.',
 'cpm': 'projeto das caixas (VO778-CV-219) fora da pasta; reforço da CPMTR (dobro de concreto) é premissa; dreno pela CIV-0098 (dreno de muro, SINAPI 102723) como aproximação.',
 'banco': 'envelope de areia lançado como reaterro com soquete (sem atividade própria); comprimentos aproximados, medidos na planta.',
 'ccom': 'sem projeto de casa de comando (medidas do projeto Gujão); cobertura e esquadrias preliminares.',
 'cmed': 'sem projeto de casa de medição; alturas de parede da composição anterior.',
 'pcf': 'montagem de pilares e placas com horas internas de Munck, sem referência SINAPI; escavação de tubulão (CIV-0073) pode incluir a concretagem.',
 'ext': 'concreto, fôrma e aço Ø8 do abrigo com coeficientes provisórios.',
 'cerca': 'portão com concreto magro e armação, mas sem fundação dos pilares; 6 fios de arame farpado é premissa; portão (GOINFRA, sem código) e arame farpado (SINAPI 101188) não conferidos.',
 'pav': 'base e sub-base fora; meio-fio e sarjeta nos dois lados (2 × comprimento), como aprovado.',
 'brit': 'referência de lastro de brita (SINAPI 100322) usada para o pátio.',
 'calc': 'área de calçadas deve vir do arranjo (padrão 0).',
}
GEN = ('VALIDAÇÃO:', '[BLOQUEADA] Auditoria 19/10/2026', '[REVISÃO TÉCNICA] Auditoria 19/10/2026')
for sid in CIVIL:
    s = S[sid]
    s['notas'] = [n for n in s['notas'] if not n.startswith(GEN)]
    assert not any(n.startswith('[') for n in s['notas']), (sid, [n for n in s['notas'] if n.startswith('[')])
    if sid == 'trafoalv':
        st = f'[BLOQUEADA] {DATA}: grauteamento das canaletas calculado em 0,658 m³, mas a lista do VO778-CV-207 diz 3,00 m³. Resolver com o projeto antes de usar; grauteamento com coeficientes provisórios (MEC-0059).'
    else:
        st = f'[REVISÃO TÉCNICA] {DATA}: ' + SIT[sid]
    s['notas'].insert(0, st)

# 3.10 nomes dos parâmetros
LAB = {
 'malha': {'n': 'Condutores por direção (un)', 'lv': 'Comprimento total de cabo (m)', 'bv': 'Largura da vala (m)', 'hv': 'Profundidade da vala (m)', 'vala': 'Volume de vala (m³)'},
 'terra': {'ecorte': 'Espessura média de corte (m)', 'fh': 'Fator de homogeneização (corte ÷ compactado)', 'corte': 'Volume de corte (m³)', 'aterro': 'Volume de aterro compactado (m³)'},
 'calc': {'esp': 'Espessura da calçada (m)'},
 'brit': {'esp': 'Espessura da camada de brita (m)'},
 'trafocon': {'C': 'Comprimento da bacia (m)', 'L': 'Largura da bacia (m)', 'bc': 'Comprimento do bloco do trafo (m)', 'bl': 'Largura do bloco do trafo (m)', 'bh': 'Altura do bloco do trafo (m)',
              'hp': 'Altura das paredes da bacia (m)', 'ep': 'Espessura das paredes (m)', 'el': 'Espessura da laje de fundo (m)', 'eb': 'Espessura da brita nº 3 (m)',
              'taxa': 'Taxa de aço do bloco (kg/m³)', 'tp': 'Taxa de aço das paredes (kg/m³)', 'ab': 'Área do bloco (m²)', 'al': 'Área da laje sem o bloco (m²)', 'per': 'Perímetro externo da bacia (m)'},
 'trafoalv': {'C': 'Comprimento da bacia (m)', 'L': 'Largura da bacia (m)', 'bc': 'Comprimento do bloco do trafo (m)', 'bl': 'Largura do bloco do trafo (m)', 'bh': 'Altura do bloco do trafo (m)',
              'hp': 'Altura das paredes de bloco (m)', 'el': 'Espessura da laje de fundo (m)', 'eb': 'Espessura da brita nº 3 (m)', 'taxa': 'Taxa de aço do bloco (kg/m³)',
              'ab': 'Área do bloco (m²)', 'al': 'Área da laje sem o bloco (m²)'},
 'eletro': {'C': 'Comprimento do radier (m)', 'L': 'Largura do radier (m)', 'np': 'Pilotis de apoio (un)', 'A': 'Área do radier (m²)'},
 'cpm': {'L1': 'Lado interno da caixa CP1 (m)', 'P1': 'Profundidade da caixa CP1 (m)', 'L2': 'Lado interno das caixas CPMT/CPMTR (m)', 'P2': 'Profundidade das caixas CPMT/CPMTR (m)',
         'fr': 'Fator de reforço da CPMTR (concreto)', 'ext1': 'Área externa da CP1 (m²)', 'ext2': 'Área externa da CPMT/CPMTR (m²)', 'nt': 'Total de caixas (un)'},
 'canc': {'be': 'Largura externa da canaleta (m)', 'hp': 'Altura das paredes (m)', 'et': 'Espessura da tampa (m)'},
 'banco': {'b': 'Largura da vala (m)', 'ad': 'Seção de um duto Ø125 mm (m²)'},
 'ccom': {'e': 'Espessura da parede (m)', 'A': 'Área construída (m²)', 'P': 'Perímetro externo (m)', 'Pi': 'Perímetro interno (m)', 'vaos': 'Área de portas e janelas (m²)'},
 'cmed': {'C': 'Comprimento externo (m)', 'L': 'Largura externa (m)', 'port': 'Portas (un)', 'jan': 'Janelas (un)', 'e': 'Espessura da parede (m)', 'A': 'Área construída (m²)',
          'P': 'Perímetro externo (m)', 'Pi': 'Perímetro interno (m)', 'vaos': 'Área de portas e janelas (m²)'},
 'pcf': {'vaos': 'Vãos entre pilares (un)', 'np': 'Pilares (un)', 'placas': 'Placas (un)'},
}
for s in SEED:
    lab = LAB.get(s['id'], {})
    for v in s['vars']:
        assert v[0] in lab, (s['id'], v[0])
        v[:] = [v[0], v[1], lab[v[0]]]
    assert set(lab) == {v[0] for v in s['vars']}, (s['id'], set(lab) ^ {v[0] for v in s['vars']})
# nomes de parâmetros de versões anteriores (projetos salvos antes da 1.7.0)
ANT = {'terra': {'decl': 'Declividade média do terreno', 'esp': 'Espessura da raspagem (m)', 'mc': 'Talude de corte (H:V)', 'ma': 'Talude de aterro (H:V)', 'fh': 'Fator de homogeneização',
                 'aprov': 'Reaproveitamento do corte (0 ou 1)', 'dbota': 'Distância ao bota-fora (km)', 'demp': 'Distância ao empréstimo (km)', 'ecomp': 'Camada final compactada (m)',
                 's': 'Lado da plataforma (m)', 'vgeo': 'Volume geométrico (m³)', 'corte': 'Volume de corte (m³)', 'aterro': 'Volume de aterro (m³)', 'reuso': 'Corte reaproveitado (m³)',
                 'emp': 'Empréstimo (m³)', 'bota': 'Bota-fora (m³)', 'compactado': 'Aterro compactado (m³)', 'deficit': 'Déficit de aterro (m³)'},
       'limp': {'esp': 'Espessura da raspagem (m)', 'dbota': 'Distância ao bota-fora (km)'},
       'cmed': {'cint': 'Canaleta interna de cabos (m)'}, 'pcf': {'A': 'Área da parede (m²)'}}
L[isd] = 'const SEED=' + json.dumps(SEED, ensure_ascii=False) + ';'
L.insert(isd + 1, 'const VAR_ANT=' + json.dumps(ANT, ensure_ascii=False) + ';')
t = '\n'.join(L)

# ---------------------------------------------------------------- 4) app: nomes de parâmetros, valores calculados
rep("  vars:t.vars.map(([k,f])=>({k,f})),", "  vars:t.vars.map(([k,f,l])=>l?{k,f,l}:{k,f}),")
rep(" out.varErr=varErr;return out}", " out.varErr=varErr;out.env=env;return out}")
rep("function setVar(i,v){cur().vars[i].f=v;render()}",
    "function setVar(i,v){cur().vars[i].f=v;render()}\n"
    "// v1.7.0: nome do parâmetro — o do próprio parâmetro, ou o da composição padrão de mesmo id/nome (projetos antigos).\n"
    "const VAR_LAB=(()=>{const m={};SEED.forEach(t=>{const o=Object.assign({},VAR_ANT[t.id]||{});(t.vars||[]).forEach(v=>{if(v[2])o[v[0]]=v[2]});m['id:'+t.id]=o;m['nm:'+t.nome]=o});return m})();\n"
    "function varLabel(c,w){if(w.l)return w.l;const o=VAR_LAB['id:'+c.id]||VAR_LAB['nm:'+c.nome];return o&&o[w.k]||''}\n"
    "async function nomeVar(i){const c=cur(),w=c.vars[i];const f=await askForm('Nome do parâmetro',[{k:'l',l:'Nome como aparece na tela (identificador nas fórmulas: '+w.k+')',v:varLabel(c,w),ph:'ex.: Espessura média de corte (m)'}],{ok:'Salvar'});if(!f)return;const l=f.l.trim();if(l)w.l=l;else delete w.l;render()}\n"
    "// Parâmetros e Observações recolhidos: o app lembra se ficaram abertos (só neste navegador).\n"
    "const UIO={par:false,obs:false};try{Object.assign(UIO,JSON.parse(localStorage.getItem('volga_hist_ui_open')||'{}'))}catch(e){}\n"
    "function uiOpen(k,v){UIO[k]=!!v;try{localStorage.setItem('volga_hist_ui_open',JSON.stringify(UIO))}catch(e){}}\n"
    "const fmtV=v=>Number.isFinite(+v)?Number(v).toLocaleString('pt-BR',{maximumFractionDigits:3}).replace(/\\./g,'\\u202f'):String(v);")

# bloco de entradas, parâmetros e observações
a = t.index(' <div style="background:var(--gt);border:1px solid #c3d6ba;border-radius:10px;padding:12px;margin-bottom:14px"><h4 style="margin:0 0 8px">Dados de entrada</h4>')
b = t.index(' <h4>Atividades</h4>', a)
old = t[a:b]
assert old.count('<div class="notas">') == 1 and 'Nas fórmulas use' in old
NEW = (
 ' <div class="din"><h4>Dados de entrada</h4>\n'
 ' <div class="ins">${(c.inputs||[]).map((p,i)=>`<label class="ci" title="Identificador nas fórmulas: ${esc(p.k)}"><span>${esc(p.l)}</span>${p.o?`<select onchange="setIn(${i},this.value,0)">${p.o.map(o=>`<option value="${esc(o[0])}" ${String(p.v)===o[0]?\'selected\':\'\'}>${esc(o[1])}</option>`).join(\'\')}</select>`:`<input type="number" step="any" value="${esc(p.v)}" onchange="setIn(${i},this.value,1)">`}${p.u?`<span class="u">${esc(p.u)}</span>`:\'\'}</label>`).join(\'\')||\'<span class="hint">Sem entradas.</span>\'}</div>\n'
 ' <div class="sub">\n'
 ' <details class="mini${Object.keys(L.varErr).length?\' err\':\'\'}" ${UIO.par||Object.keys(L.varErr).length?\'open\':\'\'} ontoggle="uiOpen(\'par\',this.open)"><summary>Parâmetros (${(c.vars||[]).length})${Object.keys(L.varErr).length?\' — erro nas fórmulas\':\'\'}</summary>\n'
 ' <p class="hint">Premissas e cálculos do padrão técnico desta composição. Alterar muda as quantidades.</p>\n'
 ' ${(c.vars||[]).length?`<div class="pars">${c.vars.map((w,i)=>{const lb=varLabel(c,w);return`<div class="pr"><span class="pn">${lb?esc(lb):\'<i>Sem nome</i>\'} <span class="hint">[${esc(w.k)}]</span><button class="lnk" title="Renomear" aria-label="Renomear parâmetro ${esc(w.k)}" onclick="nomeVar(${i})">✎</button></span><input aria-label="${esc(lb||w.k)}" style="${L.varErr[i]?\'border-color:var(--red)\':\'\'}" title="${esc(L.varErr[i]||\'\')}" value="${esc(w.f)}" onchange="setVar(${i},this.value)"><span class="pv">${L.varErr[i]?`<span style="color:var(--red)">${esc(L.varErr[i])}</span>`:(/^\\s*-?[\\d.]+\\s*$/.test(String(w.f))?\'\':\'= \'+fmtV(L.env[w.k]))}</span></div>`}).join(\'\')}</div>`:\'<p class="hint">Sem parâmetros.</p>\'}\n'
 ' <div class="pin"><span class="hint">Entradas nas fórmulas:</span> ${(c.inputs||[]).map((p,i)=>`<span class="chip">${esc(p.l)} [${esc(p.k)}] <button class="lnk" title="Excluir entrada" aria-label="Excluir entrada ${esc(p.k)}" onclick="rmIn(${i})">×</button></span>`).join(\'\')}<button onclick="addIn()">+ Entrada</button></div>\n'
 ' <div class="hint">Nas fórmulas use os identificadores entre colchetes, mais sqrt(), ceil(), floor(), max(), min(), PI e operadores (+ − * / **). Um número fixo também vale.</div>\n'
 ' </details>\n'
 ' <details class="mini" ${UIO.obs?\'open\':\'\'} ontoggle="uiOpen(\'obs\',this.open)"><summary>Observações (${(c.notas||[]).length})</summary>\n'
 ' <div class="notas">${(c.notas||[]).map((n,i)=>`<div class="nl"><span class="hint">•</span><input class="nota-in" value="${esc(n)}" placeholder="Digite a observação" aria-label="Observação ${i+1}" onchange="setNota(${i},this.value)"><button class="d i" title="Excluir observação" aria-label="Excluir observação" onclick="rmNota(${i})">×</button></div>`).join(\'\')||\'<div class="hint" style="margin-bottom:6px">Nenhuma observação.</div>\'}<button onclick="addNota()">+ Observação</button></div>\n'
 ' </details></div></div>\n')
# o fechamento </div> da caixa de entrada original fica no fim de old (antes de <h4>Atividades</h4>)
assert old.rstrip().endswith('</div></div>'), old[-200:]
t = t[:a] + NEW + t[b:]
# observações: abrir ao incluir uma nova
rep("function addNota(){const c=cur();c.notas=c.notas||[];c.notas.push('');render();",
    "function addNota(){const c=cur();c.notas=c.notas||[];c.notas.push('');UIO.obs=true;render();")
CSS = (".din{background:var(--gt);border:1px solid #c3d6ba;border-radius:10px;padding:9px 12px 8px;margin-bottom:14px}"
       ".din h4{margin:0 0 6px!important;font-size:13px!important}"
       ".din .ins{display:flex;flex-wrap:wrap;gap:6px 20px;align-items:center}"
       ".din .ci{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:var(--tx,#1f2a1c);margin:0}"
       ".din .ci input{width:92px;padding:4px 7px;margin:0}.din .ci select{padding:4px 6px;margin:0;max-width:240px}.din .ci .u{color:var(--gr);font-weight:500;font-size:12px}"
       ".din .sub{display:flex;flex-wrap:wrap;gap:4px 22px;margin-top:7px}"
       ".din details.mini>summary{cursor:pointer;color:var(--g2);font-weight:600;font-size:12.5px;padding:2px 0}"
       ".din details.mini[open]{flex:1 1 100%;background:#fff;border:1px solid #c3d6ba;border-radius:8px;padding:6px 10px 8px}"
       ".din details.mini.err>summary{color:var(--red)}"
       ".pars{display:grid;grid-template-columns:minmax(0,max-content) minmax(140px,260px) minmax(70px,auto);justify-content:start;gap:5px 14px;align-items:center;margin:4px 0 8px}"
       ".pars .pr{display:contents}.pars .pn{font-size:12.5px;font-weight:600;color:var(--tx,#1f2a1c)}.pars input{padding:4px 7px;margin:0;width:100%}"
       ".pars .pv{font-size:12px;color:var(--gr);white-space:nowrap;font-variant-numeric:tabular-nums}"
       "button.lnk{background:none;border:0;padding:0 3px;margin:0;color:var(--g2);cursor:pointer;font-size:12px;min-height:0;box-shadow:none}"
       ".pin{display:flex;flex-wrap:wrap;gap:4px;align-items:center;margin:2px 0 6px}"
       "@media (max-width:520px){.pars{grid-template-columns:minmax(0,1fr) auto}.pars .pn{grid-column:1/-1;margin-top:4px}.din .ci{flex:1 1 100%;justify-content:space-between}.din .ci span:first-child{flex:1}}\n")
rep(".notas{margin:10px 0 6px}", CSS + ".notas{margin:4px 0 2px}")
open(dst, 'w', encoding='utf-8').write(t)
print('ok', len(t.encode()), 'SEED', len(SEED))
