import sys
from lex import *

# keeps track of current token and check if the code matches the grammar
class Parser:
    def __init__(self,lexer):
        self.lexer=lexer
        
        self.cur_token=None
        self.peek_token=None
        self.next_token()
        self.next_token() # call twice to fill cur_token and peek_token

    # return true if the current token matches
    def check_token(self,token):
        return kind==self.cur_token.kind

    # return true if the next token matches
    def check_peek(self,kind):
        return kind==self.peek_token.kind

    # try to match current token. if not，print error message. advances the current token
    def match(self,kind):
        if not self.check_token(kind):
            self.abort("Expected "+kind.name+",but got"+self.cur_token.kind.name)
            
        self.next_token()

    # advance teh current token
    def next_token(self):
        self.cur_token=self.peek_token
        self.peek_token=self.lexer.get_token()
        # lexer handle EOF

    def abort(self,message):
        sys.exit("Parsing Error: "+message)