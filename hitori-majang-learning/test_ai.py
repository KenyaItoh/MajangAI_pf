import sys, os
sys.path.append(os.pardir+"\\files")
import function
import majang
import random
import keras
import numpy as np
from keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Dropout
from keras.optimizers import SGD
from keras.optimizers import Adam
from collections import deque
from tensorflow.keras.losses import categorical_crossentropy

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

def input_string_convert(a):
    string = ""
    for i in a:
        string = string + str(i)
    string = string + "\n"
    return string

def convert(read_text):
    splitted_read_text = read_text.replace('\n','')
    splitted_read_text = list(splitted_read_text)
    for i in range(len(splitted_read_text)):
        splitted_read_text[i] = int(splitted_read_text[i])
    return splitted_read_text

janshi = majang.Janshi_p(2)
taku = majang.Taku()

taku.kaze_honba[0] = random.randrange(8)
janshi.kaze = random.randrange(4)

input_data = ['3m',"3m","4m","4m","5m","6m","7m","7m","4m","4p","3p","5P","7z","7z"]
taku.dorahyouji = ["1m"]
janshi.tehai = input_data

input_str = []
input_str.extend(function.tehai_convert_binary(function.tehai_convert(janshi.tehai)))
input_str.extend(function.bin_convert(function.tehai_convert(taku.dorahyouji)[0],5))
input_str.extend(function.bin_convert(janshi.kaze,2))
input_str.extend(function.bin_convert(taku.kaze_honba[0],3))
input_str = input_string_convert(input_str)
print(input_str)

#2→41　3→124 4→データ型改善
main_nn = N_network(124, 38)
main_nn.model.load_weights("v1.hdf5")

x=convert(input_str)

x = np.array(x)
y = x.reshape(1,124) #重要

print("input")
print(y)
result = main_nn.model.predict(y)
print("result")
print(result)

print("AI 打："+function.hai_convert_reverse(np.argmax(result)))