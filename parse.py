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
        
        # if program first token is newline,need to skip
        while self.check_token(Token_Type.NEWLINE):
            self.next_token()
        
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
            else:
                self.expression()
            
        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.check_token(Token_Type.IF):
            print("STATEMENT-IF")
            self.next_token()
            self.comparison()

            self.match(Token_Type.THEN)
            self.nl()

            # zero or more statements in the if block
            while not self.check_token(Token_Type.ENDIF):
                self.statement()

            self.match(Token_Type.ENDIF)

        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.check_token(Token_Type.WHILE):
            print("STATEMENT-WHILE")
            self.next_token()
            self.comparison()

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
                
        # "GOTO" ident
        elif self.check_token(Token_Type.GOTO):
            print("STATEMENT-GOTO")
            self.next_token()
            self.match(Token_Type.IDENT)

        # "LET" ident "=" expression
        elif self.check_token(Token_Type.LET):
            print("STATEMENT-LET")
            self.next_token()
            self.match(Token_Type.IDENT)
            self.match(Token_Type.EQ)
            self.expression()

        # "INPUT" ident
        elif self.check_token(Token_Type.INPUT):
            print("STATEMENT-INPUT")
            self.next_token()
            self.match(Token_Type.IDENT)

        # not a valid statement
        else:
            self.abort("Invalid statement at "+self.cur_token.text+"("+self.cur_token.kind.name+")")

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


    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+ 
    def comparison(self):
        print("COMPARSON")

        self.expression()
        #at least one compairson operator and another expression
        if self.is_comparison_operator():
            self.next_token()
            self.expression()
        else:
            self.abort("Expected comparison operator at: "+self.cur_token.text)

        # more comparsion operators
        while self.is_comparison_operator():
            self.next_token()
            self.expression()

    # return true if the current token is a comparison operator
    def is_comparison_operator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)

    # expression ::= term {("-"|"+") term}
    def expression(self):
        print("EXPRESSION")

        self.term()

        # 0 or more +/- and term
        while self.check_token(Token_Type.PLUS) or self.check_token(Token_Type.MINUS):
            self.next_token()
            self.term()


    # term ::= unary {("/" | "*") unary}
    def term(self):
        print("TERM")
        
        self.unary()

        # 0 or more '*' or '/ and unary
        while self.check_token(Token_Type.ASTERISK) or self.check_token(Token_Type.SLASH):
            self.next_token()
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY")

        # optional unary +/-
        if self.check_token(Token_Type.PLUS) or self.check_token(Token_Type.MINUS):
            self.next_token()

        self.primary()

    
    # primary ::= number | ident
    def primary(self):
        print("PRIMARY ("+self.cur_token.text+")")

        if self.check_token(Token_Type.NUMBER):
            self.next_token()
        elif self.check_token(Token_Type.IDENT):
            self.next_token()
        else:
            # Error
            self.abort("Unexpected token at "+self.cur_token.text)
        
        
