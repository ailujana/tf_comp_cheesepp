import sys
from cheesepp.parser import parse
from cheesepp.runtime import Runtime

def main():
    rt = Runtime()
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            code = f.read()
            rt.run(parse(code))
    else:
        while True:
            try:
                line = input("cheese++> ")
                result = rt.run(parse(line))
                if result is not None:
                    print(result)
            except EOFError:
                break