import os
import cv2
from tqdm import tqdm

def modify_class_name(class_name, label_dir_path):
  """label 파일의 class_name 수정하는 함수"""
  
  label_list = os.listdir(label_dir_path)
  for label in tqdm(label_list):
    label_path = os.path.join(label_dir_path, label)
    
    coords = []
    if label[-4:] == ".txt":
      with open(label_path, "r+", encoding="utf8") as f:
        labeled, xmin, ymin, xmax, ymax = f.read().split(" ")
        coords.append(xmin)
        coords.append(ymin)
        coords.append(xmax)
        coords.append(ymax)
      with open(label_path, "w", encoding="utf8") as f:
        f.write(class_name + " " + coords[0] + " " + coords[1] + " " + coords[2] + " " + coords[3])



def video_capture(video_path, frame_step, save_dir):
  """주어진 frame step 마다 영상을 이미지로 캡쳐하는 함수"""
  vidcap = cv2.VideoCapture(video_path)
  total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
  print("Total Frames: ", total_frames)
  frame_num = int(total_frames / frame_step)
  print("Num of Frames: ", frame_num)
  
  try:
    os.mkdir(save_dir)
  except FileExistsError:
    pass
  
  for i in tqdm(range(1, frame_num)):
    vidcap.set(1, i * frame_step)
    success, image = vidcap.read()    
    cv2.imwrite(os.path.join(save_dir, str(i) + ".png"), image)
    
    if cv2.waitKey(33) == 27:
      break
    
  vidcap.release()
  cv2.destroyAllWindows()
