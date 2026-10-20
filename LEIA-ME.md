# Projeto — Dimensionamento de Histograma

Esta pasta é a fonte de trabalho do app. As versões prontas para publicar ficam em `..\versoes`.

- `index.html` — a última versão (hoje 1.9.0). É o app inteiro, num arquivo só.
- `CLAUDE.md` — regras do projeto e mapa do arquivo, escrito para quem for mexer (pessoa ou IA).
- `testes\` — testes automáticos e valores de referência.
- `ferramentas\geradores\` — scripts antigos que geraram as versões 1.5.0 a 1.9.0. Ficam só como
  histórico: a partir da 1.9.0 o arquivo é editado direto.

## Onde editar os dados

Abra `index.html` num editor de texto (VS Code, Notepad++) e procure:

- `id="dados-base"` — base de atividades: uma atividade por linha (código, disciplina, grupo, serviço,
  unidade, fonte, observação e as horas por unidade de cada recurso).
- `id="dados-composicoes"` — composições padrão: entradas, parâmetros com nome, atividades com a fórmula
  da quantidade e observações, cada item numa linha.

O app de verdade usa a base da nuvem quando ela carrega. Mudanças na base de atividades que já está na
nuvem são feitas pelo administrador na tela Base de atividades.

## Como rodar os testes (Windows)

Uma vez só:

```
py -m pip install -r testes\requisitos.txt
py -m playwright install chromium
```

Depois, a cada versão, dentro da pasta `projeto`:

```
py testes\rodar.py index.html
```

A última linha diz `RESULTADO: OK` ou lista o que mudou (por exemplo, o HH de uma composição).
