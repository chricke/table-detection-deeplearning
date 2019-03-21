import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from shutil import copyfile
import cv2

root = os.getcwd()
labelsPath = os.path.join(root, 'labels')
imagePath = os.path.join(root, 'images')
trainPath = os.path.join(imagePath, 'train')
testPath = os.path.join(imagePath, 'test')
xml_data_dir = os.path.join(root, 'unlv_xml_gt')

os.chdir(root)

def preprocess_images(file):
    img = cv2.imread(os.path.join(image_source_dir, filename))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    b = cv2.distanceTransform(img, distanceType=cv2.DIST_L2, maskSize=5)
    g = cv2.distanceTransform(img, distanceType=cv2.DIST_L1, maskSize=5)
    r = cv2.distanceTransform(img, distanceType=cv2.DIST_C, maskSize=5)

    transformed_image = cv2.merge((b, g, r))
    target_file = os.path.join(image_target_dir, filename)
    print("Writing target file {}".format(target_file))
    cv2.imwrite(target_file, transformed_image)

def xml_to_csv(path):
    xml_list = []

    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)

        root = tree.getroot()
        filename = xml_file.split('/')[-1].split('.')[0] + ".png"
        source_file = "dataset/output/" + filename
        if os.path.isfile(source_file):
            copyfile(source_file, "data/images/" + filename)
            for member in root[0]:
                print(member.attrib)

                value = (filename,
                         member.attrib['x0'],
                         member.attrib['y0'],
                         member.attrib['x1'],
                         member.attrib['y1'],
                         'Table'
                    )
                print(value)
                xml_list.append(value)
    column_name = ['filename', 'xmin', 'ymin', 'xmax', 'ymax', 'class']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def main():
    xml_df = xml_to_csv(xml_data_dir)
    xml_df.to_csv('data/train.csv', index=None, header=None)
    print('Successfully converted xml to csv.')

main()