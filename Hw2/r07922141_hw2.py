import cv2
import matplotlib.pyplot as plt
import pandas as pd
import collections

lena_img = cv2.imread('lena.bmp')

cv2.imshow('lena', lena_img)

## thresholding and histogram
bi_lena = lena_img.copy()

wd = hg = len(bi_lena)
clr = len(bi_lena[0][0])

his_list = [0] * 256

for i in range(wd):
	for j in range(wd):
		for k in range(clr):
			# For thresholding
			if bi_lena[i][j][k] < 128:
				bi_lena[i][j][k] = 0
			else:
				bi_lena[i][j][k] = 255

			# For histogram
			his_list[lena_img[i][j][k]] += 1

cv2.imshow('binary', bi_lena)
cv2.imwrite('binary_lena.jpg', bi_lena)

plt.style.use('dark_background')
plt.bar([i for i in range(256)], his_list, color='white', width=1)
plt.axis('off')
plt.show()

# cv2.waitKey(0)
