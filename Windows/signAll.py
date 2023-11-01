
import os
import glob
import subprocess
 
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
    with open(file_path, 'r') as file:
        content = file.read()

    return content

# 定义 ANSI 转义序列
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
# 输出彩色文本

# 当前目录

# # 获取目录名和平台参数
directory = sys.argv[1]
# platform = sys.argv[2]
# 当前目录
current_dir = f"{os.getcwd()}\{directory}"
print(current_dir )
directory = current_dir
dbtype_list = os.listdir(current_dir) 
for dbtype in dbtype_list: 
    if os.path.isfile(os.path.join(current_dir,dbtype)): 
        print("dbtype: ",dbtype)
        # 获取签名文件，验证签名 
        # ///Design/KeyStore/keyStoreDetails.txt
        print("正在检查签名文件")
        dbtype_list.remove(dbtype)
    # else:
        # dbtype_list.remove(dbtype)

print (dbtype_list)


def execute_cmd(cmd):
    # print("#" * 10, cmd)
    status = os.system(cmd)
    return status, ""

# 定义脚本列表
scriptsss = []

for dbtype in dbtype_list: 

    aliases = ""
    Pwd = ""
    organization = ""
    
    keystoreContent = ""
    apkpath = ""
    first_file = ""
    print(f"目錄： {directory}/{dbtype}/")
    for filename in os.listdir(f"{directory}/{dbtype}/"):
        if filename.endswith('.txt'):
            file_path = os.path.join(f"{directory}/{dbtype}/", filename)
            with open(file_path, 'r') as f:
                # 读取文件内容
                content = f.read()
                keystoreContent = content
        if filename.endswith('.keystore'):
            first_file  = os.path.join(f"{directory}/{dbtype}/", filename)

        if filename.endswith('.jks'):
            first_file  = os.path.join(f"{directory}/{dbtype}/", filename)

        if filename.endswith('.apk'):
            apkpath  = os.path.join(f"{directory}/{dbtype}/", filename)

    # keystoreContent = get_file_content(f"{directory}/{dbtype}/keyStoreDetails.txt")
    if keystoreContent.find("-") != -1:

        if keystoreContent:
            print(RED + f"{keystoreContent}"+ RESET) 

            for line in keystoreContent.split("\n"):
                key, value = line.split("-")
                if key.strip() == "Alias":
                    aliases = value.strip()
                if key.strip() == "Password":
                    Pwd = value.strip()
                if key.strip() == "Pwd":
                    Pwd = value.strip()
                if key.strip() == "organization":
                    organization = value.strip()                
                    #aliases[key] = value 
    
    else:
        # 读取txt密码 然后取alias值
        keystore_password  = keystoreContent
        Pwd = keystore_password
        keystore_file = first_file
        # 定义 keytool 命令及参数
        Pwd = keystore_password
        # 构建 keytool 命令
        command = f'keytool -list -v -keystore "{keystore_file}" -storepass "{keystore_password}"'

        # 执行命令并获取输出
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        output_str = output.decode('cp936')
        # print(output_str)
        
        # 解析输出以获取 alias 字符串
        alias_index = output_str.find("Alias:")
        if alias_index != -1:
            alias_end_index = output_str.find("\n", alias_index)
            alias_string = output_str[alias_index:alias_end_index]
            aliasnamestring = alias_string.split(":")[1].strip()
            print(f"Alias: <{aliasnamestring}>")
            if len(aliasnamestring)>0 :
                aliases = aliasnamestring
        else:
            print("Alias not found")

        # 解析输出以获取 alias 字符串
        alias_index = output_str.find("别名:")
        if alias_index != -1:
            alias_end_index = output_str.find("\n", alias_index)
            alias_string = output_str[alias_index:alias_end_index]
            aliasnamestring = alias_string.split(":")[1].strip()
            print(f"别名: <{aliasnamestring}>")
            if len(aliasnamestring)>0 :
                aliases = aliasnamestring
        else:
            print("别名 not found")


        # 检查错误信息
        if process.returncode != 0:
            print(f"Error: {error.decode('cp936')}")


    print(RED + f"{first_file}"+ RESET) 
 

    if Pwd is not None and aliases is not None and len(Pwd)>2:
        print("拆分结果：",aliases,Pwd,organization)

            # exec: python.exe bundletool.py -i  ${input_path}  -o ${des_path} --keystore ${first_file}  --store_password BlackJackPoker1!@# --key_alias  BlackJackPoker  --key_password   BlackJackPoker1!@#
        time_now = datetime.now()
        current_time = time_now.strftime("%H_%M_%S")
        
        signstring = (f"python.exe bundletool.py -i {apkpath} -o {apkpath}_{current_time}.aab  --keystore {first_file}  --store_password {Pwd} --key_alias  {aliases}  --key_password  {Pwd}")
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
        print(RED + f" Pwd is not None and aliases is not None.."+ RESET) 
         




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
        print("\n"+f"{index}"+"\n")
        index = index + 1
        subprocess.run(cmd, shell=True, check=True)
    except Exception as e:
        print("error ",e)
    continue

# 所有脚本执行完成后继续其他操作
print("所有脚本执行完成") 
