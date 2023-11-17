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
        self.exit = None
        self.set_step(step)
        self.check_step()

    def set_step(self, step: list) -> None:
        """设置 Step 的内容

        Args:
            step (list): Step 的内容，由 parser 生成
        """
        try:
            for action in step:
                if action[0] == 'speak':
                    if not self.speak:
                        self.speak = action[1]
                    else:
                        raise Exception(f"Step {self.id} 的 speak 字段有多个") # 每个 Step 只能有一个 speak 字段
                elif action[0] == 'listen':
                    if not self.listen:
                        self.listen = action[1]
                    else:
                        raise Exception(f"Step {self.id} 的 listen 字段有多个") # 每个 Step 只能有一个 listen 字段
                elif action[0] == 'branch':
                    self.answer.update(action[1]) # 每个 Step 可以有多个 branch 字段
                elif action[0] == 'silence':
                    if not self.silence:
                        self.silence = action[1]
                    else:
                        raise Exception(f"Step {self.id} 的 silence 字段有多个") # 每个 Step 只能有一个 silence 字段
                elif action[0] == 'default':
                    if not self.default:
                        self.default = action[1]
                    else:
                        raise Exception(f"Step {self.id} 的 default 字段有多个") # 每个 Step 只能有一个 default 字段
                elif action[0] == 'exit':
                    if self.exit == None:
                        self.exit = True
                    else:
                        raise Exception(f"Step {self.id} 的 exit 字段有多个") # 每个 Step 只能有一个 exit 字段
        except Exception as e:
            print('SemanticFault:', e)
            exit(1)

    def check_step(self) -> None:
        """检查 Step 的语义是否正确，并给出错误信息

        Raises:
            Exception: speak 字段不存在
            Exception: Step 是 exit 步骤，但是含有其他动作
            Exception: Step 的 listen 起始时间小于 0
            Exception: Step 的 listen 终止时间小于 0
            Exception: Step 的 listen 起始时间大于终止时间
        """
        try:
            # 每个 Step 必须有且只有一个 speak 字段
            if not self.speak:
                raise Exception(f"Step {self.id} 的 speak 字段不存在")

            # 有 exit 的 Step 不能有除了 speak 以外的其他动作
            if self.exit and (self.listen or self.answer or self.silence or self.default):
                raise Exception(f"Step {self.id} 是 exit 步骤，但是含有其他动作")

            # 检查 listen 的起止时间是否正确
            if self.listen:
                if self.listen[0] < 0:
                    raise Exception(f"Step {self.id} 的 listen 起始时间小于 0")
                if self.listen[1] < 0:
                    raise Exception(f"Step {self.id} 的 listen 终止时间小于 0")
                if self.listen[0] > self.listen[1]:
                    raise Exception(f"Step {self.id} 的 listen 起始时间大于终止时间")
        except Exception as e:
            print('SemanticFault:', e)
            exit(1)

    def __str__(self) -> str:
        """Step 的字符串表示，用于调试

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
    
    def __eq__(self, __value: object) -> bool:
        """Step 的相等比较

        Args:
            __value (object): 要比较的对象

        Returns:
            bool: 相等返回 True，否则返回 False
        """
        if not isinstance(__value, Step):
            return False
        return self.id == __value.id and \
            self.speak == __value.speak and \
            self.listen == __value.listen and \
            self.answer == __value.answer and \
            self.silence == __value.silence and \
            self.default == __value.default and \
            self.exit == __value.exit


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
            try:
                if 'welcome' not in self.step_table:
                    raise Exception('缺少 Step welcome 作为入口')
                else:
                    self.step = self.step_table['welcome']
            except Exception as e:
                print('SemanticFault:', e)
                exit(1)
            self.check_semantic()

    def make_step_table(self, script: list) -> None:
        """生成 Step 表，用于存储每个步骤的信息

        Args:
            script (list): 脚本，由 parser 生成
        """
        try:
            for step in script:
                id = step[0]
                if id in self.step_table:
                    raise Exception(f"Step {id} 的 ID 重复")
                self.step_table[id] = Step(id, step[1])
        except Exception as e:
            print('SemanticFault:', e)
            exit(1)

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

        if self.step.listen:
            answer = input()
        else:
            answer = ''

        for key, value in self.step.answer.items():
            if not answer:
                break
            elif key in answer:
                return self.step_table[value]

        if not answer:
            return self.step_table[self.step.silence]
        else:
            return self.step_table[self.step.default]

    def check_semantic(self) -> None:
        try:
            # 如果有的话，检查分支的目标是否存在
            for step in self.step_table.values():
                for key, value in step.answer.items():
                    if value not in self.step_table:
                        raise Exception(f"Step {step.id} 的分支 {key} 的目标 {value} 不存在")

            # 如果有的话，检查 silence 和 default 的目标是否存在
            for step in self.step_table.values():
                if step.silence and step.silence not in self.step_table:
                    raise Exception(f"Step {step.id} 的 silence 目标 {step.silence} 不存在")
                if step.default and step.default not in self.step_table:
                    raise Exception(f"Step {step.id} 的 default 目标 {step.default} 不存在")
        except Exception as e:
            print('SemanticFault:', e)
            exit(1)
