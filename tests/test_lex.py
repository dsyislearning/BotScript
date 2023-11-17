import sys
sys.path.append('../src')

import pytest

from lex import lexer

def test_tokens():
    lexer.lineno = 1
    lexer.input('''
        step speak listen branch silence default exit
        $var + "string"
        5, 20
        : ;
    ''')

    tokens = [
        'STEP', 'SPEAK', 'LISTEN', 'BRANCH', 'SILENCE', 'DEFAULT', 'EXIT',
        'VAR', '+', 'STRING', 'NUMBER', ',', 'NUMBER',
        ':', ';',
    ]

    for token in tokens:
        assert lexer.token().type == token

    lexer.lineno = 1

def test_lex_error_0(capsys):
    lexer.lineno = 1
    lexer.input('!')

    with pytest.raises(SystemExit) as e:
        token = lexer.token()
        while token:
            token = lexer.token()
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'LexError: lineno 1 lexpos 0: !\n'

    lexer.lineno = 1

def test_lex_error_1(capsys):
    lexer.lineno = 1
    lexer.input('step buhe &')

    with pytest.raises(SystemExit) as e:
        token = lexer.token()
        while token:
            token = lexer.token()
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'LexError: lineno 1 lexpos 10: &\n'

    lexer.lineno = 1

def test_lex_error_2(capsys):
    lexer.lineno = 1
    lexer.input('step buhe \n &n')

    with pytest.raises(SystemExit) as e:
        token = lexer.token()
        while token:
            token = lexer.token()
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'LexError: lineno 2 lexpos 12: &\n'

    lexer.lineno = 1
