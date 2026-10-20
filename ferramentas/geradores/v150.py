#!/usr/bin/env python3
"""Gera a v1.5.0 a partir da v1.4.0:
 1) barra verde original + logo Volga em branco;
 2) mudanças do Arthur publicadas no site (base de recursos, impacto, observações editáveis, administradores);
 3) base embutida = base v22 da nuvem + CIV-0128, com a CIV-0128 valendo no app enquanto não estiver na nuvem;
 4) composições padrão substituídas pelas revisadas (Serviços Preliminares, Fundações, Malha, Infra e Estruturas Auxiliares).
Uso: python3 v150.py v1.4.0-ui.html v1.5.0.html
"""
import sys, json, re, copy
src, dst = sys.argv[1], sys.argv[2]
COMP = '/tmp/claude-0/-home-claude/dac5aa45-9aec-505d-be91-ce54ee35c5a1/scratchpad/comp/'
t = open(src, encoding='utf-8').read()

def rep(old, new, count=1):
    global t
    n = t.count(old)
    assert n == count, (n, old[:90])
    t = t.replace(old, new)

# ---------------------------------------------------------------- 1) barra verde + logo branco
rep("header{background:#fff;color:var(--tx);border-bottom:3px solid #2a451d;box-shadow:0 1px 0 var(--bd)}",
    "header{background:var(--g1);color:#fff;border-bottom:3px solid var(--g3)}\n"
    "header .logo,header .logo-sym{filter:brightness(0) invert(1)}")
rep("header h1.app{font-size:15px;font-weight:600;color:#003437;margin:0;padding-left:12px;border-left:1px solid var(--bd);",
    "header h1.app{font-size:15px;font-weight:600;color:#fff;margin:0;padding-left:12px;border-left:1px solid rgba(255,255,255,.22);")
rep(".proj{border-left:1px solid var(--bd)}.proj-l{color:var(--gr)}#projname{color:#003437}\n",
    ".proj{border-left:1px solid rgba(255,255,255,.22)}\n")
rep("header button{background:#fff;color:var(--tx);border:1px solid var(--bd)}header button:hover{background:var(--gl)}\n", "")
rep("header button.lnk{color:var(--g2);border-color:transparent;background:none;font-weight:600}header button.lnk:hover{background:var(--gl)}",
    "header button.lnk{font-weight:600}")
rep(".menu>summary{background:#fff;color:var(--tx);border:1px solid var(--bd)}.menu[open]>summary,.menu>summary:hover{background:var(--gl)}\n.menu>summary:focus-visible{outline:2px solid var(--g3)}",
    ".menu[open]>summary,.menu>summary:hover{background:rgba(255,255,255,.18)}")
rep("#cloudstatus{color:var(--gr);font-size:12.5px}", "#cloudstatus{font-size:12.5px}")
rep("@media (max-width:1100px){#cloudstatus{font-size:0}#cloudstatus::before{background:var(--g3)}#cloudstatus.err::before{background:var(--red)}}",
    "@media (max-width:1100px){#cloudstatus{font-size:0}}")
rep("@media (max-width:520px){header h1.app{display:none}.proj{border-left:1px solid var(--bd);padding-left:8px}}",
    "@media (max-width:520px){header h1.app{display:none}.proj{border-left:1px solid rgba(255,255,255,.22);padding-left:8px}}")

# ---------------------------------------------------------------- 2) mudanças do Arthur
# 2a. faixa do modo administrador
rep("body.readonly-project #readonly-banner{display:block}",
    "body.readonly-project #readonly-banner{display:block}\n"
    "#admin-banner{display:none;background:#e7f0e2;border-bottom:1px solid #c3d6ba;padding:9px 24px;color:#1f3a16}\n"
    "body.admin-other #admin-banner{display:block}\n"
    "/* v1.5.0 — base de recursos, observações editáveis, atividades só no app */\n"
    "table.rtab{min-width:520px}table.rtab td.n,table.rtab th.n{text-align:right}table.rtab td.act{white-space:nowrap;text-align:right}\n"
    ".soapp{display:inline-block;margin-left:6px;padding:1px 7px;border-radius:999px;background:#fff1d6;color:#7a4b00;font-size:11px;font-weight:600;white-space:nowrap}\n"
    ".notas{margin:10px 0 6px}.notas .nl{display:flex;gap:6px;align-items:center;margin-bottom:6px}.notas .nl input{flex:1;min-width:0}\n"
    ".imp-l{margin:6px 0 0 20px;padding:0}.imp-g{margin-bottom:10px}")
rep('<div id="readonly-banner">Projeto de outro funcionário — somente leitura. Para editar, use <b>Todos os projetos → Duplicar</b>.</div>',
    '<div id="readonly-banner">Projeto de outro funcionário — somente leitura. Para editar, use <b>Todos os projetos → Duplicar</b>.</div>'
    '<div id="admin-banner">Modo administrador — você está editando o projeto de outro funcionário. As alterações são salvas no projeto original.</div>')

# 2b. recursos vindos da nuvem
rep("const REC=DB.recursos.map(r=>r[0]),TIPO=Object.fromEntries(DB.recursos);",
    "let REC,TIPO,globalRecursos=[];function applyRecursos(l){globalRecursos=(l||DB.recursos).map(x=>[x[0],x[1]]);REC=globalRecursos.map(r=>r[0]);TIPO=Object.fromEntries(globalRecursos)}applyRecursos(DB.recursos);")

# 2c. abas
rep("const T=[['comp','Composições'],['cron','Cronograma'],['hist','Histograma'],['base','Base de atividades'],['library','Base de composições'],['par','Parâmetros']];",
    "const T=[['comp','Composições'],['cron','Cronograma'],['hist','Histograma'],['base','Base de atividades'],['recursos','Base de recursos'],['library','Base de composições'],['par','Parâmetros']];")
rep("({comp:rComp,cron:rCron,hist:rHist,base:rBase,library:rLibrary,par:rPar})[tab]();",
    "({comp:rComp,cron:rCron,hist:rHist,base:rBase,recursos:rRecursos,library:rLibrary,par:rPar})[tab]();")
rep("if(cloudReady&&!currentProjectId&&!['base','library'].includes(tab)){",
    "if(cloudReady&&!currentProjectId&&!['base','recursos','library'].includes(tab)){")
rep("<p class=\"hint\">Base de atividades e Base de composições podem ser consultadas sem projeto aberto.</p>",
    "<p class=\"hint\">Base de atividades, Base de recursos e Base de composições podem ser consultadas sem projeto aberto.</p>")
rep("function applyReadOnly(){if(!document.body.classList.contains('readonly-project')||['base','library'].includes(tab))return;",
    "function applyReadOnly(){if(!document.body.classList.contains('readonly-project')||['base','recursos','library'].includes(tab))return;")

# 2d. administradores e edição de projeto de outro funcionário
rep("const canEditProject=()=>!currentProjectId||currentOwnerId===auth.currentUser?.uid;",
    "const canEditProject=()=>!currentProjectId||currentOwnerId===auth.currentUser?.uid||isAdmin();")
rep("const isAdmin=()=>allowed(auth.currentUser)&&auth.currentUser.email.toLowerCase()==='arthur.araujo@volga.com.br';",
    "const ADMINS=['arthur.araujo@volga.com.br','osvaldo.junior@volga.com.br'];\n"
    "const isAdmin=()=>allowed(auth.currentUser)&&ADMINS.includes(auth.currentUser.email.toLowerCase());")
rep("function setReadOnly(){document.body.classList.toggle('readonly-project',!!currentProjectId&&!canEditProject());}",
    "function setReadOnly(){document.body.classList.toggle('readonly-project',!!currentProjectId&&!canEditProject());document.body.classList.toggle('admin-other',!!currentProjectId&&currentOwnerId!==auth.currentUser?.uid&&isAdmin());}")
rep("try{await projectsRef().doc(currentProjectId).set({nome:S.projectName||'Projeto sem nome'",
    "try{await projectRef(currentOwnerId||auth.currentUser.uid,currentProjectId).set({nome:S.projectName||'Projeto sem nome'")
rep("'+(own?'Abrir':'Visualizar')+'", "'+(own||isAdmin()?'Abrir':'Visualizar')+'")
rep("<p class=\"hint\">Todos podem visualizar e duplicar. Somente o proprietário pode editar o original.</p>",
    "<p class=\"hint\">Todos podem visualizar e duplicar. Somente o proprietário e os administradores podem editar o original.</p>")

# 2e. base global guarda também os recursos
rep("await r.set({activities:baseFrom(),version:1,",
    "await r.set({activities:baseFrom(),recursos:DB.recursos,version:1,")
rep("const final=await r.get();globalBase=final.data().activities||[];lastGlobalCommitted=clone(globalBase);",
    "const final=await r.get();globalBase=final.data().activities||[];applyRecursos(final.data().recursos);lastGlobalCommitted=clone(globalBase);")
rep("globalUnsub=r.onSnapshot(x=>{if(x.exists){const vAnt=globalVersion;globalBase=x.data().activities||[];lastGlobalCommitted",
    "globalUnsub=r.onSnapshot(x=>{if(x.exists){const vAnt=globalVersion;globalBase=x.data().activities||[];applyRecursos(x.data().recursos);lastGlobalCommitted")

# 2f. impacto ao excluir/alterar atividade (Arthur), com as janelas do app
IMPACTO = r"""
// ---------- Impacto de uma alteração na base (projetos de todos e biblioteca)
async function impactoAtividade(cod){
 const grupos={};
 const add=(origem,comp)=>{(grupos[origem]=grupos[origem]||new Set()).add(comp)};
 const q=await db.collectionGroup('projetos').get();
 q.docs.filter(d=>d.ref.parent.parent&&d.ref.parent.parent.parent.id==='usuarios'&&d.id!==currentProjectId).forEach(d=>{try{const nome=d.data().nome||'Projeto sem nome';(projectData(d.data()).comps||[]).forEach(c=>{if(usedCodes(c).has(cod))add('Projeto: '+nome,c.nome||'Composição sem nome')})}catch(e){}});
 const lib=await libraryRef().get();
 lib.docs.forEach(d=>{try{const c=JSON.parse(d.data().compJson);if(usedCodes(c).has(cod))add('Biblioteca: '+(d.data().nome||'composição'),c.nome||'Composição sem nome')}catch(e){}});
 if(S&&S.comps)S.comps.forEach(c=>{if(usedCodes(c).has(cod))add('Projeto aberto: '+(S.projectName||'Projeto'),c.nome||'Composição sem nome')});
 return grupos}
function textoImpacto(g){return Object.keys(g).map(o=>o+'\n'+[...g[o]].map(c=>'   - '+c).join('\n')).join('\n')}
function diffAtividade(a,b){const l=[];
 if(a.cod!==b.cod)l.push('Código: '+a.cod+' → '+b.cod);
 if(a.serv!==b.serv)l.push('Serviço: "'+a.serv+'" → "'+b.serv+'"');
 if(a.un!==b.un)l.push('Unidade: "'+a.un+'" → "'+b.un+'"');
 const ks=[...new Set([...Object.keys(a.r||{}),...Object.keys(b.r||{})])];
 ks.forEach(k=>{const x=(a.r||{})[k],y=(b.r||{})[k];
  if(x==null)l.push('Recurso incluído: '+k+' ('+y+' h por unidade)');
  else if(y==null)l.push('Recurso removido: '+k);
  else if(x!==y)l.push(k+': '+x+' → '+y+' h por unidade')});
 return l.length?'<ul class="imp-l">'+l.map(t=>'<li>'+esc(t)+'</li>').join('')+'</ul>':'<p style="margin:0">Nenhuma alteração de dados foi identificada.</p>'}
function respImpacto(v){closeDialog();const r=window.__impactoRes;window.__impactoRes=null;if(r)r(v)}
function confirmarImpacto(titulo,botao,cod,nome,detalhe,grupos){
 const origens=Object.keys(grupos);
 const nComp=origens.reduce((n,o)=>n+grupos[o].size,0);
 const lista=origens.length
  ?origens.map(o=>'<div class="imp-g"><b>'+esc(o)+'</b><ul class="imp-l">'+[...grupos[o]].map(c=>'<li>'+esc(c)+'</li>').join('')+'</ul></div>').join('')
  :'<p style="margin:0">Nenhum projeto ou composição usa esta atividade.</p>';
 const resumo=origens.length?'<p style="margin:4px 0 8px">'+origens.length+' projeto(s) ou biblioteca(s) e '+nComp+' composição(ões) serão afetados.</p>':'';
 return new Promise(res=>{window.__impactoRes=res;dialog(
  '<div>'
  +'<div style="display:flex;justify-content:space-between;align-items:center;gap:12px"><h2 id="dlgtitle">'+esc(titulo)+'</h2><button onclick="respImpacto(false)">Fechar</button></div>'
  +'<p style="margin:14px 0 4px"><b>Atividade:</b> '+esc(cod)+' — '+esc(nome)+'</p>'
  +'<div style="margin:14px 0"><b>O que será feito</b><div style="margin-top:4px">'+detalhe+'</div></div>'
  +'<div style="margin:14px 0"><b>Impacto nos projetos</b>'+resumo+lista+'</div>'
  +'<div style="display:flex;gap:8px;justify-content:flex-end;margin-top:18px"><button onclick="respImpacto(false)">Cancelar</button><button class="d" onclick="respImpacto(true)">'+esc(botao)+'</button></div>'
  +'</div>')})}
function aviso(title,msg){return uiDialog({title,msg,buttons:[{v:true,l:'Entendi',cls:'p',primary:true}]})}
"""
rep("let editIdx=null;\nasync function delAct(i){", IMPACTO + "let editIdx=null;\nasync function delAct(i){")
rep(""" try{const uso=await usoAtividades(new Set([a.cod]));
  if(uso[a.cod])return alert('Não é possível excluir '+a.cod+': a atividade é usada em '+[...uso[a.cod]].join(', ')+'.\\n\\nRemova a atividade dessas composições antes de excluir.');
  if(!await ask(a.cod+' — '+a.serv+'\\n\\nA atividade sai da base global para todos os usuários.',{title:'Excluir atividade da base',ok:'Excluir',danger:true}))return;""",
    """ try{const grupos=await impactoAtividade(a.cod);
  const ok=await confirmarImpacto('Excluir atividade','Excluir atividade',a.cod,a.serv,'<p style="margin:0">A atividade será removida da base global. Nas composições listadas abaixo, ela deixará de ser considerada no cálculo até ser substituída ou removida manualmente.</p>',grupos);
  if(!ok)return;""")
rep("""  if(editIdx!=null){const old=editIdx;
   if(old!==cod){const uso=await usoAtividades(new Set([old]));if(uso[old])return alert('Não é possível alterar o código de '+old+': a atividade é usada em '+[...uso[old]].join(', ')+'.\\nUse Duplicar para criar uma atividade com o novo código.')}
   globalBase[pos]=o}""",
    """  if(editIdx!=null){const old=globalBase[pos];
   const grupos=await impactoAtividade(old.cod);
   if(old.cod!==cod&&Object.keys(grupos).length)return aviso('Código não pode ser alterado','A atividade '+old.cod+' já é usada em:\\n'+textoImpacto(grupos)+'\\n\\nUse Duplicar para criar uma atividade com o novo código.');
   const ok=await confirmarImpacto('Salvar alterações na atividade','Salvar alterações',cod,o.serv,diffAtividade(old,o),grupos);
   if(!ok)return;
   globalBase[pos]=o}""")

# 2g. Base de recursos (Arthur), no visual da Base de atividades
RECURSOS = r"""
// ---------- Base de recursos (nome e tipo de cada recurso; fica na base global, junto das atividades)
const usoRecurso=n=>globalBase.filter(a=>a.r&&n in a.r);
const lstAtv=l=>l.slice(0,15).map(a=>'   - '+a.cod+' — '+a.serv).join('\n')+(l.length>15?'\n   … e mais '+(l.length-15)+' atividade(s)':'');
async function commitRecursos(action,nome,newRec,newBase){
 if(!isAdmin())return alert("Acesso restrito ao administrador.");
 if(!cloudReady)return;
 const oldVersion=globalVersion,oldBase=clone(lastGlobalCommitted),oldRec=clone(globalRecursos);
 try{
  await db.runTransaction(async tx=>{
   const ref=baseRef(),snap=await tx.get(ref);
   if(!snap.exists||snap.data().version!==oldVersion)throw Error('A base global mudou em outra sessão. Reabra o projeto e tente novamente.');
   tx.update(ref,{activities:newBase,recursos:newRec,version:oldVersion+1,updatedAt:firebase.firestore.FieldValue.serverTimestamp(),updatedBy:auth.currentUser.uid});
   const hist=ref.collection('historico').doc();tx.set(hist,{action,cod:nome,by:auth.currentUser.uid,at:firebase.firestore.FieldValue.serverTimestamp(),previous:oldBase,previousRecursos:oldRec,version:oldVersion+1});
  });
  globalBase=clone(newBase);lastGlobalCommitted=clone(newBase);applyRecursos(newRec);globalVersion=oldVersion+1;render();
 }catch(e){globalBase=oldBase;applyRecursos(oldRec);render();reportError(e)}
}
function rRecursos(){const adm=isAdmin();
 $('#main').innerHTML=`<div id="modal"></div><div class="card"><h3>Base de recursos</h3><p class="desc">Recursos que aparecem nas atividades, na equipe das composições e no histograma. ${adm?'Renomear um recurso atualiza as atividades da base que o usam; excluir remove o recurso dessas atividades.':'Somente o administrador altera esta base.'}</p>
 <div class="row">${adm?'<button class="p" onclick="recForm(null)">+ Novo recurso</button>':''}<span class="hint">${globalRecursos.length} recursos</span></div>
 <div class="scroll" style="max-height:620px"><table class="rtab"><thead><tr><th>Recurso</th><th>Tipo</th><th class="n">Atividades que usam</th>${adm?'<th><span class="sr">Ações</span></th>':''}</tr></thead><tbody>${globalRecursos.map((r,i)=>`<tr><td>${esc(r[0])}</td><td>${esc(r[1])}</td><td class="n">${usoRecurso(r[0]).length}</td>${adm?`<td class="act"><button class="i" title="Editar" aria-label="Editar ${esc(r[0])}" onclick="recForm(${i})">✎</button><button class="i d" title="Excluir" aria-label="Excluir ${esc(r[0])}" onclick="recDel(${i})">✕</button></td>`:''}</tr>`).join('')}</tbody></table></div></div>`}
function recForm(i){if(!isAdmin())return alert("Acesso restrito ao administrador.");
 const r=i==null?['','Mão de obra']:globalRecursos[i];const tipos=[...new Set(globalRecursos.map(x=>x[1]))];
 $('#modal').innerHTML=`<div class="card" style="border-color:var(--g3)"><h3>${i==null?'Novo recurso':'Editar recurso'}</h3><div class="row"><label>Nome<input id="rc_n" value="${esc(r[0])}" style="width:260px"></label><label>Tipo<input id="rc_t" list="rc_tl" value="${esc(r[1])}" style="width:200px"><datalist id="rc_tl">${tipos.map(t=>`<option value="${esc(t)}">`).join('')}</datalist></label></div><div class="row"><button class="p" onclick="recSave(${i==null?'null':i})">Salvar</button><button onclick="$('#modal').innerHTML=''">Cancelar</button></div></div>`;
 $('#modal').scrollIntoView({behavior:'smooth',block:'start'})}
async function recSave(i){if(!isAdmin())return alert("Acesso restrito ao administrador.");
 const n=$('#rc_n').value.trim(),t=$('#rc_t').value.trim();
 if(!n||!t)return alert('Informe o nome e o tipo do recurso.');
 const dup=globalRecursos.findIndex(r=>r[0].toLowerCase()===n.toLowerCase());
 if(dup>=0&&dup!==i)return alert('Já existe um recurso com esse nome.');
 const rec=clone(globalRecursos);
 if(i==null){rec.push([n,t]);return commitRecursos('recurso-incluir',n,rec,clone(globalBase))}
 const old=globalRecursos[i];
 if(old[0]===n&&old[1]===t){$('#modal').innerHTML='';return}
 let base=clone(globalBase);
 if(old[0]!==n){const usos=usoRecurso(old[0]);
  if(!await ask((usos.length?'Serão atualizadas '+usos.length+' atividade(s) da base:\n'+lstAtv(usos):'Nenhuma atividade da base usa este recurso.')+'\n\nEquipes já definidas nas composições com o nome antigo precisarão ser redefinidas.',{title:'Renomear "'+old[0]+'" para "'+n+'"?',ok:'Renomear'}))return;
  base=base.map(a=>{if(a.r&&old[0] in a.r)a.r=Object.fromEntries(Object.entries(a.r).map(([k,v])=>[k===old[0]?n:k,v]));return a})}
 rec[i]=[n,t];commitRecursos('recurso-editar',old[0]+' → '+n,rec,base)}
async function recDel(i){if(!isAdmin())return alert("Acesso restrito ao administrador.");
 const r=globalRecursos[i],usos=usoRecurso(r[0]);
 const vazias=usos.filter(a=>Object.keys(a.r).length===1);
 if(vazias.length)return aviso('Não é possível excluir "'+r[0]+'"','As atividades abaixo ficariam sem nenhum recurso:\n'+lstAtv(vazias)+'\n\nEdite essas atividades antes de excluir o recurso.');
 if(!await ask((usos.length?'Ele será removido de '+usos.length+' atividade(s) da base:\n'+lstAtv(usos):'Nenhuma atividade da base usa este recurso.')+'\n\nEquipes já definidas nas composições para este recurso deixam de existir.',{title:'Excluir o recurso "'+r[0]+'" ('+r[1]+')?',ok:'Excluir',danger:true}))return;
 const base=clone(globalBase).map(a=>{if(a.r&&r[0] in a.r)delete a.r[r[0]];return a});
 commitRecursos('recurso-excluir',r[0],globalRecursos.filter((_,j)=>j!==i).map(x=>x.slice()),base)}
"""
rep("function newAct(){actForm(null)}", "function newAct(){actForm(null)}" + RECURSOS)

# 2h. observações editáveis na composição (Arthur)
rep("""${(c.notas||[]).map(n=>`<div class="hint">• ${esc(n)}</div>`).join('')}""",
    """<div class="notas"><h4 style="margin:0 0 6px;font-size:13px">Observações</h4>${(c.notas||[]).map((n,i)=>`<div class="nl"><span class="hint">•</span><input class="nota-in" value="${esc(n)}" placeholder="Digite a observação" aria-label="Observação ${i+1}" onchange="setNota(${i},this.value)"><button class="d i" title="Excluir observação" aria-label="Excluir observação" onclick="rmNota(${i})">×</button></div>`).join('')||'<div class="hint" style="margin-bottom:6px">Nenhuma observação.</div>'}<button onclick="addNota()">+ Observação</button></div>""")
rep("function cur(){return S.comps.find(c=>c.id===sel)}",
    "function cur(){return S.comps.find(c=>c.id===sel)}\n"
    "function setNota(i,v){const c=cur();c.notas=c.notas||[];v=v.trim();if(!v)c.notas.splice(i,1);else c.notas[i]=v;render()}\n"
    "function rmNota(i){const c=cur();if(!c.notas||c.notas[i]===undefined)return;c.notas.splice(i,1);render()}\n"
    "function addNota(){const c=cur();c.notas=c.notas||[];c.notas.push('');render();const l=document.querySelectorAll('.nota-in');if(l.length)l[l.length-1].focus()}")

# 2i. cálculos intermediários recolhidos em "Premissas da composição" (fechado por padrão; abre sozinho se houver erro)
rep("""${(c.vars||[]).length?`<div class="row">${c.vars.map((w,i)=>`<label>Cálculo intermediário [${esc(w.k)}]<input""",
    """${(c.vars||[]).length?`<details class="prem" ${premOpen||Object.values(L.varErr||{}).some(Boolean)?'open':''} ontoggle="premOpen=this.open"><summary>Premissas da composição (${c.vars.length})<span class="hint"> — medidas padrão e contas internas; não vêm do arranjo</span></summary><div class="row">${c.vars.map((w,i)=>`<label>[${esc(w.k)}]<input""")
rep("""<span class="hint" style="color:var(--red)">${esc(L.varErr[i])}</span>`:''}</label>`).join('')}</div>`:''}""",
    """<span class="hint" style="color:var(--red)">${esc(L.varErr[i])}</span>`:''}</label>`).join('')}</div></details>`:''}""")
rep("let pickOpen=false;", "let pickOpen=false;\nlet premOpen=false;")
rep(".notas{margin:10px 0 6px}",
    ".prem{margin:8px 0 2px}.prem>summary{cursor:pointer;font-size:13px;font-weight:600;color:var(--g1);padding:4px 0;width:max-content;max-width:100%}.prem>summary .hint{font-weight:400}.prem>.row{margin-top:6px}\n.notas{margin:10px 0 6px}")

# ---------------------------------------------------------------- 3) base embutida = v22 + CIV-0128
L = t.split('\n')
idx = [i for i, l in enumerate(L) if l.startswith('const DB=')][0]
D = json.loads(L[idx][len('const DB='):].rstrip(';'))
def norm(r): return {k: (int(v) if float(v).is_integer() else v) for k, v in r.items()}
V22 = {
 'CIV-0002': ["CIV-0002","CIVIL","SERVIÇOS PRELIMINARES","TERRAPLANAGEM-CORTE","m³","https://planningengineer.net/earth-moving-equipment-function","FRONT-END LOADERS -> Mix planting soil, including loam, manure, and peat, by skid steer loader at a productivity of 27.7 m3 / hour.",{"Escavadeira":0.05}],
 'CIV-0005': ["CIV-0005","CIVIL","ALVENARIA","ELEVAÇÃO DE ALVENARIA","m²","SINAPI 103340","ALVENARIA DE VEDAÇÃO DE BLOCOS VAZADOS DE CONCRETO APARENTE DE 19X19X39 CM (ESPESSURA 19 CM) E ARGAMASSA DE ASSENTAMENTO COM PREPARO EM BETO",{"Pedreiro":2,"Op. Betoneira":0.061204,"Aux. Pedreiro":0.735}],
 'CIV-0010': ["CIV-0010","CIVIL","DRENAGEM","FABRICAÇÃO, MONTAGEM E DESMONTAGEM DE FORMA PARA RADIER, PISO DE CONCRETO OU LAJE SOBRE SOLO, EM COMPENSADO RESINADO","m²","SINAPI 107283","",{"Aux. Carpinteiro":0.51,"Carpinteiro":2.8}],
 'CIV-0023': ["CIV-0023","CIVIL","SUPERESTRUTURA","ELEVAÇÃO DE ALVENARIA","m²","SINAPI 103318","CALVENARIA DE VEDAÇÃO DE BLOCOS VAZADOS DE CONCRETO DE 14X19X39 CM (ESPESSURA 14 CM) E ARGAMASSA DE ASSENTAMENTO COM PREPARO EM BETONEIRA.",{"Aux. Pedreiro":0.5,"Pedreiro":1,"Op. Betoneira":0.048772}],
}
for b in D['base']:
    if b[0] in V22: b[:] = V22[b[0]]
    if b[0] == 'CIV-0063': b[7] = {"Pedreiro":0.587,"Vibrador por Imersão":0.3,"Aux. Pedreiro":0.881}
    if b[0] == 'CIV-0077': b[7] = {"Vibrador por Imersão":0.01,"Aux. Pedreiro":0.393843,"Pedreiro":0.393843}
    b[7] = norm(b[7])
NEWACT = ['CIV-0128','CIVIL','SERVIÇOS PRELIMINARES','LOCAÇÃO DA OBRA COM TOPOGRAFIA E GABARITO DE MADEIRA','m²','ORSE 4177',
          'LOCAÇÃO DE CONSTRUÇÃO ACIMA DE 1000 M², INCLUSIVE EXECUÇÃO DE GABARITO DE MADEIRA (ORSE 4176 ENTRE 200 E 1000 M², MESMOS COEFICIENTES). SERVENTE LANÇADO COMO AUX. CARPINTEIRO.',
          {'Topógrafo':0.02,'Aux. Topógrafo':0.02,'Carpinteiro':0.04,'Aux. Carpinteiro':0.04}]
assert not any(b[0] == 'CIV-0128' for b in D['base'])
D['base'].append(NEWACT)
L[idx] = 'const DB=' + json.dumps(D, ensure_ascii=False) + ';'
t = '\n'.join(L)

rep("function baseAll(){return globalBase}",
    "// Atividades novas das composições padrão desta versão: valem no app enquanto o administrador não as inclui na base da nuvem.\n"
    "const ACT_NOVAS=['CIV-0128'];\n"
    "let _baRef=null,_baLen=-1,_baOut=[];\n"
    "function baseAll(){if(globalBase!==_baRef||globalBase.length!==_baLen){_baRef=globalBase;_baLen=globalBase.length;const tem=new Set(globalBase.map(a=>a.cod));\n"
    " const extra=baseFrom().filter(a=>ACT_NOVAS.includes(a.cod)&&!tem.has(a.cod)).map(a=>Object.assign(a,{soApp:true}));_baOut=extra.length?globalBase.concat(extra):globalBase}return _baOut}\n"
    "async function incluirNaBase(cod){if(!isAdmin())return alert('Acesso restrito ao administrador.');if(globalBase.some(a=>a.cod===cod))return alert(cod+' já está na base.');\n"
    " const a=baseFrom().find(x=>x.cod===cod);if(!a)return;\n"
    " if(!await ask(a.cod+' — '+a.serv+' ('+a.un+')\\n'+Object.entries(a.r).map(([k,v])=>k+': '+v+' h/'+a.un).join('\\n')+'\\nFonte: '+a.fonte+'\\n\\nA atividade passa a fazer parte da base global, para todos os usuários.',{title:'Incluir atividade na base da nuvem',ok:'Incluir na base'}))return;\n"
    " globalBase.push(a);commitGlobalBase('incluir',cod)}")
# linha da atividade só no app: etiqueta e botão de inclusão (no lugar de editar/duplicar/excluir)
rep("""<td class="cod">${esc(a.cod)}${up.has(a.cod)?'<span class="inuse" title="Usada em composição do projeto aberto">no projeto</span>':''}</td>""",
    """<td class="cod">${esc(a.cod)}${up.has(a.cod)?'<span class="inuse" title="Usada em composição do projeto aberto">no projeto</span>':''}${a.soApp?'<span class="soapp" title="Vem embutida no app para as composições padrão; ainda não está na base da nuvem">só no app</span>':''}</td>""")
rep("""${adm?`<td class="act"><button class="i" title="Editar" aria-label="Editar ${esc(a.cod)}" onclick="actForm(${i})">✎</button>""",
    """${adm&&a.soApp?`<td class="act"><button class="p" onclick="incluirNaBase(${esc(JSON.stringify(a.cod))})">Incluir na base</button></td>`:adm?`<td class="act"><button class="i" title="Editar" aria-label="Editar ${esc(a.cod)}" onclick="actForm(${i})">✎</button>""")

# ---------------------------------------------------------------- 4) composições padrão revisadas
def load(f): return {c['id']: c for c in json.load(open(COMP + f, encoding='utf-8'))['comps']}
SP, AR, FU, IN = load('servicos_preliminares_revisados.json'), load('composicoes_arthur_revisadas.json'), load('fundacoes_revisadas.json'), load('infra_base_comps4.json')

def setact(c, cod, old_f, new):
    """troca a linha (cod, old_f) pela lista new [(cod,f),...]"""
    for i, a in enumerate(c['acts']):
        if a['cod'] == cod and a['f'] == old_f:
            c['acts'][i:i+1] = [{'cod': k, 'f': f} for k, f in new]
            return
    raise KeyError((c['id'], cod, old_f))

# Na base v22 a CIV-0010 passou a ser fôrma de radier em m². O concreto vai para a CIV-0077 (m³) e a fôrma fica na CIV-0010 (m²).
IN = copy.deepcopy(IN)
setact(IN['canal2'], 'CIV-0010', 'n*be*0.08', [('CIV-0077', 'n*be*0.08')])
IN['canal2']['notas'].append('Base v22: o fundo de 8 cm passa a ser concretado pela CIV-0077 (m³). A CIV-0010 agora é fôrma em m² e não entra: o fundo é lançado contra o solo da vala, e a cinta e a tampa já incluem fôrma.')
setact(IN['caixa2'], 'CIV-0010', '0.41*(n1*ext1+n2*ext2+n3*ext2*fr)', [('CIV-0077', '0.41*(n1*ext1+n2*ext2+n3*ext2*fr)'), ('CIV-0010', '1.55*(n1*ext1+(n2+n3)*ext2)')])
IN['caixa2']['notas'].append('Base v22: concreto do fundo e da cinta pela CIV-0077 (m³) e fôrma pela CIV-0010 (m²), com 1,55 m² de fôrma por m² de área externa (1,2 m² na caixa 60 × 60 da lista de materiais).')
for k in ('ccom2', 'cmed2'):
    setact(IN[k], 'CIV-0010', 'qtd*A*0.10', [('CIV-0077', 'qtd*A*0.10'), ('CIV-0010', 'qtd*P*0.10')])
    IN[k]['notas'].append('Base v22: radier de 10 cm concretado pela CIV-0077 (m³); a CIV-0010 (fôrma em m²) fica só na borda do radier (perímetro × 0,10 m).')
setact(IN['ext2'], 'CIV-0010', 'n*0.69', [('CIV-0077', 'n*0.69'), ('CIV-0010', 'n*4.28')])
IN['ext2']['notas'].append('Base v22: concreto pela CIV-0077 (0,69 m³ por abrigo) e fôrma pela CIV-0010 (4,28 m² por abrigo), ambos da lista do VO778-CV-229.')

SP = copy.deepcopy(SP); SP['cant']['inputs'][0]['u'] = 'und'
IN['ccom2']['inputs'][0]['l'] = 'Quantidade de casas'
# Itens padronizados: só a quantidade vem do arranjo; as medidas viram premissas internas (vars).
FU = copy.deepcopy(FU)
def so_quantidade(c, qk, ql, mover, nota, wrap=False, remover_acts=(), remover_termos=()):
    """mover: entradas que viram premissas (valor fixo). wrap: multiplica toda atividade pela nova entrada qk."""
    vals = {p['k']: p['v'] for p in c['inputs']}
    novas = [{'k': k, 'f': str(vals[k])} for k in mover]
    c['inputs'] = [p for p in c['inputs'] if p['k'] not in mover and p['k'] != qk]
    c['inputs'].insert(0, {'k': qk, 'l': ql, 'u': 'und', 'v': vals.get(qk, 1)})
    c['vars'] = novas + c.get('vars', [])
    acts = [a for a in c['acts'] if (a['cod'], a['f']) not in remover_acts]
    for a in acts:
        f = a['f']
        for termo in remover_termos: f = f.replace(termo, '')
        if wrap: f = qk if f in ('1', qk) else qk + '*(' + f + ')'
        a['f'] = f
    c['acts'] = acts
    c['notas'] = [nota] + c.get('notas', [])
so_quantidade(FU['trafoalv'], 'qtd', 'Quantidade de bases', ['C', 'L'],
              'Entrada única: quantidade de bases. Bacia padrão da SE Milhão (VO778-CV-207): 6,55 × 5,5 m externos, fixada em C e L nas premissas.')
so_quantidade(FU['trafocon'], 'qtd', 'Quantidade de bases', ['C', 'L'],
              'Entrada única: quantidade de bases. Bacia de 6,55 × 5,5 m externos, a mesma da base em alvenaria da SE Milhão (VO778-CV-207), fixada em C e L nas premissas.')
so_quantidade(FU['eletro2'], 'qtd', 'Quantidade de bases', ['C', 'L', 'np'],
              'Entrada única: quantidade de bases. Eletrocentro padrão da SE Milhão (VO778-CV-215): 10,4 × 3,5 m em radier com canaletas, fixado em C e L nas premissas.',
              wrap=True, remover_termos=('+np*1.5*1.5*1.5', '+np*0.3', '+np*1'), remover_acts=(('CIV-0079', 'np*50'),))
FU['eletro2']['vars'] = [v for v in FU['eletro2']['vars'] if v['k'] != 'np']
for k in ('disj2', 'poste2', 'bspda2'):
    FU[k]['inputs'][0].update({'l': 'Quantidade de bases', 'u': 'und'})
so_quantidade(IN['cmed2'], 'qtd', 'Quantidade de casas', ['C', 'L', 'port', 'jan', 'cint'],
              'Entrada única: quantidade de casas. Casa de medição padrão: 3,35 × 3,35 m externos, 1 porta e 2 janelas, fixados nas premissas.',
              remover_acts=(('CIV-0067', 'qtd*cint*0.71*0.68'), ('CIV-0078', 'qtd*cint*2*0.54'), ('CIV-0014', 'qtd*cint*0.71*0.05')))
IN['cmed2']['vars'] = [v for v in IN['cmed2']['vars'] if v['k'] != 'cint']
def nota_troca(c, velho, novo):
    c['notas'] = [n.replace(velho, novo) for n in c['notas']]
    assert any(novo in n for n in c['notas']), (c['id'], velho)
nota_troca(FU['eletro2'], 'Pilares (np): quantidades do Arthur por pilar, sem projeto de referência.', 'Eletrocentro sobre pilotis não entra nesta composição.')
nota_troca(IN['cmed2'], 'com as quantidades ligadas às medidas externas (C × L) do arranjo.', 'com as quantidades ligadas às medidas externas (C × L), fixadas nas premissas.')
so_quantidade(IN['pcf2'], 'qtd', 'Quantidade de paredes', ['C', 'H'],
              'Entradas: quantidade de paredes e tipo. Parede padrão do VO778-CV-234: 5,95 m de comprimento e 4,8 m acima do solo (uma por transformador), fixada em C e H nas premissas.',
              wrap=True)

def clean_name(n): return re.sub(r'\s+—\s+revisada$', '', n)
def to_seed(c, sid):
    s = {'id': sid, 'nome': clean_name(c['nome']), 'disc': c.get('disc') or 'CIVIL',
         'params': [dict({'k': p['k'], 'l': p['l'], 'u': p.get('u', ''), 'd': p['v']}, **({'o': p['o']} if p.get('o') else {})) for p in c['inputs']],
         'vars': [[v['k'], v['f']] for v in c.get('vars', [])],
         'acts': [{'cod': a['cod'], 'q': a['f']} for a in c['acts']],
         'notas': c.get('notas', [])}
    if (c.get('crewDef') or 1) != 1: s['crewDef'] = c['crewDef']
    return s

si = [i for i, l in enumerate(t.split('\n')) if l.startswith('const SEED=')][0]
L = t.split('\n')
SEED = json.loads(L[si][len('const SEED='):].rstrip(';'))
byid = {s['id']: s for s in SEED}
REPL = {  # id do SEED -> composição revisada
 'malha': AR['malha2'], 'terra': SP['terra'], 'loc': SP['loc'], 'poste': FU['poste2'], 'bspda': FU['bspda2'],
 'cpm': IN['caixa2'], 'canc': IN['canal2'], 'ext': IN['ext2'], 'cmed': IN['cmed2'], 'pcf': IN['pcf2']}
NOVAS_ANTES = {'terra': [('cant', SP['cant']), ('limp', SP['limp'])],
               'cpm': [],
               'cmed': [('ccom', IN['ccom2'])]}
NOVAS_DEPOIS = {'bspda': [('trafocon', FU['trafocon']), ('trafoalv', FU['trafoalv']), ('eletro', FU['eletro2']), ('disj', FU['disj2'])],
                'canc': [('banco', IN['banco2'])]}
out = []
for s in SEED:
    for nid, c in NOVAS_ANTES.get(s['id'], []): out.append(to_seed(c, nid))
    out.append(to_seed(REPL[s['id']], s['id']) if s['id'] in REPL else s)
    for nid, c in NOVAS_DEPOIS.get(s['id'], []): out.append(to_seed(c, nid))
assert len({s['id'] for s in out}) == len(out)
L[si] = 'const SEED=' + json.dumps(out, ensure_ascii=False) + ';'
t = '\n'.join(L)
# equipe padrão vinda da composição (terraplanagem, limpeza, malha = 2)
rep("const comps=SEED.map(t=>({id:t.id,nome:t.nome,disc:t.disc,crewDef:1,crew:{}",
    "const comps=SEED.map(t=>({id:t.id,nome:t.nome,disc:t.disc,crewDef:t.crewDef||1,crew:{}")
rep("g('terra').usar=true;g('terra').crewDef=2;g('malha').usar=true;g('malha').crewDef=2;g('malha').pred='terra';",
    "g('terra').usar=true;g('malha').usar=true;g('malha').pred='terra';")

# ---------------------------------------------------------------- versão e novidades
rep("const APP_VERSION='1.4.0';", "const APP_VERSION='1.5.0';")
t = re.sub(r'<!-- Dimensionamento de Histograma · arquivo 1\.4\.0 · [^ ]+ ·', '<!-- Dimensionamento de Histograma · arquivo 1.5.0 · 19/10/2026 ·', t, count=1)
assert 'arquivo 1.5.0' in t
NOV = """ {v:'1.5.0',data:'19/10/2026',itens:[
  'Barra do topo de volta ao verde original, com o logo da Volga em branco.',
  'Entram neste arquivo as funções que o Arthur já tinha publicado: Base de recursos (nome e tipo de cada recurso, editável pelo administrador), aviso de quais projetos e composições são afetados antes de alterar ou excluir uma atividade, observações editáveis dentro da composição e administradores podendo editar projetos de outros funcionários.',
  'Composições padrão dos projetos novos revisadas para que as entradas venham só do arranjo: Canteiro de obras, Limpeza do terreno e Terraplanagem separadas, Locação e gabarito com topógrafo, Malha de aterramento, bases de poste, de barramento/SPDA, de transformador (bacia em concreto ou em alvenaria), de eletrocentro e de disjuntor, Canaleta, Caixas de passagem (3 tipos), Banco de dutos, Casa de comando, Casa de medição, Parede corta-fogo e Abrigo de extintor.',
  'Itens padronizados pedem só a quantidade: bases de transformador, eletrocentro, disjuntor, poste de equipamentos e barramento/SPDA, casa de medição e parede corta-fogo (esta também com o tipo). As medidas padrão ficam dentro da composição.',
  'Os cálculos intermediários das composições (medidas padrão e contas internas) ficam recolhidos em "Premissas da composição", abaixo dos dados de entrada. Abrem com um clique, ou sozinhos quando há erro numa fórmula.',
  'Nova atividade CIV-0128 (locação com topografia e gabarito, ORSE 4177): já vale nos cálculos e aparece na Base de atividades como "só no app" até o administrador incluí-la na base com o botão "Incluir na base".',
  'Projetos já existentes não mudam: as composições revisadas entram nos projetos novos ou podem ser importadas.'
 ]},
"""
rep("const NOVIDADES=[\n {v:'1.4.0',", "const NOVIDADES=[\n" + NOV + " {v:'1.4.0',")
open(dst, 'w', encoding='utf-8').write(t)
print('ok', len(t.encode()), 'SEED', len(out), [s['id'] for s in out])
