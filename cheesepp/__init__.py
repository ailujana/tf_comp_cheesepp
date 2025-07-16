from .parser import parse
from .runtime import Runtime
from .ctx import CheeseContext, ExecutionContext, SymbolTable
from .errors import (
    CheeseError, CheeseLexicalError, CheeseSyntaxError, 
    CheeseSemanticError, CheeseRuntimeError, CheeseTypeError,
    ErrorReporter
)
from .ast import *

def compile_and_run(source_code: str, debug: bool = False) -> str:
    """
    Compile and run Cheese++ source code.
    
    Args:
        source_code (str): The Cheese++ source code to compile and execute
        debug (bool): Whether to enable debug mode
        
    Returns:
        str: The output of the program execution
        
    Raises:
        CheeseError: If compilation or execution fails
    """
    try:
        ast = parse(source_code)
        runtime = Runtime()    
        runtime.run(ast, source_code)
        
        return runtime.env.get('__output__', '')
        
    except Exception as e:
        raise CheeseError(f"Compilation failed: {str(e)}")



# Package exports
__all__ = [
    'parse', 'compile_and_run',
    'Runtime',
    'CheeseContext', 'ExecutionContext', 'SymbolTable',
    'CheeseError', 'CheeseLexicalError', 'CheeseSyntaxError',
    'CheeseSemanticError', 'CheeseRuntimeError', 'CheeseTypeError',
    'ErrorReporter',
    'CheeseAssign', 'BinOp', 'Number', 'Var', 'CheesePrint',
    'String', 'CheeseIf', 'CheeseLoop', 'Belgian',
]