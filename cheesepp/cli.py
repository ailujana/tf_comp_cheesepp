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
    Read-Eval-Print Loop for interactive Cheese++ programming.
    """
    
    def __init__(self, debug: bool = False):
        self.context = CheeseContext()
        self.runtime = Runtime()
        self.debug = debug
        self.history: List[str] = []
        
    def welcome_message(self):
        """Display welcome message"""
        print(f"Cheese++ Interactive Shell v{__version__}")
        print(f"Authors: {__author__}")
        print("Type 'help' for help, 'exit' to quit")
        print("=" * 50)
        
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
        Execute a line of Cheese++ code.
        Returns True to continue, False to exit.
        """
        line = line.strip()
        
        # Handle special commands
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
            print("Environment reset")
            return True
        elif line.lower().startswith('debug '):
            mode = line.lower().split()[1]
            if mode == 'on':
                self.debug = True
                print("Debug mode enabled")
            elif mode == 'off':
                self.debug = False
                print("Debug mode disabled")
            else:
                print("Usage: debug on/off")
            return True
        elif line == '':
            return True
            
        # Add to history
        self.history.append(line)
        
        # Try to execute Cheese++ code
        try:
            # Parse and execute
            ast = parse(line)
            self.context.execution_context.set_source_code(line)
            result = self.runtime.run(ast, line)
            
            # Show result if available
            if result is not None:
                print(result)
                
            # Show output if any
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
    Execute a Cheese++ file.
    
    Args:
        filename: Path to the Cheese++ file
        debug: Enable debug mode
        verbose: Enable verbose output
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Check if file exists
        if not Path(filename).exists():
            print(f"Error: File '{filename}' not found")
            return 1
            
        # Read file
        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
            
        if verbose:
            print(f"Executing file: {filename}")
            print(f"Source code length: {len(source_code)} characters")
            
        # Create runtime environment
        context = CheeseContext()
        runtime = Runtime()
        error_reporter = ErrorReporter()
        
        # Parse and execute
        try:
            ast = parse(source_code)
            context.execution_context.set_source_code(source_code)
            result = runtime.run(ast, source_code)
            
            # Show output
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
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        description=f"Cheese++ Compiler v{__version__}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cheesepp                    # Start interactive shell
  cheesepp program.cheesepp   # Execute file
  cheesepp -d program.cheesepp # Execute with debug mode
  cheesepp -v program.cheesepp # Execute with verbose output
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
    
    # Execute file or start REPL
    if args.file:
        exit_code = execute_file(args.file, args.debug, args.verbose)
        sys.exit(exit_code)
    else:
        # Start REPL
        repl = CheeseREPL(debug=args.debug)
        repl.run()


if __name__ == '__main__':
    main()