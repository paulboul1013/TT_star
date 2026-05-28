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
    def check_token(self,kind):
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


    # program ::= {statement}
    def program(self):
        print("PROGRAM")
        
        # Parse all the statements in the program
        while not self.check_token(Token_Type.EOF):
            self.statement()

    # statement ::= "PRINT" (expression | string) nl
    def statement(self):
        #check first token  what kind of statement it's

        # "PRINT" (expression | string)
        if self.check_token(Token_Type.PRINT):
            print("STATEMENT-PRINT")
            self.next_token()

            if self.check_token(Token_Type.STRING):
                # string
                self.next_token()
            
            # "IF" comparsion "THEN" {statement} "ENDIF"
            elif self.check_token(Token_Type.IF):
                print("STATEMENT-IF")
                self.next_token()
                self.comparsion()

                self.match(Token_Type.THEN)
                self.nl()

                # zero or more statements in the if block
                while not self.check_token(Token_Type.ENDIF):
                    self.statement()

                self.match(Token_Type.ENDIF)

            # "WHILE" comparsion "REPEAT" {statement} "ENDWHILE"
            elif self.check_token(Token_Type.WHILE):
                print("STATEMENT-WHILE")
                self.next_token()
                self.comparsion()

                self.match(Token_Type.REPEAT)
                self.nl()

                # zero or more statements in the loop body
                while not self.check_token(Token_Type.ENDWHILE):
                    self.statement()

                self.match(Token_Type.ENDWHILE)

            # "LABEL" ident
            elif self.check_token(Token_Type.LABEL):
                print("STATEMENT-LABEL")
                self.next_token()
                self.match(Token_Type.IDENT)
                
            

            else:
                # expression
                self.expression()

        # NEWLINE
        self.nl()

    # nl ::= '\n'+ (at least one newline)
    def nl(self):
        print("NEWLINE")

        # require at least one newline
        self.match(Token_Type.NEWLINE)

        # allow extras newlines
        while self.check_token(Token_Type.NEWLINE):
            self.next_token()

