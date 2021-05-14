#!/usr/bin/env python
# coding: utf-8

# In[1]:
import os
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm
import io
import scipy.misc
import numpy as np
from six import BytesIO
from PIL import Image, ImageDraw, ImageFont
import cv2
import tensorflow as tf

from object_detection.utils import label_map_util
from object_detection.utils import config_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder


# In[2]:
res_dir_path = '/home/waycool/Desktop/heatmap_attspan_res/23092020/18001900/'
resdet_path='/home/waycool/Desktop/24sep_8to9am1_f/24sep_8to9am1_f_det.txt'
image_dir = '/home/waycool/Desktop/24sep_8to9am1_f/'
im_list=os.listdir(image_dir)
im_list=sorted(im_list)

def load_image_into_numpy_array(path):
  img_data = tf.io.gfile.GFile(path, 'rb').read()
  image = Image.open(BytesIO(img_data))
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


# In[3]:


# @title Choose the model to use, then evaluate the cell.
MODELS = {'CenterNet_HourGlass104_1024x1024':'centernet_hg104_1024x1024_coco17_tpu-32','EfficientDet_D4_1024x1024':'efficientdet_d4_coco17_tpu-32','EfficientDet_D5_1280x1280':'efficientdet_d5_coco17_tpu-32','EfficientDet_D6_1280x1280':'efficientdet_d6_coco17_tpu-32','CenterNet HourGlass104_512x512':'centernet_hg104_512x512_coco17_tpu-8','EfficientDet_D7_1536x1536':'efficientdet_d7_coco17_tpu-32'}

model_display_name = 'EfficientDet_D7_1536x1536'

model_name = MODELS[model_display_name]

models_dir =''
# In[4]:


pipeline_config = os.path.join(models_dir+'models/research/object_detection/configs/tf2/',model_name + '.config')
model_dir = models_dir+'models/research/object_detection/test_data/'+model_display_name+'/checkpoint/'

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(pipeline_config)
model_config = configs['model']
detection_model = model_builder.build(model_config=model_config, is_training=False)
print(configs)
# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(
      model=detection_model)
ckpt.restore(os.path.join(model_dir, 'ckpt-0')).expect_partial()

def get_model_detection_function(model):
  """Get a tf.function for detection."""

  @tf.function
  def detect_fn(image):
    """Detect objects in image."""

    image, shapes = model.preprocess(image)
    prediction_dict = model.predict(image, shapes)
    detections = model.postprocess(prediction_dict, shapes)

    return detections, prediction_dict, tf.reshape(shapes, [-1])

  return detect_fn

detect_fn = get_model_detection_function(detection_model)


# In[5]:


configs['eval_input_config'].label_map_path=models_dir+'models/research/cognitive_planning/label_map.txt'
label_map_path = configs['eval_input_config'].label_map_path
label_map = label_map_util.load_labelmap(label_map_path)
categories = label_map_util.convert_label_map_to_categories(
    label_map,
    max_num_classes=label_map_util.get_max_label_map_index(label_map),
    use_display_name=True)
category_index = label_map_util.create_category_index(categories)
label_map_dict = label_map_util.get_label_map_dict(label_map, use_display_name=True)


# In[6]:


def tf_od_pred_person(input_tensor,th):
    detections, predictions_dict, shapes = detect_fn(input_tensor)
    ind=0
    boxes=detections['detection_boxes'][0].numpy()
    classes=(detections['detection_classes'][0].numpy()).astype(int)
    scores=detections['detection_scores'][0].numpy()
    box=[]
    clas=[]
    score=[]
    for i in classes:
        if i==0 and scores[ind] > th:
            box.append(boxes[ind])
            clas.append(classes[ind])
            score.append(scores[ind])
        ind+=1
    clas=[k+1 for k in clas]
    dets=detections
    pred_dict=predictions_dict
    shapes=shapes

    return box,clas,score


# In[7]:



# In[8]:


for i in tqdm(im_list):

    image_path = os.path.join(image_dir+i)
    image_np = load_image_into_numpy_array(image_path)

    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)

    box,clas,score= tf_od_pred_person(input_tensor,th=0.4)

    im_h=image_np.shape[0]
    im_w=image_np.shape[1]
    det=''
    ind=0
    f_no=int(i.split('.')[0])
    
    f=open(resdet_path,'a')
    for bb in box:
        bb[0] *= im_h
        
        bb[1] *= im_w
        bb[2] *= im_h
        bb[3] *= im_w
        t1 = bb[2]-bb[0]
        t2 = bb[3]-bb[1]
        
        det=det+str(f_no)+',-1,'+str(bb[1])+','+str(bb[0])+','+str(t2)+','+str(t1)+','+str(score[ind])+',-1,-1,-1\n'
        ind+=1

    f.write(det)
f.close()
print('Processed successfully..!!!!')

if os.path.exists(res_dir_path+'seqinfo.ini'):
    os.remove(res_dir_path+'seqinfo.ini')
f=open(res_dir_path+'seqinfo.ini','a')

path=res_dir_path.split('/')
date=path[-3]
time=path[-2]
name='name='+str(date) +'-'+ str(time) +'\n'
seqLength='seqLength='+str(f_no)+'\n'

f.write('[Sequence]\n')
f.write(name)
f.write('imDir=img1\n')
f.write('frameRate=1\n')
f.write(seqLength)
f.write('imWidth=960\n')
f.write('imHeight=540\n')
f.write('imExt=.jpg')
f.close()

