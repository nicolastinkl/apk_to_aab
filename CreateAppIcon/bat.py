import  os,sys
import  shutil
import  subprocess,sips
from PIL import Image


def  say_hello(foldername,  size ,pngnamepath):     
    # size = int(size)
    src_file  =  pngnamepath     
    current_path = os.path.dirname(__file__)
    dst_file1  =  f"{current_path}/{foldername}/app_icon.png"    
    dst_file2  =  f"{current_path}/{foldername}/app_icon_round.png"     
    dst_file3  =  f"{current_path}/{foldername}/ic_launcher.png"     
    print(dst_file3,"  ",pngnamepath)
    image = Image.open(pngnamepath)
    new_image = image.resize((size, size))
    new_image.save(dst_file1)
    

    new_image2 = image.resize((size, size))
    new_image2.save(dst_file2)
 
    new_image3 = image.resize((size, size))
    new_image3.save(dst_file3)
    # subprocess.run(["sips",  "-z",  str(size),  str(size),  src_file,  "--out",  dst_file1])     
    # subprocess.run(["sips",  "-z",  str(size),  str(size),  src_file,  "--out",  dst_file2])     
    # subprocess.run(["sips",  "-z",  str(size),  str(size),  src_file,  "--out",  dst_file3])
if  __name__  ==  "__main__":     
    # input_path  =  input("请输入文件路径：")    
        
    current_path = os.path.dirname(__file__)
    print("脚本运行目录：",current_path)

    pngnamepath = sys.argv[1]
            
    say_hello("mipmap-hdpi", 72 , pngnamepath)
    say_hello ("mipmap-ldpi" ,36,  pngnamepath)
    say_hello ("mipmap-mdpi", 48 , pngnamepath)
    say_hello ("mipmap-xhdpi", 96 , pngnamepath)
    say_hello ("mipmap-xxhdpi", 144, pngnamepath)
    say_hello( "mipmap-xxxhdpi" ,192 , pngnamepath)
