import os
import shutil
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--seconds', default=15,type=int, help="seconds")
parser.add_argument('--start', default=0,type=int, help="start")
parser.add_argument('--frames_dir', default='./Dataset01/frames',type=str)
parser.add_argument('--choose_frames_all_dir', default='./Dataset01/choose_frames_all/',type=str)

arg = parser.parse_args()

frames_dir=arg.frames_dir
choose_frames_all_dir = arg.choose_frames_all_dir

#这里输入视频有多少秒
#seconds = 180
#传参 这里传入视频多少秒
seconds = arg.seconds

# 默认从第二秒开始检测标注
# start = 2
#传参 这里传入视频从那一秒开始，这里需要设置为 0
start = arg.start

# 需要检测标注的时间位置[0,1,2,3,4,5,6,7,8,9,10]
frames = range(start, seconds+1)

# num_frames 存放对应图片的编号
num_frames = []

for i in frames:
    num_frames.append(i*30+1)
#遍历./frames
for filepath,dirnames,filenames in os.walk(frames_dir):
    filenames=sorted(filenames)
    #找到指定的图片，然后移动到choose_frames中对应的文件夹下
    temp_name = filepath.split('/')[-1]
    for filename in filenames:
        if "checkpoint" in filename:
            continue
        if "Store" in filename:
            continue
        temp_num = filename.split('_')[1]
        temp_num = temp_num.split('.')[0]
        temp_num = int(temp_num)
        if '3' in num_frames:
            temp_num = str(temp_num)
            temp_num = temp_num.zfill(6)
            temp_num = temp_name + "_" + temp_num + ".jpg"
            
            srcfile = filepath + '/' + temp_num
            dstpath = choose_frames_all_dir + temp_num
            # 复制文件
            shutil.copy(srcfile, dstpath)
