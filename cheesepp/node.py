from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Union
from dataclasses import dataclass
from enum import Enum


class NodeType(Enum):
    """Enumeração de todos os tipos de nós no AST do Cheese++"""
    PROGRAM = "program"
    STATEMENT = "statement"
    EXPRESSION = "expression"
    VARIABLE = "variable"
    ASSIGNMENT = "assignment"
    BINARY_OP = "binary_op"
    UNARY_OP = "unary_op"
    FUNCTION_CALL = "function_call"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    LITERAL = "literal"
    BLOCK = "block"


@dataclass
class Position:
    """Representa uma posição no código-fonte"""
    line: int
    column: int
    
    def __repr__(self):
        return f"({self.line}:{self.column})"


class ASTNode(ABC):
    """
    Classe base abstrata para todos os nós AST.
    
    Todos os nós do AST do Cheese++ herdam essa classe e devem implementar
    o método accept para o padrão de visitante.
    """
    
    def __init__(self, node_type: NodeType, position: Optional[Position] = None):
        self.node_type = node_type
        self.position = position
        self.parent: Optional['ASTNode'] = None
        self.children: List['ASTNode'] = []
    
    @abstractmethod
    def accept(self, visitor):
        """Aceita um visitante para o padrão de visitante"""
        pass
    
    def add_child(self, child: 'ASTNode') -> None:
        """Adiciona um nó filho ao nó atual."""
        if child:
            child.parent = self
            self.children.append(child)
    
    def remove_child(self, child: 'ASTNode') -> None:
        """Remove um nó filho do nó atual."""
        if child in self.children:
            child.parent = None
            self.children.remove(child)
    
    def get_children(self) -> List['ASTNode']:
        """Pega uma cópia da lista de nós filhos."""
        return self.children.copy()
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.node_type.value})"


class ProgramNode(ASTNode):
    """Nó raiz do AST que representa todo o programa"""
    
    def __init__(self, statements: List[ASTNode], position: Optional[Position] = None):
        super().__init__(NodeType.PROGRAM, position)
        self.statements = statements
        for stmt in statements:
            self.add_child(stmt)
    
    def accept(self, visitor):
        return visitor.visit_program(self)


class StatementNode(ASTNode):
    """Classe base para todos os nós de declaração"""
    
    def __init__(self, position: Optional[Position] = None):
        super().__init__(NodeType.STATEMENT, position)


class ExpressionNode(ASTNode):
    """Classe base para todos os nós de expressão"""
    
    def __init__(self, position: Optional[Position] = None):
        super().__init__(NodeType.EXPRESSION, position)


class BlockNode(StatementNode):
    """Nó que representa um bloco de instruções"""
    
    def __init__(self, statements: List[StatementNode], position: Optional[Position] = None):
        super().__init__(position)
        self.node_type = NodeType.BLOCK
        self.statements = statements
        for stmt in statements:
            self.add_child(stmt)
    
    def accept(self, visitor):
        return visitor.visit_block(self)


class AssignmentNode(StatementNode):
    """Nó que representa uma atribuição de variável"""
    
    def __init__(self, variable: str, value: ExpressionNode, 
                 assignment_type: str = "=", position: Optional[Position] = None):
        super().__init__(position)
        self.node_type = NodeType.ASSIGNMENT
        self.variable = variable
        self.value = value
        self.assignment_type = assignment_type  # "=", "Cheddar...Coleraine", etc.
        self.add_child(value)
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)


class BinaryOpNode(ExpressionNode):
    """Nó que representa operações binárias"""
    
    def __init__(self, left: ExpressionNode, operator: str, right: ExpressionNode,
                 position: Optional[Position] = None):
        super().__init__(position)
        self.node_type = NodeType.BINARY_OP
        self.left = left
        self.operator = operator
        self.right = right
        self.add_child(left)
        self.add_child(right)
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)


class UnaryOpNode(ExpressionNode):
    """Nó que representa operações unárias"""
    
    def __init__(self, operator: str, operand: ExpressionNode,
                 position: Optional[Position] = None):
        super().__init__(position)
        self.node_type = NodeType.UNARY_OP
        self.operator = operator
        self.operand = operand
        self.add_child(operand)
    
    def accept(self, visitor):
        return visitor.visit_unary_op(self)


class VariableNode(ExpressionNode):
    """Nó que representa variáveis"""
    
    def __init__(self, name: str, position: Optional[Position] = None):
        super().__init__(position)
        self.node_type = NodeType.VARIABLE
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_variable(self)


class LiteralNode(ExpressionNode):
    """Nó que representa literais (números, strings, etc.)"""
    
    def __init__(self, value: Any, literal_type: str, position: Optional[Position] = None):
        super().__init__(position)
        self.node_type = NodeType.LITERAL
        self.value = value
        self.literal_type = literal_type  
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


class FunctionCallNode(ExpressionNode):
    """Nó que representa chamadas de função"""
    
    def __init__(self, name: str, arguments: List[ExpressionNode],
                 position: Optional[Position] = None):
        super().__init__(position)
        self.node_type = NodeType.FUNCTION_CALL
        self.name = name
        self.arguments = arguments
        for arg in arguments:
            self.add_child(arg)
    
    def accept(self, visitor):
        return visitor.visit_function_call(self)


class ConditionalNode(StatementNode):
    """Nó que representa instruções condicionais"""
    
    def __init__(self, condition: ExpressionNode, then_branch: StatementNode,
                 else_branch: Optional[StatementNode] = None,
                 position: Optional[Position] = None):
        super().__init__(position)
        self.node_type = NodeType.CONDITIONAL
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
        
        self.add_child(condition)
        self.add_child(then_branch)
        if else_branch:
            self.add_child(else_branch)
    
    def accept(self, visitor):
        return visitor.visit_conditional(self)


class LoopNode(StatementNode):
    """Nó que representa laços de repetição"""
    
    def __init__(self, body: StatementNode, condition: ExpressionNode,
                 loop_type: str = "while", position: Optional[Position] = None):
        super().__init__(position)
        self.node_type = NodeType.LOOP
        self.body = body
        self.condition = condition
        self.loop_type = loop_type 
        
        self.add_child(body)
        self.add_child(condition)
    
    def accept(self, visitor):
        return visitor.visit_loop(self)


class PrintNode(StatementNode):
    """Nó que representa instruções de impressão"""
    
    def __init__(self, expression: ExpressionNode, position: Optional[Position] = None):
        super().__init__(position)
        self.expression = expression
        self.add_child(expression)
    
    def accept(self, visitor):
        return visitor.visit_print(self)


class DebugNode(StatementNode):
    """Nó que representa instruções de depuração"""
    
    def __init__(self, position: Optional[Position] = None):
        super().__init__(position)
    
    def accept(self, visitor):
        return visitor.visit_debug(self)


class NodeVisitor(ABC):
    """
    Classe base abstrata para visitantes de nós AST.
    
    Implementa o padrão de visitante para percorrer e processar nós AST.
    """
    
    @abstractmethod
    def visit_program(self, node: ProgramNode):
        pass
    
    @abstractmethod
    def visit_block(self, node: BlockNode):
        pass
    
    @abstractmethod
    def visit_assignment(self, node: AssignmentNode):
        pass
    
    @abstractmethod
    def visit_binary_op(self, node: BinaryOpNode):
        pass
    
    @abstractmethod
    def visit_unary_op(self, node: UnaryOpNode):
        pass
    
    @abstractmethod
    def visit_variable(self, node: VariableNode):
        pass
    
    @abstractmethod
    def visit_literal(self, node: LiteralNode):
        pass
    
    @abstractmethod
    def visit_function_call(self, node: FunctionCallNode):
        pass
    
    @abstractmethod
    def visit_conditional(self, node: ConditionalNode):
        pass
    
    @abstractmethod
    def visit_loop(self, node: LoopNode):
        pass
    
    @abstractmethod
    def visit_print(self, node: PrintNode):
        pass
    
    @abstractmethod
    def visit_debug(self, node: DebugNode):
        pass


class ASTTraverser:
    """
    Classe utilitária para percorrer nós AST.
    
    Fornece métodos para diferentes estratégias de passagem.
    """
    
    @staticmethod
    def depth_first_search(node: ASTNode, visitor: NodeVisitor):
        """Performa uma busca em profundidade no AST"""
        node.accept(visitor)
        for child in node.children:
            ASTTraverser.depth_first_search(child, visitor)
    
    @staticmethod
    def breadth_first_search(node: ASTNode, visitor: NodeVisitor):
        """Performa uma busca em largura no AST"""
        queue = [node]
        while queue:
            current = queue.pop(0)
            current.accept(visitor)
            queue.extend(current.children)
    
    @staticmethod
    def find_nodes_by_type(node: ASTNode, node_type: NodeType) -> List[ASTNode]:
        """Encontra todos os nós de um tipo específico no AST"""
        result = []
        
        def collector(n):
            if n.node_type == node_type:
                result.append(n)
        
        ASTTraverser._traverse_with_function(node, collector)
        return result
    
    @staticmethod
    def _traverse_with_function(node: ASTNode, func):
        """Ajuda a percorrer o AST com uma função personalizada"""
        func(node)
        for child in node.children:
            ASTTraverser._traverse_with_function(child, func)


class ASTBuilder:
    """
    Classe utilitária para criar nós AST.
    
    Fornece métodos de fábrica para criar padrões de nós comuns.
    """
    
    @staticmethod
    def create_program(statements: List[StatementNode]) -> ProgramNode:
        """Cria um nó de programa com suas declarações"""
        return ProgramNode(statements)
    
    @staticmethod
    def create_assignment(variable: str, value: ExpressionNode, 
                         assignment_type: str = "=") -> AssignmentNode:
        """Cria um nó de atribuição"""
        return AssignmentNode(variable, value, assignment_type)
    
    @staticmethod
    def create_binary_op(left: ExpressionNode, operator: str, 
                        right: ExpressionNode) -> BinaryOpNode:
        """Cria um nó de operação binária"""
        return BinaryOpNode(left, operator, right)
    
    @staticmethod
    def create_literal(value: Any, literal_type: str) -> LiteralNode:
        """Cria um nó de literal"""
        return LiteralNode(value, literal_type)
    
    @staticmethod
    def create_variable(name: str) -> VariableNode:
        """Cria um nó de variável"""
        return VariableNode(name)
    
    @staticmethod
    def create_function_call(name: str, arguments: List[ExpressionNode]) -> FunctionCallNode:
        """Cria um nó de chamada de função"""
        return FunctionCallNode(name, arguments)
    
    @staticmethod
    def create_conditional(condition: ExpressionNode, then_branch: StatementNode,
                          else_branch: Optional[StatementNode] = None) -> ConditionalNode:
        """Cria um nó de condicional"""
        return ConditionalNode(condition, then_branch, else_branch)
    
    @staticmethod
    def create_loop(body: StatementNode, condition: ExpressionNode,
                   loop_type: str = "while") -> LoopNode:
        """Cria um nó de laço de repetição"""
        return LoopNode(body, condition, loop_type)


def ast_to_dict(node: ASTNode) -> Dict[str, Any]:
    """Converte o nó AST em uma representação de dicionário"""
    result = {
        'type': node.node_type.value,
        'class': node.__class__.__name__,
        'position': str(node.position) if node.position else None,
        'children': []
    }
    
    
    if hasattr(node, 'value'):
        result['value'] = node.value
    if hasattr(node, 'name'):
        result['name'] = node.name
    if hasattr(node, 'operator'):
        result['operator'] = node.operator
    if hasattr(node, 'variable'):
        result['variable'] = node.variable
    

    for child in node.children:
        result['children'].append(ast_to_dict(child))
    
    return result


def dict_to_ast(data: Dict[str, Any]) -> ASTNode:
    """Converte a representação do dicionário de volta para o nó AST"""
   
    node_type = NodeType(data['type'])
    
    if node_type == NodeType.PROGRAM:
        return ProgramNode([])
    elif node_type == NodeType.LITERAL:
        return LiteralNode(data.get('value'), data.get('literal_type', 'unknown'))
    elif node_type == NodeType.VARIABLE:
        return VariableNode(data.get('name', ''))
   
    
    return None
