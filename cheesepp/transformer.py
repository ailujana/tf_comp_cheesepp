from lark import Transformer
from cheesepp.ast import *

class CheeseTransformer(Transformer):
    def assignment(self, items):
        name = str(items[0])
        expr = items[1]
        return CheeseAssign(name, expr)

    def print_stmt(self, items):
        return CheesePrint(items[0])

    def expr_stmt(self, items):
        return items[0]

    def if_stmt(self, items):
        condition = items[0]
        split = items[1:]
        white_index = next(i for i, stmt in enumerate(split) if isinstance(stmt, CheesePrint) and stmt.expr == "WHITE_MARKER")
        then_branch = split[:white_index]
        else_branch = split[white_index+1:]
        return CheeseIf(condition, then_branch, else_branch)

    def loop_stmt(self, items):
        *body, condition = items
        return CheeseLoop(body, condition)

    def belgian_stmt(self, _):
        return Belgian()

    def number(self, items):
        return Number(float(items[0]))

    def var(self, items):
        return Var(str(items[0]))

    def glyn_var(self, items):
        return Var(str(items[0]))

    def string(self, items):
        value = str(items[0])[5:-5]
        return String(value)

    def add(self, items): return BinOp(items[0], '+', items[1])
    def sub(self, items): return BinOp(items[0], '-', items[1])
    def mul(self, items): return BinOp(items[0], '*', items[1])
    def div(self, items): return BinOp(items[0], '/', items[1])
    def eq(self, items): return BinOp(items[0], '==', items[1])
    def ne(self, items): return BinOp(items[0], '!=', items[1])
    def gt(self, items): return BinOp(items[0], '>', items[1])
    def lt(self, items): return BinOp(items[0], '<', items[1])
    def ge(self, items): return BinOp(items[0], '>=', items[1])
    def le(self, items): return BinOp(items[0], '<=', items[1])