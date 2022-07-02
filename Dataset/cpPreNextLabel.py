import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--label_dir', default='./detect/exp/labels',type=str)
parser.add_argument('--new_label_dir', default='./detect/exp/newLabels',type=str,)

arg = parser.parse_args()

try:
    # 创建新的文件夹，存放新的label
    os.mkdir(arg.new_label_dir);
except:
    print('File exists:',arg.new_label_dir )

try:
    os.system('rm -r ' + arg.new_label_dir + '/*')
except:
    print(arg.new_label_dir + " is empty")

for root, dirs, files in os.walk(arg.label_dir, topdown=False):

    for name in files:
        video_crop_name = name.split("_")[0]
        frame_num = name.split("_")[1].split('.')[0]
        
        pre_txt_name = video_crop_name + '_' + (str(int(frame_num)-30)).zfill(6) + '.txt'
        next_txt_name = video_crop_name + '_' + (str(int(frame_num)+30)).zfill(6) + '.txt'
                   
        os.system('cp ' + os.path.join(root, name) + ' ' + os.path.join(arg.new_label_dir, name))
        os.system('cp ' + os.path.join(root, name) + ' ' + os.path.join(arg.new_label_dir, pre_txt_name))
        os.system('cp ' + os.path.join(root, name) + ' ' + os.path.join(arg.new_label_dir, next_txt_name))
        
        
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--label_dir', default='./detect/exp/labels',type=str)
parser.add_argument('--new_label_dir', default='./detect/exp/newLabels',type=str,)

arg = parser.parse_args()

try:
    # 创建新的文件夹，存放新的label
    os.mkdir(arg.new_label_dir);
except:
    print('File exists:',arg.new_label_dir )

try:
    os.system('rm -r ' + arg.new_label_dir + '/*')
except:
    print(arg.new_label_dir + " is empty")

for root, dirs, files in os.walk(arg.label_dir, topdown=False):

    for name in files:
        video_crop_name = name.split("_")[0]
        frame_num = name.split("_")[1].split('.')[0]
        
        pre_txt_name = video_crop_name + '_' + (str(int(frame_num)-30)).zfill(6) + '.txt'
        next_txt_name = video_crop_name + '_' + (str(int(frame_num)+30)).zfill(6) + '.txt'
                   
        os.system('cp ' + os.path.join(root, name) + ' ' + os.path.join(arg.new_label_dir, name))
        os.system('cp ' + os.path.join(root, name) + ' ' + os.path.join(arg.new_label_dir, pre_txt_name))
        os.system('cp ' + os.path.join(root, name) + ' ' + os.path.join(arg.new_label_dir, next_txt_name))
