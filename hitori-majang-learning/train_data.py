import os,sys
sys.path.append(os.pardir + "\\files")
import majang
import random
#import modified_yuukouhai_explorer
import function
import shanten_check_new
import eval_ensemble
import numpy as np
import keras
from keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Dropout
from keras.optimizers import SGD
from keras.optimizers import Adam
from collections import deque
from tensorflow.keras.losses import categorical_crossentropy
import time
import re

class N_network:
    def __init__(self, state_size, action_size):
        self.model = Sequential()
        self.model.add(Dense(1000, activation='tanh', input_dim=state_size))
        self.model.add(Dropout(rate=0.2)) # ドロップアウト
        self.model.add(Dense(2000, activation='tanh'))
        self.model.add(Dropout(rate=0.5)) # ドロップアウト
        self.model.add(Dense(2000, activation='tanh'))   
        self.model.add(Dropout(rate=0.5)) # ドロップアウト
        self.model.add(Dense(2000, activation='tanh'))   
        self.model.add(Dropout(rate=0.5)) # ドロップアウト
        self.model.add(Dense(action_size, activation='softmax'))
        self.model.compile(loss="categorical_crossentropy", optimizer=SGD(lr=0.001),metrics=['accuracy'])

def convert(read_text):
    splitted_read_text = read_text.replace('\n','')
    #splitted_read_text = splitted_read_text.replace(' ','')
    #splitted_read_text = splitted_read_text.replace('[','')
    #splitted_read_text = splitted_read_text.replace(']','')
    #splitted_read_text = re.split("[ ]", splitted_read_text)
    splitted_read_text = list(splitted_read_text)
    #splitted_read_text.remove("")
    #print(splitted_read_text)
    for i in range(len(splitted_read_text)):
        splitted_read_text[i] = int(splitted_read_text[i])
    #count = splitted_read_text.count("")
    #for i in range(count):
    #    splitted_read_text.remove("")
    #print(splitted_read_text)
    return splitted_read_text

#2→41　3→124 4→データ型改善
main_nn = N_network(124, 38)
#main_nn.model.save_weights("v1.hdf5")
main_nn.model.load_weights("v1.hdf5")

#paths = [[os.getcwd() + "\data\inputs\inputs4.txt", os.getcwd() + "\data\\targets\\targets4.txt"],
#[os.getcwd() + "\data\inputs\inputs4-2.txt", os.getcwd() + "\data\\targets\\targets4-2.txt"],
#[os.getcwd() + "\data\inputs\inputs4-3.txt", os.getcwd() + "\data\\targets\\targets4-3.txt"],
#[os.getcwd() + "\data\inputs\inputs4-4.txt", os.getcwd() + "\data\\targets\\targets4-4.txt"]]

paths = [[os.getcwd() + "\data\inputs\inputs5-1.txt", os.getcwd() + "\data\\targets\\targets5-1.txt"],
        [os.getcwd() + "\data\inputs\inputs5-2.txt", os.getcwd() + "\data\\targets\\targets5-2.txt"],
        [os.getcwd() + "\data\inputs\inputs5-3.txt", os.getcwd() + "\data\\targets\\targets5-3.txt"],
        [os.getcwd() + "\data\inputs\inputs5-4.txt", os.getcwd() + "\data\\targets\\targets5-4.txt"],
        [os.getcwd() + "\data\inputs\inputs5-5.txt", os.getcwd() + "\data\\targets\\targets5-5.txt"],
        [os.getcwd() + "\data\inputs\inputs5-6.txt", os.getcwd() + "\data\\targets\\targets5-6.txt"],
        [os.getcwd() + "\data\inputs\inputs5-7.txt", os.getcwd() + "\data\\targets\\targets5-7.txt"],
        [os.getcwd() + "\data\inputs\inputs5-8.txt", os.getcwd() + "\data\\targets\\targets5-8.txt"]]



#path1 = os.getcwd() + "\data\inputs\inputs4.txt"
#path2 = os.getcwd() + "\data\\targets\\targets4.txt"

inputs = []
targets = []


for path in paths:
    input_file = open(path[0])
    target_file = open(path[1])

    line1 = input_file.readline()
    line1 = convert(line1)

    line2 = target_file.readline()
    line2 = convert(line2)

    #print(line1)

    #print(line)
    count2 = 0
    while line1:
        inputs.append(line1)
        targets.append(line2)
        line1=input_file.readline()
        if not line1:
            break
        line1 = convert(line1)
        line2 = target_file.readline()
        line2 = np.array(convert(line2))
        
    input_file.close()
    target_file.close()

inputs = np.array(inputs)
print(inputs)
targets = np.array(targets)    

#シャッフル
time_seed = int(time.time())
np.random.seed(time_seed)
np.random.shuffle(inputs)
np.random.seed(time_seed)
np.random.shuffle(targets)

#print(inputs)
#print(targets)
#print(len(targets))

print(len(inputs))
for j in range(30):
    print(j)
    main_nn.model.fit(inputs, targets, epochs=10, verbose=2, batch_size=100, validation_split=0.2)
    main_nn.model.save_weights("v1.hdf5")