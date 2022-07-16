# cd /home/AVA-6-seconds/Dataset/
# python copy_label_via.py --label_dir ./choose_frames_middle/
# rm Dataset.zip
# zip -r Dataset.zip ./choose_frames_middle/*
# 将中间一帧（第二帧）的标注信息，复制到第一和第三帧
import os
import argparse
import json

parser = argparse.ArgumentParser()

parser.add_argument('--label_dir', default='./choose_frames_middle/',type=str)

arg = parser.parse_args()

for root, dirs, files in os.walk(arg.label_dir, topdown=False):
    for name in files:
        if '_finish.json' in name:
            print(name)
            f = open(os.path.join(root, name), 'r')
            content = f.read()
            label_json = json.loads(content)
            new_label_json = label_json.copy()
            for imageInfo in label_json['metadata']:
                frame_ID = imageInfo.split('_')[0]
                label_ID = imageInfo.split('_')[1]
                if frame_ID == 'image2':
                    continue
                cp_label_image = 'image2_'+label_ID
                cp_label_av = label_json['metadata'][cp_label_image]['av']
                new_label_json['metadata'][imageInfo]['av'] = cp_label_av
            new_name = name.split('.')[0] + '_s' + '.json'
            f2 = open(os.path.join(root, new_name), 'w')
            new_label_str = json.dumps(new_label_json)
            f2.write(new_label_str)
            f2.close()
            f.close()
            
