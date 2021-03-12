##各種機能
#import shanten_check
import shanten_check_new
import copy
import numpy as np
import tensu_calc
import teyaku_check

shanten_normal = 0
toitsu_suu = 0 #トイツ数
koutsu_suu = 0 #コーツ数
shuntsu_suu = 0 #シュンツ数
taatsu_suu = 0 #ターツ数
mentsu_suu = 0 #メンツ数
syanten_temp = 0 #シャンテン数
syanten_normal = 8 #シャンテン数

kanzen_koutsu_suu = 0 #完全コーツ数
kanzen_shuntsu_suu = 0 #完全シュンツ数
kanzen_Koritsu_suu = 0 #完全孤立牌数

#すべてのアガリ牌についてダマでロンアガリできるか
#オーラスのリーチ判断用
#すべてでロンアガリできない→0
#すべてでロンアガリできる→meanを返す
def dama_hantei(janshi, taku, kiruhai):
    temp_janshi = copy.deepcopy(janshi)
    temp_janshi.tehai.remove(kiruhai)
    yuukouhai_list = find_yuukouhai(temp_janshi, 0, taku.hash_table)
    vertual_yama_index_list = tehai_convert(temp_janshi.vertual_yama)
    for i in yuukouhai_list:
        if vertual_yama_index_list[i] == 0:
            yuukouhai_list.remove(i)
    count = 0
    point_sum = 0
    for i in yuukouhai_list:
        hai_str = hai_convert_reverse(i)
        #print(hai_str)
        #print(temp_janshi.tehai)
        #temp_janshi.tehai = ["1m", "2m", "3m", "3m", "3m", "5z", "5z", "5z", "1s", "2s", "3s", "6s", "7s"]
        temp_point = tensu_calc.tensu_calc(temp_janshi, taku, hai_str)
        #print(teyaku_check.teyaku_check(temp_janshi, taku, hai_str))
        #print(temp_point)
        #一つでもダマアガリできない牌があれば0を返す
        if len(temp_point) == 0:
            return 0
        count += vertual_yama_index_list[i]
        point_sum += temp_point[0]*vertual_yama_index_list[i]
    point_mean = point_sum/(float(count)+0.001) #バグ防止
    #本場供託を追加
    point_mean = point_mean + taku.kaze_honba[1] * 300 + taku.kyoutaku_tensuu
    return point_mean



def find_yuukou_sutehai(janshi, old_shanten_suu, hash_table):
    yuukou_sutehai_index_list = []
    tehai = function.tehai_convert(janshi.tehai)
    for i in range(len(tehai)):
        if tehai[i] != 0:
            temp_janshi = copy.deepcopy(janshi)
            temp_tehai = tehai.copy()
            temp_tehai[i] -=1
            temp_janshi.tehai = function.tehai_convert_reverse(temp_tehai)
            if shanten_check_new.shanten_check(temp_janshi, hash_table) == old_shanten_suu:
                yuukou_sutehai_index_list.append(i)
    #普通の5があるときは赤5を切らない
    if 0 in yuukou_sutehai_index_list and 5 in yuukou_sutehai_index_list:
        yuukou_sutehai_index_list.remove(0)
    if 10 in yuukou_sutehai_index_list and 15 in yuukou_sutehai_index_list:
        yuukou_sutehai_index_list.remove(10)
    if 20 in yuukou_sutehai_index_list and 25 in yuukou_sutehai_index_list:
        yuukou_sutehai_index_list.remove(20)
    return yuukou_sutehai_index_list



#リーチ判定用。フリテンかどうかを判定する。
def furiten_hantei(janshi, taku):
    assert shanten_check_new.shanten_check(janshi, taku.hash_table) == 0
    sutehai_index = tehai_convert3(akadora_convert(janshi.sutehai)[0])
    yuukouhai_index = find_yuukouhai(janshi, 0, taku.hash_table)
    for i in range(len(yuukouhai_index)):
        if yuukouhai_index[i] in sutehai_index:
            return True
    return False
    

#赤ドラ入り(5M,5P,5S)の手牌ｓｔｒを赤ドラなしの手牌strに変換
def akadora_convert(tehai_str_akadora):
    akadora_maisuu = 0
    temp_tehai = tehai_str_akadora.copy()
    for i in range(len(tehai_str_akadora)):
        if tehai_str_akadora[i] == "5M":
            akadora_maisuu += 1
            temp_tehai[i] = "5m"
        elif tehai_str_akadora[i] == "5P":
            akadora_maisuu += 1
            temp_tehai[i] = "5p"
        elif tehai_str_akadora[i] == "5S":
            akadora_maisuu += 1
            temp_tehai[i] = "5s"
            
    return [temp_tehai ,akadora_maisuu]

def akadora_convert2(tehai_akadora):
    akadora_maisuu = 0
    temp_tehai = tehai_akadora.copy()
    if tehai_akadora[0] == 1:
        akadora_maisuu += 1
        temp_tehai[0] = 0
        temp_tehai[5] += 1
    if tehai_akadora[10] == 1:
        akadora_maisuu += 1
        temp_tehai[10] = 0
        temp_tehai[15] += 1
    if tehai_akadora[20] == 1:
        akadora_maisuu += 1
        temp_tehai[20] = 0
        temp_tehai[25] += 1
    return [temp_tehai, akadora_maisuu]

def akadora_convert3(tehai_akadora):
    akadora_maisuu = 0
    temp_tehai = tehai_akadora.copy()
    for i in range(len(temp_tehai)):
        if tehai_akadora[i] == 0:
            temp_tehai.remove(0)
            temp_tehai.append(5)
            akadora_maisuu += 1
        elif tehai_akadora[i] == 10:
            temp_tehai.remove(10)
            temp_tehai.append(15)
            akadora_maisuu += 1
        elif tehai_akadora[i] == 20:
            temp_tehai.remove(20)
            temp_tehai.append(25)
            akadora_maisuu += 1
    return temp_tehai, akadora_maisuu
        

def akadora_hai_convert(hai_akadora):
    #akadora = False
    if hai_akadora == "5M":
        #akadora = True
        hai = "5m"
    elif hai_akadora == "5P":
        #akadora = True
        hai = "5p"
    elif hai_akadora == "5S":
        #akadora = True
        hai = "5s"
    else:
        hai = hai_akadora
    return hai

def akadora_hai_convert2(hai_index):
    if hai_index%10 == 0:
        hai_index += 5
    return hai_index

def akadora_hai_convert_reverse(hai_index):
    if hai_index == 0:
        return "5M"
    if hai_index == 10:
        return "5P"
    if hai_index == 20:
        return "5S"
            

#13-3n枚の手牌を受け取って有効牌の枚数を返す
def calc_yuukouhai_maisuu(janshi, old_shanten_suu, hash_table):
    yama = tehai_convert(janshi.vertual_yama)
    yuukouhai_index_list = find_yuukouhai(janshi, old_shanten_suu, hash_table)
    yuukouhai_maisuu = 0
    for i in yuukouhai_index_list:
        yuukouhai_maisuu += yama[i]
    return yuukouhai_maisuu
    
#calc_yuukouhai_maisuu用
def find_yuukouhai(janshi, old_shanten_suu, hash_table):
    yuukouhai_index_list = []
    tehai = tehai_convert(janshi.tehai)
    for i in range(len(tehai)):
        if tehai[i] < 4 and i != 30:
            temp_janshi = copy.deepcopy(janshi)
            temp_tehai = tehai.copy()
            temp_tehai[i] += 1
            temp_janshi.tehai = tehai_convert_reverse(temp_tehai)
            if shanten_check_new.shanten_check(temp_janshi, hash_table) < old_shanten_suu:
                yuukouhai_index_list.append(i)
    return yuukouhai_index_list

def riipai(tehai_str):

    tehai_str = sorted(tehai_str)
    manzu = [s for s in tehai_str if 'm' in s]
    pinzu = [s for s in tehai_str if 'p' in s]
    souzu = [s for s in tehai_str if 's' in s]
    zihai = [s for s in tehai_str if 'z' in s]
    tehai = manzu + pinzu + souzu + zihai
    return tehai


def agari_hantei(tehai_str):
    global mentsu_suu
    if len(tehai_str) == 38:
        temp_tehai = tehai_str.copy()
    else:
        temp_tehai = tehai_convert(tehai_str)
    for i in range(1, 30):
        if temp_tehai[i] == 1 and temp_tehai[i-1] == 0 and temp_tehai[i+1] == 0:
            return False
    for i in range(31, 38):
        if temp_tehai[i] == 1:
            return False
    
    for i in range(0, 38):
        if temp_tehai[i] >= 2:
            mentsu_suu = 0
            temp_tehai[i] -= 2
            for j in range(31,38):
                if temp_tehai[j] >= 3:
                    mentsu_suu += 1
            if mentsu_cut2(temp_tehai, 1):
                return True
            temp_tehai[i] += 2   
    return False

def tenpai_hantei(tehai_str):
    temp_tehai = tehai_convert(tehai_str)
    for i in range(38):
        if i%10 != 0:
            temp_tehai[i] += 1
            if agari_hantei(temp_tehai):
                return True
            else:
                temp_tehai[i] -= 1
    
    return False
            
def find_machihai(janshi, hash_table):
    
    machihai = []
    for i in range(38): 
        if i != 30:
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.tehai.append(hai_convert_reverse(i))
            #print(temp_janshi.tehai)
            
            if shanten_check_new.shanten_check(temp_janshi, hash_table) == -1:
                machihai.append(i)                          
    
    return tehai_convert_reverse2(machihai)
           
#手牌を[0,1,2,0,3,0,0,0,1...]で返す
def tehai_convert(tehai_str):
    
    tehai = [0]*38
    str_to_num = {"5M":0, "5P":10, "5S":20, "1m":1, "2m":2, "3m":3, "4m":4, "5m":5, "6m":6, "7m":7, "8m":8, "9m":9, "1p":11, "2p":12, "3p":13, "4p":14, "5p":15, "6p":16, "7p":17, "8p":18, "9p":19, "1s":21, "2s":22, "3s":23, "4s":24, "5s":25, "6s":26, "7s":27, "8s":28, "9s":29, "1z":31, "2z":32, "3z":33, "4z":34, "5z":35, "6z":36, "7z":37}
    
    for i in range(0,len(tehai_str)):
        tehai[str_to_num[tehai_str[i]]] += 1
        
    return tehai

#手牌を[1, 3, 7, 12, 17, 26, 26...]で返す
def tehai_convert2(tehai_str):
    temp_tehai = [0]*len(tehai_str)
    str_to_num = {"5M":0, "5P":10, "5S":20, "1m":1, "2m":2, "3m":3, "4m":4, "5m":5, "6m":6, "7m":7, "8m":8, "9m":9, "1p":11, "2p":12, "3p":13, "4p":14, "5p":15, "6p":16, "7p":17, "8p":18, "9p":19, "1s":21, "2s":22, "3s":23, "4s":24, "5s":25, "6s":26, "7s":27, "8s":28, "9s":29, "1z":31, "2z":32, "3z":33, "4z":34, "5z":35, "6z":36, "7z":37}
    for i in range(len(tehai_str)):
        temp_tehai[i] = str_to_num[tehai_str[i]]
    return temp_tehai

#tehai_convert2の被りなし版
def tehai_convert3(tehai_str):
    temp_tehai = []
    str_to_num = {"5M":0, "5P":10, "5S":20, "1m":1, "2m":2, "3m":3, "4m":4, "5m":5, "6m":6, "7m":7, "8m":8, "9m":9, "1p":11, "2p":12, "3p":13, "4p":14, "5p":15, "6p":16, "7p":17, "8p":18, "9p":19, "1s":21, "2s":22, "3s":23, "4s":24, "5s":25, "6s":26, "7s":27, "8s":28, "9s":29, "1z":31, "2z":32, "3z":33, "4z":34, "5z":35, "6z":36, "7z":37}
    for i in range(len(tehai_str)):
        hai = str_to_num[tehai_str[i]]
        if not (hai in temp_tehai):
            temp_tehai.append(hai)
    return temp_tehai
    
#[0,1,2,0,3,0,0,0,1...]型を受け取ってstr型で返す
def tehai_convert_reverse(tehai):
    num_to_str = {0:"5M", 10:"5P", 20:"5S", 1:"1m", 2:"2m", 3:"3m", 4:"4m", 5:"5m", 6:"6m", 7:"7m", 8:"8m", 9:"9m", 11:"1p", 12:"2p", 13:"3p", 14:"4p", 15:"5p", 16:"6p", 17:"7p", 18:"8p", 19:"9p", 21:"1s", 22:"2s", 23:"3s", 24:"4s", 25:"5s", 26:"6s", 27:"7s", 28:"8s", 29:"9s", 31:"1z", 32:"2z", 33:"3z", 34:"4z", 35:"5z", 36:"6z", 37:"7z"}
    tehai_str = []
    temp_tehai = tehai.copy()
    for i in range(38):
        while temp_tehai[i] > 0:
            tehai_str.append(num_to_str[i])
            temp_tehai[i] -=1
    return tehai_str  

def tehai_convert_reverse2(tehai_index_list):
    num_to_str = {0:"5M", 10:"5P", 20:"5S", 1:"1m", 2:"2m", 3:"3m", 4:"4m", 5:"5m", 6:"6m", 7:"7m", 8:"8m", 9:"9m", 11:"1p", 12:"2p", 13:"3p", 14:"4p", 15:"5p", 16:"6p", 17:"7p", 18:"8p", 19:"9p", 21:"1s", 22:"2s", 23:"3s", 24:"4s", 25:"5s", 26:"6s", 27:"7s", 28:"8s", 29:"9s", 31:"1z", 32:"2z", 33:"3z", 34:"4z", 35:"5z", 36:"6z", 37:"7z"}
    tehai_str = []
    for i in range(len(tehai_index_list)):
        tehai_str.append(num_to_str[tehai_index_list[i]])
    return tehai_str
    
    
def hai_convert(hai_str):
    str_to_num = {"5M":0, "5P":10, "5S":20, "1m":1, "2m":2, "3m":3, "4m":4, "5m":5, "6m":6, "7m":7, "8m":8, "9m":9, "1p":11, "2p":12, "3p":13, "4p":14, "5p":15, "6p":16, "7p":17, "8p":18, "9p":19, "1s":21, "2s":22, "3s":23, "4s":24, "5s":25, "6s":26, "7s":27, "8s":28, "9s":29, "1z":31, "2z":32, "3z":33, "4z":34, "5z":35, "6z":36, "7z":37}
    return str_to_num[hai_str]

def hai_convert_reverse(hai):
    num_to_str = {0:"5M", 10:"5P", 20:"5S", 1:"1m", 2:"2m", 3:"3m", 4:"4m", 5:"5m", 6:"6m", 7:"7m", 8:"8m", 9:"9m", 11:"1p", 12:"2p", 13:"3p", 14:"4p", 15:"5p", 16:"6p", 17:"7p", 18:"8p", 19:"9p", 21:"1s", 22:"2s", 23:"3s", 24:"4s", 25:"5s", 26:"6s", 27:"7s", 28:"8s", 29:"9s", 31:"1z", 32:"2z", 33:"3z", 34:"4z", 35:"5z", 36:"6z", 37:"7z"}
    return num_to_str[hai]

#[0,1..]型の手牌を受け取って牌があるところにはTrueを、ないところにはFalseを返す
def tehai_bool_convert(tehai):
    bool_tehai = [False]*38
    for i in range(len(tehai)):
        if tehai[i] >= 1:
            bool_tehai[i] = True
    return bool_tehai

def merge_tehai_and_fuurohai(janshi):
    tehai = tehai_convert(janshi.tehai)
    for i in range(len(janshi.fuurohai)):
        if janshi.fuurohai[i][0] == 1:
            if janshi.fuurohai[i][2] == 0:
                tehai[janshi.fuurohai[i][1]] += 1
                tehai[janshi.fuurohai[i][1]-1] += 1
                tehai[janshi.fuurohai[i][1]-2] += 1
            elif janshi.fuurohai[i][2] == 1:
                tehai[janshi.fuurohai[i][1]+1] += 1
                tehai[janshi.fuurohai[i][1]] += 1
                tehai[janshi.fuurohai[i][1]-1] += 1
            elif janshi.fuurohai[i][2] == 1:
                tehai[janshi.fuurohai[i][1]] += 1
                tehai[janshi.fuurohai[i][1]+1] += 1
                tehai[janshi.fuurohai[i][1]+2] += 1
        else:
            tehai[janshi.fuurohai[i][1]] += 3
    
    for i in range(len(janshi.ankan_list)):
        tehai[janshi.ankan_list[i]] += 3
    
    return tehai

#指定されたインデックスの副露牌を[0,1,...]型で返す カンは3枚計算
def fuurohai_convert_reverse(janshi, i):
    tehai = [0]*38
    if janshi.fuurohai[i][0] == 1:
        if janshi.fuurohai[i][2] == 0:
            tehai[janshi.fuurohai[i][1]] += 1
            tehai[janshi.fuurohai[i][1]-1] += 1
            tehai[janshi.fuurohai[i][1]-2] += 1
        elif janshi.fuurohai[i][2] == 1:
            tehai[janshi.fuurohai[i][1]+1] += 1
            tehai[janshi.fuurohai[i][1]] += 1
            tehai[janshi.fuurohai[i][1]-1] += 1
        elif janshi.fuurohai[i][2] == 1:
            tehai[janshi.fuurohai[i][1]] += 1
            tehai[janshi.fuurohai[i][1]+1] += 1
            tehai[janshi.fuurohai[i][1]+2] += 1
    else:
        tehai[janshi.fuurohai[i][1]] += 3
    return tehai

def ankan_convert_reverse(janshi,i):
    tehai = [0]*38
    tehai[janshi.ankan_list[i]] += 3
    return tehai

#[0,1,..]型の手牌を受け取ってその中にヤオチュウ字牌が1枚でもあったらTrueを返す
def yaochuji_hantei(tehai):
    yaochuji_list  = [1,9,11,19,21,29,31,32,33,34,35,36,37]
    for i in yaochuji_list:
        if tehai[i] >= 1:
            return True
    return False

def tanyao_sum_up(janshi):
    temp_tehai = np.array(tehai_convert(janshi.tehai))
    for i in range(len(janshi.fuurohai)):
        temp_fuurohai = np.array(fuurohai_convert_reverse(janshi, i))
        if yaochuji_hantei(temp_fuurohai):
            return 0
        temp_tehai += temp_fuurohai
        
    for i in range(len(janshi.ankan_list)):
        temp_ankan = np.array(ankan_convert_reverse(janshi, i))
        if yaochuji_hantei(temp_ankan):
            return 0
        temp_tehai += temp_ankan
        
    tanyao_sum = 0
    for i in range(len(temp_tehai)):
        if 2 <= i%10 <=8 and i <30:
            tanyao_sum += temp_tehai[i]
    return tanyao_sum

def ittsuu_sum_up(janshi, index):
    temp_tehai = tehai_convert(janshi.tehai)
    bool_tehai = np.array(tehai_bool_convert(temp_tehai))
    for i in range(len(janshi.fuurohai)):
        temp_fuurohai = np.array(tehai_bool_convert(fuurohai_convert_reverse(janshi, i)))
        if temp_fuurohai[index*10+1] and temp_fuurohai[index*10+2] and temp_fuurohai[index*10+3]:
            bool_tehai += temp_fuurohai
        elif temp_fuurohai[index*10+4] and temp_fuurohai[index*10+5] and temp_fuurohai[index*10+6]:
            bool_tehai += temp_fuurohai
        elif temp_fuurohai[index*10+7] and temp_fuurohai[index*10+8] and temp_fuurohai[index*10+9]:
            bool_tehai += temp_fuurohai    
    return sum(bool_tehai[index*10:index*10+10])

def sansyoku_sum_up(janshi, index):
    temp_tehai = tehai_convert(janshi.tehai)
    bool_tehai = np.array(tehai_bool_convert(temp_tehai))
    for i in range(len(janshi.fuurohai)):
        temp_fuurohai = np.array(tehai_bool_convert(fuurohai_convert_reverse(janshi, i)))
        for j in range(3):
            if temp_fuurohai[index+j*10] and temp_fuurohai[index+j*10 + 1] and temp_fuurohai[index+j*10 + 2]:
                bool_tehai += temp_fuurohai       
    return sum(bool_tehai[index:index+3]) + sum(bool_tehai[index+10:index+13]) + sum(bool_tehai[index+20:index+23])

def honitsu_sum_up(janshi, index):
    temp_tehai = np.array(tehai_convert(janshi.tehai))
    honitsu_sum = 0
    for i in range(len(janshi.fuurohai)):
        temp_fuurohai = np.array(fuurohai_convert_reverse(janshi, i))
        temp_tehai += temp_fuurohai
    for i in range(index*10, index*10+10):
        honitsu_sum += temp_tehai[i]
    for i in range(31,38):
        honitsu_sum += temp_tehai[i]
    return honitsu_sum

#param1→222、 param2→122or221、param3→212、param4→212(1,9含み)、param5→221 or 122(1,9含み)
def yipeko_eval(janshi, index, param1, param2, param3, param4, param5):
    if len(janshi.fuurohai) != 0:
        return 0
    index10 = index*10
    temp_tehai = tehai_convert(janshi.tehai)
    yipeko_sum = 0
    for i in range(1,8):
        if temp_tehai[index10+i] >= 2 and temp_tehai[index10+i+1] >= 2 and temp_tehai[index10+i+2] >= 2:
            yipeko_sum += param1
            temp_tehai[index10+i] -= 2
            temp_tehai[index10+i+1] -= 2
            temp_tehai[index10+i+2] -= 2
    for i in range(2,7):
        if temp_tehai[index10+i] >= 1 and temp_tehai[index10+i+1] >= 2 and temp_tehai[index10+i+2] >= 2:
            yipeko_sum += param2
            temp_tehai[index10+i] -= 1
            temp_tehai[index10+i+1] -= 2
            temp_tehai[index10+i+2] -= 2
    for i in range(2,7):
       if temp_tehai[index10+i] >= 2 and temp_tehai[index10+i+1] >= 2 and temp_tehai[index10+i+2] >= 1:
           yipeko_sum += param2
           temp_tehai[index10+i] -= 2
           temp_tehai[index10+i+1] -= 2
           temp_tehai[index10+i+2] -= 1
    for i in range(2,7):
       if temp_tehai[index10+i] >= 2 and temp_tehai[index10+i+1] >= 1 and temp_tehai[index10+i+2] >= 2:
           yipeko_sum += param3
           temp_tehai[index10+i] -= 2
           temp_tehai[index10+i+1] -= 1
           temp_tehai[index10+i+2] -= 2
    if temp_tehai[index10+1] >= 1 and temp_tehai[index10+2] >= 2 and temp_tehai[index10+3] >= 2:
            yipeko_sum += param2
            temp_tehai[index10+i] -= 1
            temp_tehai[index10+i+1] -= 2
            temp_tehai[index10+i+2] -= 2
    if temp_tehai[index10+1] >= 2 and temp_tehai[index10+2] >= 1 and temp_tehai[index10+3] >= 2:
            yipeko_sum += param4
            temp_tehai[index10+i] -= 2
            temp_tehai[index10+i+1] -= 1
            temp_tehai[index10+i+2] -= 2
    if temp_tehai[index10+1] >= 2 and temp_tehai[index10+2] >= 2 and temp_tehai[index10+3] >= 1:
            yipeko_sum += param5
            temp_tehai[index10+i] -= 2
            temp_tehai[index10+i+1] -= 2
            temp_tehai[index10+i+2] -= 1
    if temp_tehai[index10+7] >= 2 and temp_tehai[index10+8] >= 2 and temp_tehai[index10+9] >= 1:
            yipeko_sum += param2
            temp_tehai[index10+i+7] -= 2
            temp_tehai[index10+i+8] -= 2
            temp_tehai[index10+i+9] -= 1
    if temp_tehai[index10+7] >= 2 and temp_tehai[index10+8] >= 1 and temp_tehai[index10+9] >= 2:
            yipeko_sum += param4
            temp_tehai[index10+i+7] -= 2
            temp_tehai[index10+i+8] -= 1
            temp_tehai[index10+i+9] -= 2 
    if temp_tehai[index10+7] >= 1 and temp_tehai[index10+8] >= 2 and temp_tehai[index10+9] >= 2:
            yipeko_sum += param5
            temp_tehai[index10+i+7] -= 1
            temp_tehai[index10+i+8] -= 2
            temp_tehai[index10+i+9] -= 2
    #print(yipeko_sum)
    return yipeko_sum

#[1,6,2]型の副露を受け取って食い変えとなる牌のインデックスリストを返す。赤ドラ修正済み
def kuikae_convert(fuuro):
    temp_fuuro = fuuro.copy()
    kuikae_list = []
    #ポン
    if temp_fuuro[0] == 2:
        kuikae_list.append(temp_fuuro[1])
        if(temp_fuuro[1]%10 == 5) and temp_fuuro[1] < 30:
            kuikae_list.append(temp_fuuro[1]-5)
    elif temp_fuuro[0] == 1:
        if temp_fuuro[2] == 0:
            kuikae_list.append(temp_fuuro[1])
            if(temp_fuuro[1]%10 == 5):
                kuikae_list.append(temp_fuuro[1]-5)
            kuikae_list.append(temp_fuuro[1]-3)
            if((temp_fuuro[1]-3)%10 == 5):
                kuikae_list.append(temp_fuuro[1]-8)
        elif temp_fuuro[2] == 1:
            kuikae_list.append(temp_fuuro[1])
            if(temp_fuuro[1]%10 == 5):
                kuikae_list.append(temp_fuuro[1]-5)
        elif temp_fuuro[2] == 2:
            kuikae_list.append(temp_fuuro[1])
            if(temp_fuuro[1]%10 == 5):
                kuikae_list.append(temp_fuuro[1]-5)
            kuikae_list.append(temp_fuuro[1]+3)
            if((temp_fuuro[1]+3)%10 == 5):
                kuikae_list.append(temp_fuuro[1]-2)
    return kuikae_list

#以下あまり使わない    
    
def shanten_check0(tehai_str):
    
    global toitsu_suu, koutsu_suu, shuntsu_suu, taatsu_suu, mentsu_suu, syanten_temp, syanten_normal, kanzen_koutsu_suu, kanzen_shuntsu_suu, kanzen_Koritsu_suu
    
    toitsu_suu = 0 #トイツ数
    koutsu_suu = 0 #コーツ数
    shuntsu_suu = 0 #シュンツ数
    taatsu_suu = 0 #ターツ数
    mentsu_suu = 0 #メンツ数
    
    syanten_temp = 0 #シャンテン数
    syanten_normal = 8 #シャンテン数
    

    kanzen_koutsu_suu = 0 #完全コーツ数
    kanzen_shuntsu_suu = 0 #完全シュンツ数
    kanzen_Koritsu_suu = 0 #完全孤立牌数
    
    if len(tehai_str) == 38:
        temp_tehai = tehai_str.copy()
    else:
        temp_tehai = tehai_convert(tehai_str)
    
    
    ###完全コーツ抜き出し####################################
    
    #字牌
    for i in range(31,38):
        if temp_tehai[i] >= 3:
            temp_tehai[i] -= 3
            kanzen_koutsu_suu += 1
    
    #数牌
    for i in range(0, 30, 10):
        #1,2
        if temp_tehai[i+1]>=3 and temp_tehai[i+2] == 0 and temp_tehai[i+3] == 0:
            temp_tehai[i+1] -= 3
            kanzen_koutsu_suu += 1
        if temp_tehai[i+1]==0 and temp_tehai[i+2] >= 3 and temp_tehai[i+3] == 0 and temp_tehai[i+4] == 0:
            temp_tehai[i+2] -= 3
            kanzen_koutsu_suu += 1 
        
        #3~7
        for j in range(0,5):
            if temp_tehai[i+j+1] == 0 and temp_tehai[i+j+2] == 0 and temp_tehai[i+j+3] >= 3 and temp_tehai[i+j+4] == 0 and temp_tehai[i+j+5] ==0:
                temp_tehai[i+j+3] -= 3
                kanzen_koutsu_suu += 1
        
        #8,9
        if temp_tehai[i+6] == 0 and temp_tehai[i+7] == 0 and temp_tehai[i+8] >= 3 and temp_tehai[i+9] ==0:
            temp_tehai[i+8] -= 3
            kanzen_Koritsu_suu += 1
        if temp_tehai[i+7] == 0 and temp_tehai[i+8] == 0 and temp_tehai[i+9] >= 3:
            temp_tehai[i+9] -= 3
            kanzen_Koritsu_suu += 1                
            
    
    ###完全シュンツ抜き出し#####################################
    
    #2枚の時
    for i in range(0,30,10):
        #123XX
        if temp_tehai[i+1] == 2 and temp_tehai[i+2] == 2 and temp_tehai[i+3] == 2 and temp_tehai[i+4] == 0 and temp_tehai[i+5] == 0:
            temp_tehai[i+1] -=2 
            temp_tehai[i+2] -=2
            temp_tehai[i+3] -=2
            kanzen_shuntsu_suu += 2
        
        #X234XX
        if temp_tehai[i+1] == 0 and temp_tehai[i+2] == 2 and temp_tehai[i+3] == 2 and temp_tehai[i+4] == 2 and temp_tehai[i+5] == 0 and temp_tehai[i+6] == 0:
            temp_tehai[i+2] -=2 
            temp_tehai[i+3] -=2
            temp_tehai[i+4] -=2
            kanzen_shuntsu_suu += 2
        
        #XX345XX
        if temp_tehai[i+1] == 0 and temp_tehai[i+2] == 0 and temp_tehai[i+3] == 2 and temp_tehai[i+4] == 2 and temp_tehai[i+5] == 2 and temp_tehai[i+6] == 0 and temp_tehai[i+7] == 0:
            temp_tehai[i+3] -=2 
            temp_tehai[i+4] -=2
            temp_tehai[i+5] -=2
            kanzen_shuntsu_suu += 2
        
        #XX456XX
        if temp_tehai[i+2] == 0 and temp_tehai[i+3] == 0 and temp_tehai[i+4] == 2 and temp_tehai[i+5] == 2 and temp_tehai[i+6] == 2 and temp_tehai[i+7] == 0 and temp_tehai[i+8] == 0:
            temp_tehai[i+4] -=2 
            temp_tehai[i+5] -=2
            temp_tehai[i+6] -=2
            kanzen_shuntsu_suu += 2
            
        #XX567XX
        if temp_tehai[i+3] == 0 and temp_tehai[i+4] == 0 and temp_tehai[i+5] == 2 and temp_tehai[i+6] == 2 and temp_tehai[i+7] == 2 and temp_tehai[i+8] == 0 and temp_tehai[i+9] == 0:
            temp_tehai[i+5] -=2 
            temp_tehai[i+6] -=2
            temp_tehai[i+7] -=2
            kanzen_shuntsu_suu += 2
            
        #XX678X
        if temp_tehai[i+4] == 0 and temp_tehai[i+5] == 0 and temp_tehai[i+6] == 2 and temp_tehai[i+7] == 2 and temp_tehai[i+8] == 2 and temp_tehai[i+9] == 0:
            temp_tehai[i+6] -=2 
            temp_tehai[i+7] -=2
            temp_tehai[i+8] -=2
            kanzen_shuntsu_suu += 2
        
        #XX789
        if temp_tehai[i+5] == 0 and temp_tehai[i+6] == 0 and temp_tehai[i+7] == 2 and temp_tehai[i+8] == 2 and temp_tehai[i+9] == 2:
            temp_tehai[i+7] -=2 
            temp_tehai[i+8] -=2
            temp_tehai[i+9] -=2
            kanzen_shuntsu_suu += 2
            
    #1枚の時
    for i in range(0,30,10):
        #123XX
        if temp_tehai[i+1] == 1 and temp_tehai[i+2] == 1 and temp_tehai[i+3] == 1 and temp_tehai[i+4] == 0 and temp_tehai[i+5] == 0:
            temp_tehai[i+1] -=1 
            temp_tehai[i+2] -=1
            temp_tehai[i+3] -=1
            kanzen_shuntsu_suu += 1
        
        #X234XX
        if temp_tehai[i+1] == 0 and temp_tehai[i+2] == 1 and temp_tehai[i+3] == 1 and temp_tehai[i+4] == 1 and temp_tehai[i+5] == 0 and temp_tehai[i+6] == 0:
            temp_tehai[i+2] -=1 
            temp_tehai[i+3] -=1
            temp_tehai[i+4] -=1
            kanzen_shuntsu_suu += 1
        
        #XX345XX
        if temp_tehai[i+1] == 0 and temp_tehai[i+2] == 0 and temp_tehai[i+3] == 1 and temp_tehai[i+4] == 1 and temp_tehai[i+5] == 1 and temp_tehai[i+6] == 0 and temp_tehai[i+7] == 0:
            temp_tehai[i+3] -=1 
            temp_tehai[i+4] -=1
            temp_tehai[i+5] -=1
            kanzen_shuntsu_suu += 1
        
        #XX456XX
        if temp_tehai[i+2] == 0 and temp_tehai[i+3] == 0 and temp_tehai[i+4] == 1 and temp_tehai[i+5] == 1 and temp_tehai[i+6] == 1 and temp_tehai[i+7] == 0 and temp_tehai[i+8] == 0:
            temp_tehai[i+4] -=1 
            temp_tehai[i+5] -=1
            temp_tehai[i+6] -=1
            kanzen_shuntsu_suu += 1
            
        #XX567XX
        if temp_tehai[i+3] == 0 and temp_tehai[i+4] == 0 and temp_tehai[i+5] == 1 and temp_tehai[i+6] == 1 and temp_tehai[i+7] == 1 and temp_tehai[i+8] == 0 and temp_tehai[i+9] == 0:
            temp_tehai[i+5] -=1 
            temp_tehai[i+6] -=1
            temp_tehai[i+7] -=1
            kanzen_shuntsu_suu += 1
            
        #XX678X
        if temp_tehai[i+4] == 0 and temp_tehai[i+5] == 0 and temp_tehai[i+6] == 1 and temp_tehai[i+7] == 1 and temp_tehai[i+8] == 1 and temp_tehai[i+9] == 0:
            temp_tehai[i+6] -=1 
            temp_tehai[i+7] -=1
            temp_tehai[i+8] -=1
            kanzen_shuntsu_suu += 1
        
        #XX789
        if temp_tehai[i+5] == 0 and temp_tehai[i+6] == 0 and temp_tehai[i+7] == 1 and temp_tehai[i+8] == 1 and temp_tehai[i+9] == 1:
            temp_tehai[i+7] -=1 
            temp_tehai[i+8] -=1
            temp_tehai[i+9] -=1
            kanzen_shuntsu_suu += 1
    
    ###完全孤立抜き出し#######################################
    
    #字牌
    for i in range(31, 38):
        if temp_tehai[i] == 1:
            temp_tehai[i] -= 1
            kanzen_Koritsu_suu += 1
    
    #数牌
    for i in range(0, 30, 10):
        
        #1
        if temp_tehai[i+1] == 1 and temp_tehai[i+2] == 0 and temp_tehai[i+3] == 0:
            temp_tehai[i+1] -= 1
            kanzen_Koritsu_suu += 1
        
        #2
        if temp_tehai[i+1] == 0 and temp_tehai[i+2] == 1 and temp_tehai[i+3] == 0 and temp_tehai[i+4] == 0:
            temp_tehai[i+2] -= 1
            kanzen_Koritsu_suu += 1
        
        #3~7
        for j in range(0,5):
            if temp_tehai[i+j+1] == 0 and temp_tehai[i+j+2] == 0 and temp_tehai[i+j+3] == 1 and temp_tehai[i+j+4] == 0 and temp_tehai[i+j+5] == 0:
                temp_tehai[i+j+3] -= 1
                kanzen_Koritsu_suu += 1
                
        #8
        if temp_tehai[i+6] == 0 and temp_tehai[i+7] == 0 and temp_tehai[i+8] == 1 and temp_tehai[i+9] == 0:
            temp_tehai[i+8] -= 1
            kanzen_Koritsu_suu += 1
        
        #9
        if temp_tehai[i+7] == 0 and temp_tehai[i+8] == 0 and temp_tehai[i+9] == 1:
            temp_tehai[i+9] -= 1
            kanzen_Koritsu_suu += 1
    
    #メイン
    for i in range(0, 38):
        if temp_tehai[i] >= 2:
            toitsu_suu += 1
            temp_tehai[i] -= 2
            mentsu_cut1(temp_tehai, 1)
            toitsu_suu -= 1
            temp_tehai[i] += 2
    
    mentsu_cut1(temp_tehai, 1)
    
    return syanten_normal

def mentsu_cut1(temp_tehai, i): #シャンテン数用
    
    global toitsu_suu, koutsu_suu, shuntsu_suu, taatsu_suu, mentsu_suu, syanten_temp, syanten_normal, kanzen_koutsu_suu, kanzen_shuntsu_suu, kanzen_Koritsu_suu

    
    for j in range(i, 30):
        
        #コーツ抜き出し
        if temp_tehai[j] >= 3:
            koutsu_suu += 1
            temp_tehai[j] -= 3
            mentsu_cut1(temp_tehai, j)
            koutsu_suu -= 1
            temp_tehai[j] += 3
    
        #シュンツ抜き出し
        if temp_tehai[j] > 0 and temp_tehai[j+1] > 0 and temp_tehai[j+2] > 0 and j < 28:
            shuntsu_suu += 1
            temp_tehai[j] -= 1
            temp_tehai[j+1] -= 1
            temp_tehai[j+2] -= 1
            mentsu_cut1(temp_tehai, j)
            shuntsu_suu -= 1
            temp_tehai[j] += 1
            temp_tehai[j+1] += 1
            temp_tehai[j+2] += 1
           
        taatsu_cut(temp_tehai, 1)

def mentsu_cut2(temp_tehai, i): #アガリ判定用
    
    global mentsu_suu
    
    for j in range(i, 30):
        
        #コーツ抜き出し
        if temp_tehai[j] >= 3:
            mentsu_suu +=1
            #print(j,j,j)
            temp_tehai[j] -= 3
            if mentsu_cut2(temp_tehai, j):
                break
            mentsu_suu -=1
            temp_tehai[j] += 3
    
        #シュンツ抜き出し
        if temp_tehai[j] > 0 and temp_tehai[j+1] > 0 and temp_tehai[j+2] > 0 and j < 28:
            mentsu_suu += 1
            #print(j,j+1,j+2)
            temp_tehai[j] -= 1
            temp_tehai[j+1] -= 1
            temp_tehai[j+2] -= 1
            if mentsu_cut2(temp_tehai, j):
                break
            mentsu_suu -= 1
            temp_tehai[j] += 1
            temp_tehai[j+1] += 1
            temp_tehai[j+2] += 1    
            
    if mentsu_suu >= 4:
        return True
    else:
        return False

def taatsu_cut(temp_tehai, i):
    
    global toitsu_suu, koutsu_suu, shuntsu_suu, taatsu_suu, mentsu_suu, syanten_temp, syanten_normal, kanzen_koutsu_suu, kanzen_shuntsu_suu, kanzen_Koritsu_suu
    
    mentsu_suu = kanzen_koutsu_suu + koutsu_suu + kanzen_shuntsu_suu + shuntsu_suu
    
    for j in range(i, 38):
        if mentsu_suu+taatsu_suu < 4:
            #トイツ抜き出し
            if temp_tehai[j] == 2:
                taatsu_suu += 1
                temp_tehai[j] -= 2
                taatsu_cut(temp_tehai,j)
                taatsu_suu -= 1
                temp_tehai[j] += 2
                
            #リャンメン・ペンチャン抜き出し
            if j<29:
                if temp_tehai[j] > 0 and temp_tehai[j+1] > 0 and j%10<9:
                    taatsu_suu += 1
                    temp_tehai[j] -= 1
                    temp_tehai[j+1] -= 1
                    taatsu_cut(temp_tehai,j)
                    taatsu_suu -= 1
                    temp_tehai[j] += 1
                    temp_tehai[j+1] += 1
            
            #カンチャン抜き出し
            if j<28:
                if temp_tehai[j] > 0 and temp_tehai[j+1] == 0 and temp_tehai[j+2] > 0 and j%10<8:
                    taatsu_suu += 1
                    temp_tehai[j] -= 1
                    temp_tehai[j+2] -= 1
                    taatsu_cut(temp_tehai,j)
                    taatsu_suu -= 1
                    temp_tehai[j] += 1
                    temp_tehai[j+2] += 1        
                
    
    syanten_temp = 8 - mentsu_suu*2 -taatsu_suu -toitsu_suu
    if syanten_temp < syanten_normal:
        syanten_normal = syanten_temp
  
def koritsu_check(tehai_str):
    temp_tehai = tehai_convert(tehai_str)
    temp_list = []
    
    #字牌
    for i in range(31, 38):
        if temp_tehai[i] == 1:
            temp_list.append(i)
    
    #数牌
    for i in range(0, 30, 10):
        
        #1
        if temp_tehai[i+1] == 1 and temp_tehai[i+2] == 0 and temp_tehai[i+3] == 0:       
            temp_list.append(i+1)
        #2
        if temp_tehai[i+1] == 0 and temp_tehai[i+2] == 1 and temp_tehai[i+3] == 0 and temp_tehai[i+4] == 0:
            temp_list.append(i+2)
        #3~7
        for j in range(0,5):
            if temp_tehai[i+j+1] == 0 and temp_tehai[i+j+2] == 0 and temp_tehai[i+j+3] == 1 and temp_tehai[i+j+4] == 0 and temp_tehai[i+j+5] == 0:
                    temp_list.append(i+j+3)
                
        #8
        if temp_tehai[i+6] == 0 and temp_tehai[i+7] == 0 and temp_tehai[i+8] == 1 and temp_tehai[i+9] == 0:
            temp_list.append(i+8)
        
        #9
        if temp_tehai[i+7] == 0 and temp_tehai[i+8] == 0 and temp_tehai[i+9] == 1:
            temp_list.append(i+9)
            
    return temp_list

def koritsu_hantei(tehai_str): #孤立牌があればTrueなければFalseを返す
    if len(koritsu_check(tehai_str)) == 0:
        return False
    else:
        return True
    
def koritsu_hantei2(tehai_str, i): #i番目にある牌が孤立牌かどうか
    str_to_num = {"1m":1, "2m":2, "3m":3, "4m":4, "5m":5, "6m":6, "7m":7, "8m":8, "9m":9, "1p":11, "2p":12, "3p":13, "4p":14, "5p":15, "6p":16, "7p":17, "8p":18, "9p":19, "1s":21, "2s":22, "3s":23, "4s":24, "5s":25, "6s":26, "7s":27, "8s":28, "9s":29, "1z":31, "2z":32, "3z":33, "4z":34, "5z":35, "6z":36, "7z":37}
    temp_tehai = tehai_convert(tehai_str)
    current_hai = str_to_num[tehai_str[i]]
    if temp_tehai[current_hai] > 1:
        return False
    
    if current_hai > 30:
        return True
    
    if current_hai % 10 == 1 and temp_tehai[current_hai+1] == 0 and temp_tehai[current_hai+2] == 0:
        return True
    
    if current_hai % 10 == 9 and temp_tehai[current_hai-1] == 0 and temp_tehai[current_hai-2] == 0:
        return True
    
    if temp_tehai[current_hai-2] == 0 and temp_tehai[current_hai-1] == 0 and temp_tehai[current_hai+1] == 0 and temp_tehai[current_hai+2] == 0:
        return True
    
    return False

def tehai_koritsu_hantei(tehai_str): #手牌を受け取って孤立牌である牌の手牌中の番号のリストを返す
    return_list = []
    for i in range(len(tehai_str)):
        if koritsu_hantei2(tehai_str,i):
            return_list.append(i)   
    return return_list


    