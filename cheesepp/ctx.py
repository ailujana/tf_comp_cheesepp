from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class SymbolType(Enum):
    """Enumeration for symbol types in Cheese++"""
    VARIABLE = "variable"
    FUNCTION = "function"
    CONSTANT = "constant"


@dataclass
class Symbol:
    """Represents a symbol in the symbol table"""
    name: str
    type: SymbolType
    value: Any
    scope_level: int
    line_number: Optional[int] = None
    
    def __repr__(self):
        return f"Symbol({self.name}, {self.type.value}, {self.value}, scope={self.scope_level})"


class SymbolTable:
    """
    Symbol table implementation for the Cheese++ compiler.
    Manages variable declarations, lookups, and scope management.
    """
    
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}
        self.scope_stack: List[int] = [0]  # Global scope starts at 0
        self.current_scope: int = 0
        
    def enter_scope(self) -> None:
        """Enter a new scope level"""
        self.current_scope += 1
        self.scope_stack.append(self.current_scope)
        
    def exit_scope(self) -> None:
        """Exit current scope and remove symbols from that scope"""
        if len(self.scope_stack) > 1:
            exiting_scope = self.scope_stack.pop()
            # Remove symbols from exiting scope
            to_remove = [name for name, symbol in self.symbols.items() 
                        if symbol.scope_level == exiting_scope]
            for name in to_remove:
                del self.symbols[name]
            self.current_scope = self.scope_stack[-1]
    
    def define(self, name: str, symbol_type: SymbolType, value: Any, 
               line_number: Optional[int] = None) -> bool:
        """
        Define a new symbol in the current scope.
        Returns True if successful, False if symbol already exists in current scope.
        """
        # Check if symbol already exists in current scope
        if name in self.symbols and self.symbols[name].scope_level == self.current_scope:
            return False
            
        self.symbols[name] = Symbol(
            name=name,
            type=symbol_type,
            value=value,
            scope_level=self.current_scope,
            line_number=line_number
        )
        return True
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Lookup a symbol in the symbol table (search from current scope upwards)"""
        # Look for symbol in current and parent scopes
        for scope_level in reversed(self.scope_stack):
            if name in self.symbols:
                symbol = self.symbols[name]
                if symbol.scope_level <= scope_level:
                    return symbol
        return None
    
    def update(self, name: str, value: Any) -> bool:
        """Update the value of an existing symbol"""
        symbol = self.lookup(name)
        if symbol:
            symbol.value = value
            return True
        return False
    
    def get_all_symbols(self) -> Dict[str, Symbol]:
        """Get all symbols in the current context"""
        return self.symbols.copy()
    
    def __repr__(self):
        return f"SymbolTable(scope={self.current_scope}, symbols={len(self.symbols)})"


class ExecutionContext:
    """
    Execution context for the Cheese++ runtime.
    Manages the execution environment, including symbol tables and runtime state.
    """
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.output_buffer: List[str] = []
        self.error_messages: List[str] = []
        self.debug_mode: bool = False
        self.source_code: Optional[str] = None
        self.current_line: int = 1
        
    def set_source_code(self, source: str) -> None:
        """Set the source code for debugging purposes"""
        self.source_code = source
        
    def add_output(self, message: str) -> None:
        """Add message to output buffer"""
        self.output_buffer.append(str(message))
        
    def add_error(self, message: str, line_number: Optional[int] = None) -> None:
        """Add error message to error buffer"""
        if line_number:
            error_msg = f"Line {line_number}: {message}"
        else:
            error_msg = message
        self.error_messages.append(error_msg)
        
    def get_output(self) -> str:
        """Get all output as a single string"""
        return '\n'.join(self.output_buffer)
        
    def get_errors(self) -> List[str]:
        """Get all error messages"""
        return self.error_messages.copy()
        
    def has_errors(self) -> bool:
        """Check if there are any errors"""
        return len(self.error_messages) > 0
        
    def clear_output(self) -> None:
        """Clear the output buffer"""
        self.output_buffer.clear()
        
    def clear_errors(self) -> None:
        """Clear error messages"""
        self.error_messages.clear()
        
    def reset(self) -> None:
        """Reset the execution context"""
        self.symbol_table = SymbolTable()
        self.output_buffer.clear()
        self.error_messages.clear()
        self.current_line = 1
        
    def __repr__(self):
        return (f"ExecutionContext(symbols={len(self.symbol_table.symbols)}, "
                f"output_lines={len(self.output_buffer)}, "
                f"errors={len(self.error_messages)})")


class CheeseContext:
    """
    Main context class for the Cheese++ compiler and runtime.
    Provides a unified interface for managing compilation and execution context.
    """
    
    def __init__(self):
        self.execution_context = ExecutionContext()
        self.compilation_phase = "lexical"  # lexical, syntax, semantic, execution
        self.statistics = {
            "variables_declared": 0,
            "functions_called": 0,
            "expressions_evaluated": 0,
            "statements_executed": 0
        }
        
    def set_compilation_phase(self, phase: str) -> None:
        """Set the current compilation phase"""
        self.compilation_phase = phase
        
    def increment_stat(self, stat_name: str) -> None:
        """Increment a statistic counter"""
        if stat_name in self.statistics:
            self.statistics[stat_name] += 1
            
    def get_statistics(self) -> Dict[str, int]:
        """Get compilation/execution statistics"""
        return self.statistics.copy()
        
    def declare_variable(self, name: str, value: Any, line_number: Optional[int] = None) -> bool:
        """Declare a variable in the current context"""
        success = self.execution_context.symbol_table.define(
            name, SymbolType.VARIABLE, value, line_number
        )
        if success:
            self.increment_stat("variables_declared")
        return success
        
    def get_variable(self, name: str) -> Any:
        """Get variable value from context"""
        symbol = self.execution_context.symbol_table.lookup(name)
        return symbol.value if symbol else None
        
    def set_variable(self, name: str, value: Any) -> bool:
        """Set variable value in context"""
        return self.execution_context.symbol_table.update(name, value)
        
    def execute_print(self, value: Any) -> None:
        """Execute a print statement"""
        self.execution_context.add_output(str(value))
        self.increment_stat("statements_executed")
        
    def execute_belgian(self) -> None:
        """Execute the Belgian command (print source code)"""
        if self.execution_context.source_code:
            self.execution_context.add_output("=== Belgian Mode ===")
            self.execution_context.add_output(self.execution_context.source_code)
        else:
            self.execution_context.add_output("No source available.")
        self.increment_stat("statements_executed")
        
    def get_output(self) -> str:
        """Get all output from execution"""
        return self.execution_context.get_output()
        
    def has_errors(self) -> bool:
        """Check if there are compilation or runtime errors"""
        return self.execution_context.has_errors()
        
    def get_errors(self) -> List[str]:
        """Get all error messages"""
        return self.execution_context.get_errors()
        
    def reset(self) -> None:
        """Reset the entire context"""
        self.execution_context.reset()
        self.compilation_phase = "lexical"
        self.statistics = {
            "variables_declared": 0,
            "functions_called": 0,
            "expressions_evaluated": 0,
            "statements_executed": 0
        }
        
    def __repr__(self):
        return (f"CheeseContext(phase={self.compilation_phase}, "
                f"vars={self.statistics['variables_declared']}, "
                f"stmts={self.statistics['statements_executed']})")
