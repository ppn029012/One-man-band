import sys
from math import sin, cos, sqrt, pi
import cv
import urllib2

# toggle between CV_HOUGH_STANDARD and CV_HOUGH_PROBILISTIC
USE_STANDARD = False

filename = "drawing.png"
src = cv.LoadImage(filename, cv.CV_LOAD_IMAGE_GRAYSCALE)


cv.NamedWindow("Hough", 1)

dst = cv.CreateImage(cv.GetSize(src), 8, 1)
color_dst = cv.CreateImage(cv.GetSize(src), 8, 3)
storage = cv.CreateMemStorage(0)
lines = 0
cv.Canny(src, dst, 50, 200, 3)
cv.CvtColor(dst, color_dst, cv.CV_GRAY2BGR)

while True:
    dst = cv.CreateImage(cv.GetSize(src), 8, 1)
    color_dst = cv.CreateImage(cv.GetSize(src), 8, 3)
    storage = cv.CreateMemStorage(0)
    lines = 0
    cv.Canny(src, dst, 50, 200, 3)
    cv.CvtColor(dst, color_dst, cv.CV_GRAY2BGR)

    if USE_STANDARD:
        lines = cv.HoughLines2(dst, storage, cv.CV_HOUGH_STANDARD, 1, pi / 180, 100, 0, 0)
        for (rho, theta) in lines[:100]:
            a = cos(theta)
            b = sin(theta)
            x0 = a * rho 
            y0 = b * rho
            pt1 = (cv.Round(x0 + 1000*(-b)), cv.Round(y0 + 1000*(a)))
            pt2 = (cv.Round(x0 - 1000*(-b)), cv.Round(y0 - 1000*(a)))
            cv.Line(color_dst, pt1, pt2, cv.RGB(255, 0, 0), 3, 8)
    else:
        lines = cv.HoughLines2(dst, storage, cv.CV_HOUGH_PROBABILISTIC, 0.5, pi/720, 50, 50, 20)
        for line in lines:
            cv.Line(color_dst, line[0], line[1], cv.CV_RGB(255, 0, 0), 3, 8)


    cv.ShowImage("Hough", color_dst)

    k = cv.WaitKey(0)
    if k == 1048603:
        break
cv.DestroyAllWindows()
