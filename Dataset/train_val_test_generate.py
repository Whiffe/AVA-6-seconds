# cd /home/AVA-6-seconds/Dataset
# python train_val_test_generate.py --DatasetXX_dir ./ --annotations_dir ../annotations/
# 将现有的标签dense_proposals_train.pkl、train_all.csv分成train、val、test
import os
import shutil
import sys
import argparse
import pickle
import numpy as np
import csv
import random

parser = argparse.ArgumentParser()

parser.add_argument('--DatasetXX_dir', default='./',type=str)
parser.add_argument('--annotations_dir', default='../annotations/',type=str)

arg = parser.parse_args()

DatasetXX_dir=arg.DatasetXX_dir
annotations_dir=arg.annotations_dir

train_proposals = []
test_proposals = []
val_proposals = []


# 遍历./DatasetXX_dir中的video_crop
# 将现有的标签分成train、val、test
for filepath,dirnames,filenames in os.walk(DatasetXX_dir):
    if 'video_crop' in filepath:
        for filename in filenames:
            if 'mp4' in filename:
                rad = random.randint(1,10)
                if rad  <= 6:
                    train_proposals.append(filename.split('.')[0])
                elif rad <= 8:
                    test_proposals.append(filename.split('.')[0])
                else:
                    val_proposals.append(filename.split('.')[0])

train_results_dict = {}
test_results_dict = {}
val_results_dict = {}

#遍历./DatasetXX_dir
for filepath,dirnames,filenames in os.walk(DatasetXX_dir):
    if 'annotations' in filepath:
        for filename in filenames:
            if 'dense_proposals_train' in filename:
                path = os.path.join(filepath,filename)

                f = open(path,'rb')
                info = pickle.load(f, encoding='iso-8859-1')
                for i in info:
                    tempArr = np.array(info[i])
                    video_crop_name = i.split(',')[0]
                    if video_crop_name in train_proposals:
                        dicts = []
                        for temp in tempArr:
                            temp = temp.astype(np.float64)
                            dicts.append(temp)
                        train_results_dict[i] = np.array(dicts)
                    elif video_crop_name in test_proposals:
                        dicts = []
                        for temp in tempArr:
                            temp = temp.astype(np.float64)
                            dicts.append(temp)
                        test_results_dict[i] = np.array(dicts)
                    elif video_crop_name in val_proposals:
                        dicts = []
                        for temp in tempArr:
                            temp = temp.astype(np.float64)
                            dicts.append(temp)
                        val_results_dict[i] = np.array(dicts)
                    else:
                        print("!!!ERROR!!!!")

dense_proposals_train = annotations_dir + 'dense_proposals_train.pkl'
dense_proposals_test = annotations_dir + 'dense_proposals_test.pkl'
dense_proposals_val = annotations_dir + 'dense_proposals_val.pkl'
# 保存为pkl文件
with open(dense_proposals_train,"wb") as pklfile: 
    print(dense_proposals_train)
    pickle.dump(train_results_dict, pklfile)
with open(dense_proposals_test,"wb") as pklfile: 
    print(dense_proposals_test)
    pickle.dump(test_results_dict, pklfile)
with open(dense_proposals_val,"wb") as pklfile: 
    print(dense_proposals_val)
    pickle.dump(val_results_dict, pklfile)
                    
#遍历./DatasetXX_dir
train_temp = []
test_temp = []
val_temp = []
for filepath,dirnames,filenames in os.walk(DatasetXX_dir):
    if 'annotations' in filepath:
        for filename in filenames:
            if 'train_all.csv' in filename:
                path = os.path.join(filepath,filename)
                with open(path) as csvfile:
                    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
                    for row in csv_reader: 
                        video_crop_name = row[0]

                        if video_crop_name in train_proposals:
                            train_temp.append(row)
                        elif video_crop_name in test_proposals:
                            test_temp.append(row)
                        elif video_crop_name in val_proposals:
                            val_temp.append(row)
                        else:
                            print("!!!ERROR!!!!")


trainDir = annotations_dir + 'train.csv'
testDir = annotations_dir + 'test.csv'
valDir = annotations_dir + 'val.csv'

with open(trainDir,"w") as csvfile: 
    print(trainDir)
    writer = csv.writer(csvfile)
    writer.writerows(train_temp)
with open(testDir,"w") as csvfile: 
    print(testDir)
    writer = csv.writer(csvfile)
    writer.writerows(test_temp)
with open(valDir,"w") as csvfile: 
    print(valDir)
    writer = csv.writer(csvfile)
    writer.writerows(val_temp)
