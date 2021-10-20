import os
import cv2
from cv2 import cuda
import shutil
import random
from tqdm import tqdm



def change_file_name(dir_path, file_name):
  "파일 이름을 정렬하는 함수"
  file_list = os.listdir(dir_path)
  
  i = 1
  for file in file_list:
    file_src = os.path.join(dir_path, file)
    name, format = file.split(".")
    file_rename = file_name + "-" + str(i) + "." + format
    file_dst = os.path.join(dir_path, file_rename)
    
    os.rename(file_src, file_dst)
    i += 1



def gather_data(object_name, gathered_path, destination_path = "D:\\Object_Detection\\yolov4-custom-functions\\detections\\dataset"):
  """cropped image 와 label file 을 한 곳으로 모아 정리하는 함수"""

  new_path = os.path.join(destination_path, object_name)
  label_path = os.path.join(new_path, "Label")
  lst = [1]
  try:
    os.mkdir(new_path)
    os.mkdir(label_path)
  except FileExistsError:
    label_list = os.listdir(label_path)
    for label in label_list:
      label_num = int(label.replace(".txt", "").split("-")[1])
      lst.append(label_num)
    pass
  lst.sort()
  
  print("PWD: ", gathered_path)
  print("Destination: ", new_path)
  
  i = 1
  frame_list = os.listdir(gathered_path)
  for frame in tqdm(frame_list):
    frame_path = os.path.join(gathered_path, frame)
    data_list = os.listdir(frame_path)
    for data in data_list:
      data_path = os.path.join(frame_path, data)
      
      try:
        if data[-4:] == ".png":
          img_rename = object_name + "-" + str(i) + ".png"
          img_dst = os.path.join(new_path, img_rename)
          os.rename(data_path, img_dst)
      except FileExistsError:
        if data[-4:] == ".png":
          img_rename = object_name + "-" + str(lst[-1] + i) + ".png"
          img_dst = os.path.join(new_path, img_rename)
          os.rename(data_path, img_dst)
        
      try:
        if data[-4:] == ".txt":
          txt_rename = object_name + "-" + str(i) + ".txt"
          txt_dst = os.path.join(label_path, txt_rename)
          os.rename(data_path, txt_dst)
      except FileExistsError:
        if data[-4:] == ".txt":
          txt_rename = object_name + "-" + str(lst[-1] + i) + ".txt"
          txt_dst = os.path.join(label_path, txt_rename)
          os.rename(data_path, txt_dst)
          
          i += 1
    os.rmdir(frame_path)
  os.rmdir(gathered_path)



def modify_class_name(object_name, label_dir_path):
  """label 파일의 class_name 수정하는 함수"""
  
  print("CLASS: ", object_name)
  label_list = os.listdir(label_dir_path)
  for label in tqdm(label_list):
    label_path = os.path.join(label_dir_path, label)
    
    coords = []
    if label[-4:] == ".txt":
      with open(label_path, "r+", encoding="utf8") as f:
        class_name, xmin, ymin, xmax, ymax = f.read().split(" ")
        coords.append(xmin)
        coords.append(ymin)
        coords.append(xmax)
        coords.append(ymax)
      with open(label_path, "w", encoding="utf8") as f:
        f.write(object_name + " " + coords[0] + " " + coords[1] + " " + coords[2] + " " + coords[3])



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



def make_train_test(train_ratio):
  """dataset 폴더의 image 파일들과 text 파일들을 주어진 train 비율로 계산하여 train set과 test set으로 나눠주는 함수"""
  dataset_path = "E:\\Object_Detection\\yolov4-custom-functions\\detections\\dataset"
  train_path = os.path.join(dataset_path, "obj")
  test_path = os.path.join(dataset_path, "test")
  
  try:
    os.mkdir(train_path)
    os.mkdir(test_path)
  except FileExistsError:
    pass
  
  class_list = os.listdir(dataset_path)
  class_list.remove("classes.txt")
  class_list.remove("obj")
  class_list.remove("test")
  
  for class_name in class_list:
    class_path = os.path.join(dataset_path, class_name)
    name_list = export_file_name(class_path)
    train_list = random.sample(name_list, int(len(name_list)*train_ratio))
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



def video_capture(video_path, frame_step, save_dir):
  """영상파일을 주어진 frame step 간격으로 나눠 저장하는 함수"""
  vidcap = cv2.VideoCapture(video_path)
  total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
  print("Total Frames: ", total_frames)
  frame_num = int(total_frames / frame_step)
  print("Num of Frames: ", frame_num)
  
  try:
    os.mkdir(save_dir)
  except FileExistsError:
    pass
  
  i = 1
  for i in tqdm(range(1, frame_num)):
    vidcap.set(1, i * frame_step)
    success, image = vidcap.read()    
    cv2.imwrite(os.path.join(save_dir, str(i) + ".png"), image)
    i += 1
    
    if cv2.waitKey(33) == 27:
      break
    
  vidcap.release()
  cv2.destroyAllWindows()



# change_file_name("D:\\Object_Detection\\yolov4-custom-functions\\data\\video\\K2", "K2")


# # gather img, txt files in one directory.
# crop_path = "D:\\Object_Detection\\yolov4-custom-functions\\detections\\crop"
# dir_list = os.listdir(crop_path)
# for dir in dir_list:
#   dir_path = os.path.join(crop_path, dir)
#   gather_data("Type_90", os.path.join(crop_path, dir))

# img_list = os.listdir("D:\\Object_Detection\\yolov4-custom-functions\\detections\\dataset\\Type_90")
# img_list.remove("Label")
# label_list = os.listdir("D:\\Object_Detection\\yolov4-custom-functions\\detections\\dataset\\Type_90\\Label")
# print("Num of Images: ", len(img_list))
# print("Num of Labels: ", len(label_list))


# modify_class_name("K1A1", "D:\\Object_Detection\\yolov4-custom-functions\\detections\\dataset\\K1A1\\Label")


# # delete random files
# p = "D:\\Object_Detection\\yolov4-custom-functions\\detections\\dataset\\Type_90"
# img_list = os.listdir(p)
# img_list.remove("Label")
# d_img_list = random.sample(img_list, int(len(img_list)*0.4))
# for d_img in tqdm(d_img_list):
#   d_img_path = os.path.join(p, d_img)
#   d_txt_path = os.path.join(p, "Label", d_img.replace(".png", ".txt"))
#   os.remove(d_img_path)
#   os.remove(d_txt_path)


# # modify class_name in txt files.
# dataset_path = "D:\\Object_Detection\\yolov4-custom-functions\\detections\\dataset"
# object_list = os.listdir(dataset_path)
# object_list.remove("classes.txt")
# for object in object_list:
#   object_path = os.path.join(dataset_path, object)
#   label_path = os.path.join(object_path, "Label")
#   modify_class_name(object, label_path)


# make_train_test(0.8)


# # delete random frames
# p = "D:\\Object_Detection\\yolov4-custom-functions\\detections\\crop\\K2_4"
# frame_list = os.listdir(p)
# d_frame_list = random.sample(frame_list, int(len(frame_list)*0.2))
# print("Num of Delete", len(d_frame_list))
# for frame in tqdm(d_frame_list):
#   frame_path = os.path.join(p, frame)
#   shutil.rmtree(frame_path)


# # capture video
# video_path = "D:\\Tank_dataset\\edited_video\\full\\Type_90.mp4"
# save_dir = "D:\\Object_Detection\\yolov4-custom-functions\\detections\\dataset\\Type_90"
# video_capture(video_path, 15, save_dir)


# #delete txt file
# path = "D:\\Tank_dataset\\edited_video\\fail\K1A1"
# file_list = os.listdir(path)
# for file in file_list:
#   file_path = os.path.join(path, file)
#   if file[-4:] == ".txt":
#     os.remove(file_path)
#   else:
#     pass


# # change file name
# path = "D:\\Object_Detection\\yolov4-custom-functions\\detections\\dataset\\Type_90"
# obj_dir = "Type_90"
# file_list = os.listdir(path)
# try:
#   file_list.remove("classes.txt")
# except Exception as e:
#   print(e)
#   pass
  
# i = 1
# for file in tqdm(file_list):
#   file_path = os.path.join(path, file)
  
#   if file_path[-4:] == ".png":
#     file_rename = obj_dir + "-" + str(i) + ".png"
#     file_dst = os.path.join(path, file_rename)
#     os.rename(file_path, file_dst)
#   # elif file_path[-4:] == ".txt":
#   #   file_rename = obj_dir + "-" + str(i) + ".txt"
#   #   file_dst = os.path.join(path, file_rename)
#   #   os.rename(file_path, file_dst)
    
#     i += 1
