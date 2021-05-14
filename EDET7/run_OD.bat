@echo off 
call conda activate tf-gpu
python tf_gendet_temp.py
call conda deactivate
