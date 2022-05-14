import numpy as np
import cv2 as cv
import os
import time
import xml.etree.ElementTree as ET

def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
def chuanjianxml(imgpath,h,w,c):
    str1 = imgpath.split('/')
    str2 = str1[len(str1) - 1]
    print(str1[len(str1) - 1])
    # ------------新增XML----------
    # 创建根节点
    a = ET.Element("annotation")
    # 创建子节点，并添加属性
    b = ET.SubElement(a, "folder")
    # b.attrib = {"NO.": ""}
    # 添加数据
    b.text = "111"
    b = ET.SubElement(a, "filename")
    # b.attrib = {"NO.": ""}
    # 添加数据
    b.text = str2
    # <path>C:\Users\94366\Desktop\111\162.jpg</path>
    b = ET.SubElement(a, "path")
    # b.attrib = {"NO.": ""}
    # 添加数据
    b.text = imgpath
    b = ET.SubElement(a, "source")
    # b.attrib = {"NO.": ""}
    # 添加数据
    c = ET.SubElement(b, "database")
    c.text = "Unknown"

    b = ET.SubElement(a, "size")
    # b.attrib = {"NO.": ""}
    # 添加数据
    c = ET.SubElement(b, "width")
    c.text = str(h)
    c = ET.SubElement(b, "height")
    c.text = str(w)
    c = ET.SubElement(b, "depth")
    c.text = str(3)

    b = ET.SubElement(a, "segmented")
    # b.attrib = {"NO.": ""}
    # 添加数据
    b.text = "0"
    # 创建elementtree对象，写文件
    indent(a, 0)
    tree = ET.ElementTree(a)
    dir = r'G:\Work\Meiling\refrigerator\20220514\xml/' + str2.split('.')[0] + '.xml'
    tree.write(dir, encoding="utf-8")

def addxml(x,y,w,h,text,imgpath):
    str1 = imgpath.split('/')
    str2 = str1[len(str1) - 1]
    str3 = r'G:\Work\Meiling\refrigerator\20220514\xml/' + str2.split('.')[0]+'.xml'
    print(str3)
    updateTree = ET.parse(str3)
    root = updateTree.getroot()

    # --新增--

    # 创建新节点并添加为root的子节点
    newnode = ET.Element("object")
    #       <name>R</name>
    # 		<pose>Unspecified</pose>
    # 		<truncated>0</truncated>
    # 		<difficult>0</difficult>
    # 		<bndbox>
    # 			<xmin>880</xmin>
    # 			<ymin>3257</ymin>
    # 			<xmax>968</xmax>
    # 			<ymax>3337</ymax>
    # 		</bndbox>
    c = ET.Element('name')
    c.text = text.split(':')[0]
    newnode.append(c)
    c = ET.Element('pose')
    c.text = 'Unspecified'
    newnode.append(c)
    c = ET.Element('truncated')
    c.text = '0'
    newnode.append(c)
    c = ET.Element('difficult')
    c.text = '0'
    newnode.append(c)
    c = ET.Element('bndbox')
    d = ET.Element('xmin')
    d.text = str(x)
    c.append(d)
    d = ET.Element('ymin')
    d.text = str(y)
    c.append(d)
    d = ET.Element('xmax')
    d.text = str(x+w)
    c.append(d)
    d = ET.Element('ymax')
    d.text = str(y+h)
    c.append(d)

    newnode.append(c)

    root.append(newnode)

    # 写回原文件
    indent(root, 0)
    updateTree.write(str3, encoding="utf-8", xml_declaration=True)


#yolo_dir = '/home/hessesummer/github/NTS-Net-my/yolov3'  # YOLO文件路径
weightsPath = os.path.join('model/TC.weights')  # 权重文件
configPath = os.path.join('model/TC.cfg')  # 配置文件
labelsPath = os.path.join('model/TC.names')  # label名称
imgPath = os.path.join('images/tt.jpg')  # 测试图像
CONFIDENCE = 0.5  # 过滤弱检测的最小概率
THRESHOLD = 0.4  # 非最大值抑制阈值

# 加载网络、配置权重
net = cv.dnn.readNetFromDarknet(configPath, weightsPath)  # #  利用下载的文件
print("[INFO] loading YOLO from disk...")  # # 可以打印下信息

# 加载图片、转为blob格式、送入网络输入层
# img = cv.imread(imgPath)
# h,w,c = img.shape
# chuanjianxml(imgPath,h,w,c)
print(2)
def yolov3(img):
    # cv.imshow('detected image', img)
    # cv.waitKey(0)

    blobImg = cv.dnn.blobFromImage(img, 1.0/255.0, (416, 416), None, True, False)   # # net需要的输入是blob格式的，用blobFromImage这个函数来转格式
    net.setInput(blobImg)  # # 调用setInput函数将图片送入输入层

    # 获取网络输出层信息（所有输出层的名字），设定并前向传播
    outInfo = net.getUnconnectedOutLayersNames()  # # 前面的yolov3架构也讲了，yolo在每个scale都有输出，outInfo是每个scale的名字信息，供net.forward使用
    start = time.time()
    layerOutputs = net.forward(outInfo)  # 得到各个输出层的、各个检测框等信息，是二维结构。
    end = time.time()
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))  # # 可以打印下信息

    # 拿到图片尺寸
    (H, W) = img.shape[:2]
    # 过滤layerOutputs
    # layerOutputs的第1维的元素内容: [center_x, center_y, width, height, objectness, N-class score data]
    # 过滤后的结果放入：
    boxes = [] # 所有边界框（各层结果放一起）
    confidences = [] # 所有置信度
    classIDs = [] # 所有分类ID

    # # 1）过滤掉置信度低的框框
    for out in layerOutputs:  # 各个输出层
        for detection in out:  # 各个框框
            # 拿到置信度
            scores = detection[5:]  # 各个类别的置信度
            classID = np.argmax(scores)  # 最高置信度的id即为分类id
            confidence = scores[classID]  # 拿到置信度

            # 根据置信度筛查
            if confidence > CONFIDENCE:
                box = detection[0:4] * np.array([W, H, W, H])  # 将边界框放会图片尺寸
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # # 2）应用非最大值抑制(non-maxima suppression，nms)进一步筛掉
    idxs = cv.dnn.NMSBoxes(boxes, confidences, CONFIDENCE, THRESHOLD) # boxes中，保留的box的索引index存入idxs
    # 得到labels列表
    with open(labelsPath, 'rt') as f:
        labels = f.read().rstrip('\n').split('\n')
    # 应用检测结果
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")  # 框框显示颜色，每一类有不同的颜色，每种颜色都是由RGB三个值组成的，所以size为(len(labels), 3)
    if len(idxs) > 0:
        for i in idxs.flatten():  # indxs是二维的，第0维是输出层，所以这里把它展平成1维
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = [int(c) for c in COLORS[classIDs[i]]]
            cv.rectangle(img, (x, y), (x+w, y+h), color, 2)  # 线条粗细为2px  可以获取框的坐标
            text = "{}: {:.4f}".format(labels[classIDs[i]], confidences[i]) #可以获得框的类别
            cv.putText(img, text, (x, y-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)  # cv.FONT_HERSHEY_SIMPLEX字体风格、0.5字体大小、粗细2px
            addxml(x,y,w,h,text,imgPath)
    cv.imshow('detected image', img)
    cv.waitKey(0)
#yolov3(img)

image_path = r'G:\Work\Meiling\refrigerator\20220514\img'
files = os.listdir(image_path)  # 得到文件夹下的所有文件名称
# 遍历文件夹
prefix = image_path + '/'
for file in files:
    imgPath = prefix + file
    img = cv.imread(imgPath)
    h, w, c = img.shape
    chuanjianxml(imgPath, h, w, c)
    yolov3(img)