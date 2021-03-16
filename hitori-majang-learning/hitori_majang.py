import os,sys
sys.path.append(os.pardir + "\\files")
import majang
import random
import function
import shanten_check_new
import eval_ensemble
import numpy as np
import time

class Yama:
    def __init__(self):
        self.nokori_yama = ['1m', '1m', '1m', '1m', '2m', '2m', '2m', '2m', '3m', '3m', '3m', '3m', '4m', '4m', '4m', '4m', '5M', '5m', '5m', '5m', '6m', '6m', '6m', '6m', '7m', '7m', '7m', '7m', '8m', '8m', '8m', '8m', '9m', '9m', '9m', '9m', '1p', '1p', '1p', '1p', '2p', '2p', '2p', '2p', '3p', '3p', '3p', '3p', '4p', '4p', '4p', '4p', '5P', '5p', '5p', '5p', '6p', '6p', '6p', '6p', '7p', '7p', '7p', '7p', '8p', '8p', '8p', '8p', '9p', '9p', '9p', '9p', '1s', '1s', '1s', '1s', '2s', '2s', '2s', '2s', '3s', '3s', '3s', '3s', '4s', '4s', '4s', '4s', '5S', '5s', '5s', '5s', '6s', '6s', '6s', '6s', '7s', '7s', '7s', '7s', '8s', '8s', '8s', '8s', '9s', '9s', '9s', '9s','1z','1z','1z','1z','2z','2z','2z','2z','3z','3z','3z','3z','4z','4z','4z','4z', '5z', '5z', '5z', '5z', '6z', '6z', '6z', '6z', '7z', '7z', '7z', '7z']
    def reset(self):
        self.nokori_yama = ['1m', '1m', '1m', '1m', '2m', '2m', '2m', '2m', '3m', '3m', '3m', '3m', '4m', '4m', '4m', '4m', '5M', '5m', '5m', '5m', '6m', '6m', '6m', '6m', '7m', '7m', '7m', '7m', '8m', '8m', '8m', '8m', '9m', '9m', '9m', '9m', '1p', '1p', '1p', '1p', '2p', '2p', '2p', '2p', '3p', '3p', '3p', '3p', '4p', '4p', '4p', '4p', '5P', '5p', '5p', '5p', '6p', '6p', '6p', '6p', '7p', '7p', '7p', '7p', '8p', '8p', '8p', '8p', '9p', '9p', '9p', '9p', '1s', '1s', '1s', '1s', '2s', '2s', '2s', '2s', '3s', '3s', '3s', '3s', '4s', '4s', '4s', '4s', '5S', '5s', '5s', '5s', '6s', '6s', '6s', '6s', '7s', '7s', '7s', '7s', '8s', '8s', '8s', '8s', '9s', '9s', '9s', '9s','1z','1z','1z','1z','2z','2z','2z','2z','3z','3z','3z','3z','4z','4z','4z','4z', '5z', '5z', '5z', '5z', '6z', '6z', '6z', '6z', '7z', '7z', '7z', '7z']

def input_string_convert(a):
    string = ""
    for i in a:
        string = string + str(i)
    string = string + "\n"
    return string

def create_dataset(input_file_name, target_file_name):

    janshi = majang.Janshi_p(2)
    taku = majang.Taku()
    yama = Yama()

    t = str(int(time.time()))

    path1 = os.getcwd() + "\data\inputs\\" + input_file_name + ".txt"
    path2 = os.getcwd() + "\data\\targets\\" +target_file_name + ".txt"

    input_file = open(path1, "w")
    target_file = open(path2, "w")

    #create data
    for ep in range(1000):
        input_file.close()
        input_file.close()
        input_file = open(path1, "a")
        target_file = open(path2, "a")
        print()
        print("episode = " + str(ep))
        yama.reset()
        janshi.janshi_reset()
        taku.taku_reset()

        #配牌
        for _ in range(14):
            temp1 = random.randrange(len(yama.nokori_yama))
            janshi.tehai.append(yama.nokori_yama[temp1])
            del yama.nokori_yama[temp1]

        #ドラ表
        temp2 = random.randrange(len(yama.nokori_yama))
        taku.dorahyouji = [yama.nokori_yama[temp2]]
        del yama.nokori_yama[temp2]

        #仮想山更新
        janshi.init_vertual_yama(taku)
        #print("ドラ表示" + taku.dorahyouji[0])

        #風
        taku.kaze_honba[0] = random.randrange(8)
        janshi.kaze = random.randrange(4)
        
        #ゲーム開始
        for junme in range(50):
            #print(str(junme) + "巡目")
            janshi.riipai()
            #print(janshi.tehai)        
            shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)      
            taku.yama_nokori = 50
            if shanten_suu >= 0:
                temp = np.argmax(eval_ensemble.eval_tehai_point(janshi, taku)) #temp:手牌中における打牌のindex
            #elif shanten_suu == 1 or shanten_suu == 0:
            #    temp = np.argmax(eval_ensemble.new_yuukouhai_explore(shanten_suu, janshi, taku)[0])
            else:
                break
            #print("打 " + janshi.tehai[temp])

            ###inputs
            input_str = []
            input_str.extend(function.tehai_convert_binary(function.tehai_convert(janshi.tehai)))
            input_str.extend(function.bin_convert(function.tehai_convert(taku.dorahyouji)[0],5))
            input_str.extend(function.bin_convert(janshi.kaze,2))
            input_str.extend(function.bin_convert(taku.kaze_honba[0],3))
            input_str = input_string_convert(input_str)
            input_file.write(input_str)
            print(input_str)

            temp_str = janshi.tehai[temp]
            temp_list = function.tehai_convert([temp_str])
            #for i in range(14):
            #    if janshi.tehai[i] == temp_str:
            #        temp_list.append(1)
            #    else:
            #        temp_list.append(0)
            target_str = input_string_convert(temp_list)
            target_file.write(target_str)

            del janshi.tehai[temp]
            temp3 = random.randrange(len(yama.nokori_yama))
            #print("ツモ " + yama.nokori_yama[temp3])
            janshi.tehai.append(yama.nokori_yama[temp3])
            janshi.vertual_yama.remove(yama.nokori_yama[temp3])
            del yama.nokori_yama[temp3]

            if janshi.vertual_yama != yama.nokori_yama:
                print("ERROR")

    input_file.close()
    target_file.close()
