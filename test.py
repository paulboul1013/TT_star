from lex import *


def main():
    source = "+-123 9.8654*/"
    lexer = Lexer(source)

    token=lexer.get_token()
    while token.kind!=Token_Type.EOF:
        print(token.kind)
        token=lexer.get_token()

main()