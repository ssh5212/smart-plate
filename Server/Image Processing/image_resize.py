import os
import glob
from PIL import Image

files = glob.glob('./image/*.*')

for f in files:
    try:
        img = Image.open(f)
        # width, height = img.size
        img_resize = img.resize((int(img.width / 2), int(img.height / 2))) # 이미지 사이즈 변환
        title, ext = os.path.splitext(f) # title, 확장자 분리
        img_resize.save(title + '_edit' + ext) # save
    except OSError as e:
        print(e)