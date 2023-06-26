#!/bin/bash


# Define a function that takes two arguments
function say_hello() {
    #  echo "Hello, $1 and $2!"

    # Set the source and destination file paths
    SRC_FILE="$3"
    DEST_FILE1="$1/app_icon.png"
    DEST_FILE2="$1/app_icon_round.png"
    DEST_FILE3="$1/ic_launcher.png"
    # 

    # Set the desired width and height of the destination image
    WIDTH=$2
    HEIGHT=$2

    # Use sips to resize the image and save it to the destination file
    sips -z $HEIGHT $WIDTH $SRC_FILE --out $DEST_FILE1 
    sips -z $HEIGHT $WIDTH $SRC_FILE --out $DEST_FILE2
    sips -z $HEIGHT $WIDTH $SRC_FILE --out $DEST_FILE3
 

}

input_path=$1
# echo "请输入文件路径："
# read input_path
echo "请输入文件路径：${input_path}" 
du -sh $input_path



say_hello "mipmap-hdpi" "72"  "$input_path"
say_hello "mipmap-ldpi" "36"  "$input_path"

say_hello "mipmap-mdpi" "48"  "$input_path"
say_hello "mipmap-xhdpi" "96"  "$input_path"
say_hello "mipmap-xxhdpi" "144" "$input_path"
say_hello "mipmap-xxxhdpi" "192"  "$input_path"
