#! /bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate pytor
echo 'successfully activated pytor environment!!!'
python scheduler.py
