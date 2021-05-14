# Heatmap-and-attention-span
when a a video file(store, malls, etc..) is put into a specified target folder, then for that video footage heatmap will be generated and heatcount(how many people went through that spot) at a particular spot and how total time spent by the people at a particular spot.    Used Effdet-7 for person object detection and Graph network technique for Multi object tracking.

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

