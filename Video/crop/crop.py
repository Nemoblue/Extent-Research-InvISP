import cv2

img = cv2.imread("DSC03382.png")
print(img.shape)
cropped = img[256:3416, 256:5240]
cv2.imwrite("DSC03382_CROP.png", cropped)
