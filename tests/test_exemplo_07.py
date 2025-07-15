from cheesepp.parser import parse
from cheesepp.runtime import Runtime

def test_programa_vazio():
    """Testa programa Cheese++ vazio"""
    code = """Cheese
NoCheese"""
    rt = Runtime()
    result = rt.run(parse(code), code)
    
    assert result is None
    assert len(rt.env) == 0

def test_apenas_pontos_virgula():
    """Testa programa com apenas separadores"""
    code = """Cheese
;
Brie
;;
NoCheese"""
    rt = Runtime()
    result = rt.run(parse(code), code)
    
    assert result is None
    assert len(rt.env) == 0

def test_numeros_decimais():
    """Testa números com ponto decimal"""
    code = """Cheese
Glyn(pi) = 3.14159;
Glyn(metade) = 0.5;
Glyn(resultado) = pi * metade;
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    
    assert abs(rt.env["pi"] - 3.14159) < 0.0001
    assert rt.env["metade"] == 0.5
    assert abs(rt.env["resultado"] - 1.570795) < 0.0001

def test_numeros_negativos():
    """Testa números negativos através de subtração"""
    code = """Cheese
Glyn(zero) = 0;
Glyn(negativo) = zero - 5;
Glyn(calculo) = negativo * 2;
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    
    assert rt.env["negativo"] == -5
    assert rt.env["calculo"] == -10

def test_divisao_por_zero():
    """Testa divisão por zero (pode gerar exceção ou inf)"""
    code = """Cheese
Glyn(x) = 10;
Glyn(zero) = 0;
Glyn(resultado) = x / zero;
NoCheese"""
    rt = Runtime()
    
    try:
        rt.run(parse(code), code)
        # Se não houve exceção, verifica se o resultado é infinito
        assert rt.env["resultado"] == float('inf') or str(rt.env["resultado"]) == 'inf'
    except ZeroDivisionError:
        # Se houve exceção, isso também é um comportamento válido
        pass

def test_precedencia_operadores():
    """Testa precedência de operadores matemáticos"""
    code = """Cheese
Glyn(resultado1) = 2 + 3 * 4;  
Glyn(resultado2) = 2 * 3 + 4;  
Glyn(resultado3) = 10 / 2 + 3; 
Glyn(resultado4) = 10 + 2 / 2; 
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    
    assert rt.env["resultado1"] == 14  # 2 + (3*4) = 2 + 12 = 14
    assert rt.env["resultado2"] == 10  # (2*3) + 4 = 6 + 4 = 10
    assert rt.env["resultado3"] == 8   # (10/2) + 3 = 5 + 3 = 8
    assert rt.env["resultado4"] == 11  # 10 + (2/2) = 10 + 1 = 11
