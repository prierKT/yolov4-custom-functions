import os
import cv2
from tqdm import tqdm

def label_to_xml():
  """crop을 통하여 만들어진 label file을 변환하여 xml 형식으로 annotation file을 생성하는 함수(PASCAL VOC)"""
  
  dataset_path = "detections\\dataset"
  folder_list = os.listdir(dataset_path)
  remove_list = ["classes.txt", "obj", "test", "obj.zip", "test.zip"]
  for remove_file in remove_list:
    try:
      folder_list.remove(remove_file)
    except Exception as e:
      print(e)
      pass
  
  for per_class in folder_list:
    print("CLASS : ", per_class)
    img_dir_path = os.path.join(dataset_path, per_class)
    label_dir_path = os.path.join(img_dir_path, "Label")
    
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




if __name__ == "__main__":
  label_to_xml()