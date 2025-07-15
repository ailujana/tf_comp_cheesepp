from cheesepp.parser import parse
from cheesepp.runtime import Runtime

def test_exemplo_06(capsys):
    code = """Cheese
Glyn(name) Cheddar SwissJoão VictorSwiss Coleraine
Wensleydale(Glyn(name));
Belgian;
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    captured = capsys.readouterr()
    assert "João Victor" in captured.out
    assert "Belgian;" in captured.out or "Wensleydale" in captured.out