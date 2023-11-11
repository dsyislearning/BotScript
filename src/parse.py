import ply.yacc as yacc

from lex import tokens

class Tree:
    def __init__(self, root, branches=[]) -> None:
        for b in branches:
            assert isinstance(b, Tree)
        self.root = root
        self.branches = list(branches)
    
    def is_leaf(self):
        return not self.branches

    def __str__(self) -> str:
        def print_tree(t, indent=0):
            tree_str = '  ' * indent + str(t.root) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str
        return print_tree(self).rstrip()

# 语法分析规则
def p_script(p):
    '''script : step
              | step script'''
    if len(p) == 2:
        p[0] = Tree('script', [p[1]])
    else:
        p[0] = Tree('script', [p[1], p[2]])

def p_step(p):
    '''step : STEP ID actions'''
    p[0] = Tree('step', [Tree(p[2]), p[3]])

def p_actions(p):
    '''actions : INDENT action
               | INDENT action actions'''
    if len(p) == 3:
        p[0] = Tree('actions', [p[2]])
    else:
        p[0] = Tree('actions', [p[2], p[3]])

def p_action(p):
    '''action : speak
              | listen
              | branch
              | silence
              | default
              | exit'''
    p[0] = Tree('action', [p[1]])

def p_speak(p):
    '''speak : SPEAK string'''
    p[0] = Tree('speak', [p[2]])

def p_string(p):
    '''string : STRING
              | STRING string
              | VAR '+' string
              | STRING '+' string'''
    if len(p) == 2:
        p[0] = Tree('string', [Tree(p[1])])
    elif len(p) == 3:
        p[0] = Tree('string', [Tree(p[1]), p[2]])
    else:
        p[0] = Tree('string', [Tree(p[1]), p[3]])

def p_listen(p):
    '''listen : LISTEN NUMBER ',' NUMBER'''
    p[0] = Tree('listen', [Tree(p[2]), Tree(p[4])])

def p_branch(p):
    '''branch : BRANCH STRING ',' ID'''
    p[0] = Tree('branch', [Tree(p[2]), Tree(p[4])])

def p_silence(p):
    '''silence : SILENCE ID'''
    p[0] = Tree('silence', [Tree(p[2])])

def p_default(p):
    '''default : DEFAULT ID'''
    p[0] = Tree('default', [Tree(p[2])])

def p_exit(p):
    '''exit : EXIT'''
    p[0] = Tree('exit')

def p_error(p):
    print(f"Syntax error in input! {p.lineno}:{p.lexpos} {p.value}")

parser = yacc.yacc()
