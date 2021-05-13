# encoding: UTF-8
import glob as gb
import cv2
#可以运行
img_path = gb.glob("E:/2_Tang/work/Recognize/predict/Project1/Project1/*.jpg")
videoWriter = cv2.VideoWriter('test.avi', cv2.VideoWriter_fourcc(*'MJPG'), 25, (640,1080))

for path in img_path:
    img  = cv2.imread(path)
    img = cv2.resize(img,(640,1080))
    videoWriter.write(img)
videoWriter.release()