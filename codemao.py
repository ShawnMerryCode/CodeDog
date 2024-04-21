# CodeDog编程猫黑客端
# Beta1.0
# Powered By ShawnMerry
from colorama import Fore, Style, init
from datetime import datetime
from tqdm import tqdm, trange
from time import sleep
import configparser
import ping3
import requests
import json
import pandas
import sys
import os

init(autoreset=True)
Connect_Status = False
config = configparser.ConfigParser()

if os.path.exists("config.ini") and os.path.isfile("config.ini"):  # 初始化
    config.read("config.ini")
    account_file = config["Paths"]["account_file"]
else:
    config["Paths"] = {
        "account_file": "accounts.xlsx"
    }
    config["Data"] = {
        "token": "",
        "testURL": "codemao.cn"
    }
    with open("config.ini", "w") as configfile:
        config.write(configfile)
    account_file = "accounts.xlsx"  # 配置


def print_line(char='-', width=54):
    print(char * width)


def main():
    welcome_text = Style.BRIGHT + "欢迎使用" + Fore.RED + "「编程狗」" + Fore.RESET + "编程猫黑客端!"
    print(welcome_text.center(54), "\n", "Powered By ShawnMerry".center(50), "\n", "输入\"help\"以获取帮助".center(45))
    print_line()
    if len(config.get("Data", "token")) > 0:
        response = requests.get("https://api.codemao.cn/tiger/v3/web/accounts/profile",
                                cookies={"authorization": config.get("Data", "token")})
        print(Style.BRIGHT + "欢迎您，" + json.loads(response.text)["nickname"] + "!")
        print(Style.BRIGHT + "现在是" + str(datetime.now()))
        print_line()
    while True:
        command = input(">>> ")
        if command == "test":
            test()
        elif command == "info":
            info()
        elif command == "exit":
            print(Style.BRIGHT + "Bye!")
            exit()
        elif command[0:3] == "sel":
            sel(command.split())
        elif command[0:5] == "login":
            login(command.split())
        elif command == "send":
            send()
        elif command == "like":
            like()
        elif command == "report":
            report()
        elif command == "collection":
            collection()
        elif command == "follow":
            follow()
        elif command == "fork":
            fork()
        elif command == "help":
            codedog_help()
        elif command[0:5] == "token":
            token(command.split())
        elif command == "raname":
            random_nickname()
        elif command[0:6] == "config":
            config_command(command.split())
        else:
            print(Style.BRIGHT + Fore.RED + "[×] Unknown Command")


def codedog_help():
    print(Style.BRIGHT + "CodeDog 帮助".center(54))
    print_line("_ ", 27)
    print("    欢迎使用CodeDog客户端！CodeDog是一款基于Python开发的编程猫操作\n"
          "软件，Normal Version支持登录、点赞等，Hacker Version则可以刷\n"
          "赞/收藏/粉丝/再创作/举报等。")
    print(Style.BRIGHT + "CodeDog使用手册正在编写中！".center(54))
    print_line()


def test():
    result = ping3.ping(config.get("Data", "testURL"))
    if result:
        print(Fore.LIGHTGREEN_EX + "Client Status:OK " + Fore.RESET + '/' + Fore.LIGHTGREEN_EX + " Connect Status:OK")
    else:
        print(Fore.LIGHTGREEN_EX + "Client Status:OK " + Fore.RESET + '/' + Fore.LIGHTRED_EX + " Connect Status:NO")
    print_line()


def info():
    print(Style.BRIGHT + "CodeDog".center(54) + "\n" + "Hacker Version".center(54) + "\n" + Style.RESET_ALL +
          "Build24042101".center(54) + "\n" + "Beta 1.0".center(54))
    print_line()


def random_nickname():
    response = json.loads(requests.get("https://api.codemao.cn/api/user/random/nickname").text)
    print(Style.BRIGHT + "随机昵称：" + Style.RESET_ALL + response["data"]["nickname"])


def token(sub):
    if sub[1] == "query":
        print("您的Token：" + config.get("Data", "token"))
    elif sub[1] == "change":
        config["Data"]["token"] = sub[2]
        with open("config.ini", "w") as configfile1:
            config.write(configfile1)
        print(Style.BRIGHT + "更改成功！")
    elif sub[1] == "delete":
        config["Data"]["token"] = ""
        print(Style.BRIGHT + "删除成功！")
    else:
        print(Style.BRIGHT + Fore.RED + "[×] Unknown Sub Command")
    print_line()


def config_command(sub):
    if sub[1] == "create" or sub[1] == "reset":
        config["Paths"] = {
            "account_file": "accounts.xlsx"
        }
        config["Data"] = {
            "token": "",
            "testURL": "codemao.cn"
        }
        with open("config.ini", "w") as configfile2:
            config.write(configfile2)
        print(Style.BRIGHT + "配置创建成功！")
    elif sub[1] == "set":
        config[sub[2]][sub[3]] = sub[4]
        with open("config.ini", "w") as configfile2:
            config.write(configfile2)
        print(Style.BRIGHT + "配置设置成功！")
    elif sub[1] == "query":
        print(Style.BRIGHT + sub[2] + " 类中的 " + sub[3] + " 配置的值为：" + Style.RESET_ALL + config[sub[2]][sub[3]])
    print_line()


def sel(sub):
    if sub[1] == "edu":
        print("给我找Natriumchlorid去！")
    else:
        print(Style.BRIGHT + Fore.RED + "[×] Unknown Sub Command")
    print_line()


def login(account):
    if len(account) > 1:
        data = {"pid": "65edCTyg", "identity": account[1], "password": account[2]}
        response = requests.post("https://api.codemao.cn/tiger/v3/web/accounts/login", json=data)
        response_fin = json.loads(response.text)
        if response.status_code != 200:
            print(Style.BRIGHT + Fore.RED +
                  "[×] Account:" + account[1] + " error!\nError Code:" + str(response.status_code))
            return
        print("您好，" + response_fin["user_info"]["nickname"] + "!")
        print("您的Token：" + response_fin["auth"]["token"])
        config["Data"]["token"] = response_fin["auth"]["token"]
        with open("config.ini", "w") as configfile3:
            config.write(configfile3)
    else:
        print(Style.BRIGHT + Fore.RED + "[×] Identity or Password is empty")
    print_line()


def send():
    send_type = input("发布类型（1：发帖 2：回帖 3：回复）:")
    if send_type == '1':
        board_id = input("板块ID：")
        user_token = input("用户Token：")
        if user_token == "Default":
            user_token = config.get("Data", "token")
        title = input("帖子标题：")
        content = input("帖子内容（HTML格式）：")
        execute_times = int(input("执行次数："))
        url = "https://api.codemao.cn/web/forums/boards/" + board_id + "/posts"
        cookie = {"authorization": user_token}
        data = {"title": title, "content": content}
        for _ in trange(execute_times, desc="刷帖子中", unit="％", file=sys.stdout):
            sleep(5)
            response = requests.post(url=url, json=data, cookies=cookie)
            if response.status_code == 201:
                temp1 = json.loads(response.text)
                tqdm.write("\n发送成功！帖子ID为：" + temp1["id"])
            else:
                tqdm.write(Style.BRIGHT + Fore.RED + "\n发送失败，状态码：" + str(response.status_code))
    elif send_type == '2':
        post_id = input("帖子ID：")
        user_token = input("用户Token：")
        if user_token == "Default":
            user_token = config["Data"]["token"]
        content = input("回帖内容（HTML格式）：")
        execute_times = int(input("执行次数："))
        url = "https://api.codemao.cn/web/forums/posts/" + post_id + "/replies"
        cookie = {"authorization": user_token}
        data = {"content": content}
        for _ in trange(execute_times, desc="刷回帖中", unit="％", file=sys.stdout):
            sleep(5)
            response = requests.post(url=url, json=data, cookies=cookie)
            if response.status_code != 201:
                tqdm.write(Style.BRIGHT + Fore.RED + "\n发送失败，状态码：" + str(response.status_code))
    else:
        print(Style.BRIGHT + Fore.RED + "[×] Unknown send type:" + send_type)
    print_line()


def like():
    data = pandas.read_excel(account_file)
    url_login = "https://api.codemao.cn/tiger/v3/web/accounts/login"
    times = int(input("请输入刷赞账号个数："))
    work_id = input("请输入作品ID：")
    url_like = "https://api.codemao.cn/nemo/v2/works/" + work_id + "/like"
    for i in trange(times, desc="刷赞中", unit="％", file=sys.stdout):
        identity = data.at[i, "账号"]
        password = data.at[i, "初始密码"]
        data_login = {"pid": "65edCTyg", "identity": str(identity), "password": str(password)}
        response_login = requests.post(url_login, json=data_login)
        if response_login.status_code != 200:
            tqdm.write(Style.BRIGHT + Fore.RED +
                       "\n[×] Account:" + str(identity) + " error!\nError Code:" + str(response_login.status_code))
            continue
        user_token = json.loads(response_login.text)["auth"]["token"]
        cookie = {"authorization": user_token}
        response_like = requests.post(url=url_like, cookies=cookie)
        if response_like.status_code != 200:
            tqdm.write(Style.BRIGHT + Fore.RED +
                       "\n[×] Like:" + str(identity) + " error!\nError Code:" + str(response_like.status_code))
        sleep(0.5)
    print_line()


def collection():
    data = pandas.read_excel(account_file)
    url_login = "https://api.codemao.cn/tiger/v3/web/accounts/login"
    times = int(input("请输入刷收藏账号个数："))
    work_id = input("请输入作品ID：")
    url_collect = "https://api.codemao.cn/nemo/v2/works/" + work_id + "/collection"
    for i in trange(times, desc="刷收藏中", unit="％", file=sys.stdout):
        identity = data.at[i, "账号"]
        password = data.at[i, "初始密码"]
        data_login = {"pid": "65edCTyg", "identity": str(identity), "password": str(password)}
        response_login = requests.post(url_login, json=data_login)
        if response_login.status_code != 200:
            tqdm.write(Style.BRIGHT + Fore.RED +
                       "\n[×] Account:" + str(identity) + " error!\nError Code:" + str(response_login.status_code))
            continue
        user_token = json.loads(response_login.text)["auth"]["token"]
        cookie = {"authorization": user_token}
        response_collect = requests.post(url=url_collect, cookies=cookie)
        if response_collect.status_code != 200:
            tqdm.write(Style.BRIGHT + Fore.RED +
                       "\n[×] Collect:" + str(identity) + " error!\nError Code:" + str(response_collect.status_code))
    print_line()


def fork():
    data = pandas.read_excel(account_file)
    url_login = "https://api.codemao.cn/tiger/v3/web/accounts/login"
    times = int(input("请输入刷再创作账号个数："))
    work_id = input("请输入作品ID：")
    url_fork = "https://api.codemao.cn/nemo/v2/works/" + work_id + "/fork"
    for i in trange(times, desc="刷再创作中", unit="％", file=sys.stdout):
        identity = data.at[i, "账号"]
        password = data.at[i, "初始密码"]
        data_login = {"pid": "65edCTyg", "identity": str(identity), "password": str(password)}
        response_login = requests.post(url_login, json=data_login)
        if response_login.status_code != 200:
            tqdm.write(Style.BRIGHT + Fore.RED +
                       "\n[×] Account:" + str(identity) + " error!\nError Code:" + str(response_login.status_code))
            continue
        user_token = json.loads(response_login.text)["auth"]["token"]
        cookie = {"authorization": user_token}
        response_fork = requests.post(url=url_fork, cookies=cookie)
        if response_fork.status_code != 200:
            tqdm.write(Style.BRIGHT + Fore.RED +
                       "\n[×] Fork:" + str(identity) + " error!\nError Code:" + str(response_fork.status_code))
        sleep(0.5)
    print_line()


def follow():
    data = pandas.read_excel(account_file)
    url_login = "https://api.codemao.cn/tiger/v3/web/accounts/login"
    times = int(input("请输入刷粉账号个数："))
    user_id = input("请输入用户ID：")
    url_follow = "https://api.codemao.cn/nemo/v2/user/" + user_id + "/follow"
    for i in trange(times, desc="刷粉中", unit="％", file=sys.stdout):
        identity = data.at[i, "账号"]
        password = data.at[i, "初始密码"]
        data_login = {"pid": "65edCTyg", "identity": str(identity), "password": str(password)}
        response_login = requests.post(url_login, json=data_login)
        if response_login.status_code != 200:
            tqdm.write(Style.BRIGHT + Fore.RED +
                       "\n[×] Account:" + str(identity) + " error!\nError Code:" + str(response_login.status_code))
            continue
        user_token = json.loads(response_login.text)["auth"]["token"]
        cookie = {"authorization": user_token}
        response_follow = requests.post(url=url_follow, cookies=cookie)
        if response_follow.status_code != 204:
            tqdm.write(Style.BRIGHT + Fore.RED +
                       "\n[×] Follow:" + str(identity) + " error!\nError Code:" + str(response_follow.status_code))
        sleep(0.5)
    print_line()


def report():
    data = pandas.read_excel(account_file)
    url_login = "https://api.codemao.cn/tiger/v3/web/accounts/login"
    times = int(input("请输入举报账号个数："))
    post_id = input("请输入帖子ID：")
    reason_id = input("请输入举报原因ID（ID见举报界面顺序）：")
    description = input("请输入举报描述：")
    for i in trange(times, desc="刷举报中", unit="％", file=sys.stdout):
        identity = data.at[i, "账号"]
        password = data.at[i, "初始密码"]
        data_login = {"pid": "65edCTyg", "identity": str(identity), "password": str(password)}
        response_login = requests.post(url_login, json=data_login)
        if response_login.status_code != 200:
            tqdm.write(Style.BRIGHT + Fore.RED +
                       "\n[×] Account:" + str(identity) + " error!\nError Code:" + str(response_login.status_code))
            continue
        user_token = json.loads(response_login.text)["auth"]["token"]
        data_report = {"description": description, "post_id": post_id, "reason_id": reason_id}
        cookie = {"authorization": user_token}
        response_report = requests.post(url="https://api.codemao.cn/web/reports/posts", json=data_report,
                                        cookies=cookie)
        if response_report.status_code != 201:
            tqdm.write(Style.BRIGHT + Fore.RED +
                       "\n[×] Report:" + str(identity) + " error!\nError Code:" + str(response_report.status_code))
        sleep(0.5)
    print_line()


if __name__ == "__main__":
    main()
