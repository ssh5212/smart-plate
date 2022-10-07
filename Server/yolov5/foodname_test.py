import os

output = os.popen('python D:/dang/yolo/detect.py --weights "D:/dang/yolo/runs/train/exp3/weights/best.pt" --source "ttest/"').read() 

print(output) 

output = output.split('\n')
output.pop()

print(output)