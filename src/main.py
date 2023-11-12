from interpreter import *

def main():
    env = Environment("../tests/test.bs") # 读取脚本，创建环境
    while env.step != None: # 执行脚本
        env.speak()
        env.step = env.listen()

if __name__ == "__main__":
    main()
