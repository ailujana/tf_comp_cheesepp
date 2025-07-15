class CheeseAssign:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number:
    def __init__(self, value):
        self.value = value

class Var:
    def __init__(self, name):
        self.name = name

class CheesePrint:
    def __init__(self, expr):
        self.expr = expr

class String:
    def __init__(self, value):
        self.value = value

class CheeseIf:
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class CheeseLoop:
    def __init__(self, body, condition):
        self.body = body
        self.condition = condition

class Belgian:
    def __init__(self):
        pass