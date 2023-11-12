import ply.lex as lex

# token 列表
tokens = [
    'ID',
    'VAR',
    'STRING',
    'NUMBER',
    'COMMENT',
    'INDENT'
]

# 字面量
literals = ['+', ',']

# 保留字
reversed = {
    'step': 'STEP',
    'speak': 'SPEAK',
    'listen': 'LISTEN',
    'branch': 'BRANCH',
    'silence': 'SILENCE',
    'default': 'DEFAULT',
    'exit': 'EXIT',
}

tokens = tokens + list(reversed.values())

# 正则表达式规则
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reversed.get(t.value, 'ID')
    return t

def t_VAR(t):
    r'\$[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_STRING(t):
    r'\".*?\"'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_INDENT(t):
    r'\n(\s+)'
    t.lexer.lineno += 1
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

# 忽略的字符
t_ignore  = ' \t'

# 错误处理
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# 构建词法分析器
lexer = lex.lex()
