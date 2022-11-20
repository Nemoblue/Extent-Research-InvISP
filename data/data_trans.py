import shutil

file = open('/disk1/yazhou/projects/fivek_dataset/raw_photos/Canon EOS 5D.txt', 'r')
lines = file.readlines()
target = '/disk1/zhouji/Invertible-ISP/data/Canon EOS 5D/DNG/'
count = 0

for original in lines:
	file_name = original.split('/')[-1].split('.')[0]
	shutil.copyfile(original.split()[0], target + file_name + '.dng')
	count += 1
	print('count: ' + str(count))
