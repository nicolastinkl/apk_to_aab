import datetime
import json
import re
import yaml
import argparse
import time
import sys
import subprocess
import os  
import zipfile
import shutil
import argparse 


if hasattr(sys, "_flask"):
    from .utils import *
else:
    try:
        from utils import *
    except:
        from .utils import *

import xml.etree.ElementTree as ET

# from files_pb2 import Assets
# from google.protobuf import json_format

def get_base_dir() -> str:
    # return "D:/build_aab_tool"
    if hasattr(sys, "_flask"):
        return os.path.dirname(os.path.realpath(__file__))
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return ""



def get_system() -> str:
    return platform.system()

# APKTOOL_PATH = os.path.join(get_base_dir(), "tools", "apktool_2.5.0.jar")
# APKTOOL_PATH = os.path.join(get_base_dir(), "tools", "apktool-aapt2-2.5.0.jar")
APKTOOL_PATH = os.path.join(get_base_dir(), "tools", "apktool_2.7.0.jar") #我的版本
AAPT2_PATH =  os.path.join(get_base_dir(), "tools", "aapt2", get_system(), "aapt2")
print(AAPT2_PATH)
# sys.exit(0)
ANDROID_JAR_PATH = os.path.join(get_base_dir(), "tools", "android_33.jar")
BUNDLETOOL_TOOL_PATH = os.path.join(get_base_dir(), "tools", "bundletool-all-1.15.1.jar") #bundletool-all-1.6.1.jar


KEYSTORE = os.path.join(get_base_dir(), "tools", "test.jks")
STORE_PASSWORD = "test123"
KEY_ALIAS = "test"
KEY_PASSWORD = "test123"

BUNDLE_MODULE_TEMPLATE_PATH = os.path.join(get_base_dir(), "tools", "pad_template")




bundletool = BUNDLETOOL_TOOL_PATH


class BuildOptions:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="自动打包文件")
        self.parser.add_argument("--path", type=str, required=True, help="aab的路径")
        self.parser.add_argument("--password", type=str, required=True, help="你自己的密码")
        self.parser.add_argument("--jks_path", type=str, required=True, help="你自己jks的地址")
        self.parser.add_argument("--alias", type=str, default="release", help="你自己alias")

    def parse(self):
        return self.parser.parse_args()

 
def query_by_java_jar(jar_path, param):
    execute = "java -jar {} {}".format(jar_path, param)
    print(execute)
    output = subprocess.Popen(execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res = output.stdout.readlines()
    return res
 



if __name__ == '__main__':
    parser = BuildOptions()
    args = parser.parse()
    
    jks_path = args.jks_path
     
    password = args.password

    aab_path = args.path
    # print('aab_path', aab_path)
    dir_name = os.path.dirname(aab_path)

    apks_path = dir_name + os.sep + os.path.basename(aab_path).replace('.aab', '.apks')
    
    query_by_java_jar(bundletool,
                      'build-apks --bundle=' + aab_path + ' --output=' + apks_path + ' --mode=universal --ks=' + jks_path + ' --ks-pass=pass:' + password + ' --ks-key-alias=' + args.alias + ' --key-pass=pass:' + password)
    zip_path = apks_path.replace('.apks', f'{ time.strftime("%m_%d_%H_%M_%S", time.localtime())}.zip')
    os.renames(apks_path, zip_path)
    zFile = zipfile.ZipFile(zip_path, "r")
    zip_apk_path = dir_name + os.sep + 'signed'
    
    if os.path.exists(zip_apk_path):
        shutil.rmtree(zip_apk_path)
    for fileM in zFile.namelist():
        zFile.extract(fileM, zip_apk_path)
    
    rename = zip_apk_path + os.sep + os.path.basename(apks_path).replace(
        '.apks', '.apk')    
    os.renames(zip_apk_path + os.sep + 'universal.apk', rename)
    print("output apk", rename)
    zFile.close()
    os.remove(zip_path)

    # 然后再次签名从apk to aab
    if rename is not None:
        apkpath = rename
        signstring = (f"python.exe bundletool.py -i {apkpath} -o {apkpath}_signed.aab  --keystore {args.jks_path}  --store_password {args.password} --key_alias  {args.alias}  --key_password  {args.password}")
        
        print(signstring)
        try:  
            subprocess.run(signstring, shell=True, check=True)
        except Exception as e:
            print("error ",e)


        #删除旧的aab_path
        os.remove(aab_path)        