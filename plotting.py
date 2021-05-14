base_project_path='/home/waycool/Documents/'
base_output_path='/home/waycool/Desktop/'

video='heatmap_attspan_res/23092020/18001900.mp4'
vid_path=str(base_output_path+video)
vid_name=vid_path.split('/')[-1].split('.')[0]
vid_dir_path='/'.join(vid_path.split('/')[:-1])+'/'

res_dir_path=vid_dir_path+vid_name+'/'

import os
import numpy as np
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


# In[35]:


print('[info] : Generating result files in .txt format..')
file_folder=res_dir_path+'results/'
file_list=['count.npy','time.npy','average.npy','heatmap.npy']
       
for f in file_list:
    npyfile=file_folder+f
    name=f.split('.')[0]
    txtfile=file_folder+name+'.txt'   
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

