from glob import glob
import numpy as np
import math
import cv2
import os


def psnr(img1, img2):
    img1 = np.float64(img1)
    img2 = np.float64(img2)
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))


root_path = '/disk1/yazhou/projects/IISP/data/sony/'
out_path = '/disk1/zhouji/'
crf = 35

with open(out_path + 'lossy_%d_psnr.txt'%crf, 'w') as f:
    f.write('')
all_folders = sorted(glob(root_path + 'lossless_image/*'))[:151]
final_psnr = 0

for idx, folder in enumerate(all_folders):
    all_images = sorted(glob(folder + '/*.png'))
    video_psnr = 0
    n = 0
    for path in all_images:
        t1 = cv2.imread(path)
        t2 = cv2.imread(path.replace('lossless_image', 'lossy_%d_image'%crf))
        curr_psnr = psnr(t1, t2)
        n = n + 1
        video_psnr = video_psnr + (curr_psnr - video_psnr) / n

        print(path.split('/')[-2] + '/' + path.split('/')[-1] +
              ' curr: %f' % curr_psnr + ' video: %f' % video_psnr)
    
    final_psnr = final_psnr + (video_psnr - final_psnr) / (idx + 1)
    print(folder.split('/')[-1] + ': %f ' % video_psnr + 'final: %f\n'%final_psnr)
    with open(out_path + 'lossy_%d_psnr.txt'%crf, 'a') as f:
        f.write(folder.split('/')[-1] + ': %f\n' % video_psnr)

with open(out_path + 'lossy_%d_psnr.txt'%crf, 'a') as f:
    f.write('\nfinal_psnr: %f\n' % final_psnr)
