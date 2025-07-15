from lark import Lark
from cheesepp.transformer import CheeseTransformer

with open("cheesepp/grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, start='start', parser='lalr', transformer=CheeseTransformer())

def parse(code):
    return parser.parse(code)
