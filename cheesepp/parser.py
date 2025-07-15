from lark import Lark
from cheesepp.transformer import CheeseTransformer
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
grammar_path = os.path.join(current_dir, "grammar.lark")

with open(grammar_path) as f:
    grammar = f.read()

parser = Lark(grammar, start='start', parser='lalr', transformer=CheeseTransformer())

def parse(code):
    return parser.parse(code)
