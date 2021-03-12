import math

def Cal_MinDistance(loc1, loc2):
    dist_tmp = 999999
    clickPoint = None
    #a = 0
    for pt1 in zip(*loc1[::-1]):
        #a += 1
        for pt2 in zip(*loc2[::-1]):
            dist = math.sqrt(math.pow(pt1[0] - pt2[0], 2) + math.pow(pt1[1] - pt2[1], 2))
            #print("pt1 = {0}, pt2 = {1}, dist = {2}".format(pt1, pt2, dist))
            if dist < dist_tmp:
                dist_tmp = dist
                clickPoint = (pt2[0], pt2[1])
    #print(a)
    return clickPoint

# if __name__ == '__main__':
    # print(Cal_MinDistance(loc1, loc2))