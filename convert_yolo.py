import os
import cv2
from tqdm import tqdm

def label_to_yolo():
  """crop을 통하여 만들어진 label file을 변환하여 yolo 형식으로 annotation file을 생성하는 함수"""
  
  dataset_path = "detections\\dataset"
  class_list = os.listdir(dataset_path)
  remove_list = ["classes.txt", "obj", "test", "obj.zip", "test.zip"]
  for remove_file in remove_list:
    try:
      class_list.remove(remove_file)
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





if __name__ == "__main__":
  label_to_yolo()