from blackbox import blackboxscore
import cv2
import glob
import random
import time
import operator, collections, itertools

# print(blackboxscore(flist,(0, 150, 200),(60, 230, 255),sample=-1))
# print(blackboxscore(flist,(0, 150, 200),(60, 230, 255),sample=10))

def myoptimizer(flist):
    scores = {}

    # Establishing the bounds
    for i in range(0, 65):
        v11 = random.randint(0, 160)
        vdiff = random.randint(10, 60)
        v21 = v11 + vdiff
        for i in range(0,255,65):
            v12 = random.randint(0+i,65+i)
            s = blackboxscore(flist,(v11, v12, 0),(v21, 255, 255),sample=10)
            if s > 0:
                if s in scores.keys():
                    scores[s].append([(v11, v12, 0), (v21, 255,255)])
                else:
                    scores[s] = [[(v11, v12, 0), (v21, 255,255)]]

    smax = max([s for s in scores.keys()])
    print(smax)
    return scores[smax]

DATA_DIRECTORY = "data"
datalist = glob.glob(DATA_DIRECTORY+"/*")
for dd in datalist:
    print(dd)
    flist = glob.glob(dd+"/*")
    flist.sort()
    t = time.process_time()
    print(myoptimizer(flist))
    print(time.process_time() - t)


