import cv2
import random, math, copy

lena = cv2.imread('lena.bmp', 0)
cv2.imshow('lena', lena)

kernel01 = [[1,0,0,0,1], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,1]]
kernel33 = [[0,0,0],[0,0,0],[0,0,0]]
kernel55 = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

# FROM HW6 *****************************************************************************
# Get neighbour point according to given center
def get_neighbour(center, kernel):
	to_return = []
	for y in range(len(kernel)):
		for x in range(len(kernel[0])):
			if kernel[x][y] == 0:
				to_return.append([x - center[0], y - center[1]])
	return to_return

def dilation(img, kernel):
	to_return = copy.deepcopy(img)
	for i in range(512):
		for j in range(512):
			lst = []
			for k in kernel:
				if (i+k[0] >= 0 and i+k[0] <= 511) and (j+k[1] >= 0  and j+k[1] <= 511):
					lst.append(img[i+k[0]][j+k[1]])
			to_return[i][j] = max(lst)
	return to_return

def erosion(img, kernel):
	to_return = copy.deepcopy(img)
	for i in range(512):
		for j in range(512):
			lst = []
			for k in kernel:
				if (i+k[0] >= 0 and i+k[0] <= 511) and (j+k[1] >= 0  and j+k[1] <= 511):
					lst.append(img[i+k[0]][j+k[1]])
			to_return[i][j] = min(lst)
	return to_return

def opening(img, kernel):
	to_return = erosion(img, kernel)
	to_return = dilation(to_return, kernel)
	return to_return

def closing(img, kernel):
	to_return = dilation(img, kernel)
	to_return = erosion(to_return, kernel)
	return to_return

# END FROM HW6 **************************************************************************

def GaussianNoise(image, amplitude):
	noise_lena = copy.deepcopy(image)

	for i in range(512):
		for j in range(512):
			noise = image[i][j] + amplitude*random.gauss(0,1)
			noise_lena[i][j] = max(0, min(255, int(noise)))

	return noise_lena

def SaltAndPepperNoise(image, probability):
	noise_lena = copy.deepcopy(image)

	for i in range(512):
		for j in range(512):
			r = random.uniform(0, 1)
			if r < probability:
				noise_lena[i][j] = 0
			elif r > 1 - probability:
				noise_lena[i][j] = 255

	return noise_lena

def BoxFilter(image, kernel):
	filtered_lena = copy.deepcopy(image)

	if kernel == (3, 3):
		k = get_neighbour((1, 1), kernel33)
	else:
		k = get_neighbour((2, 2), kernel55)

	for i in range(512):
		for j in range(512):
			lst = []
			for t in k:
				if (i+t[0] >= 0 and i+t[0] <= 511) and (j+t[1] >= 0  and j+t[1] <= 511):
					lst.append(image[i+t[0]][j+t[1]])

			filtered_lena[i][j] = int(sum(lst)/len(lst))

	return filtered_lena

def MedianFilter(image, kernel):
	filtered_lena = copy.deepcopy(image)

	if kernel == (3, 3):
		k = get_neighbour((1, 1), kernel33)
	else:
		k = get_neighbour((2, 2), kernel55)

	for i in range(512):
		for j in range(512):
			lst = []
			for t in k:
				if (i+t[0] >= 0 and i+t[0] <= 511) and (j+t[1] >= 0  and j+t[1] <= 511):
					lst.append(image[i+t[0]][j+t[1]])

			# median
			med = int(len(lst)/2)
			lst.sort()
			if len(lst) % 2 == 0:
				tmp = int((int(lst[med-1]) + int(lst[med]))/2)
			else:
				tmp = lst[med]

			filtered_lena[i][j] = tmp

	return filtered_lena	

def getSNR(image, noise_image):
	total = float(512**2)

	# calculate mean
	m1, m2 = 0.0, 0.0
	for i in range(512):
		for j in range(512):
			m1 += float(image[i][j])
			m2 += float(noise_image[i][j]) - float(image[i][j])
	m1 /= total
	m2 /= total

	# calculate variance
	v1, v2 = 0.0, 0.0
	for i in range(512):
		for j in range(512):
			v1 += (float(image[i][j]) - m1)**2
			v2 += (float(noise_image[i][j]) - float(image[i][j]) - m2)**2
	v1 /= total
	v2 /= total

	return 20 * math.log(math.sqrt(v1)/math.sqrt(v2), 10)

SNR = []

# Gaussian
gn10 = GaussianNoise(lena, 10)
gn30 = GaussianNoise(lena, 30)
# cv2.imshow('Gaussian Noise Lena, 10', gn10)
cv2.imwrite('gn_lena_10.png', gn10)
# cv2.imshow('Gaussian Noise Lena, 30', gn30)
cv2.imwrite('gn_lena_30.png', gn30)

SNR.append(('Gaussian noise, 10:', getSNR(lena, gn10)))
SNR.append(('Gaussian noise, 30:', getSNR(lena, gn30)))

# Gausasian box 3x3
box_3_gn10 = BoxFilter(gn10, (3, 3))
box_3_gn30 = BoxFilter(gn30, (3, 3))
# cv2.imshow('Box filter, 3x3, Gaussian Noise Lena, 10', box_3_gn10)
cv2.imwrite('gn_lena_10_b3.png', box_3_gn10)
# cv2.imshow('Box filter, 3x3, Gaussian Noise Lena, 30', box_3_gn30)
cv2.imwrite('gn_lena_30_b3.png', box_3_gn30)

SNR.append(('Gaussian noise, 10, box 3x3:', getSNR(lena, box_3_gn10)))
SNR.append(('Gaussian noise, 30, box 3x3:', getSNR(lena, box_3_gn30)))

# Gaussian box 5x5
box_5_gn10 = BoxFilter(gn10, (5, 5))
box_5_gn30 = BoxFilter(gn30, (5, 5))
# cv2.imshow('Box filter, 5x5, Gaussian Noise Lena, 10', box_5_gn10)
cv2.imwrite('gn_lena_10_b5.png', box_5_gn10)
# cv2.imshow('Box filter, 5x5, Gaussian Noise Lena, 30', box_5_gn30)
cv2.imwrite('gn_lena_30_b5.png', box_5_gn30)

SNR.append(('Gaussian noise, 10, box 5x5:', getSNR(lena, box_5_gn10)))
SNR.append(('Gaussian noise, 30, box 5x5:', getSNR(lena, box_5_gn30)))

# Gausasian median 3x3
med_3_gn10 = MedianFilter(gn10, (3, 3))
med_3_gn30 = MedianFilter(gn30, (3, 3))
# cv2.imshow('Median filter, 3x3, Gaussian Noise Lena, 10', med_3_gn10)
cv2.imwrite('gn_lena_10_m3.png', med_3_gn10)
# cv2.imshow('Median filter, 3x3, Gaussian Noise Lena, 30', med_3_gn10)
cv2.imwrite('gn_lena_30_m3.png', med_3_gn30)

SNR.append(('Gaussian noise, 10, median 3x3:', getSNR(lena, med_3_gn10)))
SNR.append(('Gaussian noise, 30, median 3x3:', getSNR(lena, med_3_gn30)))

# Gausasian median 5x5
med_5_gn10 = MedianFilter(gn10, (5, 5))
med_5_gn30 = MedianFilter(gn30, (5, 5))
# cv2.imshow('Median filter, 5x5, Gaussian Noise Lena, 10', med_5_gn10)
cv2.imwrite('gn_lena_10_m5.png', med_5_gn10)
# cv2.imshow('Median filter, 5x5, Gaussian Noise Lena, 30', med_5_gn10)
cv2.imwrite('gn_lena_30_m5.png', med_5_gn30)

SNR.append(('Gaussian noise, 10, median 5x5:', getSNR(lena, med_5_gn10)))
SNR.append(('Gaussian noise, 30, median 5x5:', getSNR(lena, med_5_gn30)))

# Salt and Pepper
sapn005 = SaltAndPepperNoise(lena, 0.05)
sapn01 = SaltAndPepperNoise(lena, 0.1)
# cv2.imshow('Salt and Pepper Noise Lena, 0.05', sapn005)
cv2.imwrite('sapn_lena_005.png', sapn005)
# cv2.imshow('Salt and Pepper Noise Lena, 0.1', sapn01)
cv2.imwrite('sapn_lena_01.png', sapn01)

SNR.append(('Salt and Pepper noise, 0.05:', getSNR(lena, sapn005)))
SNR.append(('Salt and Pepper noise, 0.1:', getSNR(lena, sapn01)))

# Salt and Pepper box 3x3
box_3_sapn005 = BoxFilter(sapn005, (3, 3))
box_3_sapn01 = BoxFilter(sapn01, (3, 3))
cv2.imwrite('sapn_lena_005_b3.png', box_3_sapn005)
cv2.imwrite('sapn_lena_01_b3.png', box_3_sapn01)

SNR.append(('Salt and Pepper noise, 0.05, box 3x3:', getSNR(lena, box_3_sapn005)))
SNR.append(('Salt and Pepper noise, 0.1, box 3x3:', getSNR(lena, box_3_sapn01)))

# Salt and Pepper box 5x5
box_5_sapn005 = BoxFilter(sapn005, (5, 5))
box_5_sapn01 = BoxFilter(sapn01, (5, 5))
cv2.imwrite('sapn_lena_005_b5.png', box_5_sapn005)
cv2.imwrite('sapn_lena_01_b5.png', box_5_sapn01)

SNR.append(('Salt and Pepper noise, 0.05, box 5x5:', getSNR(lena, box_5_sapn005)))
SNR.append(('Salt and Pepper noise, 0.1, box 5x5:', getSNR(lena, box_5_sapn01)))

# Salt and Pepper median 3x3
med_3_sapn005 = MedianFilter(sapn005, (3, 3))
med_3_sapn01 = MedianFilter(sapn01, (3, 3))
cv2.imwrite('sapn_lena_005_m3.png', med_3_sapn005)
cv2.imwrite('sapn_lena_01_m3.png', med_3_sapn01)

SNR.append(('Salt and Pepper noise, 0.05, median 3x3:', getSNR(lena, med_3_sapn005)))
SNR.append(('Salt and Pepper noise, 0.1, median 3x3:', getSNR(lena, med_3_sapn01)))

# Salt and Pepper median 5x5
med_5_sapn005 = MedianFilter(sapn005, (5, 5))
med_5_sapn01 = MedianFilter(sapn01, (5, 5))
cv2.imwrite('sapn_lena_005_m5.png', med_5_sapn005)
cv2.imwrite('sapn_lena_01_m5.png', med_5_sapn01)

SNR.append(('Salt and Pepper noise, 0.05, median 5x5:', getSNR(lena, med_5_sapn005)))
SNR.append(('Salt and Pepper noise, 0.1, median 5x5:', getSNR(lena, med_5_sapn01)))

# Closing and Opening
gn10_co = opening(closing(gn10, get_neighbour((2,2), kernel01)), get_neighbour((2,2), kernel01))
gn30_co = opening(closing(gn30, get_neighbour((2,2), kernel01)), get_neighbour((2,2), kernel01))
sapn005_co = opening(closing(sapn005, get_neighbour((2,2), kernel01)), get_neighbour((2,2), kernel01))
sapn01_co = opening(closing(sapn01, get_neighbour((2,2), kernel01)), get_neighbour((2,2), kernel01))
cv2.imwrite('gn_lena_10_co.png', gn10_co)
cv2.imwrite('gn_lena_30_co.png', gn30_co)
cv2.imwrite('sapn_lena_005_co.png', sapn005_co)
cv2.imwrite('sapn_lena_01_co.png', sapn01_co)

SNR.append(('Gaussian noise, 10, Close then Open:', getSNR(lena, gn10_co)))
SNR.append(('Gaussian noise, 30, Close then Open:', getSNR(lena, gn30_co)))
SNR.append(('Salt and Pepper noise, 0.05, Close then Open:', getSNR(lena, sapn005_co)))
SNR.append(('Salt and Pepper noise, 0.1, Close then Open:', getSNR(lena, sapn01_co)))

# Opening and Closing
gn10_oc = closing(opening(gn10, get_neighbour((2,2), kernel01)), get_neighbour((2,2), kernel01))
gn30_oc = closing(opening(gn30, get_neighbour((2,2), kernel01)), get_neighbour((2,2), kernel01))
sapn005_oc = closing(opening(sapn005, get_neighbour((2,2), kernel01)), get_neighbour((2,2), kernel01))
sapn01_oc = closing(opening(sapn01, get_neighbour((2,2), kernel01)), get_neighbour((2,2), kernel01))
cv2.imwrite('gn_lena_10_oc.png', gn10_oc)
cv2.imwrite('gn_lena_30_oc.png', gn30_oc)
cv2.imwrite('sapn_lena_005_oc.png', sapn005_oc)
cv2.imwrite('sapn_lena_01_oc.png', sapn01_oc)

SNR.append(('Gaussian noise, 10, Open then Close:', getSNR(lena, gn10_oc)))
SNR.append(('Gaussian noise, 30, Open then Close:', getSNR(lena, gn30_oc)))
SNR.append(('Salt and Pepper noise, 0.05, Open then Close:', getSNR(lena, sapn005_oc)))
SNR.append(('Salt and Pepper noise, 0.1, Open then Close:', getSNR(lena, sapn01_oc)))

with open('SNR.txt', 'w') as fout:
	for i in SNR:
		s = i[0] + ' ' + str(i[1]) + '\n'
		fout.write(s)
# cv2.waitKey(0)