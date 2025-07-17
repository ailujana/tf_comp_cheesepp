import sys
import os
import argparse
from typing import Optional, List
from pathlib import Path

from .parser import parse
from .runtime import Runtime
from .ctx import CheeseContext
from .errors import CheeseError, ErrorReporter
from . import __version__, __author__


class CheeseREPL:
    """
        Estrutura de repetição Read-Eval-Print para programação interativa Cheese++.
    """
    
    def __init__(self, debug: bool = False):
        self.context = CheeseContext()
        self.runtime = Runtime()
        self.debug = debug
        self.history: List[str] = []
        
        
    def help_message(self):
        """Display help message"""
        print("Cheese++ Commands:")
        print("  help          - Show this help message")
        print("  exit          - Exit the interactive shell")
        print("  clear         - Clear the screen")
        print("  history       - Show command history")
        print("  debug on/off  - Toggle debug mode")
        print("  vars          - Show current variables")
        print("  reset         - Reset the environment")
        print("\nCheesepp++ Language Reference:")
        print("  Cheese        - Start program")
        print("  NoCheese      - End program")
        print("  Wensleydale() - Print function")
        print("  Swiss...Swiss - String literals")
        print("  Glyn()        - Variable function")
        print("  Brie          - Statement terminator")
        
    def show_variables(self):
        """Show current variables"""
        symbols = self.context.execution_context.symbol_table.get_all_symbols()
        if symbols:
            print("Current variables:")
            for name, symbol in symbols.items():
                print(f"  {name} = {symbol.value} (scope: {symbol.scope_level})")
        else:
            print("No variables defined")
            
    def show_history(self):
        """Show command history"""
        if self.history:
            print("Command history:")
            for i, cmd in enumerate(self.history, 1):
                print(f"  {i}: {cmd}")
        else:
            print("No command history")
            
    def execute_line(self, line: str) -> bool:
        """
        Executa uma linha de código do Cheese++.
        Retorna True para continuar, False para sair
        """
        line = line.strip()
        
        if line.lower() == 'exit':
            return False
        elif line.lower() == 'help':
            self.help_message()
            return True
        elif line.lower() == 'clear':
            os.system('clear' if os.name == 'posix' else 'cls')
            return True
        elif line.lower() == 'history':
            self.show_history()
            return True
        elif line.lower() == 'vars':
            self.show_variables()
            return True
        elif line.lower() == 'reset':
            self.context.reset()
            self.runtime = Runtime()
            print("Reset de ambiente realizado")
            return True
        elif line.lower().startswith('debug '):
            mode = line.lower().split()[1]
            if mode == 'on':
                self.debug = True
                print("Modo de debug ativado")
            elif mode == 'off':
                self.debug = False
                print("Modo de debug desativado")
            else:
                print("Uso: debug on/off")
            return True
        elif line == '':
            return True
            
        self.history.append(line)
        
        # Tentativa de execução do código
        try:
            # Parse e execução
            ast = parse(line)
            self.context.execution_context.set_source_code(line)
            result = self.runtime.run(ast, line)
            
            # Mostra o resultado da execução, se possível
            if result is not None:
                print(result)
                
            # Mostra a saída do ambiente, se tiver uma
            output = self.context.get_output()
            if output:
                print(output)
                
        except CheeseError as e:
            print(f"Error: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
        except Exception as e:
            print(f"Unexpected error: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
                
        return True
        
    def run(self):
        """Run the REPL"""
        self.welcome_message()
        
        while True:
            try:
                line = input("cheese++> ")
                if not self.execute_line(line):
                    break
            except EOFError:
                print("\nGoodbye!")
                break
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
                continue


def execute_file(filename: str, debug: bool = False, verbose: bool = False) -> int:
    """
    Executa um arquivo Cheese++.
    
    Args:
        filename: Caminho para o arquivo Cheese++
        debug: Habilita o modo de depuração
        verbose: Habilita a saída detalhada
        
    Retorna:
        Código de saída (0 para sucesso, 1 para erro)
    """
    try:
        # Verifica se o arquivo existe
        if not Path(filename).exists():
            print(f"Error: File '{filename}' not found")
            return 1
            
        # Le o arquivo
        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
            
        if verbose:
            print(f"Executing file: {filename}")
            print(f"Source code length: {len(source_code)} characters")
            
        # Cria um ambiente de execução e contexto
        context = CheeseContext()
        runtime = Runtime()
        error_reporter = ErrorReporter()
        
        # Parse e executa
        try:
            ast = parse(source_code)
            context.execution_context.set_source_code(source_code)
            result = runtime.run(ast, source_code)
            
            # Mostra a saida do resultado, se houver
            output = context.get_output()
            if output:
                print(output)
                
            if verbose:
                print(f"Execution completed successfully")
                stats = context.get_statistics()
                print(f"Statistics: {stats}")
                
            return 0
            
        except CheeseError as e:
            print(f"Compilation error: {e}")
            if debug:
                import traceback
                traceback.print_exc()
            return 1
            
    except Exception as e:
        print(f"Error reading file: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        return 1


def main():
    parser = argparse.ArgumentParser(
        description=f"Cheese++ Compiler v{__version__}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cheesepp                    # Inicia um terminal interativo
  cheesepp program.cheesepp   # Executa um arquivo Cheese++
  cheesepp -d program.cheesepp # Executa com o modo de depuração
  cheesepp -v program.cheesepp # Executa com saída detalhada
        """
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='Cheese++ file to execute (if not provided, starts REPL)'
    )
    
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'Cheese++ {__version__}'
    )
    
    args = parser.parse_args()
    
    if args.file:
        exit_code = execute_file(args.file, args.debug, args.verbose)
        sys.exit(exit_code)
    else:
        repl = CheeseREPL(debug=args.debug)
        repl.run()


if __name__ == '__main__':
    main()