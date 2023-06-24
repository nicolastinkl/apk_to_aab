
import os
import glob
import subprocess
 
import sys
import shutil
import random
import hashlib 

# 当前目录
current_dir = os.getcwd()

# 获取所有.aab文件
aab_files = glob.glob(os.path.join(current_dir, '*.apk'))

# 遍历每个.aab文件
for aab_file in aab_files:
    # 执行命令获取package
    cmd = ['aapt2', 'dump', 'packagename', aab_file]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate()

    # 解析输出获取package
    package = ''
    output_lines = output.decode('utf-8').split('\n')
    
    for line in output_lines:
      
        if line.find(".") != -1:
            package = line.strip()
            print("package:",package)
            #     创建目录
            target_dir = os.path.join(current_dir, package)
            target_file = os.path.join(target_dir, os.path.basename(aab_file))
            if not os.path.exists(target_dir):
                os.makedirs(package)                 
                # 移动.aab文件到目标目录
                
                print(target_file)
                # os.rename(aab_file, target_file)
                # 
                # 
            shutil.copyfile(aab_file,target_file)
            

       
       
        
