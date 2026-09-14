from PIL import Image, ImageOps, ImageEnhance
import cv2, numpy as np

src='/mnt/data/reet.jpeg'
out='/mnt/data/reet_profile/data/source-prepped.png'
im=cv2.imread(src)
im=cv2.resize(im,(450,800))
mask=np.zeros(im.shape[:2],np.uint8)
mask[:]=cv2.GC_BGD
# likely foreground central person
mask[15:755,45:425]=cv2.GC_PR_FGD
# strong foreground seeds: face/hair/clothes/hand approximate regions
mask[40:350,150:390]=cv2.GC_FGD
mask[200:780,40:400]=cv2.GC_PR_FGD
bgd=np.zeros((1,65),np.float64); fgd=np.zeros((1,65),np.float64)
cv2.grabCut(im,mask,None,bgd,fgd,7,cv2.GC_INIT_WITH_MASK)
fg=np.where((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD),255,0).astype('uint8')
# soften mask
fg=cv2.GaussianBlur(fg,(9,9),0)
# crop around person
rgba=cv2.cvtColor(im,cv2.COLOR_BGR2BGRA); rgba[:,:,3]=fg
white=np.full_like(rgba,255); alpha=rgba[:,:,3:4]/255.0
comp=(rgba[:,:,:3]*alpha+255*(1-alpha)).astype(np.uint8)
gray=cv2.cvtColor(comp,cv2.COLOR_BGR2GRAY)
gray=cv2.createCLAHE(clipLimit=2.2,tileGridSize=(8,8)).apply(gray)
gray=cv2.normalize(gray,None,0,255,cv2.NORM_MINMAX)
Image.fromarray(gray).save(out)
print(out)
