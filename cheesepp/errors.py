from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class ErrorType(Enum):
    """Enumeração de diferentes tipos de erros no Cheese++"""
    LEXICAL = "lexical"
    SYNTAX = "syntax"
    SEMANTIC = "semantic"
    RUNTIME = "runtime"
    TYPE = "type"


@dataclass
class ErrorInfo:
    """Estrutura para armazenar informações de erro"""
    error_type: ErrorType
    message: str
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    context: Optional[str] = None
    suggestions: Optional[List[str]] = None
    
    def __str__(self):
        result = f"{self.error_type.value.upper()} ERROR: {self.message}"
        if self.line_number:
            result += f" at line {self.line_number}"
            if self.column_number:
                result += f", column {self.column_number}"
        if self.context:
            result += f"\nContext: {self.context}"
        if self.suggestions:
            result += f"\nSuggestions: {', '.join(self.suggestions)}"
        return result


class CheeseError(Exception):
    """Classe de exceção básica para todos os erros do Cheese++"""
    
    def __init__(self, message: str, error_type: ErrorType = ErrorType.RUNTIME,
                 line_number: Optional[int] = None, column_number: Optional[int] = None,
                 context: Optional[str] = None, suggestions: Optional[List[str]] = None):
        self.error_info = ErrorInfo(
            error_type=error_type,
            message=message,
            line_number=line_number,
            column_number=column_number,
            context=context,
            suggestions=suggestions
        )
        super().__init__(str(self.error_info))


class CheeseLexicalError(CheeseError):
    """Erros de análise léxica"""
    
    def __init__(self, message: str, line_number: Optional[int] = None,
                 column_number: Optional[int] = None, context: Optional[str] = None):
        super().__init__(message, ErrorType.LEXICAL, line_number, column_number, context)


class CheeseSyntaxError(CheeseError):
    """Erros de análise sintática"""
    
    def __init__(self, message: str, line_number: Optional[int] = None,
                 column_number: Optional[int] = None, context: Optional[str] = None,
                 suggestions: Optional[List[str]] = None):
        super().__init__(message, ErrorType.SYNTAX, line_number, column_number, context, suggestions)


class CheeseSemanticError(CheeseError):
    """Erros semânticos"""
    
    def __init__(self, message: str, line_number: Optional[int] = None,
                 column_number: Optional[int] = None, context: Optional[str] = None,
                 suggestions: Optional[List[str]] = None):
        super().__init__(message, ErrorType.SEMANTIC, line_number, column_number, context, suggestions)


class CheeseRuntimeError(CheeseError):
    """Erros de tempo de execução"""
    
    def __init__(self, message: str, line_number: Optional[int] = None,
                 column_number: Optional[int] = None, context: Optional[str] = None,
                 suggestions: Optional[List[str]] = None):
        super().__init__(message, ErrorType.RUNTIME, line_number, column_number, context, suggestions)


class CheeseTypeError(CheeseError):
    """Erros de tipo"""
    
    def __init__(self, message: str, line_number: Optional[int] = None,
                 column_number: Optional[int] = None, context: Optional[str] = None,
                 suggestions: Optional[List[str]] = None):
        super().__init__(message, ErrorType.TYPE, line_number, column_number, context, suggestions)


class ErrorReporter:
    """
    Sistema de gerenciamento e relatório de erros para o compilador Cheese++.
    Coleta, formata e relata erros durante a compilação e a execução.
    """
    
    def __init__(self):
        self.errors: List[CheeseError] = []
        self.warnings: List[str] = []
        self.max_errors = 10  
        
    def report_error(self, error: CheeseError) -> None:
        """Reporta um erro"""
        self.errors.append(error)
        
    def report_lexical_error(self, message: str, line_number: Optional[int] = None,
                           column_number: Optional[int] = None, context: Optional[str] = None) -> None:
        """Reporta um erro léxico"""
        error = CheeseLexicalError(message, line_number, column_number, context)
        self.report_error(error)
        
    def report_syntax_error(self, message: str, line_number: Optional[int] = None,
                          column_number: Optional[int] = None, context: Optional[str] = None,
                          suggestions: Optional[List[str]] = None) -> None:
        """Reporta um erro de sintaxe"""
        error = CheeseSyntaxError(message, line_number, column_number, context, suggestions)
        self.report_error(error)
        
    def report_semantic_error(self, message: str, line_number: Optional[int] = None,
                            column_number: Optional[int] = None, context: Optional[str] = None,
                            suggestions: Optional[List[str]] = None) -> None:
        """Reporta um erro semântico"""
        error = CheeseSemanticError(message, line_number, column_number, context, suggestions)
        self.report_error(error)
        
    def report_runtime_error(self, message: str, line_number: Optional[int] = None,
                           column_number: Optional[int] = None, context: Optional[str] = None,
                           suggestions: Optional[List[str]] = None) -> None:
        """Reporta um erro de tempo de execução"""
        error = CheeseRuntimeError(message, line_number, column_number, context, suggestions)
        self.report_error(error)
        
    def report_type_error(self, message: str, line_number: Optional[int] = None,
                         column_number: Optional[int] = None, context: Optional[str] = None,
                         suggestions: Optional[List[str]] = None) -> None:
        """Reporta um erro de tipo"""
        error = CheeseTypeError(message, line_number, column_number, context, suggestions)
        self.report_error(error)
        
    def report_warning(self, message: str) -> None:
        """Reporta um aviso"""
        self.warnings.append(message)
        
    def has_errors(self) -> bool:
        """Checka se existe algum erro"""
        return len(self.errors) > 0
        
    def has_warnings(self) -> bool:
        """Checka se existe algum aviso"""
        return len(self.warnings) > 0
        
    def get_error_count(self) -> int:
        """Pega o número de erros"""
        return len(self.errors)
        
    def get_warning_count(self) -> int:
        """Pega o número de avisos"""
        return len(self.warnings)
        
    def should_stop_compilation(self) -> bool:
        """Verificar se a compilação deve ser interrompida devido ao excesso de erros"""
        return len(self.errors) >= self.max_errors
        
    def get_errors_by_type(self, error_type: ErrorType) -> List[CheeseError]:
        """Pega erros de um tipo específico"""
        return [error for error in self.errors if error.error_info.error_type == error_type]
        
    def get_formatted_errors(self) -> str:
        """Obter todos os erros formatados como uma string"""
        if not self.errors:
            return "Não foram encontrados erros"
            
        result = f"Encontrados {len(self.errors)} erro(s):\n"
        for i, error in enumerate(self.errors, 1):
            result += f"{i}. {error}\n"
            
        return result
        
    def get_formatted_warnings(self) -> str:
        """Obter todos os avisos formatados como uma string"""
        if not self.warnings:
            return "Não foram encontrados avisos"
            
        result = f"Encontrados {len(self.warnings)} alerta(s):\n"
        for i, warning in enumerate(self.warnings, 1):
            result += f"{i}. WARNING: {warning}\n"
            
        return result
        
    def get_summary(self) -> str:
        """Obter um resumo de todos os erros e avisos"""
        summary = f"Compilation Summary:\n"
        summary += f"- Errors: {len(self.errors)}\n"
        summary += f"- Warnings: {len(self.warnings)}\n"
        
        if self.errors:
            summary += f"\nErros por tipo:\n"
            for error_type in ErrorType:
                count = len(self.get_errors_by_type(error_type))
                if count > 0:
                    summary += f"- {error_type.value.title()}: {count}\n"
                    
        return summary
        
    def clear(self) -> None:
        """Limpar todos os erros e avisos"""
        self.errors.clear()
        self.warnings.clear()
        
    def __repr__(self):
        return f"ErrorReporter(errors={len(self.errors)}, warnings={len(self.warnings)})"



ERROR_MESSAGES = {
    "undefined_variable": "Variable '{var_name}' is not defined",
    "redefined_variable": "Variable '{var_name}' is already defined",
    "invalid_operation": "Invalid operation '{op}' between {type1} and {type2}",
    "missing_cheese": "Missing 'Cheese' at the beginning of the program",
    "missing_nocheese": "Missing 'NoCheese' at the end of the program",
    "missing_brie": "Missing 'Brie' statement terminator",
    "invalid_swiss": "Invalid Swiss string format",
    "division_by_zero": "Division by zero",
    "invalid_syntax": "Invalid syntax near '{token}'",
}

SUGGESTIONS = {
    "undefined_variable": ["Check variable name spelling", "Ensure variable is declared before use"],
    "missing_cheese": ["Add 'Cheese' at the beginning of your program"],
    "missing_nocheese": ["Add 'NoCheese' at the end of your program"],
    "missing_brie": ["Add 'Brie' at the end of the statement"],
    "invalid_swiss": ["Use Swiss...Swiss format for strings"],
}
