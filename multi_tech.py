import os
import cv2
import glob as gb
from PIL import Image
# 得到两文件夹下交集文件
def delete_repetitive_file(path1, path2):
    list = []
    images = os.listdir(path1)
    xmls = os.listdir(path2)
    for xml in xmls:
        list.append(xml.split(".")[0])
    for file in images:
        front = file.split(".")[0]
        if front not in list:
            os.remove(path1 + "/" + file)

# 多文件夹文件合并
def file_merge():
    path = "E:/2_Tang/work/dijiaorecog/dijiaoimg/28"
    folder = os.listdir(path)
    for fold in folder:
        lr = os.listdir(path + "/" + fold)
        os.chdir(path + "/" + fold)
        print(os.getcwd())
        os.rename("右侧", "right")
        os.rename("左侧", "left")
    path = r"E:\2_Tang\work\Recognize\dijiaorecog\dijiaoimg\28"
    i = 10000
    folder = os.listdir(path)
    for fold in folder:
        lr = os.listdir(path + "/" + fold)

        for lrfold in lr:
            img = os.listdir(path + "/" + fold + "/" + lrfold)
            for image in img:
                img = os.path.join(path + "/" + fold + "/" + lrfold + "/", image)
                img = cv2.imread(img)
                path1 = "E:/000000000newwwwwwwwwwwwwwwwwww/bin/Debug/YOUSHOULDFALLIN/a"
                cv2.imwrite(os.path.join(path1, str(i) + ".jpg"), img)

# 图片合成视频
def image_video():
    img_path = gb.glob("E:/2_Tang/work/Recognize/predict/predict/Result/*.jpg")
    videoWriter = cv2.VideoWriter('test.avi', cv2.VideoWriter_fourcc(*'MJPG'), 25, (640, 1080))

    for path in img_path:
        img = cv2.imread(path)
        img = cv2.resize(img, (640, 1080))
        videoWriter.write(img)
    videoWriter.release()

# 图片重命名
    def changename(path):
        file = os.listdir(path)
        file.sort(key=lambda x: x.split('.')[0])
        j = 10000
        for i in file:
            old_name = os.path.join(path, i)
            new_name = os.path.join(path, i.replace("-", "bc") + ".jpg")
            img = os.rename(old_name, new_name)
            j += 1

#图片格式转换
    def bmp_jpg(file_path):
        i = 10000
        for filename in os.listdir(file_path):
            newfilename = str(i) + ".jpg"
            image = Image.open(file_path + "/" + filename)
            image.save("E:/2_Tang/work/Recognize/benchirecog/车椅/Image_jpg/" + newfilename)
            i += 1


if __name__ == "__main__":
    pass