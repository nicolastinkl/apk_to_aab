
import os
import glob
import subprocess
import platform
 
import sys
import shutil
import random
import hashlib 


# # 获取目录名和平台参数
directory=""
try:
    directory = sys.argv[1]
except:
    print("用法不对，例如： python3.10 signAll xxxx")
# platform = sys.argv[2]


if  len(directory ) <= 0 :
    sys.exit(0)
# 当前目录

WINDOWS = "Windows"
Linux = "Linux"
MACOS = "Darwin"

def get_base_dir() -> str:
    if hasattr(sys, "_flask"):
        return os.path.dirname(os.path.realpath(__file__))
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return ""



def get_system() -> str:
    return platform.system()


def execute_cmd(cmd):
    # print("#" * 10, cmd)
    status = os.system(cmd)
    return status, ""


platform_system = get_system()

if platform_system == WINDOWS:
    current_dir = f"{os.getcwd()}\{directory}"
else:
    current_dir = f"{os.getcwd()}/{directory}" 

print("目录：",current_dir)


APKTOOL_PATH = os.path.join(get_base_dir(), "tools", "apktool_2.7.0.jar")
AAPT2_PATH = os.path.join(get_base_dir(), "tools", "aapt2", get_system(), "aapt2")
ANDROID_JAR_PATH = os.path.join(get_base_dir(), "tools", "android_33.jar")
BUNDLETOOL_TOOL_PATH = os.path.join(get_base_dir(), "tools", "bundletool-all-1.6.1.jar")


# 当前目录
# current_dir = os.getcwd()

# 获取所有.aab文件
aab_files = glob.glob(os.path.join(current_dir, '*.apk'))
print(aab_files)
# 遍历每个.aab文件
for aab_file in aab_files:
    # 执行命令获取package
    cmdtest = f"{AAPT2_PATH} version"
    #cmd = f"cd {src_dir} && zip -r -q -D {os.path.abspath(zip_name)} *"
  
    
    # cmd = [AAPT2_PATH, 'dump', 'packagename', aab_file]
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # output, err = p.communicate()

    cmd = f"{AAPT2_PATH} dump packagename {aab_file}"
    # status, message = execute_cmd(cmd)
    # print(f"<{message}><{status}>")

    # 使用 subprocess.run 函数执行命令，并捕获执行结果
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # 打印命令的执行信息
    # print("Command: ", result.args)
    # print("Exit Code: ", result.returncode)
    print("Output: ", result.stdout)
    print("Error: ", result.stderr)
 
    # 解析输出获取package
    package = ''
    # output_lines = result.stdout.decode('utf-8').split('\n')
    # print(output_lines,err) 
    line = result.stdout
    # for line in output_lines:
      
    if line.find(".") != -1:
        package = line.strip()
        print("package:",package)
        #     创建目录
        target_dir = os.path.join(current_dir, package)
        print(target_dir)
        target_file = os.path.join(target_dir, os.path.basename(aab_file))
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)                 
            # 移动.aab文件到目标目录            
            print(target_file)
            # os.rename(aab_file, target_file)
            # 
            # 
        shutil.copyfile(aab_file,target_file)
        print("复制完成，查看文件信息")

        result22 = subprocess.run(f"du -sh {target_file}", shell=True, capture_output=True, text=True)
        # 打印命令的执行信息
        # print("Command: ", result.args)
        # print("Exit Code: ", result.returncode)
        print("result22 Output: ", result22.stdout)

       
       
        
