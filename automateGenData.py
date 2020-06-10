import gdal
from PIL import Image
import cv2
import glob
import numpy as np

MAX_FEATURES = 1000
GOOD_MATCH_PERCENT = 0.30

def imageRotateCrop(temp,i,index):
    print("Rotating")
    band1 = glob.glob(temp+"**B1.TIF")
    band2 = glob.glob(temp + "**B2.TIF")
    band3 = glob.glob(temp + "**B3.TIF")
    b1 = cv2.imread(str(band1[0]), cv2.IMREAD_LOAD_GDAL)

    b2 = cv2.imread(str(band2[0]), cv2.IMREAD_LOAD_GDAL)
    b3 = cv2.imread(str(band3[0]), cv2.IMREAD_LOAD_GDAL)
    rgb = np.dstack((b3, b2, b1))
    rgbIm=Image.fromarray(rgb)
    im = rgbIm.rotate(13.4)
    p = 900
    q = 900

    area1 = (p, q, p + 6050, q + 5600)
    im = im.crop(area1)
    im.save("original_cropped"+str(i)+str(index)+".png")
    print(im.size)
    return im




def getOrigin(band):
    band1=gdal.Open(band)
    list= (str(gdal.Info(band))).split('\n')
    origin=str([s for s in list if "Origin" in s])
    x = float((origin.partition(',')[0]).partition('(')[2])
    y = float((origin.partition(',')[2]).partition(')')[0])
    return x,y

def imageCrop(im,inc_x,inc_y,num,index):


    j=0
    for x in range(0, 4400, 128):
        for y in range(0, 3900, 128):

            x=x+inc_x
            y=y+inc_y
            j = j + 1

            area = (x, y, x + 512, y + 512)
            cropped_img = im.crop(area)
            imResize = cropped_img.resize((256, 256), Image.ANTIALIAS)
            imResize.save('Dataset/testDataset/temp'+str(num)+'/landsat' + str(num) +'_'+str(index*10000+j)+ '.jpg')
for index in range(1,2,1):

    temp1=r"D:/Satellite/data/temp1/new/"+str(index)+"/"
    imageF1=imageRotateCrop(temp1,1,index)
    temp2=r"D:/Satellite/data/temp2/new/"+str(index)+"/"
    im2=imageRotateCrop(temp2,2,index)
    #newIm1=cv2.cvtColor(np.array(imageF1), cv2.COLOR_RGB2BGR)
    #newIm2=cv2.cvtColor(np.array(im2), cv2.COLOR_RGB2BGR)
    '''
    print("Aligning images ...")
    imReg, h = alignImages(newIm2, newIm1)
    im_rgb = cv2.cvtColor(imReg, cv2.COLOR_BGR2RGB)
    imageF2=Image.fromarray(im_rgb)
    imageF2.save("hi.png")
    '''
    newTemp1=str((glob.glob(temp1+"*B1.TIF"))[0])
    newTemp2=str((glob.glob(temp2+"*B1.TIF"))[0])

    temp1X,temp1Y=getOrigin(newTemp1)
    temp2X,temp2Y=getOrigin(newTemp2)
    inc_x=(temp1X-temp2X)/30
    inc_y=(temp1Y-temp2Y)/30
    imageCrop(im2, inc_x, inc_y, 2, index)
    imageCrop(imageF1,0,0,1,index)






