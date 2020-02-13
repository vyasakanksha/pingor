from blackbox import blackboxscore
import cv2
import glob
import random
import time
import operator, collections, itertools

DATA_DIRECTORY = "orangeball"

flist = glob.glob(DATA_DIRECTORY+"/*")
flist.sort()

print(blackboxscore(flist,(0, 150, 200),(60, 230, 255),sample=-1))
print(blackboxscore(flist,(0, 150, 200),(60, 230, 255),sample=10))

def myoptimizer():
    scores = {}

    # Establishing the bounds
    for i in range(0, 200):
        v11 = random.randint(0, 195)
        vdiff = random.randint(10, 60)
        v21 = v11 + vdiff
        for i in range(0,255,65):
            v12 = random.randint(0+i,65+i)
            s = blackboxscore(flist,(v11, v12, 0),(v21, 255, 255),sample=20)
            if s > 0:
                print(s, v11, v12, 0, v21, 255,255)
                if s in scores.keys():
                    scores[s].append([(v11, v12, 0), (v21, 255,255)])
                else:
                    scores[s] = [[(v11, v12, 0), (v21, 255,255)]]

    print("int", max([s for s in scores.keys()]))

    # # determining the ranges for the highest scores
    # sscores = {}
    # vmin1= []
    # vmin2 = []
    # vmax1 = []
    # for k in sorted(scores.keys(), reverse = True):
    #     sscores[k] = scores[k]

    # for k, value in sscores.items():
    #     print(k, value)
    #     for v in value:
    #         vmin1.append(v[0][0])
    #         vmin2.append(v[0][1])
    #         vmax1.append(v[1][0])
    #         if len(vmin1) > 2:
    #             break
    #     if len(vmin1) > 2:
    #         break

    # print("v1min", vmin1, min(vmin1), max(vmin1))
    # print("v2min", vmin2, min(vmin2), max(vmin2))
    # print("v1max", vmax1, min(vmax1), max(vmax1))

    # Rerunning with tighter ranges for a better score
    # for i in range(0, 70):
    #     v11 = random.randint(min(vmin1), max(vmin1))
    #     v12 = random.randint(min(vmin2), max(vmin2))
    #     v21 = random.randint(min(vmax1), max(vmax1))
    #     v11 = random.randint(3, 10)
    #     v12 = random.randint(90, 150)
    #     v21 = random.randint(25, 35)
    #     s = blackboxscore(flist,(v11, v12, 0),(v21, 255, 255),sample=20)

    #     if s > 0:
    #         print(s, v11, v12, 0, v21, 255,255)
    #         if s in scores.keys():
    #             scores[s].append([(v11, v12, 0), (v21, 255,255)])
    #         else:
    #             scores[s] = [[(v11, v12, 0), (v21, 255,255)]]


    # print("final", max([s for s in scores.keys()]))


for k in range(10):
    t = time.process_time()
    myoptimizer()
    print(time.process_time() - t)

