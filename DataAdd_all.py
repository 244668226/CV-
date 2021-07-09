from PIL import Image #python中的图像处理库PIL来实现不同图像格式的转换。
import numpy as np
# Element类型是一种灵活的容器对象，用于在内存中存储结构化数据。
import xml.etree.ElementTree as ET #
import os
import shutil
#该函数返回文件名字
def standardize(filename):
    filename = str(filename)
    c = len(filename)
    filename = '0'*(6-c)+filename
    return filename
#该函数返回xml中的图像根结点、图像的长和宽以及左上角和右下角的顶点坐标
def xml_parse(xml_path):
    width,height,label = 0, 0, 0
    tree = ET.parse(xml_path)#ET.parse：直接解析XML文件并获得根节点
    gtboxes, filename = [], ''#初始化变量为列表、字符串
    for child_root in tree.getroot():#tree.getroot()：获得根节点

        if child_root.tag == 'size':#tag，即标签，用于标识该元素表示哪种数据
            for son_item in child_root:
                if son_item.tag == 'height':
                    height = int(son_item.text)#text，文本字符串，可以用来存储一些数据
                if son_item.tag == 'width':
                    width = int(son_item.text)

        if child_root.tag == 'object':##xml中的第二个标签
            sbox = []
            for son_root in child_root:
                if son_root.tag == 'bndbox':
                    for son_item in son_root:
                        ##list.append() 方法用于在列表末尾添加新的对象。该方法无返回值,但是会修改原来的列表。
                        sbox.append(int(son_item.text))
            gtboxes.append(sbox)

    return tree, height, width, np.array(gtboxes)#array()函数生成矩阵时数据只能为列表形式

def rotate(img, xml, degree, save_img_path, save_xml_path, filename, format='.png',name = None):


    image = np.array(img)
    tree, height, width, gtboxes = xml_parse(xml)#%调用xml_parse函数
    gtboxes_copy = []
    # x0,y0,x1,y1

    if degree == 90:
        height, width = width, height
        image = np.rot90(image, 3)
        for boxes in gtboxes:
            gtboxes_copy.append([width - boxes[3], boxes[0], width - boxes[1], boxes[2]])
    elif degree == 180:
        image = np.rot90(image, 2)
        for boxes in gtboxes:
            gtboxes_copy.append([width - boxes[2], height - boxes[3], width - boxes[0], height - boxes[1]])
    elif degree == 270:
        height, width = width, height
        image = np.rot90(image)
        for boxes in gtboxes:
            gtboxes_copy.append([boxes[1], height - boxes[2], boxes[3], height - boxes[0]])

    for child_root in tree.getroot():#获得根结点
        if child_root.tag == 'filename':
            child_root.text = filename
        if child_root.tag == 'size':
            for son_item in child_root:
                if son_item.tag == 'height':
                    son_item.text = str(height)
                if son_item.tag == 'width':
                    son_item.text = str(width)

        if child_root.tag == 'object':
            sbox = gtboxes_copy[0]
            for son_root in child_root:
                if son_root.tag == 'bndbox':
                    for idx,son_item in enumerate(son_root):
                        son_item.text = str(sbox[idx])
            del gtboxes_copy[0]
    image = Image.fromarray(image)#使用PIL打开图片，并将其分离为RGB三个通道
    imgfilename = os.path.join(save_img_path, name+str(degree)+format)

    image.save(imgfilename)
    xmlfilename = os.path.join(save_xml_path, name+str(degree)+'.xml')
    tree.write(xmlfilename)

def flip(img, xml, type, save_img_path, save_xml_path, filename, format='.png', name = None):

    tree, height, width, gtboxes = xml_parse(xml)
    gtboxes_copy = []
    # x0,y0,x1,y1

    if type == 'Up_Bottom':
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        for boxes in gtboxes:
            gtboxes_copy.append([boxes[0], height - boxes[3], boxes[2], height - boxes[1]])

    elif type == 'Left_Right':
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        for boxes in gtboxes:
            gtboxes_copy.append([width - boxes[2], boxes[1], width - boxes[0], boxes[3]])

    for child_root in tree.getroot():
        if child_root.tag == 'filename':
            child_root.text = filename
        if child_root.tag == 'size':
            for son_item in child_root:
                if son_item.tag == 'height':
                    son_item.text = str(height)
                if son_item.tag == 'width':
                    son_item.text = str(width)

        if child_root.tag == 'object':
            sbox = gtboxes_copy[0]
            for son_root in child_root:
                if son_root.tag == 'bndbox':
                    for idx,son_item in enumerate(son_root):
                        son_item.text = str(sbox[idx])
            del gtboxes_copy[0]
    imgfilename = os.path.join(save_img_path, name+filename+format)
    img.save(imgfilename)
    xmlfilename = os.path.join(save_xml_path, name+filename+'.xml')
    tree.write(xmlfilename)

if __name__=='__main__':

#注意：此时路径前两行为linux系统路径格式，后面两行是windows路径格式。
   # img_path, xml_path = '/media/数据备份/data_new/JPEGImages/', '/media/xhh/数据备份/data_new/Annotations/'
    #save_img_path, save_xml_path, = '/media/数据备份/AUG_Data/JPEGImages/', '/media/数据备份/AUG_Data/Annotations/'
    img_path, xml_path = r'E:\2_Tang\work\Recognize\weibolu\20210708imgseg\temp11\img', r'E:\2_Tang\work\Recognize\weibolu\20210708imgseg\temp11\xml'
    save_img_path, save_xml_path, = r'E:\2_Tang\work\Recognize\weibolu\20210708imgseg\temp11\img_save', r'E:\2_Tang\work\Recognize\weibolu\20210708imgseg\temp11\xml_save'
    #print(save_img_path)
    counter = 2
    for file in os.listdir(img_path):
        filename = file.split('.')[0]
        format = '.'+file.split('.')[-1]
        shutil.copy(os.path.join(img_path, file), os.path.join(save_img_path, standardize(counter)+format))

        tree, height, width, gtboxes = xml_parse(os.path.join(xml_path, filename+'.xml'))

        for child_root in tree.getroot():
            if child_root.tag == 'filename':
                child_root.text = standardize(counter)

        tree.write(os.path.join(save_xml_path, standardize(counter)+'.xml'))

        image = Image.open(os.path.join(img_path, file))
        xml = os.path.join(xml_path, filename+'.xml')
        print(filename)
        rotate(image, xml, 90, save_img_path, save_xml_path, standardize(counter+1), format,filename)
        rotate(image, xml, 180, save_img_path, save_xml_path, standardize(counter+1), format,filename)
        rotate(image, xml, 270, save_img_path, save_xml_path, standardize(counter+1), format,filename)
        #rotate(image, xml, 90, filename, save_img_path, save_xml_path, standardize(counter+1), format) #
        #rotate(image, xml, 180, filename, save_img_path, save_xml_path, standardize(counter+1), format) #
        #rotate(image, xml, 270, filename, save_img_path, save_xml_path, standardize(counter+1), format)#

        flip(image, xml, 'Up_Bottom', save_img_path, save_xml_path, standardize(counter+2), format,filename)
        flip(image, xml, 'Left_Right', save_img_path, save_xml_path, standardize(counter+2), format,filename)

        counter += 2
