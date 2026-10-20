# Cria o repositório privado OsvaldoSantana/dimensionamento-de-histograma com o histórico de todas as versões
# (um commit e uma etiqueta por versão), envia ao GitHub e cria uma Release por versão com o index.html anexado.
# Ao final, a pasta "projeto" vira a cópia de trabalho do repositório.
#
# Uso (PowerShell, dentro da pasta "projeto"):
#   powershell -ExecutionPolicy Bypass -File .\ferramentas\criar-repositorio.ps1
#
# Pré-requisitos: git e gh instalados, "gh auth login" feito, git config user.name / user.email definidos.

$ErrorActionPreference = 'Stop'
$Repo   = 'OsvaldoSantana/dimensionamento-de-histograma'
$Raiz   = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)   # ...\Volga Arthur
$Proj   = Join-Path $Raiz 'projeto'
$Vers   = Join-Path $Raiz 'versoes'
$Tmp    = Join-Path $env:TEMP ('hist-repo-' + (Get-Date -Format 'yyyyMMddHHmmss'))
$Utf8   = New-Object System.Text.UTF8Encoding($false)

function Passo($t) { Write-Host "`n== $t" -ForegroundColor Cyan }
function G { & git @args; if ($LASTEXITCODE -ne 0) { throw "git $args falhou" } }
# No Windows PowerShell 5.1, saída de erro de programa externo redirecionada vira erro fatal com 'Stop';
# aqui ela só é descartada e vale o código de saída.
function Ok { $ErrorActionPreference = 'Continue'; $null = & $args[0] @($args | Select-Object -Skip 1) 2>&1; return ($LASTEXITCODE -eq 0) }

Passo 'Conferindo pré-requisitos'
foreach ($c in 'git', 'gh') { if (-not (Get-Command $c -ErrorAction SilentlyContinue)) { throw "$c não encontrado. Instale e abra um PowerShell novo." } }
if (-not (Ok gh auth status)) { throw 'Faça login primeiro: gh auth login' }
if (Test-Path (Join-Path $Proj '.git')) { throw 'A pasta projeto já é um repositório Git. Nada a fazer.' }
$Versoes = @(
  @{ k='v1.0.0'; t='chore: versão 1.0.0 — original recebido do Arthur, sem alterações' },
  @{ k='v1.1.0'; t='feat: versão 1.1.0 — segurança, desempenho, calendário, praticabilidade INMET e cronograma' },
  @{ k='v1.2.0'; t='feat: versão 1.2.0 — telas proporcionais e versão para celular' },
  @{ k='v1.3.0'; t='feat: versão 1.3.0 — identidade Volga, janelas do próprio app, tabelas e linha do tempo' },
  @{ k='v1.4.0'; t='feat: versão 1.4.0 — histograma, tabelas mensais, bases de atividades e composições' },
  @{ k='publicado-2026-10-19'; t='chore: site publicado pelo Arthur em 19/10/2026 (original + mudanças dele, base v22)' },
  @{ k='v1.5.0'; t='feat: versão 1.5.0 — junta as funções do Arthur à linha 1.4.0; composições revisadas' },
  @{ k='v1.5.1'; t='feat: versão 1.5.1 — copiar tabela e marcas de auditoria' },
  @{ k='v1.6.0'; t='feat: versão 1.6.0 — revisões de composições do Osvaldo (teste, só civil; não publicar)' },
  @{ k='v1.6.1'; t='fix: versão 1.6.1 — corrige a 1.6.0: todas as disciplinas, observações, coeficientes' },
  @{ k='v1.7.0'; t='feat: versão 1.7.0 — terraplanagem nova, parâmetros com nome, revisão da civil' },
  @{ k='v1.8.0'; t='feat: versão 1.8.0 — cores por disciplina, tabela de atividades, sem avisos' },
  @{ k='v1.9.0'; t='feat: versão 1.9.0 — título e indicadores em destaque; dados legíveis e verificação' }
)
foreach ($v in $Versoes) { $f = Join-Path $Vers "$($v.k)\index.html"; if (-not (Test-Path $f)) { throw "Falta $f" } }

function Commitar($v, $extra) {
  $f = Join-Path $Vers "$($v.k)\index.html"
  Copy-Item $f (Join-Path $Tmp 'index.html') -Force
  G add index.html
  $data = (Get-Item $f).LastWriteTime
  if ($v.k -eq 'v1.5.0') { $data = $data.AddSeconds(5) }   # depois do commit do site, que ela junta
  $env:GIT_AUTHOR_DATE = $data.ToString('yyyy-MM-ddTHH:mm:ssK'); $env:GIT_COMMITTER_DATE = $env:GIT_AUTHOR_DATE
  $msg = $v.t; if ($extra) { $msg += "`n`n$extra" }
  $mf = Join-Path $env:TEMP 'hist-msg.txt'; [IO.File]::WriteAllText($mf, $msg, $Utf8)
  G commit -q -F $mf
  G tag -a $v.k -m $v.t
  Remove-Item Env:GIT_AUTHOR_DATE, Env:GIT_COMMITTER_DATE
}

Passo "Montando o histórico em $Tmp"
New-Item -ItemType Directory $Tmp | Out-Null
Push-Location $Tmp
try {
  G init -q -b main
  G config core.autocrlf false
  Copy-Item (Join-Path $Proj '.gitattributes') $Tmp
  G add .gitattributes
  Commitar $Versoes[0] 'Arquivo como foi recebido do coordenador.'
  foreach ($i in 1..4) { Commitar $Versoes[$i] $null }
  G checkout -q -b site-arthur v1.0.0
  Commitar $Versoes[5] 'Cópia exata do index.html do site em 19/10/2026: Base de recursos, aviso de impacto, observações editáveis, administradores.'
  G checkout -q main
  G merge -q --no-ff --no-commit -s ours site-arthur
  Commitar $Versoes[6] 'Junção das duas linhas: a 1.4.0 recebe as funções que o Arthur publicou no site (ramo site-arthur).'
  foreach ($i in 7..12) { Commitar $Versoes[$i] $(if ($Versoes[$i].k -eq 'v1.6.0') { 'Feita fora desta linha pelo Osvaldo, importada como recebida.' }) }

  Passo 'Último commit: estrutura do projeto'
  # .github (GitHub Actions e modelo de PR)
  New-Item -ItemType Directory (Join-Path $Proj '.github\workflows') -Force | Out-Null
  $yml = @'
name: Testes

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  testes:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: testes/requisitos.txt
      - name: Instalar Playwright e Chromium
        run: |
          pip install -r testes/requisitos.txt
          python -m playwright install --with-deps chromium
      - name: Rodar os testes (abas, dados, referência de HH, celular)
        run: python testes/rodar.py index.html
'@
  $pr = @'
## Versão

<!-- X.Y.Z desta rodada e o documento para o coordenador (link) -->

## O que muda para o usuário

-

## O que muda nos números

<!-- Composições cujo HH, duração ou dias mudaram, com antes → depois e o motivo.
     Se nada mudou, escreva "nenhum" (o teste de referência confirma). -->

## Conferência

- [ ] `APP_VERSION`, comentário da 1ª linha e entrada nova no topo de `NOVIDADES` (nenhuma antiga apagada)
- [ ] `python testes/rodar.py index.html` → `RESULTADO: OK` (ou diferenças declaradas acima e `--atualizar-referencia`)
- [ ] Pendências de engenharia decididas com o Osvaldo; nenhum aviso de revisão no arquivo
- [ ] Nada gravado na base compartilhada; atividades novas em `dados-atividades-novas`
- [ ] `docs/HISTORICO_TECNICO.md` atualizado
- [ ] Depois do merge: etiqueta `vX.Y.Z` e Release com o `index.html` anexado
'@
  [IO.File]::WriteAllText((Join-Path $Proj '.github\workflows\testes.yml'), $yml.Replace("`r`n","`n"), $Utf8)
  [IO.File]::WriteAllText((Join-Path $Proj '.github\pull_request_template.md'), $pr.Replace("`r`n","`n"), $Utf8)
  New-Item -ItemType Directory (Join-Path $Proj 'docs') -Force | Out-Null
  Copy-Item (Join-Path $Vers 'HISTORICO_TECNICO.md') (Join-Path $Proj 'docs\HISTORICO_TECNICO.md') -Force
  Copy-Item (Join-Path $Vers 'LEIA-ME.txt') (Join-Path $Proj 'docs\LEIA-ME-versoes.txt') -Force
  Get-ChildItem $Proj -Force | Where-Object { $_.Name -ne '.git' } | Copy-Item -Destination $Tmp -Recurse -Force
  G add -A
  $msg = "chore: estrutura do projeto — instruções, testes, CI e histórico técnico`n`nCLAUDE.md, README, testes com valores de referência, GitHub Actions, modelo de PR, .gitattributes e geradores das versões 1.5.0 a 1.9.0.`n`nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`nClaude-Session: https://claude.ai/code/session_01Wa3BjYZjcKRUTVdjq1Aydi"
  $mf = Join-Path $env:TEMP 'hist-msg.txt'; [IO.File]::WriteAllText($mf, $msg, $Utf8)
  G commit -q -F $mf

  Passo "Criando $Repo (privado) e enviando"
  if (-not (Ok gh repo view $Repo)) { & gh repo create $Repo --private --description 'Dimensionamento de Histograma (Volga): app em arquivo único'; if ($LASTEXITCODE -ne 0) { throw 'gh repo create falhou' } }
  G remote add origin "https://github.com/$Repo.git"
  G push -u origin main
  G push origin site-arthur
  G push origin --tags

  Passo 'Criando as Releases (index.html anexado)'
  $nf = Join-Path $env:TEMP 'hist-notas.txt'
  foreach ($v in $Versoes) {
    $notas = $v.t.Substring($v.t.IndexOf('— ') + 2) + "`n`n**Para publicar:** baixe o index.html abaixo e publique como sempre."
    [IO.File]::WriteAllText($nf, $notas, $Utf8)
    $a = @('release', 'create', $v.k, (Join-Path $Vers "$($v.k)\index.html"), '--repo', $Repo, '--title', $v.k, '--notes-file', $nf, '--verify-tag')
    if ($v.k -eq 'v1.6.0') { $a += '--prerelease' }
    if ($v.k -eq 'v1.9.0') { $a += '--latest' } else { $a += '--latest=false' }
    & gh @a | Out-Null; if ($LASTEXITCODE -ne 0) { throw "release $($v.k) falhou" }
    Write-Host "  release $($v.k) ok"
  }
} finally { Pop-Location }

Passo 'A pasta projeto vira a cópia de trabalho'
Move-Item (Join-Path $Tmp '.git') (Join-Path $Proj '.git')
Push-Location $Proj
try {
  G config core.autocrlf false
  $st = & git status --porcelain
  if ($st) { Write-Host "Arquivos diferentes do repositório (confira):`n$st" -ForegroundColor Yellow } else { Write-Host 'projeto = repositório (sem diferenças)' -ForegroundColor Green }
} finally { Pop-Location }
Remove-Item $Tmp -Recurse -Force
Passo "Pronto: https://github.com/$Repo"
