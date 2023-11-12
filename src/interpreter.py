from parse import parser
import readline

class Step:
    """Step 类，用于存储每个步骤的信息
    """
    def __init__(self, id: str, step: list) -> None:
        """Step 类的构造函数

        Args:
            id (str): Step 的 ID
            step (list): Step 的内容，由 parser 生成
        """
        self.id = id
        self.speak = []
        self.listen = ()
        self.answer = {}
        self.silence = ''
        self.default = ''
        self.exit = False
        self.set_step(step)

    def set_step(self, step: list) -> None:
        """设置 Step 的内容

        Args:
            step (list): Step 的内容，由 parser 生成
        """
        for action in step:
            if action[0] == 'speak':
                self.speak = action[1]
            elif action[0] == 'listen':
                self.listen = action[1]
            elif action[0] == 'branch':
                self.answer.update(action[1])
            elif action[0] == 'silence':
                self.silence = action[1]
            elif action[0] == 'default':
                self.default = action[1]
            elif action[0] == 'exit':
                self.exit = True

    def __str__(self) -> str:
        """Step 的字符串表示

        Returns:
            str: Step 的字符串表示
        """
        return f'{self.id}\n' + \
            f'speak: {self.speak}\n' + \
            f'listen: {self.listen}\n' + \
            f'answer: {self.answer}\n' + \
            f'silence: {self.silence}\n' + \
            f'default: {self.default}\n' + \
            f'exit: {self.exit}\n'


class Environment:
    """Environment 类，用于存储脚本的信息
    """
    def __init__(self, script_file: str) -> None:
        """Environment 类的构造函数

        Args:
            script_file (str): 脚本文件的路径
        """
        self.var_table = {}
        self.step_table = {}
        self.step = None
        with open(script_file, 'r', encoding='utf-8') as f:
            script_string = ''.join(f.readlines()).lower()
            self.script = parser.parse(script_string)
            self.make_step_table(self.script)
            self.step = self.step_table['welcome']

    def make_step_table(self, script: list) -> None:
        """生成 Step 表

        Args:
            script (list): 脚本，由 parser 生成
        """
        for step in script:
            id = step[0]
            self.step_table[id] = Step(id, step[1])

    def speak(self) -> None:
        """输出 Step 的 speak 字段
        """
        print(''.join(self.step.speak))

    def listen(self) -> str:
        """获取用户输入，并返回下一个 Step 的 ID

        Returns:
            str: 下一个 Step 的 ID
        """
        if self.step.exit:
            return None
        answer = input()
        for key, value in self.step.answer.items():
            if not answer:
                break
            elif key in answer:
                return self.step_table[value]
        if not answer:
            return self.step_table[self.step.silence]
        else:
            return self.step_table[self.step.default]
