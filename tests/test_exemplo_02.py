import pytest
from cheesepp.parser import parse
from cheesepp.runtime import Runtime

@pytest.mark.all
def test_exemplo_02(capsys):
    code = """Cheese
Glyn(greeting) Cheddar SwissHello, WorldSwiss Coleraine
Glyn(number) Cheddar 42 Coleraine
Glyn(result) Cheddar Glyn(number) times 2 Coleraine
Wensleydale(Glyn(greeting)) Brie
Wensleydale(Glyn(result)) Brie
Stilton Glyn(number) greater 40 Blue
    Wensleydale(SwissNumber is bigSwiss) Brie
White
    Wensleydale(SwissNumber is smallSwiss) Brie
NoCheese"""
    
    rt = Runtime()
    rt.run(parse(code), code)
    captured = capsys.readouterr()
    
    # Verify the expected outputs
    assert "Hello, World" in captured.out
    assert "84" in captured.out  # 42 * 2
    assert "Number is big" in captured.out  
