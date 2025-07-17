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
    Compilar e executar o código-fonte do Cheese++.
    
    Args:
        source_code (str): O código-fonte do Cheese++ a ser compilado e executado
        debug (bool): Se deve ativar o modo de depuração
        
    Retorna:
        str: A saída da execução do programa
        
    Levanta:
        CheeseError: Se a compilação ou a execução falhar
    """
    try:
        ast = parse(source_code)
        runtime = Runtime()    
        runtime.run(ast, source_code)
        
        return runtime.env.get('__output__', '')
        
    except Exception as e:
        raise CheeseError(f"Falha de interpretação: {str(e)}")



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