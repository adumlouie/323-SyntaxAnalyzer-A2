from lexer import *

# basically runs through the lexer program from A1 but shoves the tokens and lexemes in a list that the parser will call
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

# compares lexeme with expected and progresses token index
def is_token(expected):
    global token_index
    # compares current lexeme with expected 
    if tokens[token_index][1] == expected:
        token_index += 1
        return True
    return False
               
# error handling needs more work
def syntax_error():
    global token_index
    currentToken = tokens[token_index]
    print(f"Syntax Error at token: {currentToken}")
    token_index += 1
    
    return False

#production rules
def Rat23F():
    Opt_Function_Definitions()
    if is_token('#'):
        print(lexer('#'))
    else: 
        syntax_error()
        return False
    Opt_Declaration_List()
    Statement_List()
    if is_token('#'):
        print(lexer('#'))
    else:
        syntax_error()
        return False
    return True

def Opt_Function_Definitions():
    if Function_Definitions():
        return True
    else:
        Empty()
        return True

# def Function_Definitions():
#     Function()
    

def Function():
    if is_token('function'):
        print(lexer('function'))
        Identifier()
        if is_token('('):
            print(lexer('('))
            Opt_Parameter_List()
            if is_token(')'):
                print(lexer(')'))
                Opt_Declaration_List()
                Body()
                return True
    else:
        return False

# idk how to do this one                
# def Opt_Parameter_List():
#     if Parameter_List():
#         return True
#     elif 

def Parameter():
    IDs()
    Qualifier()
    
def Qualifier():
    if is_token('integer'):
        return True
    elif is_token('bool'):
        return True
    elif is_token('real'):
        return True
    else:
        return False
    
def Body():
    if is_token('{'):
        print(lexer('{'))
        Statement_List()
        if is_token('}'):
            print(lexer('}'))
            return True
    return False

def Opt_Declaration_List():
    if Declaration_List():
        Declaration_List()
        return True
    elif Empty():
        Empty()
        return True
    else:
        return False


    
        
# list will hold tokens, lexemes as entries
tokens = []
token_index = 0
filename = 'testCases/testCase1.txt'
getTokens(filename, tokens)
print(is_token('integer'))
