import os
import cv2
from tqdm import tqdm


def convert_yolo(dataset_path = "D:\\Object_Detection\\yolov4-custom-functions\\detections\\dataset"):
  """crop을 통하여 만들어진 label file을 변환하여 yolo 형식으로 annotation file을 생성하는 함수"""
  
  class_list = os.listdir(dataset_path)
  try: 
    class_list.remove("classes.txt")
    class_list.remove("obj")
    class_list.remove("test")
  except Exception as e:
    print(e)
    pass
  
  for per_class in class_list:
    print("CLASS: ", per_class)
    class_path = os.path.join(dataset_path, per_class)
    label_path = os.path.join(class_path, "Label")
    label_list = os.listdir(label_path)
    
    for label in tqdm(label_list):
      txt_path = os.path.join(label_path, label)
      img_name = label.replace(".txt", ".png")
      img_path = os.path.join(class_path, img_name)
      img = cv2.imread(img_path)
      
      class_dict = {}
      with open(os.path.join(dataset_path, "classes.txt"), "r", encoding="utf8") as classes:
        classes_list = classes.readlines()
        
        for line, classes_name in enumerate(classes_list):
          try:
            classes_name = classes_name.replace("\n", "")
          except Exception as e:
            print(e)
          class_dict[classes_name] = line
      
      with open(txt_path, "r+", encoding="utf8") as f:
        class_name, xmin, ymin, xmax, ymax = f.read().split(" ")
        class_num = class_dict[class_name]
        
        xmin = float(xmin)
        ymin = float(ymin)
        xmax = float(xmax)
        ymax = float(ymax)
        
        xmax -= xmin
        ymax -= ymin
        
        xdiff = int(xmax / 2)
        ydiff = int(ymax / 2)
        
        xmin = xmin + xdiff
        ymin = ymin + ydiff
        
        xmin /= int(img.shape[1])
        ymin /= int(img.shape[0])
        xmax /= int(img.shape[1])
        ymax /= int(img.shape[0])
        
      with open(os.path.join(class_path, label), "w", encoding="utf8") as annotation:
        annotation.write(str(class_num) + " " + str(xmin) + " " + str(ymin) + " " + str(xmax) + " " + str(ymax))




def convert_voc(img_dir_path, label_dir_path):
  """crop을 통하여 만들어진 label file을 변환하여 xml 형식으로 annotation file을 생성하는 함수(PASCAL VOC)"""
  
  label_list = os.listdir(label_dir_path)
  
  for label_file in tqdm(label_list):
    label_file_path = os.path.join(label_dir_path, label_file)
    img_file = label_file.replace(".txt", ".png")
    img_file_path = os.path.join(img_dir_path, img_file)
    img_size = cv2.imread(img_file_path).shape
    
    contents = []
    with open(label_file_path, "r", encoding="utf8") as label:
      class_name, xmin, ymin, xmax, ymax = label.read().split(" ")
      xmin = float(xmin)
      ymin = float(ymin)
      xmax = float(xmax)
      ymax = float(ymax)
      contents.append(class_name)
      contents.append(xmin)
      contents.append(ymin)
      contents.append(xmax)
      contents.append(ymax)
    
    with open(os.path.join(img_dir_path, label_file.replace(".txt", ".xml")), "w", encoding="utf8") as xml_file:
      xml_file.write(f"<annotation>\n\t<folder></folder>\n\t<filename>{img_file}</filename>\n\t<path>{img_file_path}</path>\n\t<source>\n\t\t<database>Unknown</database> \
        \n\t</source>\n\t<size>\n\t\t<width>{img_size[1]}</width>\n\t\t<height>{img_size[0]}</height>\n\t\t<depth>3</depth>\n\t</size>\n\t<segmented>0</segmented> \
        \n\t<object>\n\t\t<name>{contents[0]}</name>\n\t\t<pose>Unspecified</pose>\n\t\t<truncated>0</truncated>\n\t\t<difficult>0</difficult>\n\t\t<bndbox> \
        \n\t\t\t<xmin>{int(contents[1])}</xmin>\n\t\t\t<ymin>{int(contents[2])}</ymin>\n\t\t\t<xmax>{int(contents[3])}</xmax>\n\t\t\t<ymax>{int(contents[4])}</ymax>\n\t\t</bndbox>\n\t</object>\n</annotation>")


