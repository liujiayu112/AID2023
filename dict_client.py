"""
    dict 客户端
    功能：根据用户输入，发送请求，得到结果
    结构：一级界面：注册，登录，退出
         二级界面：查单词，历史记录，注销
"""
import sys
from socket import *
from getpass import getpass  # 只支持终端运行

# 服务器地址
IP_ADDR = ('127.0.0.1', 8000)
# tcp 套接字
s = socket()
s.connect(IP_ADDR)

first_interface = """
1. 注册
2. 登录
3. 退出
"""
after_interface = """
1. 查单词
2. 历史记录
3. 注销
"""


# ==================================================================


def do_register():
    while True:
        name = input("User：")
        passwd = getpass()
        passwd1 = getpass("Again: ")
        if passwd != passwd1:
            print("两次输入密码不一致！")
            continue
        if ' ' in name or ' ' in passwd:
            print("用户名密码不能有空格")
            continue
        msg = "R %s %s" % (name, passwd)
        s.send(msg.encode())  # 发送给服务器
        data = s.recv(128).decode()  # 接收结果
        if data == 'OK':
            print("注册成功！")
            login(name)
        else:
            print("注册失败！")
        return


def do_query(name):
    """
    查单词
    :param name:
    """
    while True:
        word = input("单词：")
        if word == '##':
            break
        msg = "Q %s %s" % (name, word)
        s.send(msg.encode())  # 发送请求
        # 得到查询结果
        data = s.recv(2048).decode()
        print(data)


def do_hist(name):
    """
    历史记录
    :param name: 用户名
    """
    msg = "H %s" % name
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print("没有查询记录")


# 二级界面，登录后的状态
def login(name):
    while True:
        print(after_interface)
        cmd = input("输入选项：")
        if cmd == "1":
            do_query(name)
        elif cmd == "2":
            do_hist(name)
        elif cmd == "3":
            return
        else:
            print("请输入正确选项！")


# 登录
def do_login():
    name = input("User: ")
    passwd = getpass()
    msg = "L %s %s" % (name, passwd)
    s.send(msg.encode())  # 发送请求
    data = s.recv(128).decode()
    if data == 'OK':
        print("登录成功")
        login(name)
    else:
        print("登录失败")


# 搭建客户端网络
def main():
    while True:
        print(first_interface)
        cmd = input("请输入选项：")
        if cmd == "1":
            do_register()
            s.send(cmd.encode())
        elif cmd == "2":
            do_login()
        elif cmd == "3":
            s.send(b'E')
            sys.exit("退出程序")
        else:
            print("请输入正确选项！")


if __name__ == "__main__":
    main()
