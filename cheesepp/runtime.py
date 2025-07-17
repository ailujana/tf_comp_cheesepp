from cheesepp.ast import *

class Runtime:
    def __init__(self):
        self.env = {}
        self.last_source = None

    def eval(self, node):
        if isinstance(node, CheeseAssign):
            value = self.eval(node.value)
            self.env[node.name] = value
            return value

        elif isinstance(node, Number):
            return node.value

        elif isinstance(node, String):
            return node.value

        elif isinstance(node, Var):
            return self.env.get(node.name, 0)

        elif isinstance(node, BinOp):
            left = self.eval(node.left)
            right = self.eval(node.right)
            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                return left / right
            elif node.op == '==':
                return left == right
            elif node.op == '!=':
                return left != right
            elif node.op == '>':
                return left > right
            elif node.op == '<':
                return left < right
            elif node.op == '>=':
                return left >= right
            elif node.op == '<=':
                return left <= right

        elif isinstance(node, CheesePrint):
            value = self.eval(node.expr)
            print(value)
            return value

        elif isinstance(node, CheeseIf):
            cond = self.eval(node.condition)
            branch = node.then_branch if cond else node.else_branch
            result = None
            for stmt in branch:
                result = self.eval(stmt)
            return result

        elif isinstance(node, CheeseLoop):
            while not self.eval(node.condition):
                for stmt in node.body:
                    self.eval(stmt)

        elif isinstance(node, Belgian):
            if self.last_source:
                print("=== Belgian Mode ===")
                print(self.last_source)
            else:
                print("No source available.")
            return None

        else:
            return node

    def run(self, program, source_code=None):
        self.last_source = source_code
        results = []

        for stmt in program:
            if stmt is not None: 
                result = self.eval(stmt)
                results.append(result)
        return results[-1] if results else None