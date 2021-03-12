from multiprocessing import Pool
import multiprocessing as multi
import time
import numpy as np

z = 2

def f(x):
    global z
    #z = 3
    zprint()
    print(id(x))
    for i in range(1000000):
        y= x[0]+x[1]+z
    return y

def y():
    global z
    z = 1
    
def zprint():
    global z
    print("z = {}".format(z))

if __name__ ==  "__main__":
    #global z

    y()
    zprint()
    
    #print(multi.cpu_count())
    print("非並列")
    start = time.time()
    for i in range(10):
        f([i,i])
    print("time: " + str(time.time()-start))

    y()
    zprint()

    print()
    print("並列")
    start = time.time()
    p = Pool(multi.cpu_count())
    print(multi.cpu_count())
    sample_list = [[i,i] for i in range(10)]
    print(sample_list)

    y()
    zprint()
    

    print(id(sample_list))
    temp_list = np.array(p.map(f, sample_list))
    print(temp_list)
    p.close()
    print("time: " + str(time.time()-start))
    #print(np.sum(temp_list))

