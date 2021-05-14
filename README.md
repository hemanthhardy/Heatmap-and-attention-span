# Heatmap-and-attention-span
when a a video file(store, malls, etc..) is put into a specified target folder, then for that video footage heatmap will be generated and heatcount(how many people went through that spot) at a particular spot and how total time spent by the people at a particular spot and these four output will be save in a target output path seperately.    
 *Used Effdet-7 for person object detection and Graph network technique for Multi object tracking.*

# to execute the code and installions.
   Go through the Documentation/heatmap_attspan_doc.pdf
   
# NOTE before installations:
   TF2 Object dection API setup with TF installed via anaconda(supported with GPU till october 2020). But now if you follow the doc, you will able to install only CPU supported env. Because when running setup.py for TF OD API setup, it looks for latest and anaconda doesnt have now and only pip has. But pip wont manage CUDA and cudnn like anaconda by itself. So if you want to install with GPU support you should manually install CUDA and CUDNN, steps for that also attached as .txt file.

# output  video link:  
https://www.youtube.com/watch?v=DHGLfOiaB-E

# output images:
1) normal store view from a CCTV camera:
![res_heatmap]![000003238](https://user-images.githubusercontent.com/28312002/118289781-515c7b00-b4f3-11eb-9f90-9ed814bd9d4d.jpg)

2) outputs:
    1) Heatmap:
        ![res_heatmap](https://user-images.githubusercontent.com/28312002/118290012-92548f80-b4f3-11eb-8144-652c538c7f0a.png)
    2) head count at a spot(total people step at a particular spot):
        ![res_count](https://user-images.githubusercontent.com/28312002/118290137-b7e19900-b4f3-11eb-83c4-2e74f83b8d39.png)

    3) Time spent at a spot by all people(total)  :
        ![res_time](https://user-images.githubusercontent.com/28312002/118290404-0858f680-b4f4-11eb-9c72-993880bc519a.png)

    4) from (2) and (3) average time spent by an individual whe he or she comes into a particular spot   :
        ![res_avgspan](https://user-images.githubusercontent.com/28312002/118290429-0f800480-b4f4-11eb-8955-747b79fa0cc8.png)

# Project Draw Backs:
  1) occlutions errors can be only avoided when an person is detect within some time and he/she should be in the same posture/ appear like the same like when they got occluded before.
  2) But if the were occluded for more than a specfic period and they didnt get detected then they will considered as new person
  3) or when detect within specfic time but looking different(in some other posture, or walked some way arround) aslso considered as new person
  4) even if he/she went away from frame and came into again then also will be considered as a new person

  The above drawbacks were the main challenge and researchers were still in engaged to find out solution for this.
