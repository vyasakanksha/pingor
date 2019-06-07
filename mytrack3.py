#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:18:29 2019

@author: abhishekroy
"""

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
 
def detectcircle(c):
    area = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    shape = area/(peri*peri)
    return (shape > .05)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
ap.add_argument("-o","--output",
    help="output video file")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
#greenLower = (29, 86, 6)
#greenUpper = (64, 255, 255)
#----in BGR space
greenLower = (100, 100, 200)
greenUpper = (170, 255, 255)
framewidth = 600

pts = deque(maxlen=args["buffer"])
#fgbg = cv2.createBackgroundSubtractorKNN(detectShadows=False)
fgbg = cv2.createBackgroundSubtractorMOG2()

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=0).start()
 
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

OUTFLAG = False
if args.get("output",False):    
    # Define the codec and create VideoWriter object
    (width,height,fps) = int(vs.get(3)),int(vs.get(4)),vs.get(5)
    OUTFLAG = True
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    out = cv2.VideoWriter(args["output"],fourcc, fps, (width,height),True)

# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
    # grab the current frame
    frame = vs.read()
 
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
 
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break
 
    # resize the frame, blur it, and convert it to the HSV
    # color space
#    frame = imutils.resize(frame, width=framewidth)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
#    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    smallblur = cv2.GaussianBlur(frame, (3,3), 0)
    smallblur = cv2.cvtColor(smallblur,cv2.COLOR_BGR2GRAY)

    framedge = cv2.Canny(smallblur, 225, 250)
    framedge = cv2.cvtColor(framedge,cv2.COLOR_GRAY2BGR)

    hsv = blurred
    
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    # Foreground mask
    fgmask = fgbg.apply(frame)
    fgmaskcol = cv2.cvtColor(fgmask,cv2.COLOR_GRAY2RGB)

    mask = mask & fgmask
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    amax = 10000
    amin = 300
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        poss = [c for c in cnts if cv2.contourArea(c) < amax and cv2.contourArea(c) > amin]
        poss = [c for c in poss if detectcircle(c)]
        posscircs = [cv2.minEnclosingCircle(c) for c in poss]
        possmoments = [cv2.moments(c) for c in poss]
        centers = [(int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) for M in possmoments]
     
        for ((x, y), radius) in posscircs:
            cv2.circle(framedge, (int(x), int(y)), int(radius),(0, 255, 255), -1)
        for center in centers:
            cv2.circle(framedge, center, 5, (0, 0, 255), -1)

#    # find contours in the mask and initialize the current
#    # (x, y) center of the ball
#    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
#        cv2.CHAIN_APPROX_SIMPLE)
#    cnts = imutils.grab_contours(cnts)
#    center = None
# 
#    # only proceed if at least one contour was found
#    if len(cnts) > 0:
#        # find the largest contour in the mask, then use
#        # it to compute the minimum enclosing circle and
#        # centroid
#        c = max(cnts, key=cv2.contourArea)
#        ((x, y), radius) = cv2.minEnclosingCircle(c)
#        M = cv2.moments(c)
#        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
# 
#        # only proceed if the radius meets a minimum size
#        if radius > 10:
#            # draw the circle and centroid on the frame,
#            # then update the list of tracked points
#            cv2.circle(frame, (int(x), int(y)), int(radius),
#                (0, 255, 255), 2)
#            cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
    # update the points queue
#    if centers:
#        pts.appendleft(centers[0])
#    
#        # loop over the set of tracked points
#    for i in range(1, len(pts)):
#        # if either of the tracked points are None, ignore
#        # them
#        if pts[i - 1] is None or pts[i] is None:
#            continue
# 
#        # otherwise, compute the thickness of the line and
#        # draw the connecting lines
#        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
#        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
    # show the frame to our screen
    cv2.imshow("Frame", framedge)
    key = cv2.waitKey(1) & 0xFF
 
    if OUTFLAG:
        out.write(framedge)
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()
 
# otherwise, release the camera
else:
    vs.release()
 
# close all windows
cv2.destroyAllWindows()



    