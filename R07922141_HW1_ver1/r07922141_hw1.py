import cv2

lena_img = cv2.imread('lena.bmp')

cv2.imshow('lena', lena_img)

## Part 1
def up_down(lena):
	length = len(lena)
	to_return = lena.copy()
	for i in range(0, length):
		to_return[:, i, :] = lena[::-1, i, :]
		

	return to_return

def left_right(lena):
	length = len(lena)
	to_return = lena.copy()
	for i in range(0, length):
		to_return[i, :, :] = lena[i, ::-1, :]

	return to_return

def diagonal(lena):
	length = len(lena_img)
	to_return = lena_img.copy()
	for i in range(0, length):
		for j in range(0,  length):
			if i == j:
				to_return[ i, :j, :] = lena_img[ :i, j, :]

	return to_return

# up_down_lena = lena_img[::-1, :, :]
up_down_lena = up_down(lena_img)
cv2.imshow('up_down_lena', up_down_lena)
cv2.imwrite('up_down_lena.jpg',up_down_lena)

# left_right_lena = lena_img[:, ::-1, :]
left_right_lena = left_right(lena_img)
cv2.imshow('left_right_lena', left_right_lena)
cv2.imwrite('left_right_lena.jpg',left_right_lena)

diagonal_lena = diagonal(lena_img)
cv2.imshow('diagonal_lena', diagonal_lena)
cv2.imwrite('diagonal_lena.jpg',diagonal_lena)

cv2.waitKey(0)