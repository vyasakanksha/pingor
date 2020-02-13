import random
from blackbox import blackboxscore

def myoptimizer(flist):
    scores = {}

    for i in range(0, 65):
        # Hue range from 0 - 179
        v11 = random.randint(0, 160)
        # Typical H range of a colour is 60
        vdiff = random.randint(10, 60)
        v21 = v11 + vdiff

        # Saturation will be similar for all the pictures. Need to find the aprox range
        for i in range(0,255,65):
            v12 = random.randint(0+i,65+i)
            s = blackboxscore(flist,(v11, v12, 0),(v21, 255, 255),sample=10)
            if s > 0:
                if s in scores.keys(): # may have multiple values with the same score
                    scores[s].append([(v11, v12, 0), (v21, 255,255)])
                else:
                    scores[s] = [[(v11, v12, 0), (v21, 255,255)]]

    smax = max([s for s in scores.keys()])
    return scores[smax][0][0], scores[smax][0][1]