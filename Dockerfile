FROM ccr.ccs.tencentyun.com/accv-train/cuda10.1-cudnn7.5.1-dev-ubuntu16.04-opencv4.1.1-torch1.4.0-openvino2020r1-workspace

# 创建默认目录，训练过程中生成的模型文件、日志、图必须保存在这些固定目录下，训练完成后这些文件将被保存
RUN mkdir -p /project/train/src_repo && mkdir -p /project/train/result-graphs && mkdir -p /project/train/log && mkdir -p /project/train/models && mkdir -p /project/train/src_repo/pre-trained-model

# 安装训练环境依赖端软件，请根据实际情况编写自己的代码
COPY . /project/train/src_repo/
RUN apt-get install software-properties-common 
RUN apt install python3-apt
RUN cd /usr/lib/python3/dist-packages && cp apt_pkg.cpython-35m-x86_64-linux-gnu.so apt_pkg.cpython-36m-x86_64-linux-gnu.so
RUN add-apt-repository -y ppa:jonathonf/python-3.8 
RUN apt-get update 
RUN apt-get install -y python3.8
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
RUN update-alternatives --install /usr/bin/python python /usr/bin/python2 100
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 150
#RUN /usr/bin/python3.6 -m pip install --upgrade pip
RUN pip install pip -U
RUN python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ -r /project/train/src_repo/requirements.txt


