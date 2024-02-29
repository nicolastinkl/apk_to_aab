
import os
import glob
import subprocess
 
import sys
import shutil
import random
import hashlib 

 

import xml.etree.ElementTree as ET

# from files_pb2 import Assets
# from google.protobuf import json_format

if hasattr(sys, "_flask"):
    from .utils import *
else:
    try:
        from utils import *
    except:
        from .utils import *


def print_log(message):
    print(message)


def get_base_dir() -> str:
    # return "D:/build_aab_tool"
    if hasattr(sys, "_flask"):
        return os.path.dirname(os.path.realpath(__file__))
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return ""

 
# # 获取目录名和平台参数
directory = sys.argv[1]
 
if not os.path.exists(directory) or os.path.isfile(directory):
    print(f"输入的apk父目录不存在:{directory}")
    sys.exit(0)

dbtype_list = os.listdir(directory)  

# 获取所有.apk文件
aab_files = glob.glob(os.path.join(directory, '*.apk'))
APKTOOL_PATH = os.path.join(get_base_dir(), "tools", "apktool_2.7.0.jar") #我的版本
AAPT2_PATH =  os.path.join(get_base_dir(), "tools", "aapt2", get_system(), "aapt2")
print(AAPT2_PATH)

if len(aab_files) <=0 :
    print(f"输入的apk父目录下不存在apk文件")
    sys.exit(0)
# 遍历每个.aab文件
for aab_file in aab_files:
    # 执行命令获取package
    cmd = [AAPT2_PATH, 'dump', 'packagename', aab_file]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate()

    if err is not None:
        print(err)
        sys.exit(0)
    
    # 解析输出获取package
    package = ''
    output_lines = output.decode('utf-8').split('\n')
    
    for line in output_lines:
      
        if line.find(".") != -1:
            package = line.strip()
            print("package:",package)
            #     创建目录
            target_dir = os.path.join(directory, package)
            target_file = os.path.join(target_dir, os.path.basename(aab_file))
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)       
                print(target_file) 
            shutil.copyfile(aab_file,target_file)
            
            print("生成所有APk对应的目录成功.")

       
       
        