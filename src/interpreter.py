from parse import parser
import readline

class Step:
    def __init__(self, id, step) -> None:
        self.id = id
        self.speak = []
        self.listen = ()
        self.answer = {}
        self.silence = ''
        self.default = ''
        self.exit = False
        self.set_step(step)

    def set_step(self, step):
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
        return f'{self.id}\n' + \
            f'speak: {self.speak}\n' + \
            f'listen: {self.listen}\n' + \
            f'answer: {self.answer}\n' + \
            f'silence: {self.silence}\n' + \
            f'default: {self.default}\n' + \
            f'exit: {self.exit}\n'


class Environment:
    def __init__(self, script_file):
        self.var_table = {}
        self.step_table = {}
        self.step = None
        with open(script_file, 'r', encoding='utf-8') as f:
            script_string = ''.join(f.readlines()).lower()
            self.script = parser.parse(script_string)
            self.make_step_table(self.script)
            self.step = self.step_table['welcome']

    def make_step_table(self, script):
        for step in script:
            id = step[0]
            self.step_table[id] = Step(id, step[1])

    def speak(self):
        print(''.join(self.step.speak))

    def listen(self) -> str:
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
