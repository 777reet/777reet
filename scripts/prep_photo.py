from pathlib import Path
import cv2, numpy as np
from PIL import Image
import sys

if len(sys.argv)!=2: raise SystemExit('Usage: python scripts/prep_photo.py photo.jpg')
src=sys.argv[1]; out=Path('data/source-prepped.png')
im=cv2.imread(src)
if im is None: raise SystemExit(f'Could not read {src}')
scale=min(1,900/max(im.shape[:2])); im=cv2.resize(im,None,fx=scale,fy=scale)
gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
gray=cv2.createCLAHE(clipLimit=2.2,tileGridSize=(8,8)).apply(gray)
gray=cv2.normalize(gray,None,0,255,cv2.NORM_MINMAX)
Image.fromarray(gray).save(out)
print(out)
