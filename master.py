#!/usr/bin/env python
# coding: utf-8

# In[25]:


import cv2
import shutil
import os
from tqdm import tqdm
from shutil import rmtree
from shutil import copyfile
from time import time
from PIL import Image
from resizeimage import resizeimage
from multiprocessing import Pool
from configure import base_project_path,base_output_path,base_input_path,store_id
import numpy as np
import platform
import requests
from glob import glob

# In[3]:
src=base_project_path+'heatmap_attspan/configure.py'
dst=base_project_path+'heatmap_attspan/GNMOT/configure.py'
copyfile(src,dst)

video=open('video.txt','r').readlines()
video=video[0]
vid_inpath=str(base_input_path+video)
vid_outpath='heatmap_attspan_res/'+video.split('/')[1]
vid_name=vid_inpath.split('/')[-1].split('.')[0]
vid_date=vid_inpath.split('/')[-2]
vid_dir_path=str(base_output_path+vid_outpath+'/')

if os.path.exists(vid_inpath):
    print('processing video : ',vid_inpath)
else:
    print('vid_path error!!!')

# In[4]:


print('\n\n\t\t\t[info] : PREPROCESSING -1    started.....\n\n')
st=time()
cap= cv2.VideoCapture(vid_inpath)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print( 'Total number of frames in the video :',length )
print('[info] : Video to image conversion going on.....  takes time depending on no of frames.. please dont stop!!!')

res_dir_path=vid_dir_path+vid_name+'/'
heat_res_dir='/'.join(res_dir_path.split('/')[:-3])+'/'
if not os.path.exists(heat_res_dir):
    os.mkdir(heat_res_dir)

date_res_dir='/'.join(res_dir_path.split('/')[:-2])+'/'
if not os.path.exists(date_res_dir):
    os.mkdir(date_res_dir)

if os.path.exists(res_dir_path):
    shutil.rmtree(res_dir_path)
os.mkdir(res_dir_path)

dir_path=res_dir_path+'img1/'
if os.path.exists(dir_path):
    shutil.rmtree(dir_path)
os.mkdir(dir_path)

i=1
mx=9
c=-1
while(cap.isOpened()):
    c+=1
    ret, frame = cap.read()
    if ret == False:
        break
    if c%25 != 0:
        continue
    l=len(str(i))
    ad=mx-l
    adj=''
    for n in range(0,ad):
        adj=adj+'0'
    cv2.imwrite(dir_path+adj+str(i)+'.jpg',frame)
    i+=1
i=i-1
print('[info] : No of Frames Taken : ',i)
print('[info] : video to image conversion successfully done !!!')


# In[5]:


folder=dir_path
srcfolder=dir_path

def resize(i):          # i = 'image_name.jpg'
    with open(srcfolder+i, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [960,540])
            cover.save(folder+i, image.format)

files=sorted(os.listdir(srcfolder))

print('[info] : Image resizing going on.....')
workers=os.cpu_count()-1
print('[info] : Using %d CPU cores'%workers, 'from %d cores for multiprocessing'%os.cpu_count())
with Pool(workers) as p:
    p.map(resize, files)
print('[info] : Image resizing done..')
print('\n\t\t\tPREPROCESSING -1 completed  !!!!!\n\t\t\tTime consumed : ',time()-st,' seconds\n\n\n')

print('\t\t\tPREPROCESSING -2 (Object Detection) started ....\n\n')


# In[6]:


tfod_file_path=base_project_path+'heatmap_attspan/EDET7/tf_gendet.py'
file=open(tfod_file_path,'r')
lines=file.read()
lines=lines.split('\n')
det_dir_path= res_dir_path + 'det/'
if os.path.exists(det_dir_path):
    shutil.rmtree(det_dir_path)
os.mkdir(det_dir_path)
det_file_path = det_dir_path+'det.txt'
lines[23]="res_dir_path = '"+ res_dir_path + "'"
lines[24]="resdet_path = '"+ det_file_path + "'"
lines[25]="image_dir = '"+ dir_path + "'"
tf_model_dir = base_project_path +'heatmap_attspan/EDET7/'
lines[47]="models_dir = '"+ tf_model_dir +"'"
lines='\n'.join(lines)
file.close()
file=file=open(base_project_path+'heatmap_attspan/EDET7/tf_gendet_temp.py','w')
file.write(lines)
file.close()

print('[info] : All is well for doing Object Detection\n\n')


# In[9]:


#### change pytor env to tf-gpu env
os.chdir(base_project_path+'heatmap_attspan/EDET7/')
ostype=platform.system()
if ostype=='Linux':
    os.system('bash run_OD.sh')
elif ostype == 'Windows':
    os.system('run_OD.bat')
else:
    print('[info] : OS plaform error :o.. executable only in Linux and Windows platform..  :(')


# In[10]:


print('\n\t\t\tPREPROCESSING -2 object detection completed !!!!!\n\n\n')

date=vid_dir_path.split('/')[-2]
timing=vid_name

tfod_file_path=base_project_path+'heatmap_attspan/GNMOT/track.py'
file=open(tfod_file_path,'r')
lines=file.read()
lines=lines.split('\n')


lines[16]="date = "+ date
lines[17]="timing = '" +timing+"'"
lines[19]="leng = "+ str(i)

lines='\n'.join(lines)
file.close()
file=file=open(base_project_path+'heatmap_attspan/GNMOT/track_temp.py','w')
file.write(lines)
file.close()

print('[info] : All is set well for tracking !!!!')


# In[16]:


print('\n\n\t\t\tTracking Process Started... !!!!\n\n\n ')
os.chdir(base_project_path+'heatmap_attspan/GNMOT/')
os.system('python track_temp.py')
print('\n\n\t\t\tTracking Process Completed... :) !!!\n\n')


# In[23]:


print('\n\n\t\t\tPlotting Process started... !!!\n\n')
tfod_file_path=base_project_path+'heatmap_attspan/ploting/heatmap.py'
file=open(tfod_file_path,'r')
lines=file.read()
lines=lines.split('\n')
lines[8]="res_dir = '"+ res_dir_path + "results/'"
lines='\n'.join(lines)
file.close()
file=file=open(base_project_path+'heatmap_attspan/ploting/heatmap_temp.py','w')
file.write(lines)
file.close()

tfod_file_path=base_project_path+'heatmap_attspan/ploting/attspan.py'
file=open(tfod_file_path,'r')
lines=file.read()
lines=lines.split('\n')
lines[8]="res_dir = '"+ res_dir_path + "results/'"
lines='\n'.join(lines)
file.close()
file=file=open(base_project_path+'heatmap_attspan/ploting/attspan_temp.py','w')
file.write(lines)
file.close()
print('[info] : All is set well for plotting !!!!')


# In[24]:


os.chdir(base_project_path+'heatmap_attspan/ploting/')
print('[info] : heatmap is generating..')
os.system('python heatmap_temp.py')
print('[info] : heatmap generated and saved..')

print('[info] : attspan-time/count/average is generating..')
os.system('python attspan_temp.py')
print('[info] : attspan-time/count/average generated and saved..')


print('[info] : Generating result files in .txt format..')
file_folder=res_dir_path+'results/'
file_list=['count.npy','time.npy','average.npy','heatmap.npy']
       
for f in file_list:
    npyfile=file_folder+f
    name=f.split('.')[0]
    txtfile=file_folder+store_id+'_'+vid_date+'_'+vid_name+'_'+name+'.txt'   
    avgspan=np.load(npyfile)
    x,y=avgspan.shape
    line=''
    for r in range(x):
        for c in range(y):
            line=line+str(avgspan[r][c])+','
        line=line+'\n'
    f=open(txtfile,'w')
    f.write(line)
    f.close()
    print('[info] : created .txt file for : ',name,'.npy')

dir_path=res_dir_path+'img1/'
if os.path.exists(dir_path):
    shutil.rmtree(dir_path)

dir_path=res_dir_path+'det/'
if os.path.exists(dir_path):
    shutil.rmtree(dir_path)

dir_path=res_dir_path+'seqinfo.ini'
if os.path.exists(dir_path):
    os.remove(dir_path)

resu_dir=res_dir_path+'results/'

files=glob(resu_dir+'/*_*_*.txt')

for f in files:
    myurl = 'http://uat.waycool.in/video_intelligence/Rpa/file_upload'
    files = {'file_to_upload': open(f, 'rb')}
    getdata = requests.post(myurl, files=files)
    print(getdata.text) 
