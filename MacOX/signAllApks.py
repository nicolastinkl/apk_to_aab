import os
import glob
import subprocess

import platform
import sys
import shutil
import random
import hashlib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def get_file_content(file_name):
    # 获取当前工作目录
    current_dir = os.getcwd()

    # 构建文件路径
    file_path = os.path.join(current_dir, file_name)

    # 检查文件是否存在
    if not os.path.isfile(file_path):
        print(f"文件 '{file_name}' 不存在")
        return None

    # 读取文件内容
    with open(file_path, "r") as file:
        content = file.read()

    return content


# 定义 ANSI 转义序列
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
# 输出彩色文本

# 当前目录

# # 获取目录名和平台参数
directory = ""
try:
    directory = sys.argv[1]
except:
    print("用法不对，例如： python signAll xxxx")
# platform = sys.argv[2]


if len(directory) <= 0:
    sys.exit(0)
# 当前目录

WINDOWS = "Windows"
Linux = "Linux"
MACOS = "Darwin"

PathStr = "\\"
if platform.platform().find("macOS") != -1 or platform.platform().find("Darwin") != -1:
    PathStr = "/"
    gradecmd = "./gradlew"


def get_system() -> str:
    return platform.system()


def execute_cmd(cmd):
    status = os.system(cmd)
    return status, ""


print("[当前系统]:")
platform_system = get_system()
print(platform_system)
current_dir = os.path.join(os.getcwd(), directory)
print(current_dir)
directory = current_dir
dbtype_list = os.listdir(current_dir)


subdirectories = [
    name for name in dbtype_list if os.path.isdir(os.path.join(current_dir, name))
]
print("[是否有存在子文件夹]:", subdirectories)

# 定义脚本列表
scriptsss = []
keystoreContent = ""
apkpath = ""
first_file = ""
hasaabfile = 0


# 首先检查签名文件夹情况
print("[检查签名文件以及信息]:")
aliases = ""
Pwd = ""
organization = ""

keystore_file = ""
keystore_file_name = ""
ndkPath = ""
print(f"[执行检测目錄]: {directory}")
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        with open(file_path, "r") as f:
            # 读取文件内容
            content = f.read()
            keystoreContent = content
    if filename.endswith(".keystore"):
        first_file = os.path.join(directory, filename)

    if filename.endswith(".jks"):
        first_file = os.path.join(directory, filename)

    if filename.endswith(".apk"):
        apkpath = os.path.join(directory, filename)

    if filename.endswith(".aab"):
        hasaabfile = 1

if keystoreContent.find("-") != -1:
    print(RED + f"{keystoreContent}" + RESET)
    keystore_file = first_file
    for line in keystoreContent.split("\n"):
        print(f"line:{line}")
        if line is None or len(line) <= 0:
            continue
        key, value = line.split("-")
        if key.strip() == "Alias":
            aliases = value.strip()
        if key.strip() == "Password":
            Pwd = value.strip()
        if key.strip() == "Pwd":
            Pwd = value.strip()
        if key.strip() == "organization":
            organization = value.strip()
            # aliases[key] = value
else:
    # 读取txt密码 然后取alias值
    keystore_password = keystoreContent.rstrip()
    Pwd = keystore_password
    keystore_file = first_file
    # 构建 keytool 命令
    command = (
        f'keytool -list -v -keystore "{keystore_file}" -storepass "{keystore_password}"'
    )
    print(command)
    # 执行命令并获取输出
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, error = process.communicate()
    try:
        output_str = output.decode("cp936")
    except:
        output_str = output.decode("utf-8")

    print("[keytool -list -v -keystore运行结果]：")

    # 解析输出以获取 alias 字符串
    alias_index = output_str.find("Alias:")
    if alias_index != -1:
        alias_end_index = output_str.find("\n", alias_index)
        alias_string = output_str[alias_index:alias_end_index]
        aliasnamestring = alias_string.split(":")[1].strip()
        print(f"Alias: <{aliasnamestring}>")
        if len(aliasnamestring) > 0:
            aliases = aliasnamestring
    else:
        print("[Alias not found]")

    # 解析输出以获取 alias 字符串
    alias_index = output_str.find("别名:")
    if alias_index != -1:
        alias_end_index = output_str.find("\n", alias_index)
        alias_string = output_str[alias_index:alias_end_index]
        aliasnamestring = alias_string.split(":")[1].strip()
        print(f"别名: <{aliasnamestring}>")
        if len(aliasnamestring) > 0:
            aliases = aliasnamestring
    else:
        print("[别名 not found]")

    #
    # 解析输出以获取 alias 字符串
    alias_index = output_str.find("Alias name:")
    if alias_index != -1:
        alias_end_index = output_str.find("\n", alias_index)
        alias_string = output_str[alias_index:alias_end_index]
        aliasnamestring = alias_string.split(":")[1].strip()
        print(f"Alias name: <{aliasnamestring}>")
        if len(aliasnamestring) > 0:
            aliases = aliasnamestring
    else:
        print("[Alias name: not found]")

    # 检查错误信息
    if process.returncode != 0:
        try:
            print(f"Error: {error.decode('cp936')}")

        except:
            print(f"Error: {error.decode('utf-8')}")

    # print(f"{first_file}")

    if Pwd is not None and aliases is not None and len(Pwd) > 2 and hasaabfile == 0:
        print("[KeyStore拆分结果]：", aliases, Pwd, organization)

        # exec: python.exe bundletool.py -i  ${input_path}  -o ${des_path} --keystore ${first_file}  --store_password BlackJackPoker1!@# --key_alias  BlackJackPoker  --key_password   BlackJackPoker1!@#
        time_now = datetime.now()
        current_time = time_now.strftime("%H_%M_%S")

        print("请选择输出格式：")
        print("1. APK")
        print("2. AAB")
        # 获取用户输入

        user_choice = input("请输入选项 (1 或 2): ").strip()
        apkout = "apk"
        if user_choice == "1":
            print("您选择了输出 APK 格式")
            apkout = "apk"
        elif user_choice == "2":
            print("您选择了输出 AAB 格式")
            apkout = "aab"
        else:
            print("默认选择输出APK")

        if platform_system == WINDOWS:
            signstring = f"python.exe bundletool.py -i {apkpath} -o {apkpath}_{current_time}_new.{apkout}  --keystore {first_file}  --store_password {Pwd} --key_alias  {aliases}  --key_password  {Pwd}"

        if platform_system == MACOS:
            signstring = f"python bundletool.py -i {apkpath} -o {apkpath}_{current_time}_new.{apkout}  --keystore {first_file}  --store_password {Pwd} --key_alias  {aliases}  --key_password  {Pwd}"

        print(GREEN + signstring + RESET)
        # status, message = execute_cmd(signstring)

        scriptsss.append(signstring)

        # # 启动子进程执行脚本
        # process = subprocess.Popen(["python.exe", signstring])
        # # 等待子进程完成
        # process.wait()
        # # 打印脚本执行完成信息
        # print(f"{signstring} 执行完成")

        #  os.system
    else:
        print(
            RED + f" Pwd is not None and aliases is not None..或者存在aab文件" + RESET
        )


# 创建线程池
# with ThreadPoolExecutor(max_workers=len(scriptsss)) as executor:
#     # 提交子进程任务
#     #  status, message = execute_cmd(signstring)
#     subprocess.run(cmd, shell=True, check=True)

# futures = [executor.submit(subprocess.call, ["python.exe", script]) for script in scriptsss]

# 等待所有子进程完成
# for future in futures:
#     future.result()


# 执行命令并等待完成
index = 1
for cmd in scriptsss:
    try:
        print(cmd)
        print("\n" + f"{index}" + "\n")
        index = index + 1
        subprocess.run(cmd, shell=True, check=True)
    except Exception as e:
        print("error ", e)
    continue

# 所有脚本执行完成后继续其他操作
print("所有脚本执行完成")
