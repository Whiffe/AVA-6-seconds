# cd /home/AVA-6-seconds/Dataset/
# python train_json_extract.py --choose_frames_middle_dir ./choose_frames_middle --train_dir ./annotations/train.csv

# 生成train.csv
import json
import os
import csv
import cv2
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--choose_frames_middle_dir', default='./choose_frames_middle',type=str)
parser.add_argument('--train_dir', default='./annotations/train.csv',type=str)

arg = parser.parse_args()

choose_frames_middle_dir = arg.choose_frames_middle_dir

# dict存放最后的json
dicts = []
# 通过循环与判断来找出via的json标注文件
for root, dirs, files in os.walk(choose_frames_middle_dir, topdown=False):
    for file in files:
        #via的json标注文件以_proposal.json结尾
        if "_finish_s.json" in file:
            jsonPath = root+'/'+file
            index = 0
            #读取标注文件
            with open(jsonPath, encoding='utf-8') as f:
                line = f.readline()
                viaJson = json.loads(line)
                
                files = {}
                for file in viaJson['file']:
                    fid = viaJson['file'][file]['fid']
                    fname = viaJson['file'][file]['fname']
                    files[fid]=fname
                for metadata in viaJson['metadata']:
                    imagen_x = viaJson['metadata'][metadata]
                    personID = metadata.split('_')[-1]
                    #获取人的坐标
                    xy = imagen_x['xy'][1:]
                    #获取vid，目的是让坐标信息与图片名称、视频名称对应
                    vid = imagen_x['vid']
                    fname = files[vid]
                    #获取视频名称
                    videoName = fname.split('_')[0]
                    #获取视频帧ID
                    frameId = int((int(fname.split('_')[1].split('.')[0])-1)/30)
                    
                    # 获取坐标对应的图片，因为最后的坐标值需要在0到1
                    # 就需要用现有坐标值/图片大小
                    imgPath = root + '/' + videoName + "_" + str(frameId*30+1).zfill(6) + '.jpg'
                    imgTemp = cv2.imread(imgPath)  #读取图片信息
                    print(imgPath)
                    sp = imgTemp.shape #[高|宽|像素值由三种原色构成]
                    img_H = sp[0]
                    img_W = sp[1]
                    
                    for action in imagen_x['av'][0]:
                        avs = imagen_x['av'][0][action]
                        #行为复选框不为空,获取复选框中的行为
                        if avs != '':
                            #一个复选框可能有多个选择
                            avArr = avs.split(',')
                            for av in avArr:
                                x1 = xy[0] / img_W
                                y1 = xy[1] / img_H
                                x2 = (xy[0]+xy[2]) / img_W
                                y2 = (xy[1]+xy[3]) / img_H
                                
                                # 防止坐标点超过图片大小
                                if x1 < 0:
                                    x1 = 0
                                if x1 > 1:
                                    x1 = 1
                                    
                                if x2 < 0:
                                    x2 = 0
                                if x2 > 1:
                                    x2 = 1
                                    
                                if y1 < 0:
                                    y1 = 0
                                if y1 > 1:
                                    y1 = 1
                                    
                                if y2 < 0:
                                    y2 = 0
                                if y2 > 1:
                                    y2 = 1
                                
                                actionId = int(av)+1
                                dict = [videoName,frameId,x1,y1,x2,y2,actionId,personID]
                                
                                
                                dicts.append(dict)
                    index = index + 1
print(arg.train_dir)
with open(arg.train_dir,"w") as csvfile: 
    writer = csv.writer(csvfile)
    writer.writerows(dicts)
