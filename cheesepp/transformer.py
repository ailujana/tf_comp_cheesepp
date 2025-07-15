from lark import Transformer
from cheesepp.ast import *

class CheeseTransformer(Transformer):
    def start(self, items):
        return items[0]  
    
    def program(self, items):
        return items  
    
    def stmt(self, items):
        if items:
            return items[0]  
        else:
            return None  
        
    def assignment(self, items):
        name = str(items[0])
        expr = items[1]
        return CheeseAssign(name, expr)
    
    def assignment2(self, items):
        name = str(items[0])
        expr = items[1]
        return CheeseAssign(name, expr)
    
    def assignment3(self, items):
        name = str(items[0])
        expr = items[1]
        return CheeseAssign(name, expr)

    def print_stmt(self, items):
        return CheesePrint(items[0])

    def expr_stmt(self, items):
        return items[0]

    def if_stmt(self, items):
        condition = items[0]
        statements = items[1:]
        
        mid = len(statements) // 2
        then_branch = statements[:mid]
        else_branch = statements[mid:]
        
        return CheeseIf(condition, then_branch, else_branch)

    def loop_stmt(self, items):
        *body, condition = items
        return CheeseLoop(body, condition)

    def belgian_stmt(self, items):
        return Belgian()

    def number(self, items):
        return Number(float(items[0]))

    def var_access(self, items):
        return Var(str(items[0]))

    def var_access_simple(self, items):
        return Var(str(items[0]))

    def string(self, items):
        return items[0]  
    
    def swiss_string(self, items):
        if len(items) > 0:
            content = str(items[0])
        else:
            content = ""
        return String(content)

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