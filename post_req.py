import requests
import os
from configure import base_output_path


date_d = '13042020'
time_d = '13001400'    




resu_dir=base_output_path+date_d+'/'+time_d+'/'
files=os.listdir(resu_dir)
for f in files:
    filee=resu_dir+f
    myurl = 'http://uat.waycool.in/video_intelligence/Rpa/file_upload'
    files = {'file_to_upload': open(filee, 'rb')}
    getdata = requests.post(myurl, files=files)
    print(getdata.text) 
