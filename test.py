from lex import *


def main():
    source = "# +-*/= \n #+-*/= #this is comment "
    lexer = Lexer(source)

    token=lexer.get_token()
    while token.kind!=Token_Type.EOF:
        print(token.kind)
        token=lexer.get_token()

main()