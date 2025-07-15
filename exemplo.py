from cheesepp.parser import parse
from cheesepp.runtime import Runtime
import sys
import os
import glob

def run_cheesepp_file(filename):
    """Executa um arquivo .cheesepp"""
    try:
        # Lê o arquivo
        with open(filename, 'r', encoding='utf-8') as file:
            code = file.read()
        
        print(f"Executando arquivo: {filename}")
        print("=" * 50)
        
        # Executa o código
        rt = Runtime()
        rt.run(parse(code), code)
        
        print("=" * 50)
        print("Execução concluída!")
        print()
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado!")
    except Exception as e:
        print(f"Erro na execução: {e}")
        print()

def run_all_examples():
    """Executa todos os arquivos .cheesepp da pasta exemplos"""
    exemplo_files = glob.glob("exemplos/*.cheesepp")
    exemplo_files.sort()  # Ordena os arquivos
    
    if not exemplo_files:
        print("Nenhum arquivo .cheesepp encontrado na pasta exemplos/")
        return
    
    print(f"Executando {len(exemplo_files)} exemplos Cheese++")
    print("=" * 60)
    print()
    
    for i, filename in enumerate(exemplo_files, 1):
        print(f"Exemplo {i}/{len(exemplo_files)}")
        run_cheesepp_file(filename)
        
        # Pausa entre exemplos (opcional)
        if i < len(exemplo_files):
            input("Pressione Enter para continuar para o próximo exemplo...")
            print()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Sem argumentos: roda todos os exemplos
        run_all_examples()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "all" or sys.argv[1] == "a":
            # Flag --all: roda todos os exemplos
            run_all_examples()
        else:
            # Arquivo específico
            run_cheesepp_file(sys.argv[1])
    else:
        print("Uso:")
        print("  python exemplo.py                           # Roda todos os exemplos")
        print("  python exemplo.py --all                     # Roda todos os exemplos")
        print("  python exemplo.py <arquivo.cheesepp>        # Roda exemplo específico")
        print()
        print("Exemplos:")
        print("  python exemplo.py                           # Todos")
        print("  python exemplo.py exemplos/exemplo_01.cheesepp  # Específico")