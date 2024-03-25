# coding=utf-8

import datetime
import json
import re
import yaml
import argparse
import time
import sys
import subprocess


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
    if global_print_fun:
        global_print_fun(message)
    else:
        print(message)
    pass


def get_base_dir() -> str:
    # return "D:/build_aab_tool"
    if hasattr(sys, "_flask"):
        return os.path.dirname(os.path.realpath(__file__))
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return ""


# APKTOOL_PATH = os.path.join(get_base_dir(), "tools", "apktool_2.5.0.jar")
# APKTOOL_PATH = os.path.join(get_base_dir(), "tools", "apktool-aapt2-2.5.0.jar")
APKTOOL_PATH = os.path.join(get_base_dir(), "tools", "apktool_2.7.0.jar")  # 我的版本
AAPT2_PATH = os.path.join(get_base_dir(), "tools", "aapt2", get_system(), "aapt2")
print(AAPT2_PATH)
# sys.exit(0)
ANDROID_JAR_PATH = os.path.join(get_base_dir(), "tools", "android_33.jar")
BUNDLETOOL_TOOL_PATH = os.path.join(
    get_base_dir(), "tools", "bundletool-all-1.15.1.jar"
)  # bundletool-all-1.6.1.jar


# # 获取目录名和平台参数
apksPath = sys.argv[1]
signstring = (
    f"{BUNDLETOOL_TOOL_PATH} --bundle='{apksPath}' --output='{apksPath}-output'"
)
print(signstring)

cmd = [
    BUNDLETOOL_TOOL_PATH,
    "extract-apks",
    "--bundle=",
    apksPath,
    "--output=",
    apksPath + "_path",
]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
output, err = p.communicate()

if err is not None:
    print("Error输出：", err)
    sys.exit(0)

# 解析输出获取package
package = ""
output_lines = output.decode("utf-8").split("\n")
print("最终输出：", output_lines)
