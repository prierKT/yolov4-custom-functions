import os
import shutil
import random
from tqdm import tqdm



def export_file_name(file_path):
  """파일 이름만 추출하는 함수 (디렉토리, 확장자 (jpg 와 txt 파일), 중복되는 이름 제거)"""
  file_list = os.listdir(file_path)
  
  try:
    file_list.remove("Label")
  except Exception as e:
    print(e)
    
  lst = []
  
  for file in file_list:
    name, format = os.path.splitext(file)
    lst.append(name)
  
  base_name = set(lst)
  name_list = list(base_name)
  
  return name_list



def devide_data():
  """dataset 폴더에 정제되어 있는 데이터를 8:2 비율로 나눠 train set 과 test set 로 나누는 함수"""
  dataset_path = "detections\\dataset"
  class_list = os.listdir(dataset_path)
  remove_list = ["classes.txt", "obj", "test", "obj.zip", "test.zip"]
  for remove_file in remove_list:
    try:
      class_list.remove(remove_file)
    except Exception as e:
      print(e)
      pass
  
  train_path = os.path.join(dataset_path, "obj")
  test_path = os.path.join(dataset_path, "test")
  
  try:
    os.mkdir(train_path)
    os.mkdir(test_path)
  except FileExistsError:
    pass
  
  for class_name in class_list:
    class_path = os.path.join(dataset_path, class_name)
    name_list = export_file_name(class_path)
    train_list = random.sample(name_list, int(len(name_list)*0.8))
    test_list = [name for name in name_list if name not in train_list]
    
    print("Num of Train: ", len(train_list))
    print("Num of Test: ", len(test_list))
    
    for train_file in tqdm(train_list):
      train_img_file = train_file + ".png"
      train_img_path = os.path.join(class_path, train_img_file)
      train_txt_path = train_img_path.replace(".png", ".txt")
      train_img_dst = os.path.join(train_path, train_img_file)
      train_txt_dst = train_img_dst.replace(".png", ".txt")
      
      os.rename(train_img_path, train_img_dst)
      os.rename(train_txt_path, train_txt_dst)
      
    for test_file in tqdm(test_list):
      test_img_file = test_file + ".png"
      test_img_path = os.path.join(class_path, test_img_file)
      test_txt_path =test_img_path.replace(".png", ".txt")
      test_img_dst = os.path.join(test_path, test_img_file)
      test_txt_dst = test_img_dst.replace(".png", ".txt")
      
      os.rename(test_img_path, test_img_dst)
      os.rename(test_txt_path, test_txt_dst)
      
    shutil.rmtree(class_path)




if __name__ == "__main__":
  devide_data()