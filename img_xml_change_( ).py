import time
from PIL import Image
import os

def change_bracket(img_path, xml_path, save_img_path, save_xml_path):
    xmllist=os.listdir(xml_path)
    for xmls in xmllist:
        name = xmls.split(".")[0]
        str1 = name.replace(" (", "_")
        str2 = str1.replace(")", "_")
        save_xml = open(save_xml_path+'/'+ str2 + ".xml", 'w')
        xml = open(xml_path + '/' + xmls, 'r')
        content = xml.readlines()
        for line in content:
            line=line.replace(' (','_')
            line = line.replace(')', '_')
            save_xml.write(line)
            xml.close()

        name = name + ".jpg"
        imgs = os.listdir(img_path)
        if name in imgs:
            img = Image.open(img_path + "/" + name)
            img.save(save_img_path + "/" + str2 + ".jpg")


if __name__ == "__main__":
    start = time.time()
    change_bracket(r"E:\2_Tang\work\Recognize\liumianti\Color_cart\color_card",
                   r"E:\2_Tang\work\Recognize\liumianti\Color_cart\xml",
                   r"E:\2_Tang\work\Recognize\liumianti\Color_cart\save_img",
                   r"E:\2_Tang\work\Recognize\liumianti\Color_cart\save_xml")
    print(time.time() - start)