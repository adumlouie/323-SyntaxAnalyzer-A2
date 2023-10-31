from lexer import *

token_index = 0

# basically runs through the lexer program from A1 but places the tokens and lexemes in a list that the parser will call
def getTokens(filename, tokensList):
    isComment = False
    with open(filename, 'r') as f:
        ch = f.read(1)
        while ch:
            buffer = ''
            # handling comments
            if ch == '[':
                nextCh = f.read(1)
                if nextCh == '*':
                    isComment = True
                else:
                    buffer += ch
                    ch = nextCh 
                    continue
            elif isComment and ch == '*':
                nextCh = f.read(1)
                if nextCh == ']':
                    isComment = False
                    ch = f.read(1)
                    continue
            if isComment:
                ch = f.read(1)
                continue
            
            # read in ch until hitting delim
            while ch not in DELIMITERS:
                buffer += ch
                ch = f.read(1)
            # if there is something in buffer call lexer for token and print
            if buffer:
                token = lexer(buffer)[0]
                lexeme = lexer(buffer)[1]
                if token:  
                    tokensList.append([token, lexeme])
            # if current char is a separator print separator
            if ch in SEPARATORS:
                token = lexer(ch)[0]
                if token:
                    tokensList.append([token, ch])
                    
            ch = f.read(1)
            
# checks the current token with the expected token and advances to the next token if theres a match
def is_token(expected): 
    global token_index
    return False

# error handling
def syntax_error():
    global token_index
    currentToken = tokens[token_index]
    print(f"Syntax Error")
    token_index += 1
    
    return False

#production rules
def Rat23F():
    if Opt_Function_Definitions():
        if is_token('#'):
            print(lexer('#'))
            if Opt_Declaration_List():
                if Statement_List():
                    if is_token('#'):
                        print(lexer('#'))
                        return True
    return syntax_error()

def Opt_Function_Definitions():
    if Function_Definitions():
        return True
    elif Empty():
        return True
    else:
        return syntax_error()

# def Function_Definitions():
#     if Function():

tokens_1 = []
filename = 'testCases/testCase1.txt'
getTokens(filename, tokens_1)
print(tokens_1)