# Interpretador Cheese++ - Trabalho final de Compiladores em 2025.1

Este trabalho teve como objetivo a implementação de um interpretador completo para a linguagem de programação Cheese++, utilizando Python e Lark para análise sintática.

## Sobre o Cheese++

Cheese++ é uma linguagem de programação baseada quase inteiramente nos princípios operacionais do queijo. A linguagem é case-sensitive e possui uma sintaxe única inspirada em nomes de queijos.

A referência utilizada para entendimento e estudo da linguagem foi [Cheese++ - Esolang](https://esolangs.org/wiki/Cheese%2B%2B).

## Sintaxe Básica

| Comando | Descrição |
|---------|-----------|
| `Cheese` | Início do programa |
| `NoCheese` | Fim do programa |
| `Wensleydale()` | Imprimir no console |
| `Swiss...Swiss` | Equivalente a aspas, usado para criar strings |
| `Glyn(operation)` | Função de variável - deve ser invocada em toda operação envolvendo variáveis |
| `Cheddar...Coleraine` | Estrutura de repetição (repeat...until) |
| `Stilton...Blue...White` | Estrutura condicional (if...then...else) |
| `Belgian` | Imprime todo o código fonte do programa (útil para debug) |
| `Brie` | Termina uma linha/seção de código |

## Exemplos

### Hello World
```cheese
Cheese
   Wensleydale(SwissHello WorldSwiss) Brie
NoCheese
```

### Declaração de Variáveis
```cheese
Cheese
Glyn(x) Cheddar 10 Coleraine
Glyn(y) Cheddar 20 Coleraine
Wensleydale(Glyn(x)) Brie
NoCheese
```

### Operações Aritméticas
```cheese
Cheese
Glyn(a) = 5;
Glyn(b) = a plus 3;
Wensleydale(Glyn(b)) Brie
NoCheese
```

### Estruturas Condicionais
```cheese
Cheese
Glyn(x) Cheddar 10 Coleraine
Stilton Glyn(x) greater 5 Blue
    Wensleydale(SwissX é maior que 5Swiss) Brie
White
    Wensleydale(SwissX é menor ou igual a 5Swiss) Brie
NoCheese
```

### Loops
```cheese
Cheese
Glyn(i) Cheddar 0 Coleraine
Cheddar
    Wensleydale(Glyn(i)) Brie
    Glyn(i) Cheddar Glyn(i) plus 1 Coleraine
Coleraine Glyn(i) minor 5
NoCheese
```

## Operadores Suportados

### Aritméticos
- `+` ou `plus` (adição)
- `-` ou `minus` (subtração)
- `*` ou `times` (multiplicação)
- `/` ou `divided` (divisão)

### Comparação
- `==` ou `equals` (igual)
- `!=` ou `not_equals` (diferente)
- `<` ou `less` ou `minor` (menor)
- `>` ou `greater` ou `great` (maior)
- `<=` ou `less_equals` (menor ou igual)
- `>=` ou `greater_equals` (maior ou igual)

## Estrutura do Projeto

```
tf_comp_cheesepp/
├── cheesepp/
│   ├── __init__.py
│   ├── ast.py          # Árvore Sintática Abstrata
│   ├── grammar.lark    # Gramática da linguagem
│   ├── parser.py       # Analisador sintático
│   ├── runtime.py      # Runtime/Interpretador
│   └── transformer.py  # Transformador AST
├── exemplos/
│   ├── exemplo_01.cheesepp
│   ├── exemplo_02.cheesepp
│   ├── exemplo_03.cheesepp
│   ├── exemplo_04.cheesepp
│   ├── exemplo_05.cheesepp
│   └── exemplo_06.cheesepp
├── tests/
│   ├── test_exemplo_01.py
│   ├── test_exemplo_02.py
│   ├── test_exemplo_03.py
│   ├── test_exemplo_04.py
│   ├── test_exemplo_05.py
│   └── test_exemplo_06.py
└── README.md
```

## Implementação

### Componentes Principais

1. **Parser (parser.py)**: Utiliza Lark para análise sintática
2. **AST (ast.py)**: Define as estruturas de dados da árvore sintática
3. **Transformer (transformer.py)**: Converte a árvore Lark em AST customizada
4. **Runtime (runtime.py)**: Interpretador que executa o código Cheese++
5. **Grammar (grammar.lark)**: Gramática formal da linguagem

### Funcionalidades Implementadas

- Análise léxica e sintática completa
- Suporte a strings Swiss com caracteres especiais e acentos
- Três tipos de declaração de variáveis:
  - `Glyn(var, expr)` - Estilo função
  - `Glyn(var) = expr` - Estilo assignment
  - `Glyn(var) Cheddar expr Coleraine` - Estilo Cheese++
- Operadores aritméticos e de comparação (símbolos e palavras)
- Estruturas condicionais (if/else)
- Estruturas de repetição (loops)
- Comando Belgian para debug
- Sistema de variáveis com ambiente de execução
- Tratamento de erros de sintaxe

## Como Executar

### Pré-requisitos
- Python 3.8+
- Lark parser: `pip install lark`

### Executar Testes
```bash
# Todos os testes
PYTHONPATH=. python3 -m pytest tests/ -v

# Teste específico
PYTHONPATH=. pytest tests/test_exemplo_X.py -v

# Teste simples
PYTHONPATH=. pytest -v
```

### Executar Código Cheese++
```python
from cheesepp.parser import parse
from cheesepp.runtime import Runtime

code = """Cheese
Glyn(x) Cheddar 42 Coleraine
Wensleydale(Glyn(x)) Brie
NoCheese"""

rt = Runtime()
rt.run(parse(code), code)
```

## Resultados dos Testes

6 testes foram implementados, e possuem 100% de aproveitamento. São eles:

- **test_exemplo_01**: Assignments e expressões aritméticas
- **test_exemplo_02**: Múltiplas funcionalidades integradas
- **test_exemplo_03**: Strings com acentos e caracteres especiais
- **test_exemplo_04**: Estruturas condicionais
- **test_exemplo_05**: Loops e operadores em palavras
- **test_exemplo_06**: Strings Swiss e comando Belgian


## Trabalho Desenvolvido Por

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/ailujana">
        <img src="https://avatars.githubusercontent.com/u/107697177?v=4" width="100" height="100" style="border-radius: 50%; object-fit: cover;" alt="Ana Júlia Mendes"/>
        <br /><sub><b>Ana Júlia Mendes</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Tutzs">
        <img src="https://avatars.githubusercontent.com/u/110691207?v=4" width="100" height="100" style="border-radius: 50%; object-fit: cover;" alt="Arthur Sousa"/>
        <br /><sub><b>Arthur Sousa</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/julia-fortunato">
        <img src="https://avatars.githubusercontent.com/u/118139107?v=4" width="100" height="100" style="border-radius: 50%; object-fit: cover;" alt="Júlia Fortunato"/>
        <br /><sub><b>Júlia Fortunato</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Oleari19">
        <img src="https://avatars.githubusercontent.com/u/110275583?v=4" width="100" height="100" style="border-radius: 50%; object-fit: cover;" alt="Maria Clara Oleari"/>
        <br /><sub><b>Maria Clara Oleari</b></sub>
      </a>
    </td>
  </tr>
</table>

## Histórico de versões

|Versão|Data|Descrição|Autor|
|:----:|----|---------|-----|
|`1.0`|14/07/2025|Criação do README com o comando dos testes|[Ana Julia](https://github.com/ailujana)|
|`1.1`|15/07/2025|Criação do README completo|[Maria Clara](https://github.com/Oleari19)|
|`1.1`|15/07/2025|Adequação e correção do README|[Júlia Fortunato](https://github.com/julia-fortunato)|
