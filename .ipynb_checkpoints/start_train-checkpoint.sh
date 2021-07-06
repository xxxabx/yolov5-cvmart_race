#!/bin/bash

project_root_dir=/project/train/src_repo
dataset_dir=/home/data
log_file=/project/train/log/log.txt

#pip install -i https://mirrors.aliyun.com/pypi/simple -r /project/train/src_repo/requirements.txt \ 
echo "Preparing..." \
&& echo "Converting dataset..." \
&& python3 -u ${project_root_dir}/voc_txt.py | tee -a ${log_file} \
&& python3 -u ${project_root_dir}/setup.py install | tee -a ${log_file} \
&& echo "Start training..." \
&& cd ${project_root_dir} && python3 -u train.py --data mydata.yaml --cfg yolov5s.yaml --weights yolov5s.pt --batch-size 32 --epochs 10 --nosave --img-size 416 | tee -a ${log_file} \
&& echo "Done" 