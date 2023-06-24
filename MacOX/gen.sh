#!/bin/bash


input_path=$1
# echo "请输入文件路径："
# read input_path
echo "请输入文件路径：${input_path}" 
du -sh $input_path

current_date=$(date +"%Y-%m-%d_%H:%M:%S")
echo "$current_date"

des_path="${input_path}_signed_$current_date.aab" 
echo "输出路径为：${des_path}" 

# 使用 ## 操作符从最后一个正斜杠开始的部分截取，即文件名
filename=${input_path##*/}

echo "$filename"

# 使用sed命令进行字符串替换
apkpath=$(echo "$input_path" | sed "s/${filename}//g")

echo "apkpath: $apkpath"
ls $apkpath

filename_pattern="*.keystore"

# 使用find命令获取匹配的文件
first_file=$(find "$apkpath" -type f -name "$filename_pattern" -not -path "$apkpath"| head -n 1)
# 打印第一个文件路径
echo "$first_file"



filename_pattern_jks="*.jks"

# 使用find命令获取匹配的文件
first_file_jks=$(find "$apkpath" -type f -name "$filename_pattern_jks" -not -path "$apkpath"| head -n 1)
# 打印第一个文件路径
echo "$first_file_jks"



# 使用条件判断语句
if [ -z "$first_file" ]; then
    echo "${first_file} 不存在...继续搜索.jks文件"
 
else
    echo "${first_file} 存在"
    # python3.10 bundletool.py -i  ${input_path}  -o ${des_path} --keystore ${filename_pattern}  --store_password JackpotMasterSlots1!@#  --key_alias  JackpotMasterSlots --key_password  JackpotMasterSlots1!@#

    echo  ${first_file}
    # python3.10 bundletool.py -i  ${input_path}  -o ${des_path} --keystore ${first_file}  --store_password 12345678 --key_alias  arsalgames  --key_password   12345678
    # python3.10 bundletool.py -i  ${input_path}  -o ${des_path} --keystore ${first_file}  --store_password Slots7775Gbet1!@# --key_alias  Slots7775Gbet  --key_password   Slots7775Gbet1!@#

    # python3.10 bundletool.py -i  ${input_path}  -o ${des_path} --keystore ${first_file}  --store_password 123456789 --key_alias  slotegame  --key_password   123456789
    # python3.10 bundletool.py -i  ${input_path}  -o ${des_path} --keystore ${first_file}  --store_password 12345678 --key_alias  slot  --key_password   12345678
    # python3.10 bundletool.py -i  ${input_path}  -o ${des_path} --keystore ${first_file}  --store_password 12345678 --key_alias  spin  --key_password   12345678
    
    # python3.10 bundletool.py -i  ${input_path}  -o ${des_path} --keystore ${first_file}  --store_password Billionaire777SlotsMachine1!@# --key_alias  Billionaire777SlotsMachine  --key_password   Billionaire777SlotsMachine1!@#
    python3.10 bundletool.py -i  ${input_path}  -o ${des_path} --keystore ${first_file}  --store_password BlackJackPoker1!@# --key_alias  BlackJackPoker  --key_password   BlackJackPoker1!@#

fi
 



# 使用条件判断语句
if [ -z "$first_file_jks" ]; then
    echo "${first_file_jks} 不存在..."
 
else
    echo "${first_file_jks} 存在"
    #  python3.10 bundletool.py -i  ${input_path}  -o ${des_path} --keystore ${filename_pattern}  --store_password JackpotMasterSlots1!@#  --key_alias  JackpotMasterSlots --key_password  JackpotMasterSlots1!@#

    echo  ${first_file_jks}
    #python3.10 bundletool.py -i  ${input_path}  -o ${des_path} --keystore ${first_file_jks}  --store_password 123458 --key_alias  superchallenge  --key_password   123458

fi
 