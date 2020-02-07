import cv2
import imutils
import random

PI = 3.14159

def circularity(c):
    M = cv2.moments(c)
    circularity = 1/(2*PI) * M['m00']**2/(M['mu20']+M['mu02'])
    return circularity
    
def detectcircle(c):
    M = cv2.moments(c)
    denominator = (M['mu20']+M['mu02'])
    if denominator > 0:
        circularity = 1/(2*PI) * M['m00']**2/(M['mu20']+M['mu02'])
        return circularity > 0.95
    else:
        return False
    
def countcircles(img,colorLower,colorUpper,MINLENGTH=300):
    # blur to remove noise
    img = cv2.blur(img, (9,9))

    # proper color segmentation
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  
    mask = cv2.inRange(hsv, colorLower, colorUpper) 

    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    pmax = 10000
    pmin = MINLENGTH

    poss = [c for c in contours if cv2.arcLength(c,True) < pmax and cv2.arcLength(c,True) > pmin]
    poss = [c for c in poss if detectcircle(c)]

    return len(poss)

def blackboxscore(flist,colorLower,colorUpper,sample=-1):
    if sample >= 0:
        myflist = random.sample(flist,sample)
    else:
        myflist = flist
    numcircles = []

    for imfile in myflist:
        cim = cv2.imread(imfile)
        numcircles += [countcircles(cim,colorLower,colorUpper,MINLENGTH=200)]

    score = len([n for n in numcircles if n>0 and n <=2])/len(numcircles)
    return score