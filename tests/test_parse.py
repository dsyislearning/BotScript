import sys
sys.path.append('../src')

import pytest

from parse import parser, lexer

def check(filename, answer):
    with open(filename, 'r', encoding='utf-8') as f:
        script_string = ''.join(f.readlines()).lower()
        script = parser.parse(script_string)
        assert script == answer

def test_parse_0():
    answer = [
        ('welcome', [
            ('speak', ['$name', '您好,请问有什么可以帮您?']),
            ('listen', (5, 20)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc')
        ]),
        ('complainproc', [
            ('speak', ['您的意见是我们改进工作的动力,请问您还有什么补充?']),
            ('listen', (5, 50)),
            ('default', 'thanks')
        ]),
        ('thanks', [
            ('speak', ['感谢您的来电,再见']),
            ('exit', True)
        ]),
        ('billproc', [
            ('speak', ['您的本月账单是', '$amount', '元,感谢您的来电,再见']),
            ('exit', True)
        ]),
        ('silenceproc', [
            ('speak', ['听不清,请您大声一点可以吗']),
            ('listen', (5, 20)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc')
        ]),
        ('defaultproc', [
            ('speak', ['你可以向我：投诉 or 查账单']),
            ('listen', (5, 20)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc')
        ])
    ]
    check('test1.bs', answer)

def test_parse_1():
    answer = [
        ('welcome', [
            ('speak', ['我是心里咨熊师完颜慧德，你有什么要问的吗？']),
            ('listen', (5, 20)),
            ('branch', {'闺蜜': 'guimidimi'}),
            ('branch', {'我老公喜欢上了我妈妈': 'lonely'}),
            ('branch', {'华为手机': 'iphone'}),
            ('branch', {'没有穿好': 'gongchuqi'}),
            ('branch', {'读书有什么用吗': 'duoshu'}),
            ('default', 'xiaoyongle')
        ]),
        ('continue', [
            ('speak', ['还有什么要问的吗？']),
            ('listen', (5, 20)),
            ('branch', {'闺蜜': 'guimidimi'}),
            ('branch', {'我老公喜欢上了我妈妈': 'lonely'}),
            ('branch', {'华为手机': 'iphone'}),
            ('branch', {'没有穿好': 'gongchuqi'}),
            ('branch', {'读书有什么用吗': 'duoshu'}),
            ('branch', {'没': 'end'}),
            ('silence', 'continue'),
            ('default', 'xiaoyongle')
        ]),
        ('guimidimi', [
            ('speak', ['好嘞，是闺咪，不好嘞，是敌咪。', '什么是敌咪？敌人的秘密就叫敌蜜']),
            ('silence', 'continue')
        ]),
        ('lonely', [
            ('speak', ['这就不对啊，这是一个lonely的问题。', '在这个过程中你要去跟你的妈妈谈，同时要跟你的老公去谈。', '如果说谈不脱，就要想进一步的办法。']),
            ('silence', 'continue')
        ]),
        ('iphone', [
            ('speak', ['啊？本来我们说的是安分守己，安分守己你怎么又提到手机了呢？']),
            ('silence', 'continue')
        ]),
        ('gongchuqi', [
            ('speak', ['你们又在这里带什么节奏！供出去！你还待在这里干嘛？供出去！\\n', '每天总有这些黑粉来捣乱，我从来一般不发火，太不像话了真的是！']),
            ('silence', 'continue')
        ]),
        ('duoshu', [
            ('speak', ['duo书的拟人最美丽，duo书的拟人最优秀，duo书的拟人最通情达理。']),
            ('silence', 'continue')
        ]),
        ('xiaoyongle', [
            ('speak', ['你这问的什么问题？你把人笑拥了我跟你说']),
            ('silence', 'continue')
        ]),
        ('end', [
            ('speak', ['没问题了就供出去']),
            ('exit', True)
        ])
    ]
    check('test2.bs', answer)

def test_parse_2():
    answer = [
        ('welcome', [
            ('speak', ['欢迎光临 ', '$storename', '，请问有什么可以帮您？']),
            ('listen', (5, 20)),
            ('branch', {'发货': 'ship'}),
            ('branch', {'快递': 'delivery'}),
            ('branch', {'新品': 'new'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc')
        ]),
        ('ship', [
            ('speak', ['是否帮您查询最近买的东西何时发货？']),
            ('listen', (5, 20)),
            ('branch', {'是': 'shipyes'}),
            ('branch', {'否': 'welcome'}),
            ('silence', 'silenceproc'),
            ('default', 'ship')
        ]),
        ('shipyes', [
            ('speak', ['发货时间为 ', '$shiptime']),
            ('exit', True)
        ]),
        ('delivery', [
            ('speak', ['是否帮您查询最近的快递信息？']),
            ('listen', (5, 20)),
            ('branch', {'是': 'deliveryyes'}),
            ('branch', {'否': 'welcome'}),
            ('silence', 'silenceproc'),
            ('default', 'delivery')
        ]),
        ('deliveryyes', [
            ('speak', ['快递情况：', '$deliveryinfo']),
            ('exit', True)
        ]),
        ('new', [
            ('speak', ['我们最近有如下新品：', '$newproducts']),
            ('exit', True)
        ]),
        ('silenceproc', [
            ('speak', ['听不清，请您再说一遍']),
            ('listen', (5, 20)),
            ('branch', {'发货': 'ship'}),
            ('branch', {'快递': 'delivery'}),
            ('branch', {'新品': 'new'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc')
        ]),
        ('defaultproc', [
            ('speak', ['你可以向我：查询发货情况 or 查询快递情况 or 查看我们的新品']),
            ('listen', (5, 20)),
            ('branch', {'发货': 'ship'}),
            ('branch', {'快递': 'delivery'}),
            ('branch', {'新品': 'new'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc')
        ])
    ]
    check('test3.bs', answer)

# 步骤定义缺少冒号
def test_parse_error_0(capsys):
    lexer.lineno = 1
    with pytest.raises(SystemExit) as e:
        with capsys.disabled():
            parser.parse("""step welcome
                            speak "您好,请问有什么可以帮您?";""")
        captured = capsys.readouterr()
        assert captured.out == 'SyntaxError: lineno 2 lexpos 41\n'
    assert e.type == SystemExit
    assert e.value.code == 1
    lexer.lineno = 1

# 动作定义缺少分号
def test_parse_error_1(capsys):
    lexer.lineno = 1
    with pytest.raises(SystemExit) as e:
        parser.parse("""step welcome
                            speak "您好,请问有什么可以帮您?"
                            listen 5, 20  """)
    assert e.value.code == 1
    lexer.lineno = 1
    captured = capsys.readouterr()
    assert captured.out == 'SyntaxError: lineno 2 lexpos 41\n'

# 动作定义缺少逗号
def test_parse_error_2(capsys):
    lexer.lineno = 1
    with pytest.raises(SystemExit) as e:
        parser.parse("""step welcome:
                            speak "您好,请问有什么可以帮您?";
                            listen 5, 20;
                            branch "投诉" complainproc;""")
    assert e.value.code == 1
    lexer.lineno = 1
    captured = capsys.readouterr()
    assert captured.out == 'SyntaxError: lineno 4 lexpos 147\n'

# speak 语法检查
def test_parse_error_3(capsys):
    lexer.lineno = 1
    with pytest.raises(SystemExit) as e:
        parser.parse("""step welcome:
                        speak $name, "您好,请问有什么可以帮您?";""")
    assert e.value.code == 1
    lexer.lineno = 1
    captured = capsys.readouterr()
    assert captured.out == 'SyntaxError: lineno 2 lexpos 49\n'

# listen 语法检查
def test_parse_error_4(capsys):
    lexer.lineno = 1
    with pytest.raises(SystemExit) as e:
        parser.parse("""step welcome:
                        speak $name + "您好,请问有什么可以帮您?";
                        listen 5 20;""")
    assert e.value.code == 1
    lexer.lineno = 1
    captured = capsys.readouterr()
    assert captured.out == 'SyntaxError: lineno 3 lexpos 102\n'

# branch 语法检查
def test_parse_error_5(capsys):
    lexer.lineno = 1
    with pytest.raises(SystemExit) as e:
        parser.parse("""step welcome:
                        speak $name + "您好,请问有什么可以帮您?";
                        listen 5, 20;
                        branch "投诉", complainproc,
                        branch "账单", billproc;""")
    assert e.value.code == 1
    lexer.lineno = 1
    captured = capsys.readouterr()
    assert captured.out == 'SyntaxError: lineno 4 lexpos 156\n'

# silence 语法检查
def test_parse_error_6(capsys):
    lexer.lineno = 1
    with pytest.raises(SystemExit) as e:
        parser.parse("""step welcome:
                        speak $name + "您好,请问有什么可以帮您?";
                        listen 5, 20;
                        branch "投诉", complainproc;
                        silence silence;""")
    assert e.value.code == 1
    lexer.lineno = 1
    captured = capsys.readouterr()
    assert captured.out == 'SyntaxError: lineno 5 lexpos 190\n'

# default 语法检查
def test_parse_error_7(capsys):
    lexer.lineno = 1
    with pytest.raises(SystemExit) as e:
        parser.parse("""step welcome:
                        speak $name + "您好,请问有什么可以帮您?";
                        listen 5, 20;
                        branch "投诉", complainproc;
                        silence silenceproc;
                        default default;""")
    assert e.value.code == 1
    lexer.lineno = 1
    captured = capsys.readouterr()
    assert captured.out == 'SyntaxError: lineno 6 lexpos 235\n'
