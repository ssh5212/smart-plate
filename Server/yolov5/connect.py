import os

output = os.popen('D:/dang/yolo/detect.py --weights "runs/train/exp3/weights/best.pt" --source "ttest/"').read() 
print(output)