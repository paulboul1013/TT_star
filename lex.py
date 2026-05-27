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
        pass

    # skip comments 
    def skip_comments(self):
        pass

    # return the next token
    def get_token(self):
        pass





