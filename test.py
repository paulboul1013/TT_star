from lex import *
from parse import *
from emit import *
import sys

def main():
    print("TT Compiler")

    if len(sys.argv)!=2:
        sys.exit("Error: need input source file")
    
    with open(sys.argv[1],'r') as input_file:
        source = input_file.read()

    lexer=Lexer(source)
    emitter=Emitter("out.c")
    parser=Parser(lexer,emitter)

    parser.program() # start parsing
    emitter.write_file() # write the output to file
    print("parsing completed")
    

main()