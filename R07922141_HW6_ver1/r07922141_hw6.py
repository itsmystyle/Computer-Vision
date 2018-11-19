import cv2
import matplotlib.pyplot as plt
import numpy as np

lena_img = cv2.imread('lena.bmp', 0)

# Downsampling and binarize
downsampled_lena = [[0 for j in range(64)] for i in range(64)]

for i in range(64):
    for j in range(64):
        pixel = lena_img[i*8][j*8]
        if pixel < 128:
            downsampled_lena[i][j] = 0
        else:
            downsampled_lena[i][j] = 255

cv2.imwrite('downsmapled_binarized_lena.png', np.array(downsampled_lena))

def getPixel(x, y):
    if (x >= 0 and x < 64) and (y >= 0 and y < 64):
        return downsampled_lena[x][y]
    else:
    	return 0

def getNeighbors(x, y):
    # x7 x2 x6
    # x3 x0 x1
    # x8 x4 x5
    x7 = getPixel(x-1, y-1)
    x2 = getPixel(x, y-1)
    x6 = getPixel(x+1, y-1)
    
    x3 = getPixel(x-1, y)
    x0 = getPixel(x, y)
    x1 = getPixel(x+1, y)

    x8 = getPixel(x-1, y+1)
    x4 = getPixel(x, y+1)
    x5 = getPixel(x+1, y+1)
    return [x0, x1, x2, x3, x4, x5, x6, x7, x8]

def h(b, c, d, e):
    if b == c and (d!=b or e!=b):
        return 'q'
    elif b == c and (d==b and e==b):
        return 'r'
    elif b != c:
        return 's'

def f(lst):
    if(lst.count('r') == 4):
        return '5'
    elif(lst.count('q') == 0):
    	return ' '
    else:
        return str(lst.count('q'))

def Yokoi(lst):
    h_lst = [h(lst[0], lst[1], lst[6], lst[2]), \
    			h(lst[0], lst[2], lst[7], lst[3]), \
    			h(lst[0], lst[3], lst[8], lst[4]), \
    			h(lst[0], lst[4], lst[5], lst[1])]
    return f(h_lst)

yokoi_lena = [[' ' for j in range(64)] for i in range(64)]

for i in range(64):
    for j in range(64):
        if downsampled_lena[i][j] != 0:
            yokoi_lena[i][j] = Yokoi(getNeighbors(i, j))

with open('yokoi_lena.txt', 'w') as fout:
    for i in range(64):
        for j in range(64):
            fout.write(yokoi_lena[i][j])
        if i != 63:
        	fout.write('\n')