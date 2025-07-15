from cheesepp.parser import parse
from cheesepp.runtime import Runtime

def test_exemplo_04(capsys):
    code = """Cheese
Glyn(x) Cheddar 5 Coleraine
Stilton Glyn(x) == 5 Blue
    Wensleydale(Swissx is fiveSwiss);
White
    Wensleydale(Swissx is not fiveSwiss);
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    captured = capsys.readouterr()
    assert "x is five" in captured.out