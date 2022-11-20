import numpy as np
import cv2

scale = 8

path = "/disk1/zhouji/NIKON/jpeg/NIKON_jpeg_30/"
#path = "/disk1/zhouji/CANON_DARK/"

#path = "/disk1/zhouji/NIKON/loss/NIKON_loss_ssim/"
#path = "/disk1/zhouji/CANON/loss/CANON_loss_ssim/"

jpeg_img = "a0088-_DGW6376_00004.jpg"
#jpeg_img = "a4230-Duggan_090426_7798_00006.jpg"

#jpeg_img = "a1100-_DGW6248_00003.jpg"
#jpeg_img = "a3307-jmac_MG_1001_00001.jpg"

pred_img = cv2.imread(path + "pred_" + jpeg_img, cv2.IMREAD_GRAYSCALE)
gt_img = cv2.imread(path + "tar_"  + jpeg_img, cv2.IMREAD_GRAYSCALE)

raw_pred_img = cv2.imread(path + "raw_pred_" + jpeg_img, cv2.IMREAD_GRAYSCALE)
raw_gt_img = cv2.imread(path + "raw_tar_" + jpeg_img, cv2.IMREAD_GRAYSCALE)

#print("pred: ", pred_img.max(),pred_img.min())
#print("gt: ", gt_img.max(), gt_img.min())

def error_map(pred_img, gt_img):
    pred_img = np.abs(pred_img)
    if pred_img.ndim == 3:
        base = np.max(np.mean((np.abs(pred_img * 1.0 - gt_img * 1.0) + 1.0), axis = -1))
        print(base)
        diff = 255.0 - np.mean((np.abs(pred_img * 1.0 - gt_img * 1.0) + 1.0) * 255.0 / base, axis = -1)
        #diff = np.mean(np.abs(pred_img*255.0 - gt_img*255.0) + 255.0, axis = -1) * scale
        #diff = np.mean(np.abs(((pred_img-gt_img)+1)*127.5), axis = -1)
    else:
        pred_img = np.expand_dims(pred_img, axis = -1)
        gt_img = np.expand_dims(gt_img, axis = -1)
        base = np.max(np.mean((np.abs(pred_img * 1.0 - gt_img * 1.0) + 1.0), axis = -1))
        print(base)
        diff = 255.0 - np.mean((np.abs(pred_img * 1.0 - gt_img * 1.0) + 1.0) * 255.0 / base, axis = -1)
        #diff = np.mean(np.abs(pred_img*255.0 - gt_img*255.0) + 255.0, axis = -1) * scale
        #diff = np.mean(np.abs(((pred_img-gt_img)+1)*127.5), axis = -1)
    diff = np.uint8(diff)
    print(diff)
    diff_color = cv2.applyColorMap(diff, cv2.COLORMAP_JET)
    return diff_color

origin_result = error_map(pred_img, gt_img)
raw_result = error_map(raw_pred_img, raw_gt_img)
cv2.imwrite(path + "origin_errormap.jpg", cv2.cvtColor(origin_result, cv2.COLOR_BGR2RGB))
cv2.imwrite(path + "raw_errormap.jpg", cv2.cvtColor(raw_result, cv2.COLOR_BGR2RGB))
