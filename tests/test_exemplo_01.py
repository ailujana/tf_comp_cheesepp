import pytest
from cheesepp.parser import parse
from cheesepp.runtime import Runtime

@pytest.mark.all
def test_exemplo_01():
    code = """Cheese
Glyn(a) = 2 + 3;
Glyn(b) = a * 4;
b;
NoCheese"""
    rt = Runtime()
    result = rt.run(parse(code), code)
    assert rt.env["a"] == 5
    assert rt.env["b"] == 20