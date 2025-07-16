from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Union
from dataclasses import dataclass
from enum import Enum


class NodeType(Enum):
    """Enumeration of all node types in the Cheese++ AST"""
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
    """Represents a position in the source code"""
    line: int
    column: int
    
    def __repr__(self):
        return f"({self.line}:{self.column})"


class ASTNode(ABC):
    """
    Abstract base class for all AST nodes.
    
    All nodes in the Cheese++ AST inherit from this class and must implement
    the accept method for the visitor pattern.
    """
    
    def __init__(self, node_type: NodeType, position: Optional[Position] = None):
        self.node_type = node_type
        self.position = position
        self.parent: Optional['ASTNode'] = None
        self.children: List['ASTNode'] = []
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern"""
        pass
    
    def add_child(self, child: 'ASTNode') -> None:
        """Add a child node"""
        if child:
            child.parent = self
            self.children.append(child)
    
    def remove_child(self, child: 'ASTNode') -> None:
        """Remove a child node"""
        if child in self.children:
            child.parent = None
            self.children.remove(child)
    
    def get_children(self) -> List['ASTNode']:
        """Get all child nodes"""
        return self.children.copy()
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.node_type.value})"


class ProgramNode(ASTNode):
    """Root node of the AST representing the entire program"""
    
    def __init__(self, statements: List[ASTNode], position: Optional[Position] = None):
        super().__init__(NodeType.PROGRAM, position)
        self.statements = statements
        for stmt in statements:
            self.add_child(stmt)
    
    def accept(self, visitor):
        return visitor.visit_program(self)


class StatementNode(ASTNode):
    """Base class for all statement nodes"""
    
    def __init__(self, position: Optional[Position] = None):
        super().__init__(NodeType.STATEMENT, position)


class ExpressionNode(ASTNode):
    """Base class for all expression nodes"""
    
    def __init__(self, position: Optional[Position] = None):
        super().__init__(NodeType.EXPRESSION, position)


class BlockNode(StatementNode):
    """Node representing a block of statements"""
    
    def __init__(self, statements: List[StatementNode], position: Optional[Position] = None):
        super().__init__(position)
        self.node_type = NodeType.BLOCK
        self.statements = statements
        for stmt in statements:
            self.add_child(stmt)
    
    def accept(self, visitor):
        return visitor.visit_block(self)


class AssignmentNode(StatementNode):
    """Node representing variable assignment"""
    
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
    """Node representing binary operations"""
    
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
    """Node representing unary operations"""
    
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
    """Node representing variable references"""
    
    def __init__(self, name: str, position: Optional[Position] = None):
        super().__init__(position)
        self.node_type = NodeType.VARIABLE
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_variable(self)


class LiteralNode(ExpressionNode):
    """Node representing literal values"""
    
    def __init__(self, value: Any, literal_type: str, position: Optional[Position] = None):
        super().__init__(position)
        self.node_type = NodeType.LITERAL
        self.value = value
        self.literal_type = literal_type  # "number", "string", "boolean"
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


class FunctionCallNode(ExpressionNode):
    """Node representing function calls"""
    
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
    """Node representing conditional statements (if/else)"""
    
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
    """Node representing loop statements"""
    
    def __init__(self, body: StatementNode, condition: ExpressionNode,
                 loop_type: str = "while", position: Optional[Position] = None):
        super().__init__(position)
        self.node_type = NodeType.LOOP
        self.body = body
        self.condition = condition
        self.loop_type = loop_type  # "while", "repeat_until", etc.
        
        self.add_child(body)
        self.add_child(condition)
    
    def accept(self, visitor):
        return visitor.visit_loop(self)


class PrintNode(StatementNode):
    """Node representing print statements (Wensleydale)"""
    
    def __init__(self, expression: ExpressionNode, position: Optional[Position] = None):
        super().__init__(position)
        self.expression = expression
        self.add_child(expression)
    
    def accept(self, visitor):
        return visitor.visit_print(self)


class DebugNode(StatementNode):
    """Node representing debug statements (Belgian)"""
    
    def __init__(self, position: Optional[Position] = None):
        super().__init__(position)
    
    def accept(self, visitor):
        return visitor.visit_debug(self)


class NodeVisitor(ABC):
    """
    Abstract base class for AST node visitors.
    
    Implements the visitor pattern for traversing and processing AST nodes.
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
    Utility class for traversing AST nodes.
    
    Provides methods for different traversal strategies.
    """
    
    @staticmethod
    def depth_first_search(node: ASTNode, visitor: NodeVisitor):
        """Perform depth-first traversal of AST"""
        node.accept(visitor)
        for child in node.children:
            ASTTraverser.depth_first_search(child, visitor)
    
    @staticmethod
    def breadth_first_search(node: ASTNode, visitor: NodeVisitor):
        """Perform breadth-first traversal of AST"""
        queue = [node]
        while queue:
            current = queue.pop(0)
            current.accept(visitor)
            queue.extend(current.children)
    
    @staticmethod
    def find_nodes_by_type(node: ASTNode, node_type: NodeType) -> List[ASTNode]:
        """Find all nodes of a specific type"""
        result = []
        
        def collector(n):
            if n.node_type == node_type:
                result.append(n)
        
        ASTTraverser._traverse_with_function(node, collector)
        return result
    
    @staticmethod
    def _traverse_with_function(node: ASTNode, func):
        """Helper method for traversal with custom function"""
        func(node)
        for child in node.children:
            ASTTraverser._traverse_with_function(child, func)


class ASTBuilder:
    """
    Utility class for building AST nodes.
    
    Provides factory methods for creating common node patterns.
    """
    
    @staticmethod
    def create_program(statements: List[StatementNode]) -> ProgramNode:
        """Create a program node with statements"""
        return ProgramNode(statements)
    
    @staticmethod
    def create_assignment(variable: str, value: ExpressionNode, 
                         assignment_type: str = "=") -> AssignmentNode:
        """Create an assignment node"""
        return AssignmentNode(variable, value, assignment_type)
    
    @staticmethod
    def create_binary_op(left: ExpressionNode, operator: str, 
                        right: ExpressionNode) -> BinaryOpNode:
        """Create a binary operation node"""
        return BinaryOpNode(left, operator, right)
    
    @staticmethod
    def create_literal(value: Any, literal_type: str) -> LiteralNode:
        """Create a literal node"""
        return LiteralNode(value, literal_type)
    
    @staticmethod
    def create_variable(name: str) -> VariableNode:
        """Create a variable node"""
        return VariableNode(name)
    
    @staticmethod
    def create_function_call(name: str, arguments: List[ExpressionNode]) -> FunctionCallNode:
        """Create a function call node"""
        return FunctionCallNode(name, arguments)
    
    @staticmethod
    def create_conditional(condition: ExpressionNode, then_branch: StatementNode,
                          else_branch: Optional[StatementNode] = None) -> ConditionalNode:
        """Create a conditional node"""
        return ConditionalNode(condition, then_branch, else_branch)
    
    @staticmethod
    def create_loop(body: StatementNode, condition: ExpressionNode,
                   loop_type: str = "while") -> LoopNode:
        """Create a loop node"""
        return LoopNode(body, condition, loop_type)


def ast_to_dict(node: ASTNode) -> Dict[str, Any]:
    """Convert AST node to dictionary representation"""
    result = {
        'type': node.node_type.value,
        'class': node.__class__.__name__,
        'position': str(node.position) if node.position else None,
        'children': []
    }
    
    # Add node-specific attributes
    if hasattr(node, 'value'):
        result['value'] = node.value
    if hasattr(node, 'name'):
        result['name'] = node.name
    if hasattr(node, 'operator'):
        result['operator'] = node.operator
    if hasattr(node, 'variable'):
        result['variable'] = node.variable
    
    # Add children
    for child in node.children:
        result['children'].append(ast_to_dict(child))
    
    return result


def dict_to_ast(data: Dict[str, Any]) -> ASTNode:
    """Convert dictionary representation back to AST node"""
    # This is a simplified version - in practice, you'd need more sophisticated reconstruction
    node_type = NodeType(data['type'])
    
    # Create appropriate node based on type
    if node_type == NodeType.PROGRAM:
        return ProgramNode([])
    elif node_type == NodeType.LITERAL:
        return LiteralNode(data.get('value'), data.get('literal_type', 'unknown'))
    elif node_type == NodeType.VARIABLE:
        return VariableNode(data.get('name', ''))
    # Add more node types as needed
    
    return None
