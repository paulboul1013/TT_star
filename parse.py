import sys
from lex import *

# keeps track of current token and check if the code matches the grammar
class Parser:
    def __init__(self,lexer):
        pass

    # return true if the current token matches
    def check_token(self,token):
        pass

    # return true if the next token matches
    def check_peek(self,kind):
        pass

    # try to match current token. if not，print error message. advances the current token
    def match(self,kind):
        pass

    # advance teh current token
    def next_token(self):
        pass

    def abort(self,message):
        sys.exit("Parsing Error: "+message)