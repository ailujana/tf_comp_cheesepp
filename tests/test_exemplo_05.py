from cheesepp.parser import parse
from cheesepp.runtime import Runtime

def test_exemplo_05(capsys):
    code = """Cheese
Glyn(i) Cheddar 0 Coleraine
Cheddar
    Wensleydale(Glyn(i));
    Glyn(i) Cheddar Glyn(i) plus 1 Coleraine
Coleraine Glyn(i) == 5;
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    captured = capsys.readouterr()
    assert all(str(n) in captured.out for n in range(5))