import cv2 as cv

image = cv.imread("test.jpg")

print("Imaginea a fost incarcata")
# cv.imshow('img',image)

winSize = (64,64)
blockSize = (16,16)
blockStride = (8,8)
cellSize = (8,8)

nbins = 9
derivAperture = 1
winSigma = 4.
histogramNormType = 0

L2HysThreshold = 2.0000000000000001e-01
gammaCorrection = 0
nlevels = 64

hog = cv.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,
                        histogramNormType,L2HysThreshold,gammaCorrection,nlevels)

#compute(img[, winStride[, padding[, locations]]]) -> descriptors
winStride = (8,8)
padding = (8,8)
locations = ((10,20),)
hist = hog.compute(image,winStride,padding,locations)

cv.imshow('hist',hist)
cv.waitKey(0)
cv.destroyAllWindows()
