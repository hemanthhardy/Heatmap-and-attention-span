import cv2
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()
from tqdm import tqdm
import json
import os

res_dir = '/home/hemanth/Desktop/heatmap_attspan_res/17102020/06000700/results/'
res_path=res_dir+'res.txt'

x,y,d=540,960,3

res=open(res_path,'r').read()
res=res.split('\n')
maxcount=0
for bb in res[:-1]:
    bb=bb.split(',')[1:-1]
    a = int(bb[0])
    if maxcount < a:
        maxcount=a

x1=int(x/18)
xx1=int(x/x1)
y1=int(y/32)
yy1=int(y/y1)
dim=(xx1)*(yy1)*(maxcount+1)
attmap=np.zeros(dim,dtype=int).reshape(xx1,yy1,maxcount+1)
print('heat map dimentions:  ',attmap.shape)


res=open(res_path,'r').read()
res=res.split('\n')
for bb in tqdm(res[:-1]):
    bb=bb.split(',')[1:-1]
    a = int(bb[0])
    b1=int(float(bb[1]))
    b2=int(float(bb[2]))
    b3=int(float(bb[3]))
    b4=int(float(bb[4]))
    x2=b2+b4
    y2=b1+b3
    y2=[b1,y2]
    y2=np.median(y2)
    y2=int(y2/y1)
    x2=int((x2-10)/x1)
    attmap[x2][y2][a]+=1

adim=(xx1,yy1)
attspan=np.zeros(adim,dtype=int)
spancnt=np.zeros(adim,dtype=int)
for xax in tqdm(range(0,xx1)):
    for yax in range(0,yy1):
        for a in range (1,maxcount+1):
            attspan[xax][yax]+=attmap[xax][yax][a]
            if attmap[xax][yax][a] > 0:
                spancnt[xax][yax]+=1



for xax in tqdm(range(0,xx1)):
    for yax in range(0,yy1):
        #attspan[xax][yax]/=25
        attspan[xax][yax]/=1
        #attspan[xax][yax]*=20
np.save(res_dir+'time.npy', attspan)
attspan=np.load(res_dir+'time.npy')


plt.subplots(figsize=(32,18))
ax = plt.axes()
ax.set_title("total seconds spent by people who came into each hotspots",fontsize=50)
sns.heatmap(attspan,cmap='nipy_spectral',annot=True, fmt="d",annot_kws={"size": 20},ax=ax)
plt.savefig(res_dir+'time.png')


plt.subplots(figsize=(32,18))
ax = plt.axes()
ax.set_title("No of people came into each hotspots",fontsize=50)
sns.heatmap(spancnt,cmap='nipy_spectral',annot=True, fmt="d",annot_kws={"size": 20},ax=ax)
np.save(res_dir+'count.npy', spancnt)
plt.savefig(res_dir+'count.png')

adim=(xx1,yy1)
avgspan=np.zeros(adim,dtype=int)
for xax in tqdm(range(0,xx1)):
    for yax in range(0,yy1):
        if attspan[xax][yax] > 0:
            avgspan[xax][yax] = attspan[xax][yax]/(spancnt[xax][yax])

plt.subplots(figsize=(32,18))
ax = plt.axes()
ax.set_title("secs that every each person spent on average",fontsize=50)
sns.heatmap(avgspan,cmap='nipy_spectral',annot=True, fmt="d",annot_kws={"size": 20},ax=ax)
np.save(res_dir+'average.npy', avgspan)
plt.savefig(res_dir+'average.png')
