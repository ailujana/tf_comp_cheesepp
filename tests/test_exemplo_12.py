from cheesepp.parser import parse
from cheesepp.runtime import Runtime

def test_sintaxes_atribuicao():
    """Testa todas as sintaxes de atribuição disponíveis"""
    code = """Cheese
Glyn(a) = 5;
Glyn(b, 10);
Glyn(c) Cheddar 15 Coleraine
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    
    assert rt.env["a"] == 5
    assert rt.env["b"] == 10
    assert rt.env["c"] == 15

def test_acesso_variaveis():
    """Testa diferentes formas de acessar variáveis"""
    code = """Cheese
Glyn(valor) = 42;
Glyn(referencia) = Glyn(valor);
Glyn(calculo) = valor + Glyn(valor);
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    
    assert rt.env["valor"] == 42
    assert rt.env["referencia"] == 42
    assert rt.env["calculo"] == 84

def test_expressoes_complexas():
    """Testa expressões matemáticas complexas"""
    code = """Cheese
Glyn(a) = 2;
Glyn(b) = 3;
Glyn(c) = 4;
Glyn(resultado1) = a + b * c;
Glyn(resultado2) = (a + b) * c;
Glyn(resultado3) = a * b + c * a;
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    
    assert rt.env["resultado1"] == 14  # 2 + 3*4 = 2 + 12 = 14
    assert rt.env["resultado2"] == 20  # (2+3)*4 = 5*4 = 20
    assert rt.env["resultado3"] == 14  # 2*3 + 4*2 = 6 + 8 = 14

def test_variaveis_nao_definidas():
    """Testa comportamento com variáveis não definidas (devem retornar 0)"""
    code = """Cheese
Glyn(resultado) = inexistente + 5;
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    
    assert rt.env["resultado"] == 5  # inexistente = 0, então 0 + 5 = 5
