import random 
from glob import glob 


root_path = '/disk1/yazhou/projects/IISP/data/'
camera_name = 'sony'
video_type = 'mp4'
out_path = '/disk1/zhouji/split_video/'


data_path = root_path + camera_name 

folders = sorted(glob(data_path + '/lossy_23/*'))[:151]
folder_names = [f.split('/')[-1] for f in folders] 

random.shuffle(folder_names)

train_names = folder_names[:113]
val_names = folder_names[113:128]
test_names = folder_names[128:]

# Copy to avi files

with open(out_path + camera_name + '_train.txt', 'w') as f:
    for i in range(len(train_names)):
        f.write(train_names[i].replace('.mp4', ''))
        f.write('\n')

with open(out_path + camera_name + '_val.txt', 'w') as f:
    for i in range(len(val_names)):
        f.write(val_names[i].replace('.mp4', ''))
        f.write('\n')


with open(out_path + camera_name + '_test.txt', 'w') as f:
    for i in range(len(test_names)):
        f.write(test_names[i].replace('.mp4', ''))
        f.write('\n')

