import skvideo.io
import cv2
import glob, os

# two settings: 1) CQP with quantization parameter 23; 2) CBR with bitrate 3000 


# crf = 23 / 40 

# crf = 18/23/30/40/50  

data_root = '/disk1/zian/data/sony/RGB'
out_root = '/disk1/zhouji/recompress/'
start = 100
end = 105

fps = '15' 
crf = '23'

all_folders = sorted(glob.glob(data_root + '/*'))
folders_to_compress = all_folders[start:end] 

os.makedirs(out_root + 'lossy_%s/'%crf, exist_ok=True) 
os.makedirs(out_root + 'lossless/', exist_ok=True) 


for idx, folder in enumerate(folders_to_compress):
    all_frames = sorted(glob.glob(folder + '/*.png')) 
    im0 = cv2.imread(all_frames[0]) 
    h,w,_ = im0.shape 

    folder_name = folder.split('/')[-1] 

    mp4_writer = skvideo.io.FFmpegWriter(out_root + 'lossy_%s/'%crf + folder_name + '.mp4', 
        inputdict={'-r': '15'},
        outputdict={
            '-vcodec': 'libx264',  #use the h.264 codec
            '-crf': crf,           #set the constant rate factor to 0, which is lossless
            '-preset':'ultrafast',   #the slower the better compression, in princple, try 
                                    #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
            '-r': fps,
            # '-qp': str(23)
    }) 


    avi_writer = skvideo.io.FFmpegWriter(out_root + 'lossless/' + folder_name + '.avi', 
        inputdict={'-r': '15'},
        outputdict={
            '-vcodec': 'libx264',  #use the h.264 codec
            '-crf': '0',           #set the constant rate factor to 0, which is lossless
            '-preset':'ultrafast',   #the slower the better compression, in princple, try 
                                    #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
            '-r': fps,
            # '-qp': str(23)
    }) 

    for path in all_frames:
        # im = cv2.resize(cv2.imread(path), (int(w/4), int(h/4))) 
        im = cv2.imread(path)
        im = im[::2, ::2, :]
        mp4_writer.writeFrame(im[:,:,::-1])  # write the frame as RGB not BGR 
        avi_writer.writeFrame(im[:,:,::-1])  # write the frame as RGB not BGR 
        print(path)

    mp4_writer.close() # close the writer
    #avi_writer.close() 

