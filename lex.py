import enum
import sys

class Lexer:
    def __init__(self,source):
        self.source=source+'\n' # add a newline simplify lex/parse the last token/statement
        self.cur_char='' # current character 
        self.cur_pos=-1 # current position 
        self.next_char()

    # process the next character
    def next_char(self):
        self.cur_pos+=1
        if self.cur_pos >= len(self.source):
            self.cur_char='\0' #EOF
        else:
            self.cur_char=self.source[self.cur_pos]

    # return the lookahead character
    def peek(self):
        if self.cur_pos+1 >= len(self.source):
            return '\0'
        return self.source[self.cur_pos+1]

    # invalid token found, print error message and exit
    def abort(self,message):
        pass

    # skip whitespace except newlines, use to indicate the end of the statement
    def skip_whitespace(self):
        while self.cur_char==' ' or self.cur_char=='\t' or self.cur_char=='\r':
            self.next_char()

    # skip comments 
    def skip_comments(self):
        if self.cur_char=='#':
            while self.cur_char!='\n':
                self.next_char()

    #invalid token found, print error message and exit
    def abort(self,message):
        sys.exit("Lexing error. "+message)

    # return the next token
    def get_token(self):
        #check first character of token
        token=None
        self.skip_whitespace()
        self.skip_comments()

        if self.cur_char=='+':
            token = Token(self.cur_char,Token_Type.PLUS)
            
        elif self.cur_char=='-':
            token = Token(self.cur_char,Token_Type.MINUS)

        elif self.cur_char=='*':
            token = Token(self.cur_char,Token_Type.ASTERISK)

        elif self.cur_char=='/':
            token = Token(self.cur_char,Token_Type.SLASH)

        elif self.cur_char=='=':
            #check whether is = or ==
            if self.peek()=='=':
                last_char=self.cur_char
                self.next_char()
                token=Token(last_char+self.cur_char,Token_Type.EQEQ)
            else:
                token = Token(self.cur_char,Token_Type.EQ)

        elif self.cur_char=='>':
            #check whether is > or >=
            if self.peek()=='=':
                last_char=self.cur_char
                self.next_char()
                token=Token(last_char+self.cur_char,Token_Type.GTEQ)
            else:
                token=Token(self.cur_char,Token_Type.GT)

        elif self.cur_char=='<':
            #check whether is < or <=
            if self.peek() =='=':
                last_char=self.cur_char
                self.next_char()
                token=Token(last_char+self.cur_char,Token_Type.LTEQ)
            else:
                token=Token(self.cur_char,Token_Type.LT)

        elif self.cur_char=='!':
            if self.peek()=='=':
                last_char=self.cur_char
                self.next_char()
                token=Token(last_char+self.cur_char,Token_Type.NOTEQ)
            else:
                self.abort("Expected !=,but only got !"+self.peek())

        elif self.cur_char=='\"':
            #get characters between " and "
            self.next_char()
            start_pos=self.cur_pos
            
            while self.cur_char!='\"':
                
                if self.cur_char=='\r' or self.cur_char=='\n' or self.cur_char=='\t' or self.cur_char=='\\' or self.cur_char=='%':
                    self.abort("Illegal character in string.")
                
                self.next_char()

            token_text=self.source[start_pos:self.cur_pos] # get the string
            token=Token(token_text,Token_Type.STRING)
                

        elif self.cur_char=='\n':
            token = Token(self.cur_char,Token_Type.NEWLINE)

        elif self.cur_char=='\0':
            token = Token('',Token_Type.EOF)

        else:
            #unkown token
            self.abort("Unknown token: "+self.cur_char)

        self.next_char()
        return token

class Token:
    def __init__(self,token_text,token_kind):
        self.text=token_text
        self.kind=token_kind

class Token_Type(enum.Enum):
    EOF=-1
    NEWLINE=0
    NUMBER=1
    IDENT=2
    STRING=3

    #keywords
    LABEL=101
    GOTO=102
    PRINT = 103
    INPUT=104
    LET = 105
    IF =106
    THEN=107
    ENDIF=108
    WHILE=109
    REPEAT = 110
    ENDWHILE=111

    #operators
    EQ=201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
