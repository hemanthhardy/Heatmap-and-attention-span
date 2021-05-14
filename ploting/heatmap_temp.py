import cv2
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()
from tqdm import tqdm
import json


res_dir = '/home/hemanth/Desktop/heatmap_attspan_res/17102020/06000700/results/'
res_path=res_dir+'res.txt'

x,y,d=540,960,3

res=open(res_path,'r').read()
res=res.split('\n')
maxcount=0
dets=0
for bb in res[:-1]:
    dets+=1
    bb=bb.split(',')[1:-1]
    a = int(bb[0])
    if maxcount < a:
        maxcount=a
print('Total detections (B.Boxes):  ',dets)
print('Total number of persons:  ',maxcount)

dim=(x+1)*(y+1)*(maxcount+1)
hmap=np.zeros(dim,dtype=bool).reshape(x+1,y+1,maxcount+1)
print('heat map dimentions:  ',hmap.shape)



res=open(res_path,'r').read()
res=res.split('\n')
for bb in tqdm(res[:-1]):
    bb=bb.split(',')[1:-1]
    a = int(bb[0])
    b1=int(float(bb[1]))
    b2=int(float(bb[2]))
    b3=int(float(bb[3]))
    b4=int(float(bb[4]))
    y2=min(b1+b3,y-1)
    x2=min(b2+b4,x-1)
    mid=[b1,y2]
    mid=int(np.median(mid))
    y1=mid-12
    y2=mid+12
    x1=x2-12
    for xax in range(x1,x2):
        for yax in range(y1,y2):
            hmap[xax][yax][a]=True

adim=(x,y)
heatmap=np.zeros(adim,dtype=int)
x1=x+1
y1=y+1
for xax in tqdm(range(0,x)):
    for yax in range(0,y):
        for a in range (1,maxcount+1):
            if hmap[xax][yax][a]==True:
                heatmap[xax][yax]+=1
np.save(res_dir+'heatmap.npy', heatmap)
heatmap=np.load(res_dir+'heatmap.npy')



heatmap=np.load(res_dir+'heatmap.npy')
plt.subplots(figsize=(32,18))
ax = plt.axes()
ax.set_title("Heat map : no of people came into a place",fontsize=50)
sns.heatmap(heatmap,cmap='nipy_spectral')
plt.savefig(res_dir+'heatmap.png')
