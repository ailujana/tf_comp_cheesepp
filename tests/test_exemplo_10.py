from cheesepp.parser import parse
from cheesepp.runtime import Runtime

def test_if_simples(capsys):
    """Testa estrutura condicional simples"""
    code = """Cheese
Glyn(idade) = 18;
Stilton Glyn(idade) >= 18 Blue
    Wensleydale(SwissMaior de idadeSwiss);
White
    Wensleydale(SwissMenor de idadeSwiss);
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    captured = capsys.readouterr()
    
    assert "Maior de idade" in captured.out
    assert "Menor de idade" not in captured.out

def test_if_else_falso(capsys):
    """Testa estrutura condicional quando condição é falsa"""
    code = """Cheese
Glyn(nota) = 5;
Stilton Glyn(nota) >= 7 Blue
    Wensleydale(SwissAprovadoSwiss);
White
    Wensleydale(SwissReprovadoSwiss);
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    captured = capsys.readouterr()
    
    assert "Aprovado" not in captured.out
    assert "Reprovado" in captured.out

def test_if_aninhado(capsys):
    """Testa estruturas condicionais aninhadas"""
    code = """Cheese
Glyn(temperatura) = 25;
Stilton Glyn(temperatura) > 30 Blue
    Wensleydale(SwissQuenteSwiss);
White
    Stilton Glyn(temperatura) > 20 Blue
        Wensleydale(SwissAgradávelSwiss);
    White
        Wensleydale(SwissFrioSwiss);
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    captured = capsys.readouterr()
    
    assert "Quente" not in captured.out
    assert "Agradável" in captured.out
    assert "Frio" not in captured.out

def test_if_multiplas_operacoes(capsys):
    """Testa if com múltiplas operações no then/else"""
    code = """Cheese
Glyn(x) = 10;
Stilton Glyn(x) > 5 Blue
    Glyn(resultado) = x * 2;
    Wensleydale(Glyn(resultado));
    Wensleydale(SwissNo then branchSwiss);
White
    Glyn(resultado) = x / 2;
    Wensleydale(Glyn(resultado));
    Wensleydale(SwissNo else branchSwiss);
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    captured = capsys.readouterr()
    
    assert rt.env["resultado"] == 20
    assert "20" in captured.out
    assert "No then branch" in captured.out
    assert "No else branch" not in captured.out
