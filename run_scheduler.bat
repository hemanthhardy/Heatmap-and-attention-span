@echo off
call conda activate pytor
python scheduler.py
call conda deactivate
