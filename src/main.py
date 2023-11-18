"""程序入口"""
from interpreter import *
import sys

def main():
    """程序入口
    """
    if len(sys.argv) != 2: # 检查参数个数
        print("Usage: ./bs <script_file>")
        return
    script_file = sys.argv[1] # 读取脚本文件路径
    env = Environment(script_file) # 读取脚本，创建环境
    while env.step != None: # 执行脚本
        env.speak()
        env.step = env.listen()

if __name__ == "__main__":
    main()
