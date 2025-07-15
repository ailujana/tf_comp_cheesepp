from cheesepp.parser import parse
from cheesepp.runtime import Runtime

def test_exemplo_03(capsys):
    code = """Cheese
Glyn(msg) = SwissHello, João Victor!Swiss;
Wensleydale(Glyn(msg));
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    captured = capsys.readouterr()
    assert "João Victor" in captured.out