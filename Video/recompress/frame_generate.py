import cv2
import glob, os
import imageio
import numpy as np

parent_path = sorted(glob.glob('/disk1/zhouji/recompress/lossless/'+ '*.avi')) 
# parent_path = ['/disk1/zhouji/recompress/lossy_23/00052.mp4']
target_path = '/disk1/zhouji/recompress/lossless_image/' 

os.makedirs(target_path, exist_ok=True) 

for child_path in parent_path: 
    video_name = os.path.basename(child_path).split('.')[0]
    print(video_name)
    if not os.path.exists(target_path + video_name):
        os.makedirs(target_path + video_name) 
    cap = cv2.VideoCapture(child_path)
    index = 0
    while True:
        success, frame = cap.read()
        if not success:
            break
        cv2.imwrite(target_path + video_name + '/%05d.png' % index, np.uint8(frame))
        print('%05d.png'%index)
        index += 1 
    
