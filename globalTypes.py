from enum import Enum

# TOKENTYPE
class TokenType(Enum):
    ENDFILE = 300
    ERROR = 401
    COMMENT = 500
    VAR = 200
    FUNCTION = 250
    EMPTY = None
    # RESERVED WORDS
    ELSE = 'else'
    IF = 'if'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'
    # MULTICHARACTER TOKENS
    ID = 111
    NUM = 000
    # SPECIAL SYMBOLS
    ASSIGN = '=='
    EQUAL = '='
    PLUS = '+'
    MINUS = '-'
    ASTERISK = '*'
    SLASH = '/'
    DIFFERENT = '!='
    LESS = '<'
    LESSEQUAL = '<='
    GREATER = '>'
    GREATEREQUAL = '>='
    OPENPARENTHESIS = '('
    CLOSEPARENTHESIS = ')'
    OPENSQBRACKET = '['
    CLOSESQBRACKET = ']'
    OPENCURLYBRACKET = '{'
    CLOSECURLYBRACKET = '}'
    COMMA = ','
    SEMICOLON = ';'


# STATETYPE
class StateType(Enum):
    START = 0
    FIRSTID = 1
    FIRSTNUM = 2
    FIRSTCOMMENT = 3
    SECONDCOMMENT = 4
    DONE = 5

# RESERVED WORDS
class ReservedWords(Enum):
    ELSE = 'else'
    IF = 'if'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'

# ***********   Syntax tree for parsing ************
class NodeKind(Enum):
    StmtK = 0
    ExpK = 1
    DecK = 2
    ParamsK = 3

class DeclarationKind(Enum):
    VarK = 0
    FunK = 1

class StmtKind(Enum):
    ExpressionK = 0
    CompoundK = 1
    SelectionK = 2
    IterationK = 3
    ReturnK = 4

class ExpKind(Enum):
    OpK = 0
    ConstK = 1
    IdK = 2

class ParamsKind(Enum):
    ListK = 0
    VoidK = 1

# ExpType is used for type checking
class DeclarationType(Enum):
    Void = 0
    Integer = 1

    

# Máximo número de hijos por nodo (3 para el if)
MAXCHILDREN = 3


class TreeNode:
    def __init__(self):
        # MAXCHILDREN = 3 está en globalTypes
        self.child = [None] * MAXCHILDREN  # tipo treeNode
        self.sibling = None               # tipo treeNode
        self.lineno = 0                   # tipo int
        self.nodekind = None              # tipo NodeKind, en globalTypes
        # en realidad los dos siguientes deberían ser uno solo (kind)
        # siendo la  union { StmtKind stmt; ExpKind exp;}
        self.stmt = None                  # tipo StmtKind
        self.exp = None                   # tipo ExpKind
        self.fun = None                   # tipo FunKind
        # en realidad los tres siguientes deberían ser uno solo (attr)
        # siendo la  union { TokenType op; int val; char * name;}
        self.op = None                    # tipo TokenType
        self.val = None                   # tipo int
        self.name = None                  # tipo String
        # for type checking of exps
        self.type = None                  # de tipo ExpType
        # for type checking of declarations
        self.declaration = None
