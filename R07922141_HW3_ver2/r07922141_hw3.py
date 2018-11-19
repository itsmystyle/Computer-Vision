import cv2
import matplotlib.pyplot as plt
import pandas as pd
import collections

lena_img = cv2.imread('lena.bmp', 0)

lena_img = lena_img//3		

cv2.imshow('lena', lena_img)
cv2.imwrite('lena_divided3.png', lena_img)

sk = {}
normal_hist_list = [0] * 256
for i in range(512):
	for j in range(512):
		normal_hist_list[lena_img[i][j]] += 1
		if lena_img[i][j] not in sk:
			sk[lena_img[i][j]] = 1
		else:
			sk[lena_img[i][j]] += 1

skk = {}
for i in range(256):
	if i not in skk:
		skk[i] = 0

	for j in range(i+1):
		if j not in sk:
			continue
		skk[i] += sk[j]

	skk[i] = int(255 * (skk[i] / (512*512)))

eq_lena = lena_img.copy()

his_eq_list = [0] * 256
for i in range(512):
	for j in range(512):
		eq_lena[i][j] = skk[eq_lena[i][j]]
		his_eq_list[eq_lena[i][j]] += 1

cv2.imshow('equalized lena', eq_lena)
cv2.imwrite('equalized_lena.png', eq_lena)

plt.style.use('dark_background')
plt.bar([i for i in range(256)], his_eq_list, color='white', width=1)
plt.axis('off')
plt.show()

plt.bar([i for i in range(256)], normal_hist_list, color='white', width=1)
plt.axis('off')
plt.show()

# cv2.waitKey(0)
