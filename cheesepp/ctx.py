from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class SymbolType(Enum):
    """Enumeração de tipos em Cheese++"""
    VARIABLE = "variable"
    FUNCTION = "function"
    CONSTANT = "constant"


@dataclass
class Symbol:
    """Representa um símbolo na tabela de símbolos"""
    name: str
    type: SymbolType
    value: Any
    scope_level: int
    line_number: Optional[int] = None
    
    def __repr__(self):
        return f"Simbolo({self.name}, {self.type.value}, {self.value}, scope={self.scope_level})"


class SymbolTable:
    """
    Implementação de tabela de símbolos para o interpretador Cheese++.
    Gerencia declarações de variáveis, pesquisas e gerenciamento de escopo.
    """
    
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}
        self.scope_stack: List[int] = [0]  
        self.current_scope: int = 0
        
    def enter_scope(self) -> None:
        """Entra em um novo escopo"""
        self.current_scope += 1
        self.scope_stack.append(self.current_scope)
        
    def exit_scope(self) -> None:
        """Sair do escopo atual e remover símbolos desse escopo"""
        if len(self.scope_stack) > 1:
            exiting_scope = self.scope_stack.pop()
            
            to_remove = [name for name, symbol in self.symbols.items() 
                        if symbol.scope_level == exiting_scope]
            for name in to_remove:
                del self.symbols[name]
            self.current_scope = self.scope_stack[-1]
    
    def define(self, name: str, symbol_type: SymbolType, value: Any, 
               line_number: Optional[int] = None) -> bool:
        """
        Define um novo símbolo no escopo atual.
        Retorna True se for bem sucedido, False se o símbolo já existir no escopo atual.
        """
        # Checka se um simbolo existe no escopo atual
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
        """Pesquisar um símbolo na tabela de símbolos (pesquisar do escopo atual para cima)"""
        
        for scope_level in reversed(self.scope_stack):
            if name in self.symbols:
                symbol = self.symbols[name]
                if symbol.scope_level <= scope_level:
                    return symbol
        return None
    
    def update(self, name: str, value: Any) -> bool:
        """Atualizar o valor de um símbolo existente"""
        symbol = self.lookup(name)
        if symbol:
            symbol.value = value
            return True
        return False
    
    def get_all_symbols(self) -> Dict[str, Symbol]:
        """Pegar todos os símbolos no contexto atual"""
        return self.symbols.copy()
    
    def __repr__(self):
        return f"SymbolTable(scope={self.current_scope}, symbols={len(self.symbols)})"


class ExecutionContext:
    """
    Contexto de execução para o tempo de execução do Cheese++.
    Gerencia o ambiente de execução, incluindo tabelas de símbolos e estado do tempo de execução.
    """
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.output_buffer: List[str] = []
        self.error_messages: List[str] = []
        self.debug_mode: bool = False
        self.source_code: Optional[str] = None
        self.current_line: int = 1
        
    def set_source_code(self, source: str) -> None:
        """Seta o código-fonte atual para o contexto de execução"""
        self.source_code = source
        
    def add_output(self, message: str) -> None:
        """Adicionar mensagem de saída ao buffer de saída"""
        self.output_buffer.append(str(message))
        
    def add_error(self, message: str, line_number: Optional[int] = None) -> None:
        """Adicionar mensagem de erro ao buffer de erros"""
        if line_number:
            error_msg = f"Line {line_number}: {message}"
        else:
            error_msg = message
        self.error_messages.append(error_msg)
        
    def get_output(self) -> str:
        """Pegar toda a saída acumulada"""
        return '\n'.join(self.output_buffer)
        
    def get_errors(self) -> List[str]:
        """Pegar todas as mensagens de erro"""
        return self.error_messages.copy()
        
    def has_errors(self) -> bool:
        """Checka se existe algum erro no contexto de execução"""
        return len(self.error_messages) > 0
        
    def clear_output(self) -> None:
        self.output_buffer.clear()
        
    def clear_errors(self) -> None:
        self.error_messages.clear()
        
    def reset(self) -> None:
        """Reseta o contexto de execução"""
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
    Classe de contexto principal para o compilador e o tempo de execução do Cheese++.
    Fornece uma interface unificada para gerenciar o contexto de compilação e execução.
    """
    
    def __init__(self):
        self.execution_context = ExecutionContext()
        self.compilation_phase = "lexical"  
        self.statistics = {
            "variables_declared": 0,
            "functions_called": 0,
            "expressions_evaluated": 0,
            "statements_executed": 0
        }
        
    def set_compilation_phase(self, phase: str) -> None:
        """Definir a fase de compilação atual"""
        self.compilation_phase = phase
        
    def increment_stat(self, stat_name: str) -> None:
        """Incrementar um contador de stats"""
        if stat_name in self.statistics:
            self.statistics[stat_name] += 1
            
    def get_statistics(self) -> Dict[str, int]:
        return self.statistics.copy()
        
    def declare_variable(self, name: str, value: Any, line_number: Optional[int] = None) -> bool:
        """Declaração de variável no contexto"""
        success = self.execution_context.symbol_table.define(
            name, SymbolType.VARIABLE, value, line_number
        )
        if success:
            self.increment_stat("variables_declared")
        return success
        
    def get_variable(self, name: str) -> Any:
        """Pega uma variável do contexto"""
        symbol = self.execution_context.symbol_table.lookup(name)
        return symbol.value if symbol else None
        
    def set_variable(self, name: str, value: Any) -> bool:
        """Seta o valor de uma variável existente"""
        return self.execution_context.symbol_table.update(name, value)
        
    def execute_print(self, value: Any) -> None:
        """Executa uma operação de impressão"""
        self.execution_context.add_output(str(value))
        self.increment_stat("statements_executed")
        
    def execute_belgian(self) -> None:
        """Executa o comando Belgian"""
        if self.execution_context.source_code:
            self.execution_context.add_output("=== Belgian Mode ===")
            self.execution_context.add_output(self.execution_context.source_code)
        else:
            self.execution_context.add_output("No source available.")
        self.increment_stat("statements_executed")
        
    def get_output(self) -> str:
        """Obter toda a saída da execução"""
        return self.execution_context.get_output()
        
    def has_errors(self) -> bool:
        """Verificar se há erros de compilação ou de tempo de execução"""
        return self.execution_context.has_errors()
        
    def get_errors(self) -> List[str]:
        """Pega todas as mensagens de erro do contexto de execução"""
        return self.execution_context.get_errors()
        
    def reset(self) -> None:
        """Reseta o contexto"""
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
