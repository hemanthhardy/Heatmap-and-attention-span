import os
from glob import glob
from configure import base_project_path, base_output_path, base_input_path
import datetime
from datetime import date

today = str(date.today().strftime('%d%m%Y'))
day_1 = str((date.today()-datetime.timedelta(days=1)).strftime('%d%m%Y'))
day_2 = str((date.today()-datetime.timedelta(days=2)).strftime('%d%m%Y'))

date_list=[day_2,day_1,today]
print('checking folders dates:',date_list)

for d in date_list:
    res_direc=base_output_path+'heatmap_attspan_res/'+d+'/'
    vid_direc=base_input_path+'heatmap_attspan_video/'+d+'/'
    if os.path.exists(vid_direc):
        mp4_list=glob(vid_direc + '/**/*.mp4', recursive=True)
        for v in mp4_list:
            check_name=v.split('/')[-1].split('.')[0]
            check_dir=glob(res_direc+check_name+'/results/*_*_heatmap.txt')
            if len(check_dir) == 0:
                video='/'.join(v.split('/')[-3:])
                f=open('video.txt','w')
                f.write(video)
                print('Scheduling video to process :  ',video)
                f.close()
                ## triggers master file
                runn='python '+ base_project_path +'heatmap_attspan/master.py'
                os.system(runn)
