import glob, os
import numpy as np
import rawpy.enhance
import imageio
import PIL
import exifread
import colour_demosaicing
from PIL import Image

root_path = '/disk1/zhouji/preprocess/sony_merged/'
out_path = '/disk1/zhouji/RGB/'
raw_path = '/disk1/zhouji/RAW/'
crop_width = 256
crop_height = 256
Bayer_Pattern = "RGGB"

start = 50
end = 100

all_folders = sorted(glob.glob(root_path + '*'))
folders_preprocess = all_folders[start:end]

with open('/disk1/zhouji/focal_length.txt', 'w') as f:
	f.write('')

def get_focal(path):
	raw_file = open(path, 'rb')
	exif_file = exifread.process_file(raw_file, details=False, strict=True)

	if 'EXIF FocalLength' in exif_file:
		focallength_str = exif_file['EXIF FocalLength'].printable
	else:
		focallength_str = exif_file['Image FocalLength'].printable
	if '/' in focallength_str:
		numerator = float(focallength_str.split('/')[0])
		denominator = float(focallength_str.split('/')[-1])
		focallength = numerator / denominator
	else:
		focallength = float(focallength_str)
	return focallength
	

for idx, folder in enumerate(folders_preprocess):
	all_images = sorted(glob.glob(folder + '/*.ARW'))
	if len(all_images) == 0:
		break
	folder_name = folder.split('/')[-1]
	out_dir = out_path + folder_name + '/'
	raw_dir = raw_path + folder_name + '/'
	if not os.path.isdir(out_dir):
    		os.mkdir(out_dir)
	if not os.path.isdir(raw_dir):
		os.mkdir(raw_dir)

	focal = get_focal(all_images[0])
	with open('/disk1/zhouji/focal_length.txt', 'a') as f:
		f.write(folder_name + ' %f\n' % focal)

	for path in all_images:
		print("Start Processing %s" % os.path.basename(path))
		image_name = path.split('/')[-1].split('.')[0]

		if focal < 20:
			aberration_para = 1.0004
		else:
			aberration_para = 1
	
		raw = rawpy.imread(path)
		cwb = raw.camera_whitebalance
		raw_width = raw.sizes.width
		raw_height = raw.sizes.height
		
		raw_img = raw.raw_image_visible
		de_raw = colour_demosaicing.demosaicing_CFA_Bayer_bilinear(raw_img, Bayer_Pattern)
		de_raw_crop = de_raw[crop_height:raw_height-crop_height,
					crop_width:raw_width-crop_width]
		print(de_raw_crop.shape)
		
		rgb = raw.postprocess(
			demosaic_algorithm=rawpy.DemosaicAlgorithm(4),
			dcb_enhance=True,
			use_camera_wb=True,
			no_auto_bright=True,
			median_filter_passes=4,
			chromatic_aberration=(aberration_para,aberration_para)
			)
		raw.close()

		PIL.Image.fromarray(rgb).crop(
			(crop_width, crop_height, 
			raw_width-crop_width, raw_height-crop_height)
			).save(out_dir+ image_name + '.png')
		np.savez(raw_dir + image_name + '.npz', raw=de_raw_crop, wb=cwb)
		print('Save in %s' % (out_dir + image_name + '.png'))
