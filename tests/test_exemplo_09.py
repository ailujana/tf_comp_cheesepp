from cheesepp.parser import parse
from cheesepp.runtime import Runtime

def test_belgian_com_codigo_fonte(capsys):
    """Testa o comando Belgian para debug"""
    code = """Cheese
Glyn(x) = 10;
Belgian;
Wensleydale(Glyn(x));
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    captured = capsys.readouterr()
    
    # Belgian deve imprimir o código fonte
    assert "=== Belgian Mode ===" in captured.out
    assert "Glyn(x) = 10" in captured.out
    assert "10" in captured.out  # Saída do Wensleydale

def test_belgian_sem_codigo_fonte(capsys):
    """Testa o comando Belgian sem código fonte fornecido"""
    code = """Cheese
Belgian;
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), "")  # Sem código fonte
    captured = capsys.readouterr()
    
    assert "No source available." in captured.out

def test_prints_multiplos(capsys):
    """Testa múltiplos comandos de print"""
    code = """Cheese
Glyn(a) = 1;
Glyn(b) = 2;
Glyn(c) = 3;
Wensleydale(Glyn(a));
Wensleydale(Glyn(b));
Wensleydale(Glyn(c));
Wensleydale(SwissFinalizadoSwiss);
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    captured = capsys.readouterr()
    
    lines = captured.out.strip().split('\n')
    assert "1" in captured.out
    assert "2" in captured.out
    assert "3" in captured.out
    assert "Finalizado" in captured.out

def test_print_calculos(capsys):
    """Testa print de cálculos diretos"""
    code = """Cheese
Glyn(x) = 5;
Wensleydale(Glyn(x) + 3);
Wensleydale(Glyn(x) * 2);
Wensleydale(Glyn(x) greater 3);
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    captured = capsys.readouterr()
    
    assert "8" in captured.out   # 5 + 3
    assert "10" in captured.out  # 5 * 2
    assert "True" in captured.out # 5 > 3
