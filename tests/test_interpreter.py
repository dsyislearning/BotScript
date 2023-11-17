import sys
sys.path.append('../src')

import pytest

from interpreter import Step, Environment

steps = []

def test_step_0():
    step = Step('welcome', [
            ('speak', ['$name', '您好,请问有什么可以帮您?']),
            ('listen', (5, 20)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc')
        ])
    steps.append(step)
    assert step.id == 'welcome'
    assert step.speak == ['$name', '您好,请问有什么可以帮您?']
    assert step.listen == (5, 20)
    assert step.answer == {"投诉": 'complainproc', "账单": 'billproc'}
    assert step.silence == 'silenceproc'
    assert step.default == 'defaultproc'
    assert step.exit == None

    step = Step('complainproc', [
            ('speak', ['您的意见是我们改进工作的动力,请问您还有什么补充?']),
            ('listen', (5, 50)),
            ('default', 'thanks')
        ])
    steps.append(step)
    assert step.id == 'complainproc'
    assert step.speak == ['您的意见是我们改进工作的动力,请问您还有什么补充?']
    assert step.listen == (5, 50)
    assert step.answer == {}
    assert step.silence == ''
    assert step.default == 'thanks'
    assert step.exit == None

    step = Step('thanks', [
            ('speak', ['感谢您的来电,再见']),
            ('exit', True)
        ])
    steps.append(step)
    assert step.id == 'thanks'
    assert step.speak == ['感谢您的来电,再见']
    assert step.listen == ()
    assert step.answer == {}
    assert step.silence == ''
    assert step.default == ''
    assert step.exit == True

    step = Step('billproc', [
            ('speak', ['您的本月账单是', '$amount', '元,感谢您的来电,再见']),
            ('exit', True)
        ])
    steps.append(step)
    assert step.id == 'billproc'
    assert step.speak == ['您的本月账单是', '$amount', '元,感谢您的来电,再见']
    assert step.listen == ()
    assert step.answer == {}
    assert step.silence == ''
    assert step.default == ''
    assert step.exit == True

    step = Step('silenceproc', [
            ('speak', ['听不清,请您大声一点可以吗']),
            ('listen', (5, 20)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc')
        ])
    steps.append(step)
    assert step.id == 'silenceproc'
    assert step.speak == ['听不清,请您大声一点可以吗']
    assert step.listen == (5, 20)
    assert step.answer == {"投诉": 'complainproc', "账单": 'billproc'}
    assert step.silence == 'silenceproc'
    assert step.default == 'defaultproc'
    assert step.exit == None

    step = Step('defaultproc', [
            ('speak', ['你可以向我：投诉 or 查账单']),
            ('listen', (5, 20)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc')
        ])
    steps.append(step)
    assert step.id == 'defaultproc'
    assert step.speak == ['你可以向我：投诉 or 查账单']
    assert step.listen == (5, 20)
    assert step.answer == {"投诉": 'complainproc', "账单": 'billproc'}
    assert step.silence == 'silenceproc'
    assert step.default == 'defaultproc'
    assert step.exit == None

def test_step_1():
    step = Step('welcome', [
            ('speak', ['我是心里咨熊师完颜慧德，你有什么要问的吗？']),
            ('listen', (5, 20)),
            ('branch', {'闺蜜': 'guimidimi'}),
            ('branch', {'我老公喜欢上了我妈妈': 'lonely'}),
            ('branch', {'华为手机': 'iphone'}),
            ('branch', {'没有穿好': 'gongchuqi'}),
            ('branch', {'读书有什么用吗': 'duoshu'}),
            ('default', 'xiaoyongle')
        ])
    steps.append(step)
    assert step.id == 'welcome'
    assert step.speak == ['我是心里咨熊师完颜慧德，你有什么要问的吗？']
    assert step.listen == (5, 20)
    assert step.answer == {'闺蜜': 'guimidimi', '我老公喜欢上了我妈妈': 'lonely', '华为手机': 'iphone', '没有穿好': 'gongchuqi', '读书有什么用吗': 'duoshu'}
    assert step.silence == ''
    assert step.default == 'xiaoyongle'
    assert step.exit == None

    step = Step('continue', [
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
        ])
    steps.append(step)
    assert step.id == 'continue'
    assert step.speak == ['还有什么要问的吗？']
    assert step.listen == (5, 20)
    assert step.answer == {'闺蜜': 'guimidimi', '我老公喜欢上了我妈妈': 'lonely', '华为手机': 'iphone', '没有穿好': 'gongchuqi', '读书有什么用吗': 'duoshu', '没': 'end'}
    assert step.silence == 'continue'
    assert step.default == 'xiaoyongle'
    assert step.exit == None

    step = Step('guimidimi', [
            ('speak', ['好嘞，是闺咪，不好嘞，是敌咪。', '什么是敌咪？敌人的秘密就叫敌蜜']),
            ('silence', 'continue')
        ])
    steps.append(step)
    assert step.id == 'guimidimi'
    assert step.speak == ['好嘞，是闺咪，不好嘞，是敌咪。', '什么是敌咪？敌人的秘密就叫敌蜜']
    assert step.listen == ()
    assert step.answer == {}
    assert step.silence == 'continue'
    assert step.default == ''
    assert step.exit == None

    step = Step('lonely', [
            ('speak', ['这就不对啊，这是一个lonely的问题。', '在这个过程中你要去跟你的妈妈谈，同时要跟你的老公去谈。', '如果说谈不脱，就要想进一步的办法。']),
            ('silence', 'continue')
        ])
    steps.append(step)
    assert step.id == 'lonely'
    assert step.speak == ['这就不对啊，这是一个lonely的问题。', '在这个过程中你要去跟你的妈妈谈，同时要跟你的老公去谈。', '如果说谈不脱，就要想进一步的办法。']
    assert step.listen == ()
    assert step.answer == {}
    assert step.silence == 'continue'
    assert step.default == ''
    assert step.exit == None

    step = Step('iphone', [
            ('speak', ['啊？本来我们说的是安分守己，安分守己你怎么又提到手机了呢？']),
            ('silence', 'continue')
        ])
    steps.append(step)
    assert step.id == 'iphone'
    assert step.speak == ['啊？本来我们说的是安分守己，安分守己你怎么又提到手机了呢？']
    assert step.listen == ()
    assert step.answer == {}
    assert step.silence == 'continue'
    assert step.default == ''
    assert step.exit == None

    step = Step('gongchuqi', [
            ('speak', ['你们又在这里带什么节奏！供出去！你还待在这里干嘛？供出去！\\n', '每天总有这些黑粉来捣乱，我从来一般不发火，太不像话了真的是！']),
            ('silence', 'continue')
        ])
    steps.append(step)
    assert step.id == 'gongchuqi'
    assert step.speak == ['你们又在这里带什么节奏！供出去！你还待在这里干嘛？供出去！\\n', '每天总有这些黑粉来捣乱，我从来一般不发火，太不像话了真的是！']
    assert step.listen == ()
    assert step.answer == {}
    assert step.silence == 'continue'
    assert step.default == ''
    assert step.exit == None

    step = Step('duoshu', [
            ('speak', ['duo书的拟人最美丽，duo书的拟人最优秀，duo书的拟人最通情达理。']),
            ('silence', 'continue')
        ])
    steps.append(step)
    assert step.id == 'duoshu'
    assert step.speak == ['duo书的拟人最美丽，duo书的拟人最优秀，duo书的拟人最通情达理。']
    assert step.listen == ()
    assert step.answer == {}
    assert step.silence == 'continue'
    assert step.default == ''
    assert step.exit == None

    step = Step('xiaoyongle', [
            ('speak', ['你这问的什么问题？你把人笑拥了我跟你说']),
            ('silence', 'continue')
        ])
    steps.append(step)
    assert step.id == 'xiaoyongle'
    assert step.speak == ['你这问的什么问题？你把人笑拥了我跟你说']
    assert step.listen == ()
    assert step.answer == {}
    assert step.silence == 'continue'
    assert step.default == ''
    assert step.exit == None

    step = Step('end', [
            ('speak', ['没问题了就供出去']),
            ('exit', True)
        ])
    steps.append(step)
    assert step.id == 'end'
    assert step.speak == ['没问题了就供出去']
    assert step.listen == ()
    assert step.answer == {}
    assert step.silence == ''
    assert step.default == ''
    assert step.exit == True

def test_step_2():
    step = Step('welcome', [
            ('speak', ['欢迎光临 ', '$storename', '，请问有什么可以帮您？']),
            ('listen', (5, 20)),
            ('branch', {'发货': 'ship'}),
            ('branch', {'快递': 'delivery'}),
            ('branch', {'新品': 'new'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc')
        ])
    steps.append(step)
    assert step.id == 'welcome'
    assert step.speak == ['欢迎光临 ', '$storename', '，请问有什么可以帮您？']
    assert step.listen == (5, 20)
    assert step.answer == {'发货': 'ship', '快递': 'delivery', '新品': 'new'}
    assert step.silence == 'silenceproc'
    assert step.default == 'defaultproc'
    assert step.exit == None

    step = Step('ship', [
            ('speak', ['是否帮您查询最近买的东西何时发货？']),
            ('listen', (5, 20)),
            ('branch', {'是': 'shipyes'}),
            ('branch', {'否': 'welcome'}),
            ('silence', 'silenceproc'),
            ('default', 'ship')
        ])
    steps.append(step)
    assert step.id == 'ship'
    assert step.speak == ['是否帮您查询最近买的东西何时发货？']
    assert step.listen == (5, 20)
    assert step.answer == {'是': 'shipyes', '否': 'welcome'}
    assert step.silence == 'silenceproc'
    assert step.default == 'ship'
    assert step.exit == None

    step = Step('shipyes', [
            ('speak', ['发货时间为 ', '$shiptime']),
            ('exit', True)
        ])
    steps.append(step)
    assert step.id == 'shipyes'
    assert step.speak == ['发货时间为 ', '$shiptime']
    assert step.listen == ()
    assert step.answer == {}
    assert step.silence == ''
    assert step.default == ''
    assert step.exit == True

    step = Step('delivery', [
            ('speak', ['是否帮您查询最近的快递信息？']),
            ('listen', (5, 20)),
            ('branch', {'是': 'deliveryyes'}),
            ('branch', {'否': 'welcome'}),
            ('silence', 'silenceproc'),
            ('default', 'delivery')
        ])
    steps.append(step)
    assert step.id == 'delivery'
    assert step.speak == ['是否帮您查询最近的快递信息？']
    assert step.listen == (5, 20)
    assert step.answer == {'是': 'deliveryyes', '否': 'welcome'}
    assert step.silence == 'silenceproc'
    assert step.default == 'delivery'
    assert step.exit == None
    
    step = Step('deliveryyes', [
            ('speak', ['快递情况：', '$deliveryinfo']),
            ('exit', True)
        ])
    steps.append(step)
    assert step.id == 'deliveryyes'
    assert step.speak == ['快递情况：', '$deliveryinfo']
    assert step.listen == ()
    assert step.answer == {}
    assert step.silence == ''
    assert step.default == ''
    assert step.exit == True

    step = Step('new', [
            ('speak', ['我们最近有如下新品：', '$newproducts']),
            ('exit', True)
        ])
    steps.append(step)
    assert step.id == 'new'
    assert step.speak == ['我们最近有如下新品：', '$newproducts']
    assert step.listen == ()
    assert step.answer == {}
    assert step.silence == ''
    assert step.default == ''
    assert step.exit == True

    step = Step('silenceproc', [
            ('speak', ['听不清，请您再说一遍']),
            ('listen', (5, 20)),
            ('branch', {'发货': 'ship'}),
            ('branch', {'快递': 'delivery'}),
            ('branch', {'新品': 'new'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc')
        ])
    steps.append(step)
    assert step.id == 'silenceproc'
    assert step.speak == ['听不清，请您再说一遍']
    assert step.listen == (5, 20)
    assert step.answer == {'发货': 'ship', '快递': 'delivery', '新品': 'new'}
    assert step.silence == 'silenceproc'
    assert step.default == 'defaultproc'
    assert step.exit == None

    step = Step('defaultproc', [
            ('speak', ['你可以向我：查询发货情况 or 查询快递情况 or 查看我们的新品']),
            ('listen', (5, 20)),
            ('branch', {'发货': 'ship'}),
            ('branch', {'快递': 'delivery'}),
            ('branch', {'新品': 'new'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc')
        ])
    steps.append(step)
    assert step.id == 'defaultproc'
    assert step.speak == ['你可以向我：查询发货情况 or 查询快递情况 or 查看我们的新品']
    assert step.listen == (5, 20)
    assert step.answer == {'发货': 'ship', '快递': 'delivery', '新品': 'new'}
    assert step.silence == 'silenceproc'
    assert step.default == 'defaultproc'
    assert step.exit == None

def test_environment_0():
    step_table = {
        'welcome': steps.pop(0),
        'complainproc': steps.pop(0),
        'thanks': steps.pop(0),
        'billproc': steps.pop(0),
        'silenceproc': steps.pop(0),
        'defaultproc': steps.pop(0)
    }

    env = Environment('test1.bs')
    assert env.step_table == step_table
    assert env.step == env.step_table['welcome']

def test_environment_1():
    step_table = {
        'welcome': steps.pop(0),
        'continue': steps.pop(0),
        'guimidimi': steps.pop(0),
        'lonely': steps.pop(0),
        'iphone': steps.pop(0),
        'gongchuqi': steps.pop(0),
        'duoshu': steps.pop(0),
        'xiaoyongle': steps.pop(0),
        'end': steps.pop(0)
    }

    env = Environment('test2.bs')
    assert env.step_table == step_table
    assert env.step == env.step_table['welcome']

def test_environment_2():
    step_table = {
        'welcome': steps.pop(0),
        'ship': steps.pop(0),
        'shipyes': steps.pop(0),
        'delivery': steps.pop(0),
        'deliveryyes': steps.pop(0),
        'new': steps.pop(0),
        'silenceproc': steps.pop(0),
        'defaultproc': steps.pop(0)
    }

    env = Environment('test3.bs')
    assert env.step_table == step_table
    assert env.step == env.step_table['welcome']

def test_step_error_0(capsys):
    with pytest.raises(SystemExit) as e:
        step = Step('welcome', [
            ('speak', ['您好,请问有什么可以帮您?']),
            ('speak', ['这是多出来的 speak']),
            ('listen', (5, 20)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc'),
            ('exit', False)
        ])
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: Step welcome 的 speak 字段有多个\n'

def test_step_error_1(capsys):
    with pytest.raises(SystemExit) as e:
        step = Step('welcome', [
            ('speak', ['您好,请问有什么可以帮您?']),
            ('listen', (5, 20)),
            ('listen', (2, 9)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc'),
            ('exit', False),
        ])
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: Step welcome 的 listen 字段有多个\n'

def test_step_error_2(capsys):
    with pytest.raises(SystemExit) as e:
        step = Step('welcome', [
            ('speak', ['您好,请问有什么可以帮您?']),
            ('listen', (5, 20)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc'),
            ('default', 'defaultproc1'),
            ('exit', False)
        ])
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: Step welcome 的 default 字段有多个\n'

def test_step_error_3(capsys):
    with pytest.raises(SystemExit) as e:
        step = Step('welcome', [
            ('speak', ['您好,请问有什么可以帮您?']),
            ('listen', (5, 20)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc'),
            ('exit', False),
            ('exit', True)
        ])
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: Step welcome 的 exit 字段有多个\n'

def test_step_error_4(capsys):
    with pytest.raises(SystemExit) as e:
        step = Step('welcome', [
            ('listen', (5, 20)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc'),
            ('exit', False),
        ])
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: Step welcome 的 speak 字段不存在\n'

def test_step_error_5(capsys):
    with pytest.raises(SystemExit) as e:
        step = Step('welcome', [
            ('speak', ['您好,请问有什么可以帮您?']),
            ('listen', (5, 20)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc'),
            ('exit', True),
        ])
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: Step welcome 是 exit 步骤，但是含有其他动作\n'

def test_step_error_6(capsys):
    with pytest.raises(SystemExit) as e:
        step = Step('welcome', [
            ('speak', ['您好,请问有什么可以帮您?']),
            ('listen', (-5, 20)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc'),
        ])
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: Step welcome 的 listen 起始时间小于 0\n'

    with pytest.raises(SystemExit) as e:
        step = Step('welcome', [
            ('speak', ['您好,请问有什么可以帮您?']),
            ('listen', (5, -20)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc'),
        ])
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: Step welcome 的 listen 终止时间小于 0\n'

    with pytest.raises(SystemExit) as e:
        step = Step('welcome', [
            ('speak', ['您好,请问有什么可以帮您?']),
            ('listen', (20, 5)),
            ('branch', {"投诉": 'complainproc'}),
            ('branch', {"账单": 'billproc'}),
            ('silence', 'silenceproc'),
            ('default', 'defaultproc'),
        ])
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: Step welcome 的 listen 起始时间大于终止时间\n'

def test_environment_error_0(capsys):
    with pytest.raises(SystemExit) as e:
        env = Environment('testbad1.bs')
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: Step thanks 的 ID 重复\n'

def test_environment_error_1(capsys):
    with pytest.raises(SystemExit) as e:
        env = Environment('testbad2.bs')
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: 缺少 Step welcome 作为入口\n'

def test_environment_error_2(capsys):
    with pytest.raises(SystemExit) as e:
        env = Environment('testbad3.bs')
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: Step welcome 的分支 咨询 的目标 consultproc 不存在\n'

def test_environment_error_3(capsys):
    with pytest.raises(SystemExit) as e:
        env = Environment('testbad4.bs')
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: Step welcome 的 silence 目标 silenceproc 不存在\n'

def test_environment_error_4(capsys):
    with pytest.raises(SystemExit) as e:
        env = Environment('testbad5.bs')
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == 'SemanticFault: Step welcome 的 default 目标 defaultproc 不存在\n'
