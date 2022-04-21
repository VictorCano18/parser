from enum import Enum
from globalTypes import *
from scanner import *

token = None # holds current token
tokenString = None # holds the token string value
Error = False
#lineno = 1
SintaxTree = None
imprimeLexer = False

class ExpressionType(Enum): # preguntar al profe
    Op = 0
    Const = 1
    Id = 2
    Type = 3
    Symb = 4

class NodoArbol:
    def __init__(self):
        self.hijoIzq = None
        self.hijoDer = None
        self.exp = None # Tipo de expresión
        self.op = None
        self.val = None

def nuevoNodo(tipo):
    t = NodoArbol()
    if (t == None):
        print("Se terminó la memoria")
    else:
        t.exp = tipo
    return t

def syntaxError(message):
    global Error
    print(">>> Syntax error at line " + str(lineno) + ": " + message, end='')
    Error = True

def imprimeEspacios():
    print(' '*endentacion, end = '')

def imprimirAST(arbol):
    global endentacion
    endentacion += 2
    if arbol != None:
        imprimeEspacios()
        if arbol.exp == ExpressionType.Op:
            print("Op: ", arbol.op)
        elif arbol.exp == ExpressionType.Const:
            print("Const: ", arbol.val)
        elif arbol.exp == ExpressionType.Type:
            print("Type: ", arbol.val)
        else:
            print("ExpNode de tipo desconocido")
        imprimirAST(arbol.hijoIzq)
        imprimirAST(arbol.hijoDer)
    endentacion -= 2

def match(c):
    global token, tokenString, lineno
    # print("Match: ", token, " == ", c)
    if (token == c):
        token, tokenString, lineno = getToken(imprimeLexer)
        print(" ", lineno, token)
    else:
        syntaxError("unexpected token -> ")
        #printToken(token,tokenString)
        print("      ")

# def exp():
#     t = term()
#     while token in '+-':
#         p = nuevoNodo(ExpressionType.Op)
#         p.hijoIzq = t
#         p.op = token
#         t = p
#         match(token)
#         t.hijoDer = term()
#     return t

# def term():
#     t = factor()
#     while token == '*':
#         p = nuevoNodo(ExpressionType.Op)
#         p.hijoIzq = t
#         p.op = token
#         t = p
#         match(token)
#         t.hijoDer = factor()
#     return t

# def factor():
#     if token in '0123456789':
#         t = nuevoNodo(ExpressionType.Const)
#         t.val = token
#         match(token)
#     elif token == '(':
#         match('(')
#         t = exp()
#         match(')')
#     else:
#         syntaxError('Token no esperado')
#     return t

endentacion = 0

# 2. declaration-list → declaration {declaration}
def declaration_list():
    global token, tokenString, lineno
    t = declaration()
    p = t
    while token!=TokenType.ENDFILE:
        q = declaration()
        if (q!=None):
            if (t==None):
                t = p = q
        else: # now p cannot be NULL either
            p.hijoIzq = q
            p = q
    return t

# 3. declaration → var-declaration|fun-declaration como sabemos si mandar a funcion o a var declaratino
def declaration():
    global token, tokenString, lineno

    ## linea prueba
    # p = nuevoNodo(ExpressionType.Const)
    t = var_declaration()
    # if p != None:
    #     p.hijoIzq = t
    #     p.op = token
    #     t = p


    # antes solo estaba esta linea
    # t = var_declaration()

    # if (token == TokenType.INT):
    #     match(TokenType.INT)
    #     match(TokenType.ID)
    #     if token == TokenType.LPAREN:
    #         match(TokenType.LPAREN)
    #         t = params()
    #         match(TokenType.RPAREN)
    # elif (token == TokenType.VOID):
    #     match(TokenType.VOID)
    #     match(TokenType.ID)


    # else:
    #     syntaxError("unexpected token -> ")
    #     #printToken(token,tokenString)
    #     token, tokenString, lineno = getToken()
    # return 

    return t

# 4. var-declaration -> type-specifier ID [ [NUM] ];
def var_declaration():
    global token, tokenString, lineno
    t = type_specifier()
    match(TokenType.ID)

    if token == TokenType.OPENSQBRACKET:
        match(TokenType.OPENSQBRACKET)
        p = nuevoNodo(ExpressionType.Const)
        if p != None:
            p.hijoIzq = t
            p.op = token
            t = p
        match(token)
        # if token == (TokenType.NUM):
        #     p = nuevoNodo(ExpressionType.Num)
        #     p.hijoIzq = t
        #     p.op = token
        #     t = p
        #     match(TokenType.NUM)
            # p = nuevoNodo(ExpressionType.Symb)
            # p.hijoIzq = t
            # p.op = token
            # t = p
        match(TokenType.CLOSESQBRACKET)
    elif token == TokenType.SEMICOLON:
        match(TokenType.SEMICOLON)
    else:
        syntaxError("unexpected token -> ")
        # printToken(token,tokenString)
        token, tokenString, lineno = getToken()
        print(token, tokenString, lineno)

    # p = nuevoNodo(ExpressionType.Const)
    # p.hijoIzq = t
    # p.op = token
    # t = p
    return t


# 5 type-specifier → int|void
def type_specifier(): # preguntar sobre que se regresaria en estos casos 
    global token, tokenString, lineno
    #t = token
    # print("TOKEE -> ", token) 
    p = None
    if ((token == TokenType.INT) or (token == TokenType.VOID)):
        p = nuevoNodo(ExpressionType.Type)
        p.val = tokenString
        match(token)
    else:
        syntaxError("unexpected token -> ")
        #printToken(token,tokenString)
        token, tokenString, lineno = getToken()
    return p


# 6. fun-declaration → type-specifier ID(params)|compound-stmt

# 7. params → params-list|void
def parms():
    pass

# 8. param-list → param{,param}
def param_list():
    t = param()
    p = t
    while token!=TokenType.OPENPARENTHESIS:# DUDA SI ESTA BIEN POR EL ) DE PARAM
        match(TokenType.COMMA)
        q = param()
        if (q!=None):
            if (t==None):
                t = p = q
            else:
                p = q
    return t


# 9. param → type-specifier ID[[]]
def param():
    t = type_specifier()
    match(TokenType.ID)
    if token==TokenType.OPENSQBRACKET:
        match(TokenType.OPENSQBRACKET)
        match(TokenType.CLOSESQBRACKET)
    return t 

# 10. compound-stmt → {local-declarations statement-list} * duda de como regresar el statemnt_list
def compound_stmt():
    match(TokenType.OPENCURLYBRACKET)
    t = local_declations()
    p = statement_list()
    match(TokenType.CLOSECURLYBRACKET)

    return t,p

# 11. local-declarations → empty{var-declaration} * como manipulo el empty
def local_declations():
    if token == None:
        match(TokenType.EMPTY)
    else:
        t = var_declaration() # implementar el while
    return t 


# 12. statement-list → empty{statement}
def statement_list():
    t = None
    if token == TokenType.EMPTY:
        match(TokenType.EMPTY)
    else: 
        match(TokenType.OPENCURLYBRACKET)
        while(token != TokenType.CLOSECURLYBRACKET):
            t = statement() #lo dejo con la misma t porque si se llega a sobreescribir, lo que se envia es la t
        match(TokenType.CLOSECURLYBRACKET)
    return t

# 13. statement → expression-stmt|compound-stmt|selection-stmt|iteration-stmt|return-stmt
def statement():
    t = None
    if token == TokenType.WHILE: # iteration
        t = iteration_stmt()
    elif token == TokenType.RETURN: #return
        t = return_stmt()
    elif token == TokenType.IF:
        t = selection_stmt()
    elif ((token == TokenType.ID) and (token == TokenType.INT)): #no estoy seguro pórque no se compararía un id o que sea int :c
        t = expression_stmt()
    elif token == TokenType.OPENCURLYBRACKET:
        t = compound_stmt()
    else:
        print("faltan las del compund y expression :C")
    return t

# 14. expression-stmt → [expression]; 
def expression_stmt():
    # aqui no se si el ebnf esté mal, creo que el ; debería de estar detro de los corchetes
    # de lo contrario estaría mal solo matchear un ;
    t = expression()
    match(TokenType.SEMICOLON)
    return t
     
# 15. selection-stmt → if(expression) statement [else statement]
def selection_stmt():
    match(TokenType.IF)
    match(TokenType.OPENPARENTHESIS)
    t = expression()
    match(TokenType.CLOSEPARENTHESIS)
    t = statement()
    if(token == TokenType.ELSE):
        match(TokenType.ELSE)
        t = statement()
    return t

# 16. iteration-stmt → while(expression) statement
def iteration_stmt():
    match(TokenType.WHILE)
    match(TokenType.OPENPARENTHESIS)
    t = expression()
    match(TokenType.CLOSEPARENTHESIS)
    t = statement()
    return t

# 17. return-stmt → return[expression];
def return_stmt():
    t = None
    match(TokenType.RETURN)
    if token == TokenType.SEMICOLON:
        match(TokenType.SEMICOLON)
    else:
        t = expression()
        match(TokenType.SEMICOLON)
    return t

# 18. expression → var=expression|simple-expression
def expression():
    return 

# 19. var → ID[[expression]]
def var():
    t = None
    match(TokenType.ID)
    if token == TokenType.OPENSQBRACKET:
        match(TokenType.OPENSQBRACKET)
        t = expression()
        match(TokenType.CLOSESQBRACKET)
    return t

# 20. simple-expression → additive-expression {relop additive-expression} 
# 21. relop → <=|<|>|>=|==|!= 
def simple_expression():
    t = additive_expression()
    # se compara con relop pero no se si se debe de hacer por aparte la de <= >=?
    while((token == TokenType.ASSIGN) or (token == TokenType.DIFFERENT) or (token == TokenType.LESSEQUAL)
    or (token == TokenType.GREATEREQUAL) or (token == TokenType.LESS) or (token == TokenType.GREATER)):
        match(token) # porque no se sabe que token type es
        t = additive_expression()
    return t

# exp  exp‐simple [ op‐comparación exp‐simple ] * se hace esta?


# 22. additive-expression → term{addop term}
# 23. addop → +|- 
def additive_expression():
    t = term()
    while((token == TokenType.PLUS) or (token == TokenType.MINUS)):
        match(token)
        t = term()
    return t

# 24. term → factor{mulop factor}
# 25. mulop → *|/
def term():
    t = factor()
    while((token == TokenType.ASTERISK) or (token == TokenType.SLASH)):
        match(token)
        t = factor()
    return t

# 26. factor → (expression)|var|call|NUM
def factor():
    t = None
    if token == TokenType.OPENPARENTHESIS:
        match(token)
        t = expression
        match(TokenType.CLOSEPARENTHESIS)
    elif token == TokenType.NUM:
        match(token)
    elif token == TokenType.ID:
        t = call()
    elif token == TokenType.INT:
        t = var()
    return t

# 27. call → ID(args)
def call():
    match(TokenType.ID)
    match(TokenType.OPENPARENTHESIS)
    t = args()
    match(TokenType.CLOSEPARENTHESIS)
    return t

# 28. args → arg-list|empty
def args():
    t = None
    if token == TokenType.EMPTY:
        match(TokenType.EMPTY)
    else:
        t = arg_list()
    return t

# 29. arg-list → expression{, expression}
def arg_list():
    t = expression()
    while token == TokenType.COMMA:
        match(token)
        t = expression()
    return t

# Procedure printToken prints a token 
# and its lexeme to the listing file
def printToken(token, tokenString):
    if token in {TokenType.ELSE, TokenType.IF, TokenType.INT, TokenType.RETURN,
                 TokenType.VOID, TokenType.WHILE}:
        print(" reserved word: " + tokenString)
    elif token == TokenType.ASSIGN:
        print("==")
    elif token == TokenType.EQUAL:
        print("=")
    elif token == TokenType.PLUS:
        print("+")
    elif token == TokenType.MINUS:
        print("-")
    elif token == TokenType.ASTERISK:
        print("*")
    elif token == TokenType.SLASH:
        print("/")
    elif token == TokenType.DIFFERENT:
        print("!=")
    elif token == TokenType.LESS:
        print("<")
    elif token == TokenType.LESSEQUAL:
        print("<=")
    elif token == TokenType.GREATER:
        print(">")
    elif token == TokenType.GREATEREQUAL:
        print(">=")
    elif token == TokenType.OPENPARENTHESIS:
        print("(")
    elif token == TokenType.CLOSEPARENTHESIS:
        print(")")
    elif token == TokenType.OPENSQBRACKET:
        print("[")
    elif token == TokenType.CLOSESQBRACKET:
        print("]")
    elif token == TokenType.OPENCURLYBRACKET:
        print("{")
    elif token == TokenType.CLOSECURLYBRACKET:
        print("}")
    elif token == TokenType.COMMA:
        print(",")
    elif token == TokenType.SEMICOLON:
        print(";")
    elif token == id:
        print("ID, name= " + tokenString)
    elif token == TokenType.ERROR:
        print("ERROR: " + tokenString)
    else:  # should never happen
        print("Unknown token: ")


def parse(imprime = True):
    global token, tokenString, lineno
    token, tokenString, lineno = getToken(imprimeLexer)
    t = declaration_list()
    if (token != TokenType.ENDFILE):
        syntaxError("Code ends before file\n")
    if imprime:
        imprimirAST(t)
    return t #, Error

def globales(prog, pos, long): # Recibe los globales del main
    recibeScanner(prog, pos, long) # Para mandar los globales