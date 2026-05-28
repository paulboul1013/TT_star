from lex import *
from parse import *
import sys

def main():
    print("TT Compiler")

    if len(sys.argv)!=2:
        sys.exit("Error: need input source file")
    
    with open(sys.argv[1],'r') as input_file:
        source = input_file.read()

    lexer=Lexer(source)
    parser=Parser(lexer)

    parser.program()
    print("parsing completed")
    

main()