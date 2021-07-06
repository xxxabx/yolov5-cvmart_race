# yolov5-cvmart_race
The competition of cvmart

代码保存在分支master.

首先需要根据数据集自己修改一些配置信息，适配yolov5.这些网上教程很多就不再赘述。

* 需要修改的地方

voc_txt.py:需要读取服务器上的数据，并写成txt到指定路径；

Dockfile：制作镜像的流程，如果需要重装镜像配置需要修改下，比如我重装了cudnn，可以参考下；

start_bash.sh:训练脚本，直接bash start_bash.sh即可开始训练
