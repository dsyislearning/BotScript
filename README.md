# BotScript

[English Version README](#en)

本项目是 BUPT 2023 秋季学期《程序设计实践》选修课的课程项目。主要考察以下内容：

- 风格
- 设计与实现
- 接口
- 测试
- 记法

## 概述

BotScript 是一个领域特定脚本语言（Domain Specific Language，DSL），这个语言能够描述在线客服机器人的自动应答逻辑，用户可以根据脚本的逻辑设计一个自己的机器人。


## 功能

- 使用 **PLY**（Python Lex Yacc）模块构建词法分析器与语法分析器并进行语法制导翻译
- 使用 **bash** 脚本实现自动配置环境，命令行用户接口运行机器人程序
- 使用 **Pytest** 模块进行单元测试、功能测试，实现脚本自动化测试
- 使用 **Sphinx** 模块及 `sphinx-autoapi` 插件根据文档字符串自动生成 API 文档

## 使用方法

克隆本项目到本地：

```zsh
git clone git@github.com:dsyislearning/BotScript.git
```

进入项目根目录：

```zsh
cd BotScript
```

根据语法规则写好机器人脚本，以 `$PWD/tests/test1.bs` 为例，使用脚本启动机器人：

```zsh
./bs ./tests/test1.bs
```

第一次执行会提示需要配置虚拟环境并安装使用到的包，输入 `y` 确认自动配置环境：

```zsh
Virtual environment not found, create one? [Y/n]
y
Creating virtual environment...
```

环境安装好后自动进入脚本编写的机器人交互界面：

```zsh
$ ./bs ./tests/test1.bs
Virtual environment not found, create one? [Y/n]
y
Creating virtual environment...
...

$name您好,请问有什么可以帮您?

```

输入用户应答后回车即可与机器人交互。

## API 文档构建

自动构建 API 文档的配置文件已经保存在 `doc/` 中，有如下文件：

```
doc
├── build
├── make.bat
├── Makefile
└── source
```

假设当前在项目根目录，并已经使用 `bs` 运行脚本配置过虚拟环境并安装好了所需的依赖，进入文档目录：

```zsh
cd doc
```

使用 Sphinx 自动构建 API 文档：

```zsh
sphinx-build ./source build
```

使用浏览器打开 `./build/index.html` 即为自动构建的 API 文档

## 简单样例

使用 `tests/test1.bs` 测试的对话机器人有如下对话：

```
$ ./bs ./tests/test1.bs
$name您好,请问有什么可以帮您?
你可以做什么
你可以向我：投诉 or 查账单
我要投诉
您的意见是我们改进工作的动力,请问您还有什么补充?
没有
感谢您的来电,再见
```

---

<h1 id="en">BotScript (English version readme)</h1>

This project is a course project of the *The Practice of Programming* elective course in BUPT's 2023 fall semester. Mainly examine the following contents:

- Style
- Design and Implementation
- Interfaces
- Testing
- Notation

## Overview

BotScript is a Domain-Specific Scripting Language (DSL) that can describe the automatic response logic of online customer service chatbots. Users can design their own chatbots based on the logic of the script.

## Features

- Use the **PLY** (Python Lex Yacc) module to build a lexer and parser and perform syntax-directed translation.
- Use a **bash** script to automate environment configuration and run the chatbot program via a command-line user interface.
- Use the **Pytest** module for unit testing and functional testing to achieve script automation testing.
- Use the **Sphinx** module and the `sphinx-autoapi` plugin to automatically generate API documentation based on docstrings.

## Usage

Clone this project to your local environment:

```zsh
git clone git@github.com:dsyislearning/BotScript.git
```

Navigate to the root directory of the project:

```zsh
cd BotScript
```

Once you have written the bot script based on the syntax rules, let's assume it is located at `$PWD/tests/test1.bs`. You can launch the bot using the following command:

```zsh
./bs ./tests/test1.bs
```

On the first execution, it will prompt you to configure a virtual environment and install the required packages. Type `y` to confirm automatic environment configuration:

```zsh
Virtual environment not found, create one? [Y/n]
y
Creating virtual environment...
```

Once the environment is set up, you will enter the interactive interface of the bot script:

```zsh
$ ./bs ./tests/test1.bs
Virtual environment not found, create one? [Y/n]
y
Creating virtual environment...
...

Hello $name, how can I assist you?

```

You can interact with the bot by entering your response and pressing Enter.

## API Docs Generation

The configuration files for automatically generating API documentation are saved in the `doc/` directory, which contains the following files:

```
doc
├── build
├── make.bat
├── Makefile
└── source
```

Assuming you are currently in the project's root directory and have already set up the virtual environment and installed the required dependencies using `bs`, navigate to the documentation directory:

```zsh
cd doc
```

Use Sphinx to automatically build the API documentation:

```zsh
sphinx-build ./source build
```

To view the automatically generated API documentation, open `./build/index.html` in a web browser.

Please note that the actual content and structure of the API documentation will depend on the configuration and source files in the `source/` directory.

## Samples

The dialogue with the chatbot tested using `tests/test1.bs` is as follows:

```
$ ./bs ./tests/test1.bs
Hello $name, how can I assist you?
What can you do?
You can: file a complaint or check your billing statement.
I want to file a complaint.
Your feedback is our motivation for improvement. Is there anything else you would like to add?
No, that's all.
Thank you for your call. Goodbye.
```

