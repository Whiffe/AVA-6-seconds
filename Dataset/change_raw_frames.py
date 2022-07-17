# cd /home/AVA-6-seconds/Dataset/
# python change_raw_frames.py --rawframes_dir ./rawframes
import os
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--rawframes_dir', default='./rawframes',type=str)

arg = parser.parse_args()

rawframes_dir = arg.rawframes_dir

for root, dirs, files in os.walk(rawframes_dir, topdown=False):
    for name in files:
        if 'checkpoint' in name:
            continue
        if "Store" in name:
            continue
        oldNamePath = os.path.join(root, name)
        
        tempName1 = name.split('_')[1] # 44_000054.jpg -> 000054.jpg
        tempName2 = tempName1.split('.')[0] # 000054.jpg -> 000054
        tempName3 = str(int(tempName2)).zfill(5) # 000054 -> 00054
        newName = 'img_' + tempName3 + '.jpg'
        newNamePath = os.path.join(root, newName)
        
        os.rename(oldNamePath,newNamePath)
