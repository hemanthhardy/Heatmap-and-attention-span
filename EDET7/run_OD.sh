#! /bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate tf-gpu
echo 'successfully activated tf-gpu environment!!!'
python tf_gendet_temp.py
