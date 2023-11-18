"""词法分析模块"""
import ply.lex as lex

tokens = [
    'ID',
    'VAR',
    'STRING',
    'NUMBER',
    'COMMENT',
]
r"""list: 词法单元，语法分析中使用的符号

ID: 标识符
VAR: 变量
STRING: 字符串
NUMBER: 数字
COMMENT: 注释
"""

literals = ['+', ',', ':', ';']
r"""list: 字面量，语法分析中直接使用的符号

+: 加号
,: 逗号
: 冒号
; 分号
"""

reversed = {
    'step': 'STEP',
    'speak': 'SPEAK',
    'listen': 'LISTEN',
    'branch': 'BRANCH',
    'silence': 'SILENCE',
    'default': 'DEFAULT',
    'exit': 'EXIT',
}
r"""dict: 保留字，不能作为标识符

step: 步骤
speak: 说话
listen: 听话
branch: 分支
silence: 沉默
default: 默认
exit: 退出
"""

tokens = tokens + list(reversed.values())
r"""list: 词法单元，语法分析中使用的符号

`tokens = tokens + list(reversed.values())`

将保留字加入词法单元
"""

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

t_ignore  = ' \t'
"""str: 忽略的字符，包括空格和制表符"""

def t_error(t):
    """错误处理

    Args:
        t (Token): 错误的词法单元对象
    """
    print(f"LexError: lineno {t.lineno} lexpos {t.lexpos}: {t.value[0]}")
    exit(1)

lexer = lex.lex()
"""lexer: 词法分析器对象"""