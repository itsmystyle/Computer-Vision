import cv2
import numpy as np
import copy

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
            
cv2.imwrite('downsampled_lena.png', np.array(downsampled_lena))

def getPixel(image, x, y):
    if (x >= 0 and x < len(image)) and (y >= 0 and y < len(image)):
        return image[x][y]
    else:
        return 0

def getNeighbors(image, x, y, cc=8):
    # x7 x2 x6
    # x3 x0 x1
    # x8 x4 x5
    c = image[x][y]
    x7 = getPixel(image, x-1, y-1)
    x2 = getPixel(image, x, y-1)
    x6 = getPixel(image, x+1, y-1)
    
    x3 = getPixel(image, x-1, y)
    x0 = getPixel(image, x, y)
    x1 = getPixel(image, x+1, y)

    x8 = getPixel(image, x-1, y+1)
    x4 = getPixel(image, x, y+1)
    x5 = getPixel(image, x+1, y+1)
    
    if cc == 8:
        return [x0, x1, x2, x3, x4, x5, x6, x7, x8]
    else:
        return [x0, x1, x2, x3, x4]

# def getInteriorBorder(image, cc=4):
#     def _h(c, d):
#         return c if c == d else 'b'
    
#     def _f(c):
#         return 'b' if c == 'b' else 'i'
    
#     toReturn = copy.deepcopy(image)
    
#     for i in range(64):
#         for j in range(64):
#             neighbors = getNeighbors(image, i, j, 8)
#             a0 = neighbors[0]
#             if cc == 4:
#                 for k in range(4):
#                     a0 = _h(a0, neighbors[k+1])
#             else:
#                 for k in range(8):
#                     a0 = _h(a0, neighbors[k+1])
#             toReturn[i][j] = _f(a0)
    
#     return toReturn

def Yokoi(image, cc=4):
	def _yokoi(lst):
		def _h(b, c, d, e):
		    if b == c and (d!=b or e!=b):
		        return 'q'
		    elif b == c and (d==b and e==b):
		        return 'r'
		    elif b != c:
		        return 's'

		def _f(lst):
		    if(lst.count('r') == 4):
		        return 5
		    else:
		        return lst.count('q')

		h_lst = [_h(lst[0], lst[1], lst[6], lst[2]), \
				_h(lst[0], lst[2], lst[7], lst[3]), \
				_h(lst[0], lst[3], lst[8], lst[4]), \
				_h(lst[0], lst[4], lst[5], lst[1])]
		return _f(h_lst)

	yokoi_lena = [[' ' for j in range(64)] for i in range(64)]

	for i in range(64):
	    for j in range(64):
	        if image[i][j] != 0:
	            yokoi_lena[i][j] = _yokoi(getNeighbors(image, i, j))

	return yokoi_lena

def getPairRelationship(image, cc=4):
    def _h(a, m=1):
        return 1 if a == m else 0
    
    toReturn = copy.deepcopy(image)
    
    for i in range(64):
        for j in range(64):
            neighbors = getNeighbors(image, i, j, 8)
            delta = 1
            x0 = neighbors[0]
            c = 0
            
            if cc == 4:
                for k in range(1, 5):
                    c += _h(neighbors[k])
            else:
                for k in range(1, 9):
                    c += _h(neighbors[k])
            
            if c < delta or x0 != 1:
                toReturn[i][j] = 'q'
            elif c >= delta and x0 == 1:
                toReturn[i][j] = 'p'
    
    return toReturn

def h(b, c, d, e, cc=4):
    if cc == 4:
        return 1 if b == c and (b != d or b != e) else 0
    else:
        return 1 if b != c and (b == d or b == e) else 0

def f(a1, a2, a3, a4, x0):
    return 'g' if (a1 + a2 + a3 + a4) == 1 else x0

thinned = copy.deepcopy(downsampled_lena)
last_thinned = copy.deepcopy(thinned)
cc = 4
count = 0

while True:
    notChange = True
    
    cv2.imwrite('lena_thinning_'+str(count)+'.png', np.array(thinned))
    count += 1
    
    borderImage = Yokoi(thinned, 4)
    pairImage = getPairRelationship(borderImage, 4)
    
    for i in range(len(thinned)):
        for j in range(len(thinned[0])):
            neighbors = getNeighbors(thinned, i, j, 8)
            
            a1 = h(neighbors[0], neighbors[1], neighbors[6], neighbors[2], cc)
            a2 = h(neighbors[0], neighbors[2], neighbors[7], neighbors[3], cc)
            a3 = h(neighbors[0], neighbors[3], neighbors[8], neighbors[4], cc)
            a4 = h(neighbors[0], neighbors[4], neighbors[5], neighbors[1], cc)
            if f(a1, a2, a3, a4, thinned[i][j]) == 'g' and pairImage[i][j] == 'p' and thinned[i][j] != 0:
                thinned[i][j] = 0
                notChange = False
    
    if notChange:
        break
        
cv2.imwrite('thinned_lena.png', np.array(thinned))
cv2.imshow('Thinned lena', np.array(thinned)*255)
cv2.waitKey(0)