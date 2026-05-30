import sys
from lex import *

# keeps track of current token and check if the code matches the grammar
class Parser:
    def __init__(self,lexer,emitter):
        self.lexer=lexer
        self.emitter=emitter

        self.symbols = set() # variables declared 
        self.labels_declared = set() # labels declared 
        self.labels_gotoed = set() # labels gotoed
        
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
        # print("PROGRAM")
        self.emitter.header_line("#include <stdio.h>")
        self.emitter.header_line("int main(void){")
        
        # if program first token is newline,need to skip
        while self.check_token(Token_Type.NEWLINE):
            self.next_token()
        
        # Parse all the statements in the program
        while not self.check_token(Token_Type.EOF):
            self.statement()

        # wrap main function
        self.emitter.emit_line("return 0;")
        self.emitter.emit_line("}")

        # check that all labels referenced in a GOTO is declared
        for label in self.labels_gotoed:
            if label not in self.labels_declared:
                self.abort("Undeclared label:"+label)

    # statement ::= "PRINT" (expression | string) nl
    def statement(self):
        #check first token  what kind of statement it's

        # "PRINT" (expression | string)
        if self.check_token(Token_Type.PRINT):
            # print("STATEMENT-PRINT")
            self.next_token()

            if self.check_token(Token_Type.STRING):
                # just string，print it
                self.emitter.emit_line("printf(\""+self.cur_token.text+"\\n\");")
                self.next_token()
            else:
                # expect an expression and print the result as a float
                self.emitter.emit("printf(\"%"+".2f\\n\",(float)(")
                self.expression()
                self.emitter.emit_line("));")
            
        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.check_token(Token_Type.IF):
            # print("STATEMENT-IF")
            self.next_token()
            self.emitter.emit("if(")
            self.comparison()

            self.match(Token_Type.THEN)
            self.nl()
            self.emitter.emit_line("){")

            # zero or more statements in the if block
            while not self.check_token(Token_Type.ENDIF):
                self.statement()

            self.match(Token_Type.ENDIF)
            self.emitter.emit_line("}")

        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.check_token(Token_Type.WHILE):
            # print("STATEMENT-WHILE")
            self.next_token()
            self.emitter.emit("while(")
            self.comparison()

            self.match(Token_Type.REPEAT)
            self.nl()
            self.emitter.emit_line("){")

            # zero or more statements in the loop body
            while not self.check_token(Token_Type.ENDWHILE):
                self.statement()

            self.match(Token_Type.ENDWHILE)
            self.emitter.emit_line("}")

        # "INPUT" ident
        elif self.check_token(Token_Type.INPUT):
            self.next_token()

            # if variable doesn't already exist, declare it
            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)
                self.emitter.header_line("float "+self.cur_token.text+';')  

            # emit scanf and check valid input，if not valid input，set the variable to 0 and clear the input
            self.emitter.emit_line("if(0==scanf(\"%"+"f\", &"+self.cur_token.text+")) {")
            self.emitter.emit_line(self.cur_token.text+" = 0;")
            self.emitter.emit("scanf(\"%")
            self.emitter.emit_line("*s\");")
            self.emitter.emit_line("}")

            self.match(Token_Type.IDENT)

        # "LET" ident = expression
        elif self.check_token(Token_Type.LET):
            self.next_token()

            # check if ident exists in symbol table. If not , then declare
            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)
                self.emitter.emit_line("float "+self.cur_token.text+";")

            self.emitter.emit(self.cur_token.text+" = ")
            self.match(Token_Type.IDENT)
            self.match(Token_Type.EQ)

            self.expression()
            self.emitter.emit_line(";")

        # "LABEL" ident
        elif self.check_token(Token_Type.LABEL):
            # print("STATEMENT-LABEL")
            self.next_token()

            # make sure this label doesn't already exist
            if self.cur_token.text in self.labels_declared:
                self.abort("Label already exists: "+self.cur_token.text)

            self.labels_declared.add(self.cur_token.text)
        
            self.emitter.emit_line(self.cur_token.text+":")
            self.match(Token_Type.IDENT)

        # "GOTO" ident
        elif self.check_token(Token_Type.GOTO):
            # print("STATEMENT-GOTO")
            self.next_token()
            self.labels_gotoed.add(self.cur_token.text)
            self.emitter.emit_line("goto "+self.cur_token.text+";")
            self.match(Token_Type.IDENT)

        # not a valid statement
        else:
            self.abort("Invalid statement at "+self.cur_token.text+"("+self.cur_token.kind.name+")")

        # NEWLINE
        self.nl()

    # nl ::= '\n'+ (at least one newline)
    def nl(self):
        # print("NEWLINE")

        # require at least one newline
        self.match(Token_Type.NEWLINE)

        # allow extras newlines
        while self.check_token(Token_Type.NEWLINE):
            self.next_token()


    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+ 
    def comparison(self):
        # print("COMPARSON")

        self.expression()
        #at least one compairson operator and another expression
        if self.is_comparison_operator():
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.expression()
        else:
            self.abort("Expected comparison operator at: "+self.cur_token.text)

        # more comparsion operators
        while self.is_comparison_operator():
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.expression()

    # return true if the current token is a comparison operator
    def is_comparison_operator(self):
        return self.check_token(Token_Type.GT) or self.check_token(Token_Type.GTEQ) or self.check_token(Token_Type.LT) or self.check_token(Token_Type.LTEQ) or self.check_token(Token_Type.EQEQ) or self.check_token(Token_Type.NOTEQ)

    # expression ::= term {("-"|"+") term}
    def expression(self):
        # print("EXPRESSION")

        self.term()

        # 0 or more +/- and term
        while self.check_token(Token_Type.PLUS) or self.check_token(Token_Type.MINUS):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.term()


    # term ::= unary {("/" | "*") unary}
    def term(self):
        # print("TERM")
        
        self.unary()

        # 0 or more '*' or '/ and unary
        while self.check_token(Token_Type.ASTERISK) or self.check_token(Token_Type.SLASH):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self):
        # print("UNARY")

        # optional unary +/-
        if self.check_token(Token_Type.PLUS) or self.check_token(Token_Type.MINUS):
            self.emitter.emit(self.cur_token.text)
            self.next_token()

        self.primary()

    
    # primary ::= number | ident
    def primary(self):
        # print("PRIMARY ("+self.cur_token.text+")")

        if self.check_token(Token_Type.NUMBER):
            self.next_token()
        elif self.check_token(Token_Type.IDENT):
            # ensure variable already exists
            if self.cur_token.text not in self.symbols:
                self.abort("Referencing variable before assignment: "+self.cur_token.text)
            self.next_token()
        else:
            # Error
            self.abort("Unexpected token at "+self.cur_token.text)
