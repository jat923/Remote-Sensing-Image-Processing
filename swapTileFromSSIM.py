import numpy as np
import matplotlib.pyplot as plt
from SSIM_PIL import compare_ssim

import argparse
import PIL
from PIL import Image
import cv2
from skimage import data, img_as_float
from skimage.metrics import structural_similarity as ssim

from PIL import Image
from geoarray import GeoArray
from skimage.measure import compare_ssim as ssim

im1=(Image.open("landsat1_10758.TIF"))
im2=(Image.open("landsat2_10758.TIF"))


mask=np.ones((256,256,3))
#mask[64:192,64:192]=1
mask[96:160,96:160,:]=0
crop=im2.crop((96,160,96+64,160+64))

crop.save("cropped_im2.TIF")
im_list=[]



count=0
for i in range(0,256,64):
    for j in range(0, 256, 64):
        count+=1

        tempIm=im1.crop((i,j,i+64,j+64))

        tempIm.save("im_"+str(count)+"_"+str(i)+str(j)+".TIF")
        ssim = compare_ssim(tempIm, crop)
        im_list.append(ssim)
        print("for image",count,"ssim is ",ssim)
        #.bar(x, y[:, i], color=plt.cm.Paired(i / 10.))
print("max",min(im_list))