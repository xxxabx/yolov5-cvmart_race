import os
import random 
import pathlib
import xml.etree.ElementTree as ET
import cv2 as cv
random.seed(0)

xmlfilepath=r'/home/data'
saveBasePath=r"/project/train/src_repo"
supported_fmt = ['.jpg', '.JPG']
classes = [["s_sleeve", "shorts"], ["s_sleeve", "trousers"], ["l_sleeve", "shorts"], ["l_sleeve", "trousers"], ["unsure"]]

trainval_percent=1
train_percent=1

dataset_path = pathlib.Path('/home/data')
total_xml = []
for xml in dataset_path.glob('**/*.xml'):
    possible_images = [xml.with_suffix(suffix) for suffix in supported_fmt]
    supported_images = list(filter(lambda p: p.is_file(), possible_images))
    if len(supported_images) == 0:
        print(f'找不到对应的图片文件: `{xml_file.as_posix()}`')
        continue
    total_xml.append({'image': supported_images[0], 'label': xml})

if not os.path.exists('/project/train/src_repo/labels'):
    os.mkdir('/project/train/src_repo/labels')

sets = ['train', 'test']
 
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)
 
 

def convert_annotation(xml_path):
    in_file = open(str(xml_path))
    image_id=os.path.split(str(xml_path))[-1].replace(os.path.splitext(xml_path)[-1], '.txt') 
    out_file = open('/project/train/src_repo/labels/%s' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
 
    for obj in root.iter('object'):
        #cls = obj.findall('class').text
        cls = obj.findall('class')
        cls = [i.text for i in cls]
        #print(cls)
        #print([i.text for i in cls])
        if "unsure" in cls:
            cls = ["unsure"]
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        for thr in bb:
            if thr>1:
                return 0
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    return 1

ftrain = open(os.path.join(saveBasePath,'train.txt'), 'w')
#ftest = open(os.path.join(saveBasePath,'test.txt'), 'w')
#fval = open(os.path.join(saveBasePath,'val.txt'), 'w')
for i in range(len(total_xml)):
    name = str(total_xml[i]['image'])
    f = open("/project/train/src_repo/wrong_format_file_list.txt","r")   #设置文件对象
    str_data = f.read()     #将txt文件的所有内容读入到字符串str中
    f.close()
    _,_,_,_,wrong_data = name.split('/')
    list1 = [str_data.split('\n')]
    if wrong_data in list1:
        continue
    if convert_annotation(total_xml[i]['label']):
        #if i < 0.8 * len(total_xml):
        ftrain.write(name)
        ftrain.write('\n')
#         elif i < 0.9 * len(total_xml):
#             ftest.write(name)
#             ftest.write('\n')
#         else:
#             fval.write(name)
#             fval.write('\n')
ftrain.close()
# ftest.close()
# fval.close()
