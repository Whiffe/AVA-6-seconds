from via3_tool import Via3Json
import pickle
import csv
from collections import defaultdict
import os
import cv2
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--dense_proposals_dir', default='./Dataset01/annotations/dense_proposals_train.pkl',type=str, help="dense_proposals_dir")
parser.add_argument('--json_path', default='./Dataset01/choose_frames_middle/',type=str)

arg = parser.parse_args()

avaMin_dense_proposals_path = arg.dense_proposals_dir

json_path = arg.json_path


f = open(avaMin_dense_proposals_path,'rb')
info = pickle.load(f, encoding='iso-8859-1') 

attributes_dict = {'1':dict(aname='眼睛状态', type=2, options={'0':'不可见', '1':'其他', '2':'睁眼', '3':'闭眼'},default_option_id="", anchor_id = 'FILE1_Z0_XY1'),

                   '2': dict(aname='口唇状态', type=2, options={'4':'不可见', '5':'其他', '6':'张口', '7':'闭口'}, default_option_id="", anchor_id='FILE1_Z0_XY1'),
                   
                   '3':dict(aname='整体状态', type=2, options={'8':'不可见', '9':'其他', '10':'正坐', '11':'侧坐', '12':'站立', '13':'趴卧', '14':'俯身', '15':'下蹲', '16':'依靠', '17':'平躺', '18':'侧躺'},default_option_id="", anchor_id = 'FILE1_Z0_XY1'),
                   
                   '4': dict(aname='左手掌状态', type=2, options={'19':'不可见', '20':'其他', '21':'手掌抓握', '22':'手掌展开', '23':'手掌指点', '24':'鼓掌', '25':'书写'}, default_option_id="", anchor_id='FILE1_Z0_XY1'),
                   
                   '5': dict(aname='左手臂状态', type=2, options={'26':'不可见', '27':'其他', '28':'手臂放平', '29':'手臂下垂', '30':'手臂前伸', '31':'手臂弯曲', '32':'手臂举起'}, default_option_id="", anchor_id='FILE1_Z0_XY1'),
                   
                   '6': dict(aname='左手行为对象', type=2, options={'33':'不可见', '34':'其他', '35':'书本', '36':'练习本', '37':'饶头', '38':'电子设备', '39':'指他人', '40':'粉笔', '41':'无交互'}, default_option_id="", anchor_id='FILE1_Z0_XY1'),
                   
                   '7': dict(aname='右手掌状态', type=2, options={'42':'不可见', '43':'其他', '44':'手掌抓握', '45':'手掌展开', '46':'手掌指点', '47':'鼓掌', '48':'书写'}, default_option_id="", anchor_id='FILE1_Z0_XY1'),
                   
                   '8': dict(aname='右手臂状态', type=2, options={'49':'不可见', '50':'其他', '51':'手臂放平', '52':'手臂下垂', '53':'手臂前伸', '54':'手臂弯曲', '55':'手臂举起'}, default_option_id="", anchor_id='FILE1_Z0_XY1'),
                   
                   '9': dict(aname='右手行为对象', type=2, options={'56':'不可见', '57':'其他', '58':'书本', '59':'练习本', '60':'饶头', '61':'电子设备', '62':'指他人', '63':'粉笔', '64':'无交互'}, default_option_id="", anchor_id='FILE1_Z0_XY1'),
                   
                   '10': dict(aname='腿部姿态', type=2, options={'65':'不可见', '66':'其他', '67':'站', '68':'跑', '69':'走', '70':'跳', '71':'踢'}, default_option_id="", anchor_id='FILE1_Z0_XY1'),
                  }

#len_x与循环的作用主要是获取每个视频下视频帧的数量
dirname = ''
len_x = {}
for i in info:
    temp_dirname = i.split(',')[0]
    if dirname == temp_dirname:
        #正在循环一个视频文件里的东西
        len_x[dirname] = len_x[dirname] + 1
    else:
        #进入下一个视频文件
        dirname = temp_dirname
        len_x[dirname] = 1

dirname = ''
for i in info:
    temp_dirname = i.split(',')[0]
    if dirname == temp_dirname:
        #正在循环一个视频文件里的东西
    
        #图片ID从1开始计算
        image_id = image_id + 1
        files_img_num = int(i.split(',')[1])
        
        # 如果当前出现 files_img_num - 1 与 image_id 不相等的情况
        # 那就代表当前 image_id对应的图片中没有人
        # 那么via的标注记为空
        if files_img_num - 1 != image_id:
            files_dict[str(image_id)] = dict(fname=i.split(',')[0] + '_' + (str((image_id+1)*30+1)).zfill(6) + '.jpg', type=2)
            via3.dumpFiles(files_dict)
            if files_img_num - 1 != image_id:
                while image_id < files_img_num - 1:   
                    image_id = image_id + 1
                    files_dict[str(image_id)] = dict(fname=i.split(',')[0] + '_' + (str((image_id+1)*30+1)).zfill(6) + '.jpg', type=2)
                    via3.dumpFiles(files_dict)
                    print("middle loss",image_id,"   ",num_images)
                    print("files_img_num-1",files_img_num-1," image_id",image_id)
                    len_x[dirname] = len_x[dirname] + 1
                    continue

        files_dict[str(image_id)] = dict(fname=i.split(',')[0] + '_' + (str(int(i.split(',')[1])*30+1)).zfill(6) + '.jpg', type=2)
        
        for vid,result in enumerate(info[i],1):
            xyxy = result
            xyxy[0] = img_W*xyxy[0]
            xyxy[2] = img_W*xyxy[2]
            xyxy[1] = img_H*xyxy[1]
            xyxy[3] = img_H*xyxy[3]
            temp_w = xyxy[2] - xyxy[0]
            temp_h = xyxy[3] - xyxy[1]
            
            metadata_dict = dict(vid=str(image_id),
                                 xy=[2, float(xyxy[0]), float(xyxy[1]), float(temp_w), float(temp_h)],
                                 av={'1': '0'})
            
            metadatas_dict['image{}_{}'.format(image_id,vid)] = metadata_dict
        
        via3.dumpFiles(files_dict)
        via3.dumpMetedatas(metadatas_dict)
        
        print("OK ",image_id,"   ",num_images)
        if image_id == num_images:
            views_dict = {}
            for i, vid in enumerate(vid_list,1):
                views_dict[vid] = defaultdict(list)
                views_dict[vid]['fid_list'].append(str(i))
            via3.dumpViews(views_dict)
            via3.dempJsonSave()
            print("save")
        
        #当一个视频的图片的标注信息遍历完后：image_id == len_x[dirname]，
        #但是视频的标注信息长度仍然小于视频实际图片长度
        #即视频图片最后几张都是没有人，导致视频标注信息最后几张没有
        #那么就执行下面的语句，给最后几张图片添加空的标注信息
        print("image_id",image_id," len_x[dirname]",len_x[dirname]," num_images",num_images)
        if image_id == len_x[dirname] and image_id < num_images:
            while image_id < num_images:
                image_id = image_id + 1
                files_dict[str(image_id)] = dict(fname=i.split(',')[0] + '_' + (str((image_id+1)*30+1)).zfill(6) + '.jpg', type=2)
                via3.dumpFiles(files_dict)
            print("end loss",image_id,"   ",num_images)
            views_dict = {}
            for i, vid in enumerate(vid_list,1):
                views_dict[vid] = defaultdict(list)
                views_dict[vid]['fid_list'].append(str(i))
            via3.dumpViews(views_dict)
            via3.dempJsonSave()
            print("save")
    else:
        #进入下一个视频文件
        dirname = temp_dirname
        print("dirname",dirname)
        
        #为每一个视频文件创建一个via的json文件
        temp_json_path = json_path + dirname + '/' + dirname + '_proposal.json'
        
        # 获取视频有多少个帧
        for root, dirs, files in os.walk(json_path + dirname, topdown=False):
            if "ipynb_checkpoints" in root:
                continue
            num_images = 0
            for file in files:
                if '.jpg' in file:
                    num_images = num_images + 1
                    temp_img_path = json_path + dirname +'/' + file #图片路径
                    img = cv2.imread(temp_img_path)  #读取图片信息
                    sp = img.shape #[高|宽|像素值由三种原色构成]
                    img_H = sp[0]
                    img_W = sp[1]
        via3 = Via3Json(temp_json_path, mode='dump')
        vid_list = list(map(str,range(1, num_images+1)))
        via3.dumpPrejects(vid_list)
        via3.dumpConfigs()
        via3.dumpAttributes(attributes_dict)
        
        
        files_dict,  metadatas_dict = {},{}
        #图片ID从1开始计算
        image_id = 1
        files_dict[str(image_id)] = dict(fname=i.split(',')[0] + '_' + (str(int(i.split(',')[1])*30+1)).zfill(6) + '.jpg', type=2)
        
        for vid,result in enumerate(info[i],1):
            xyxy = result
            xyxy[0] = img_W*xyxy[0]
            xyxy[2] = img_W*xyxy[2]
            xyxy[1] = img_H*xyxy[1]
            xyxy[3] = img_H*xyxy[3]
            temp_w = xyxy[2] - xyxy[0]
            temp_h = xyxy[3] - xyxy[1]
            
            metadata_dict = dict(vid=str(image_id),
                                 xy=[2, float(xyxy[0]), float(xyxy[1]), float(temp_w), float(temp_h)],
                                 av={'1': '0'})
            #print(metadata_dict)
            metadatas_dict['image{}_{}'.format(image_id,vid)] = metadata_dict
        
        via3.dumpFiles(files_dict)
        via3.dumpMetedatas(metadatas_dict)
