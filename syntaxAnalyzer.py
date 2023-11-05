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
    if tokens[token_index](1) != is_token:
        print(f"syntax Error at token: ")
        token_index += 1
    return False


#production rules
def Rat23F():
    print('<Rat23F> --> <Opt Function Definitions> # <Opt Declaration List> <Statement List> #')
    if Opt_Function_Definitions():
        if is_token('#'):
            print(lexer('#'))
            if Opt_Declaration_List():
                if Statement_List():
                    if is_token('#'):
                        print(lexer('#'))
                        return True
    return False

def Opt_Function_Definitions():
    if Function_Definitions():
        print('<Opt Function Definitions> --> <Function Definitions>')
        return True
    elif Empty():
        print('<Opt Function Definitions> --> <Empty>')
        return True
    else:
        return False

def Function_Definitions():
    if Function():
        if Function_Definitions():
            print('<Function Definitions> --> <Function> <Function Definitions>')
            return True
        else:
            print('<Function Definitions> --> <Function>')
            return True
    else:
        return False
    

def Function():
    print('<Function> --> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>')
    if is_token('function'):
        if Identifier():
            if is_token('('):
                print(lexer('('))
                if Opt_Parameter_List():
                    if is_token(')'):
                        print(lexer(')'))
                        if Opt_Declaration_List():
                            if Body(): 
                                return True
    else:
        return False
            
def Opt_Parameter_List():
    if Parameter_List():
        print('<Opt Parameter List> --> <Parameter List>')
        return True
    elif Empty():
        print('<Opt Parameter List> --> <Empty>')
        return True
    else:
        return False

def Parameter_List():
    if Parameter():
        if is_token(','):
            print('<Parameter List> --> <Parameter> , <Parameter List>')
            print(lexer(','))
            if Parameter_List():
                return True
        else:
            print('<Parameter List> --> <Parameter>')
            return True
    else:
        return False
    
def Parameter():
    print('<Parameter> --> <IDs > <Qualifier>')
    if IDs():
        if Qualifier():
            return True
    else:
        return False    

   
def Qualifier():
    if is_token('integer'):
        print('<Qualifier> --> integer')
        print(lexer('integer'))
        return True
    elif is_token('bool'):
        print('<Qualifier> --> bool')
        print(lexer('bool'))
        return True
    elif is_token('real'):
        print('<Qualifier> --> real')
        print(lexer('real'))
        return True
    else:
        return False
    
def Body():
    print('<Body> --> { <Statement List> }')
    if is_token('{'):
        print(lexer('{'))
        if Statement_List():
            if is_token('}'):
                print(lexer('}'))
                return True
    return False

def Opt_Declaration_List():
    if Declaration_List():
        print('<Opt Declaration List> --> <Declaration List>')
        return True
    elif Empty():
        print('<Opt Declaration List> --> <Empty>')
        return True
    else: 
        return False
    
def Declaration_List():
    if Declaration():
        if is_token(';'):
            if Declaration_List():
                print('<Declaration List> --> <Declaration> ; <Declaration List>')
                print(lexer(';'))
                return True
            else:
                print('<Declaration List> --> <Declaration> ;')
                print(lexer(';'))
                return True
    else:
        return False
    
def Declaration():
    print('<Declaration> --> <Qualifier > <IDs>')
    if Qualifier():
        if IDs():
            return True
    else:
        return False
    
def IDs():
    if Identifier():
        if is_token(','):
            print('<IDs> ::= <Identifier> | <Identifier>, <IDs>')
            print(lexer(','))
            if IDs():
                return True
    else:
        return False

def Statement_List():
    if Statement():
        if Statement_List():
             print('<Statement List> --> <Statement> <Statement List>')
             return True
        else:
            print('<Statement List> --> <Statement>')
            return True
    else:
        return False
    
def Statement():
    if Compound():
        print('<Statement> --> <Compound>')
        return True
    elif Assign():
        print('<Statement> --> <Assign>')
        return True
    elif If():
        print('<Statement> --> <If>')
        return True
    elif Return():
        print('<Statement> --> <Return>')
        return True
    elif Print():
        print('<Statement> --> <Print>')
        return True
    elif Scan():
        print('<Statement> --> <Scan>')
        return True
    elif While():
        print('<Statement> --> <While>')
        return True
    else:
        return False

def Compound():
    print('<Compound> --> { <Statement List> }')
    if is_token('{'):
        print(lexer('{'))
        if Statement_List():
            if is_token('}'):
                print(lexer('}'))
                return True
    else:
        return False

def Assign():
    print('<Assign> --> <Identifier> = <Expression> ;')
    if Identifier():
        if is_token('='):
            print(lexer('='))
            if Expression():
                if is_token(';'):
                    print(lexer(';'))
                    return True
    else:
        return False

def If():
    if is_token('if'):
        if is_token('('):
            if Condition():
                if is_token(')'):
                    if Statement():
                        if is_token('endif'):
                            print('<If> --> if ( <Condition> ) <Statement> endif')
                            print(lexer('if'))
                            print(lexer('('))
                            print(lexer(')'))
                            print(lexer('endif'))
                            return True
                        elif is_token('else'):
                            if Statement():
                                if is_token('endif'):
                                    print('<If> --> if ( <Condition> ) <Statement> else <Statement> endif')
                                    print(lexer('if'))
                                    print(lexer('('))
                                    print(lexer(')'))
                                    print(lexer('else'))
                                    print(lexer('endif'))

def Return():
    if is_token('ret'):
        print(lexer('ret'))
        if is_token(';'):
           print('<return> --> ret;')
           print(lexer(';'))
           return True
        else:
            if Expression():
                if is_token(';'):
                    print(lexer(';'))
                    print('<return> --> ret <expression>')
                    return True
    else:
        return False
                           
                                            
def Print():
    if is_token('put'):
        if is_token('('):
            if Expression():
                if is_token(')'):
                    print(lexer(';'))
                    return True
    else:
        return False

def Scan():
    print('<scan> --> get (<IDs>)')
    if is_token('get'):
        print(lexer('get'))
        if is_token('('):
            print(lexer('('))
            if IDs():
                if is_token(')'):
                    print(lexer(')'))
                    return True
    return False
    
def While():
    print('<while> --> while ( <Condition> ) <Statement>')

def Condition():
    if Expression():
        if Relop():
            if Expression():
                print('<condition> --> <expression><relop><expression>')
                return True
    return False
def Relop():
    print('<Relop> ::= == | != | > | < | <= | =>')
    if is_token('=='):
        print('<relop> --> ==')
        print(lexer('=='))
        return True
    elif is_token('!='):
        print('<relop> --> !=')
        print(lexer('!='))
        return True
    elif is_token('>'):
        print('<relop> --> >')
        print(lexer('>'))
        return True
    elif is_token('<'):
        print('<relop> --> <')
        print(lexer('<'))
        return True
    elif is_token('<='):
        print('<relop> --> <=')
        print(lexer('<='))
        return True
    elif is_token('=>'):
        print('<relop> --> =>')
        print(lexer('=>'))
        return True
    else:
        return False
    
def Expression():
    if Term():
        if Expression_n():
            print('<expression> --> <term> <expression>')
            return True
    return False

def Term():
    print('<Factor> <Term')
    if Factor():
        if Term_n():
            print('<Factor> <Term')
            return True
    return False

def Factor():
    if is_token('-'):
        print(lexer('-'))
        if Primary():
            print('<Factor> --> - <Primary>')
            return True
        else:
            print('<Factor> --> Primary')
    else:
        return False
    
def Primary():
    print('<Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) | ( <Expression> ) |<Real> | true | false')
    if Identifier():
        print('<primary> --> <identifier>')
        return True
    elif Integer():
        print('<primary> --> <integer>')
        return True
    elif Identifier():
        if is_token('('):
            print(lexer('()'))
            if IDs():
                if is_token(')'):
                    print(lexer(')'))
                    return True
    elif is_token('('):
        print(lexer('('))
        if Expression():
            if is_token(')'):
                print(lexer(')'))
                return True
    elif Real():
        print('<primary> --> <real>')
        return True
    elif is_token('true'):
        print(lexer('true'))
        return True
    elif is_token('false'):
        print(lexer('false'))
        return True
    else:
        return False


#Empty function if there is nothing inside 
def Empty():
    global token_index
    if tokens == 0:
        print(f"Empty tokens!")
        return True
    
# list will hold tokens, lexemes as entries
tokens = []
token_index = 0
filename = 'testCases/testCase1.txt'
getTokens(filename, tokens)
print(lexer('#'))
