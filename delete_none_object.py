import os
import time
import xml.etree.ElementTree as ET

def delete(img_path, xml_path):
    xml_files = os.listdir(xml_path)
    have = 0
    none = 0
    for xml_name in xml_files:
        print(xml_name)
        img_name = xml_name.split(".")[0]
        xml = ET.parse(xml_path + "/" + xml_name)
        root = xml.getroot()
        if root[-1].text is "0":
            none += 1
            os.remove(img_path + "/" + img_name + ".jpg")
            os.remove(xml_path + "/" + xml_name)
        else:
            have += 1
    print("have  :", have)
    print("none  :", none)
if __name__ == "__main__":
    start = time.time()
    delete(r"E:\000000000newwwwwwwwwwwwwwwwwww\bin\Debug\darknet\VOCdevkit\VOC2007\JPEGImages",
           r"E:\000000000newwwwwwwwwwwwwwwwwww\bin\Debug\darknet\VOCdevkit\VOC2007\Annotations")
    print(time.time() - start)