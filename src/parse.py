"""语法分析模块"""
import ply.yacc as yacc

from lex import tokens, lexer

# 语法分析规则
def p_script(p):
    '''script : step
              | step script'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_step(p):
    '''step : STEP ID ':' actions'''
    p[0] = (p[2], p[4])

def p_actions(p):
    '''actions : action ';'
               | action ';' actions'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_action(p):
    '''action : speak
              | listen
              | branch
              | silence
              | default
              | exit'''
    p[0] = p[1]

def p_speak(p):
    '''speak : SPEAK string'''
    p[0] = ('speak', p[2])

def p_string(p):
    '''string : STRING
              | VAR
              | STRING '+' string
              | VAR '+' string'''
    if len(p) == 2:
        if p[1][0] == '$':
            p[0] = [p[1]]
        else:
            p[0] = [p[1][1:-1]]
    else:
        if p[1][0] == '$':
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1][1:-1]] + p[3] # 去掉引号

def p_listen(p):
    '''listen : LISTEN NUMBER ',' NUMBER'''
    p[0] = ('listen', (int(p[2]), int(p[4])))

def p_branch(p):
    '''branch : BRANCH STRING ',' ID'''
    p[0] = ('branch', {p[2][1:-1]: p[4]}) # 去掉引号

def p_silence(p):
    '''silence : SILENCE ID'''
    p[0] = ('silence', p[2])

def p_default(p):
    '''default : DEFAULT ID'''
    p[0] = ('default', p[2])

def p_exit(p):
    '''exit : EXIT'''
    p[0] = ('exit', True)

def p_error(p):
    """语法错误处理

    Args:
        p (production): 出现语法错误的产生式
    """
    print(f"SyntaxError: lineno {p.lineno} lexpos {p.lexpos}")
    exit(1)

parser = yacc.yacc()
"""yacc: 语法分析器对象"""
