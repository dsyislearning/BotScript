from interpreter import *

def main():
    env = Environment("../tests/test.bs")
    while env.step != None:
        env.speak()
        env.step = env.listen()

if __name__ == "__main__":
    main()
