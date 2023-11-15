import ply.lex as lex

# token 列表
tokens = [
    'ID',
    'VAR',
    'STRING',
    'NUMBER',
    'COMMENT',
]

# 字面量
literals = ['+', ',', ':', ';']

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

# 丢弃空行
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# 忽略的字符，包括空格和制表符
t_ignore  = ' \t'

# 错误处理
def t_error(t):
    print(f"LexError: lineno {t.lineno} lexpos {t.lexpos}: {t.value[0]}")
    exit(1)

# 构建词法分析器
lexer = lex.lex()
