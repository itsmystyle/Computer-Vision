import cv2
import matplotlib.pyplot as plt
import pandas as pd
import collections

lena_img = cv2.imread('lena.bmp', 0)

cv2.imshow('lena', lena_img)

kernel01 = [[1,0,0,0,1], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,1]]

# Get neighbour point according to given center
def get_neighbour(center, kernel):
	to_return = []
	for y in range(len(kernel)):
		for x in range(len(kernel[0])):
			if kernel[x][y] == 0:
				to_return.append([x - center[0], y - center[1]])
	return to_return

def dilation(img, kernel):
	to_return = img.copy()
	for i in range(512):
		for j in range(512):
			lst = []
			for k in kernel:
				if (i+k[0] >= 0 and i+k[0] <=511) and (j+k[1] >= 0  and j+k[1] <= 511):
					lst.append(img[i+k[0]][j+k[1]])
			to_return[i][j] = max(lst)
	return to_return

dia_lena = dilation(lena_img, get_neighbour((2,2), kernel01))
cv2.imshow('Dilation lena', dia_lena)
cv2.imwrite('dilation_lena.png', dia_lena)

def erosion(img, kernel):
	to_return = img.copy()
	for i in range(512):
		for j in range(512):
			lst = []
			for k in kernel:
				if (i+k[0] >= 0 and i+k[0] <=511) and (j+k[1] >= 0  and j+k[1] <= 511):
					lst.append(img[i+k[0]][j+k[1]])
			to_return[i][j] = min(lst)
	return to_return

ero_lena = erosion(lena_img, get_neighbour((2,2), kernel01))
cv2.imshow('Erosion lena', ero_lena)
cv2.imwrite('erosion_lena.png', ero_lena)

def opening(img, kernel):
	to_return = erosion(img, kernel)
	to_return = dilation(to_return, kernel)
	return to_return

open_lena = opening(lena_img, get_neighbour((2,2), kernel01))
cv2.imshow('Opening lena', open_lena)
cv2.imwrite('opening_lena.png', open_lena)

def closing(img, kernel):
	to_return = dilation(img, kernel)
	to_return = erosion(to_return, kernel)
	return to_return

close_lena = closing(lena_img, get_neighbour((2,2), kernel01))
cv2.imshow('Closing lena', close_lena)
cv2.imwrite('closing_lena.png', close_lena)

cv2.waitKey(0)
