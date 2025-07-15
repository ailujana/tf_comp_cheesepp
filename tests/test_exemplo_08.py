from cheesepp.parser import parse
from cheesepp.runtime import Runtime

def test_operacoes_matematicas():
    """Testa todas as operações matemáticas básicas"""
    code = """Cheese
Glyn(a) = 10;
Glyn(b) = 3;
Glyn(soma) = a + b;
Glyn(subtracao) = a - b;
Glyn(multiplicacao) = a * b;
Glyn(divisao) = a / b;
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    
    assert rt.env["a"] == 10
    assert rt.env["b"] == 3
    assert rt.env["soma"] == 13
    assert rt.env["subtracao"] == 7
    assert rt.env["multiplicacao"] == 30
    assert abs(rt.env["divisao"] - 3.333333333333333) < 0.0001  # Divisão com ponto flutuante

def test_operacoes_em_portugues():
    """Testa operações matemáticas em português"""
    code = """Cheese
Glyn(x) = 5;
Glyn(y) = 2;
Glyn(soma_pt) = x plus y;
Glyn(sub_pt) = x minus y;
Glyn(mult_pt) = x times y;
Glyn(div_pt) = x divided y;
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    
    assert rt.env["soma_pt"] == 7
    assert rt.env["sub_pt"] == 3
    assert rt.env["mult_pt"] == 10
    assert rt.env["div_pt"] == 2.5

def test_comparacoes_logicas():
    """Testa todas as operações de comparação"""
    code = """Cheese
Glyn(a) = 10;
Glyn(b) = 5;
Glyn(c) = 10;
Glyn(igual) = a == c;
Glyn(diferente) = a != b;
Glyn(maior) = a > b;
Glyn(menor) = b < a;
Glyn(maior_igual) = a >= c;
Glyn(menor_igual) = b <= a;
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    
    assert rt.env["igual"] == True
    assert rt.env["diferente"] == True
    assert rt.env["maior"] == True
    assert rt.env["menor"] == True
    assert rt.env["maior_igual"] == True
    assert rt.env["menor_igual"] == True

def test_comparacoes_em_portugues():
    """Testa operações de comparação em português"""
    code = """Cheese
Glyn(x) = 15;
Glyn(y) = 10;
Glyn(igual_pt) = x equals y;
Glyn(diferente_pt) = x not_equals y;
Glyn(maior_pt) = x greater y;
Glyn(menor_pt) = y less x;
Glyn(maior_igual_pt) = x greater_equals y;
Glyn(menor_igual_pt) = y less_equals x;
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    
    assert rt.env["igual_pt"] == False
    assert rt.env["diferente_pt"] == True
    assert rt.env["maior_pt"] == True
    assert rt.env["menor_pt"] == True
    assert rt.env["maior_igual_pt"] == True
    assert rt.env["menor_igual_pt"] == True
