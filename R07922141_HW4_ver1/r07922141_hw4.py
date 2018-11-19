import cv2
import matplotlib.pyplot as plt
import pandas as pd
import collections

lena_img = cv2.imread('lena.bmp', 0)

cv2.imshow('lena', lena_img)

bi_lena = lena_img.copy()

# binarization
for i in range(512):
	for j in range(512):
		if lena_img[i][j] < 128:
			bi_lena[i][j] = 0
		else:
			bi_lena[i][j] = 255

cv2.imshow('binary lena', bi_lena)

kernel01 = [[0,1,1,1,0], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [0,1,1,1,0]]
kernel02 = [[1,1], [0,1]]

# Get neighbour point according to given center
def get_neighbour(center, kernel):
	to_return = []
	for y in range(len(kernel)):
		for x in range(len(kernel[0])):
			if kernel[x][y] == 1:
				to_return.append([x - center[0], y - center[1]])
	return to_return

def dilation(img, kernel):
	to_return = img.copy()
	for i in range(512):
		for j in range(512):
			if img[i][j] == 255:
				for k in kernel:
					if (i+k[0] >= 0 and i+k[0] <=511) and (j+k[1] >= 0  and j+k[1] <= 511):
						to_return[i+k[0]][j+k[1]] = 255
	return to_return

dia_lena = dilation(bi_lena, get_neighbour((2,2), kernel01))
cv2.imshow('Dilation lena', dia_lena)
cv2.imwrite('dilation_lena.png', dia_lena)

def erosion(img, kernel):
	to_return = img.copy()
	for i in range(512):
		for j in range(512):
			flag = True
			for k in kernel:
				if (i+k[0] >= 0 and i+k[0] <=511) and (j+k[1] >= 0  and j+k[1] <= 511):
					if img[i+k[0]][j+k[1]] != 255:
						flag = False
						break
				else:
					flag = False
					break
			if flag:
				to_return[i][j] = 255
			else:
				to_return[i][j] = 0

	return to_return

ero_lena = erosion(bi_lena, get_neighbour((2,2), kernel01))
cv2.imshow('Erosion lena', ero_lena)
cv2.imwrite('erosion_lena.png', ero_lena)

def opening(img, kernel):
	to_return = erosion(img, kernel)
	to_return = dilation(to_return, kernel)
	return to_return

open_lena = opening(bi_lena, get_neighbour((2,2), kernel01))
cv2.imshow('Opening lena', open_lena)
cv2.imwrite('opening_lena.png', open_lena)

def closing(img, kernel):
	to_return = dilation(img, kernel)
	to_return = erosion(to_return, kernel)
	return to_return

close_lena = closing(bi_lena, get_neighbour((2,2), kernel01))
cv2.imshow('Closing lena', close_lena)
cv2.imwrite('closing_lena.png', close_lena)

def hit_miss(img, kernel_pattern):
	reversed_img = img.copy()

	for i in range(512):
		for j in range(512):
			if reversed_img[i][j] == 255:
				reversed_img[i][j] = 0
			else:
				reversed_img[i][j] = 255

	Jkernel = get_neighbour((0,1), kernel_pattern)
	Kkernel = get_neighbour((1,0), kernel_pattern)

	A = erosion(img, Jkernel)
	Ac = erosion(reversed_img, Kkernel)

	to_return = img.copy()

	for i in range(512):
		for j in range(512):
			if A[i][j] == 255 and Ac[i][j] == 255:
				to_return[i][j] = 255
			else:
				to_return[i][j] = 0

	return to_return

hit_miss_lena = hit_miss(bi_lena, kernel02)
cv2.imshow('Hit and miss lena', hit_miss_lena)
cv2.imwrite('hit_miss_lena.png', hit_miss_lena)

cv2.waitKey(0)
