import numpy as np
import math
import imageio #Recent update of scipy excluded imsave. So, I used imageo.
import matplotlib.pyplot as plt

imgl = imageio.imread('left.png')
imgl = imgl.astype('int64')
imgr = imageio.imread('right.png')

def compat(img1,img2,i,j,ds):
    x=pow(img1[i][j][0]-img2[i+ds][j][0],2)*(-0.5)#let sigma be 1

    return math.exp(x)

def pair_compat(ds,dt,delta):
    p=min(pow(ds-dt,2),pow(delta,2))*(-0.5)

    return math.exp(p)

def message(i,j,ds,img1,img2,delta):
    res=0
    for dt in range(1,11):
        res=res+pair_compat(ds,dt,delta)*compat(img1,img2,i,j,dt)

    return res

def marg(i,j,img1,img2,ds,delta):
    messageprod=1
    for k in range(i-1,i+2):
        for s in range(j-1,j+2):
            if k!=i and s!=j:
                messageprod = messageprod*message(k,s,ds,img1,img2,delta)

    res = compat(img1,img2,i,j,ds)*messageprod

    return res

def disparity(img1,img2,i,j,delta):
    a=np.zeros(10)
    for ds in range(1,11):
        a[ds-1] = marg(i,j,img1,img2,ds,delta)

    s=np.sum(a)
    a=a/s
    return np.max(a)  

def disp_map(img1,img2,delta):
    image=np.zeros(np.shape(img1))

    for i in range(64,192):
        for j in range(64,192):
            image[i][j][0] = disparity(img1,img2,i,j,delta)
            image[i][j][1] = image[i][j][0]
            image[i][j][2] = image[i][j][0]
            image[i][j][3] = 255
            print(i)

    return image



final = disp_map(imgl,imgr,0.01)
#print(final)
#print(imgl)
plt.imshow(final)
plt.show()
