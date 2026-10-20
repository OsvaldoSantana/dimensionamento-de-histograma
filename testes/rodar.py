#!/usr/bin/env python3
"""Testes do Dimensionamento de Histograma — um comando roda tudo.

Uso (na pasta "projeto"):
  python testes/rodar.py index.html                        # roda os testes contra testes/referencia.json
  python testes/rodar.py index.html --atualizar-referencia # grava a referência a partir deste arquivo
  python testes/rodar.py index.html --teste-json SAIDA.json # também gera o .json do projeto TESTE (21 civis)

Requisitos: Python 3.10+ e Playwright (pip install playwright; python -m playwright install chromium).
Para usar um Chromium já instalado, defina a variável PW_CHROMIUM com o caminho do executável.

O que é conferido:
  1. o arquivo abre sem erro de JavaScript e todas as abas desenham sem erro;
  2. validarDados() não acha problema na base embutida nem nas composições padrão;
  3. HH de mão de obra, HH de equipamento, duração e dias úteis de cada composição padrão são iguais
     aos de testes/referencia.json (tolerância 0,05);
  4. em 390 px de largura nenhuma aba tem rolagem lateral;
  5. a tela Composições tem a lista, a busca, a tabela com a coluna "Fórmula" e o botão Copiar na barra.
A nuvem (Firebase) é substituída por um simulador: nada é lido nem gravado na base real.
"""
import asyncio, json, os, re, sys, tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REF = AQUI / 'referencia.json'
CIVIS = ['cant', 'limp', 'terra', 'loc', 'trafocon', 'trafoalv', 'eletro', 'disj', 'poste', 'bspda', 'canc', 'cpm',
         'banco', 'ccom', 'cmed', 'pcf', 'ext', 'cerca', 'pav', 'brit', 'calc']
ABAS = ['comp', 'cron', 'hist', 'base', 'recursos', 'par']

STUB = ("<script>const _p=()=>new Proxy(function(){},{get:(t,k)=>k==='then'?undefined:_p(),apply:()=>_p()});"
        "window.firebase={initializeApp(){},auth(){return{onAuthStateChanged(){},currentUser:{uid:'u1',email:'teste@volga.com.br',emailVerified:true}}},"
        "firestore:Object.assign(()=>_p(),{FieldValue:{serverTimestamp(){},delete(){}}})};</script>")
# Abre um projeto local de teste com as composições padrão e a base embutida (sem as atividades novas na "nuvem").
BOOT = ("()=>{document.getElementById('authgate').style.display='none';globalBase=baseFrom().filter(a=>!ACT_NOVAS.includes(a.cod));"
        "cloudReady=true;currentProjectId='p1';currentOwnerId='u1';S=migrate(defaults());S.params.start='2026-10-19';S.projectName='T';"
        "saveCloudProject=async()=>{};lastSavedJSON=JSON.stringify(S);if(typeof resetHistory==='function')resetHistory();render();return 1}")
INDICADORES = """()=>{const EQ=new Set(Object.entries(TIPO).filter(([k,v])=>v!=='Mão de obra').map(([k])=>k));
 return Object.fromEntries(S.comps.map(c=>{const k=compCalc(c);let mo=0,eq=0;for(const[r,v]of Object.entries(k.res))(EQ.has(r)?eq+=v:mo+=v);
  return [c.id,{nome:c.nome,hh_mo:+mo.toFixed(2),hh_eq:+eq.toFixed(2),dur_h:+k.dur.toFixed(2),dias:k.days}]}))}"""


def preparar(index):
    t = Path(index).read_text(encoding='utf-8')
    t2, n = re.subn(r'(<script src="https://www\.gstatic\.com[^"]+"></script>\s*)+', STUB, t)
    assert n == 1, 'scripts do Firebase não encontrados no index.html'
    d = Path(tempfile.mkdtemp(prefix='hist_'))
    f = d / 'h.html'; f.write_text(t2, encoding='utf-8')
    return f.as_uri()


async def principal(index, atualizar, teste_json):
    from playwright.async_api import async_playwright
    falhas, avisos = [], []
    async with async_playwright() as pw:
        exe = os.environ.get('PW_CHROMIUM')
        b = await pw.chromium.launch(**({'executable_path': exe} if exe else {}))
        pg = await b.new_page(viewport={'width': 1366, 'height': 860}, locale='pt-BR')
        erros = []
        pg.on('pageerror', lambda e: erros.append('erro de JavaScript: ' + str(e)[:200]))
        pg.on('console', lambda m: erros.append('console: ' + m.text[:200]) if m.type == 'error' else None)
        await pg.goto(preparar(index))
        await pg.evaluate(BOOT)
        versao = await pg.evaluate('()=>APP_VERSION')
        print(f'Arquivo {index} · versão {versao}')

        # 1. abas
        for aba in ABAS:
            await pg.evaluate(f"()=>setTab('{aba}')"); await pg.wait_for_timeout(120)
        # 2. dados
        prob = await pg.evaluate('()=>typeof validarDados==="function"?validarDados():["validarDados() ausente"]')
        if prob: falhas += ['dados: ' + p for p in prob]
        # 3. indicadores
        atual = await pg.evaluate(INDICADORES)
        if atualizar:
            REF.write_text(json.dumps({'versao': versao, 'composicoes': atual}, ensure_ascii=False, indent=1), encoding='utf-8')
            print(f'referência gravada: {REF} ({len(atual)} composições)')
        elif REF.exists():
            ref = json.loads(REF.read_text(encoding='utf-8'))
            print(f'comparando com a referência da versão {ref["versao"]}')
            R = ref['composicoes']
            for cid in sorted(set(R) | set(atual)):
                if cid not in atual: falhas.append(f'{cid}: composição sumiu'); continue
                if cid not in R: avisos.append(f'{cid}: composição nova, sem referência'); continue
                for campo in ('hh_mo', 'hh_eq', 'dur_h', 'dias'):
                    if abs(R[cid][campo] - atual[cid][campo]) > 0.05:
                        falhas.append(f'{cid} ({atual[cid]["nome"]}): {campo} {R[cid][campo]} → {atual[cid][campo]}')
        else:
            avisos.append('sem testes/referencia.json: rode com --atualizar-referencia')
        # 5. tela Composições
        await pg.evaluate("()=>{sel=S.comps.find(c=>c.id==='cant')?'cant':S.comps[0].id;setTab('comp')}"); await pg.wait_for_timeout(150)
        ui = await pg.evaluate("""()=>({itens:document.querySelectorAll('.list .it').length,comps:S.comps.length,busca:!!document.querySelector('input.lbusca'),
            formula:[...document.querySelectorAll('table.acts thead th')].some(e=>e.textContent==='Fórmula'),
            copiar:!!document.querySelector('.tbl-bar .table-copy-btn'),titulo:!!document.querySelector('input.ctitle'),faixa:document.querySelectorAll('.cstat>div').length})""")
        if ui['itens'] != ui['comps']: falhas.append(f'lista lateral com {ui["itens"]} itens para {ui["comps"]} composições')
        for k, msg in (('busca', 'sem campo de busca'), ('formula', 'tabela sem a coluna Fórmula'), ('copiar', 'Copiar tabela fora da barra'), ('titulo', 'sem título da composição')):
            if not ui[k]: falhas.append('tela Composições: ' + msg)
        if ui['faixa'] != 3: falhas.append('tela Composições: faixa de indicadores com %d itens' % ui['faixa'])
        # 4. celular
        await pg.set_viewport_size({'width': 390, 'height': 844})
        for aba in ABAS:
            await pg.evaluate(f"()=>setTab('{aba}')"); await pg.wait_for_timeout(120)
            w = await pg.evaluate('()=>document.documentElement.scrollWidth')
            if w > 391: falhas.append(f'celular: aba {aba} com rolagem lateral ({w} px)')
        # projeto TESTE
        if teste_json:
            txt = await pg.evaluate("""(ord)=>{const d=migrate(defaults());const m=new Map(d.comps.map(c=>[c.id,c]));
              d.comps=ord.map(id=>{const c=m.get(id);c.usar=false;c.pred='';c.lag=0;c.preds=[];return c});d.projectName='TESTE';return JSON.stringify(d,null,1)}""", CIVIS)
            Path(teste_json).write_text(txt, encoding='utf-8'); print(f'projeto TESTE gravado: {teste_json}')
        falhas += erros
        await b.close()
    for a in avisos: print('AVISO  ', a)
    for f in falhas: print('FALHA  ', f)
    print('RESULTADO:', 'OK' if not falhas else f'{len(falhas)} falha(s)')
    return 1 if falhas else 0


if __name__ == '__main__':
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass
    args = sys.argv[1:]
    if not args or args[0].startswith('-'):
        print(__doc__); sys.exit(2)
    tj = args[args.index('--teste-json') + 1] if '--teste-json' in args else None
    sys.exit(asyncio.run(principal(args[0], '--atualizar-referencia' in args, tj)))
