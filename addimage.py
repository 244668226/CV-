import shutil
import cv2 as cv
import os
import numpy as np
import random
from PIL import Image
from PIL import ImageEnhance


def gasuss_noise(image, mean=0, var=0.001):
    '''
        添加高斯噪声
        mean : 均值
        var : 方差
    '''
    image = np.array(image / 255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out * 255)
    return out

def gamma_transform(image, gamma=1.6):

    max_value = np.max(image)
    min_value = np.min(image)

    value_l = max_value - min_value

    image = (image - min_value)/value_l

    image = np.power(image, gamma)

    image = image * 255

    return image.astype(np.int)

def copy_file(file, source, target, new_name):
    """
        批量复制文件到指定目录，并重命名
    :param file_list: 需要复制的文件列表
    :param source: 文件源目录
    :param target: 目的地目录
    """
    os.chdir(source)
    shutil.copy(file, target)   # 复制文件到指定目录
    os.chdir(target)
    os.rename(file, new_name)
        # os.rename(file, '{}-{}'.format(date, file))    # 重命名表文件
    #time.sleep(2)

# 原始图像
def ImageAugument(image_path, label_path):

    files = os.listdir(image_path)  # 得到文件夹下的所有文件名称
    # 遍历文件夹
    prefix = image_path + '/'
    for file in files:

        print(file)
        label_name = os.path.join(label_path, file[0:-4] + '.xml')
        image = Image.open(prefix + file)
       # image.show()

        # 亮度增强
        enh_bri = ImageEnhance.Brightness(image)
        brightness = 1.0
        image_brightened = enh_bri.enhance(brightness)
        image_brightened.save(prefix + file[0:-4] + 'lightup' + '.jpg')
        shutil.copy(label_name, os.path.join(label_path, label_name.replace('.xml', 'lightup.xml')))

        # 色度增强
        enh_col = ImageEnhance.Color(image)
        color = 1.0
        
        image_colored = enh_col.enhance(color)
        image_colored.save(prefix + file[0:-4] + 'colorup' + '.jpg')
        shutil.copy(label_name, os.path.join(label_path, label_name.replace('.xml', 'colorup.xml')))

        # 对比度增强
        #enh_con = ImageEnhance.Contrast(image)
        #contrast = 1.0
        #image_contrasted = enh_con.enhance(contrast)
        #image_contrasted.save(prefix + file[0:-4] + 'contrastup' + '.jpg')
        #shutil.copy(label_name, os.path.join(label_path, label_name.replace('.xml', 'contrastup.xml')))

        # 锐度增强
        enh_sha = ImageEnhance.Sharpness(image)
        sharpness = 1.0
        image_sharped = enh_sha.enhance(sharpness)
        image_sharped.save(prefix + file[0:-4] + 'moreSharp' + '.jpg')
        shutil.copy(label_name, os.path.join(label_path, label_name.replace('.xml', 'moreSharp.xml')))

        # cv加载图片
        image_cv = cv.imread(prefix + file)
        image_gray = cv.cvtColor(image_cv, cv.COLOR_BGR2GRAY)

#         #噪声增强
#         enh_gas = gasuss_noise(image_cv)
#         cv.imwrite(prefix + file[0:-4] + 'gasuss' + '.jpg', enh_gas)
#         shutil.copy(label_name, os.path.join(label_path, label_name.replace('.xml', 'gasuss.xml')))

        #直方图均衡
        #enh_eql = cv.equalizeHist(image_gray)
        #cv.imwrite(prefix + file[0:-4] + 'equal' + '.jpg', enh_eql)
        #shutil.copy(label_name, os.path.join(label_path, label_name.replace('.xml', 'equal.xml')))

#         #gamma变换
#         enh_gam = gamma_transform(image_cv)
#         cv.imwrite(prefix + file[0:-4] + 'gamma' + '.jpg', enh_gam)
#         shutil.copy(label_name, os.path.join(label_path, label_name.replace('.xml', 'gamma.xml')))

        #高斯滤波
        enh_gau = cv.GaussianBlur(image_cv, (5, 5), 3)
        cv.imwrite(prefix + file[0:-4] + 'Gaussian' + '.jpg', enh_gau)
        shutil.copy(label_name, os.path.join(label_path, label_name.replace('.xml', 'Gaussian.xml')))



if __name__ == '__main__':


    image_path = 'C:/Users/QD689/Desktop/4'
    label_path = 'C:/Users/QD689/Desktop/5'

    ImageAugument(image_path, label_path)