import os
import sys
def rename():
    path="/disk1/zhouji/sony/sony_0601"
    name="0601-"
    startNumber= 0

    count=0
    filelist=os.listdir(path)
    for files in filelist:
        Olddir=os.path.join(path,files)
        index = "%05d" %(startNumber + count)
        Newdir=os.path.join(path,name+index)
        os.rename(Olddir,Newdir)
        count+=1
    print("一共修改了"+str(count)+"个文件")

rename() 