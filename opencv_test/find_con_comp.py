import cv, cv2
import numpy as np
fn = 'drawing.png'
im_gray = cv2.imread(fn, cv.CV_LOAD_IMAGE_GRAYSCALE)
im_gray_mat = cv.fromarray(im_gray)
im_bw = cv.CreateImage(cv.GetSize(im_gray_mat), cv.IPL_DEPTH_8U, 1);
im_bw_mat = cv.GetMat(im_bw)
threshold = 50 # 128#255# HAS NO EFFECT!?!?
cv.Threshold(im_gray_mat, im_bw_mat, threshold, 255, cv.CV_THRESH_BINARY_INV | cv.CV_THRESH_OTSU);
# cv2.imshow('', np.asarray(im_bw_mat))




current_contour = cv.FindContours(cv.CloneImage(im_bw), cv.CreateMemStorage(), cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
print len(current_contour)
largest_contour = current_contour
while True:
    current_contour = current_contour.h_next()
    if (not current_contour):
        break
    if (cv.ContourArea(current_contour) > cv.ContourArea(largest_contour)):
        largest_contour = current_contour


#cv.DrawContours(image, contours, (0,255,0), (255,0,0), 1)

moments = cv.Moments(largest_contour, 1)
center = (cv.GetSpatialMoment(moments, 1, 0)/cv.GetSpatialMoment(moments, 0, 0),cv.GetSpatialMoment(moments, 0, 1)/cv.GetSpatialMoment(moments, 0, 0))
cv.Circle(im_gray, (int(center[0]), int(center[1])), 2, (0,0,255), 2)

# show the images
print "displaying images [press any key to continue]"
cv.ShowImage('original image', im_gray)
cv.ShowImage('threshed image', im_bw)
cv.WaitKey(10000)

