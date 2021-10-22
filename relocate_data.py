import os
import shutil
from tqdm import tqdm


def relocate():
  """cropped image 와 label file 을 한 곳으로 모아 정리하는 함수"""
  
  crop_path = "detections\\crop"
  folder_list = os.listdir(crop_path)
  destination_path = "detections\\dataset"
  
  for folder_name in folder_list:
    gathered_path = os.path.join(crop_path, folder_name)
    new_path = os.path.join(destination_path, folder_name)
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
            img_rename = folder_name + "-" + str(i) + ".png"
            img_dst = os.path.join(new_path, img_rename)
            os.rename(data_path, img_dst)
        except FileExistsError:
          if data[-4:] == ".png":
            img_rename = folder_name + "-" + str(lst[-1] + i) + ".png"
            img_dst = os.path.join(new_path, img_rename)
            os.rename(data_path, img_dst)
          
        try:
          if data[-4:] == ".txt":
            txt_rename = folder_name + "-" + str(i) + ".txt"
            txt_dst = os.path.join(label_path, txt_rename)
            os.rename(data_path, txt_dst)
        except FileExistsError:
          if data[-4:] == ".txt":
            txt_rename = folder_name + "-" + str(lst[-1] + i) + ".txt"
            txt_dst = os.path.join(label_path, txt_rename)
            os.rename(data_path, txt_dst)
            
            i += 1
      os.rmdir(frame_path)
    os.rmdir(gathered_path)





if __name__ == "__main__":
  relocate()