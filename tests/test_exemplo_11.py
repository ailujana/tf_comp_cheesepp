from cheesepp.parser import parse
from cheesepp.runtime import Runtime

def test_strings_simples():
    """Testa manipulação básica de strings Swiss"""
    code = """Cheese
Glyn(nome) = SwissArthurSwiss;
Glyn(sobrenome) = SwissSousaSwiss;
Glyn(numero) = Swiss123Swiss;
Glyn(especiais) = Swiss!@#$%^&*()Swiss;
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    
    assert rt.env["nome"] == "Arthur"
    assert rt.env["sobrenome"] == "Sousa"
    assert rt.env["numero"] == "123"
    assert rt.env["especiais"] == "!@#$%^&*()"

def test_strings_vazias_e_espacos():
    """Testa strings com espaços e caracteres especiais"""
    code = """Cheese
Glyn(espacos) = Swiss   Swiss;
Glyn(frase) = SwissOlá, mundo!Swiss;
Glyn(com_numero) = SwissTexto 123Swiss;
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    
    assert rt.env["espacos"] == "   "
    assert rt.env["frase"] == "Olá, mundo!"
    assert rt.env["com_numero"] == "Texto 123"

def test_strings_com_numeros(capsys):
    """Testa strings que contêm números e print de strings"""
    code = """Cheese
Glyn(versao) = SwissVersão 1.0Swiss;
Glyn(codigo) = SwissGlyn(x) = 42Swiss;
Wensleydale(Glyn(versao));
Wensleydale(Glyn(codigo));
NoCheese"""
    rt = Runtime()
    rt.run(parse(code), code)
    captured = capsys.readouterr()
    
    assert rt.env["versao"] == "Versão 1.0"
    assert rt.env["codigo"] == "Glyn(x) = 42"
    assert "Versão 1.0" in captured.out
    assert "Glyn(x) = 42" in captured.out
