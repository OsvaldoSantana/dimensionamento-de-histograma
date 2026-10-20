# Dimensionamento de Histograma

App web da Volga Engenharia (Departamento de Instalação). A partir de composições de serviço (atividades,
quantidades por fórmula e coeficientes em h/unidade), monta a duração de cada composição, o cronograma com
vínculos e calendário, e o histograma de recursos. Publicado pelo coordenador em
https://dimensionamento-de-histograma.web.app.

**O app inteiro é um único arquivo: [`index.html`](index.html).** HTML, CSS, JavaScript e os dados (base de
atividades embutida e composições padrão) ficam nele. A única dependência externa é o Firebase.

## Para publicar

A publicação continua sendo copiar um arquivo. Cada versão tem uma
[Release](../../releases) com o `index.html` anexado. Baixe o da versão desejada e publique como sempre.
Para voltar uma versão, publique o `index.html` da Release anterior.

## Estrutura

| Caminho | O que é |
|---|---|
| `index.html` | O app (última versão) |
| `CLAUDE.md` | Regras do projeto, mapa do arquivo e passo a passo de versão — para quem for mexer, pessoa ou IA |
| `testes/rodar.py` | Todos os testes num comando |
| `testes/referencia.json` | HH, duração e dias de cada composição padrão (valores de referência) |
| `docs/HISTORICO_TECNICO.md` | O que mudou tecnicamente em cada versão |
| `docs/LEIA-ME-versoes.txt` | Guia da pasta de versões usada fora do repositório |
| `ferramentas/geradores/` | Scripts que geraram as versões 1.5.0 a 1.9.0 (histórico; não usar mais) |
| `ferramentas/criar-repositorio.ps1` | Script que criou este repositório a partir da pasta de versões |

## Testes

```
pip install -r testes/requisitos.txt
python -m playwright install chromium
python testes/rodar.py index.html
```

A última linha diz `RESULTADO: OK` ou lista o que mudou. Os mesmos testes rodam sozinhos no GitHub a cada
envio e em cada pedido de revisão (aba Actions).

## Versões

Numeração X.Y.Z sem sufixo (X = exige converter projetos salvos; Y = funcionalidade nova; Z = correção).
Cada versão é uma etiqueta `vX.Y.Z` neste repositório. O histórico reconstrói a linha completa: 1.0.0
(original), o site publicado pelo Arthur em 19/10/2026 (ramo `site-arthur`) e a junção das duas linhas na
1.5.0.

## Uso

Repositório privado. Código e dados de uso interno da Volga Engenharia; todos os direitos reservados.
