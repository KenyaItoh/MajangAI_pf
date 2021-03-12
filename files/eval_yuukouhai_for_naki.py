#eval_yuukouhaiの鳴き対応版 戻り値は[index, 期待値]となる
import random
#import shanten_check
import shanten_check_new
import function
import numpy as np
#import teyaku_check
#import time
#import majang
import tensu_calc
import copy

#切る前の状態から始める
def new_yuukouhai_explore(shanten_suu, janshi, taku):
    hash_table = taku.hash_table
    tehai = np.array(function.tehai_convert(janshi.tehai))
    
    #ツモって来る牌に赤ドラは考慮しない
    yama = np.array(function.tehai_convert(function.akadora_convert(janshi.vertual_yama)[0]))    
    init_shanten_suu = shanten_suu
    #index_list = [0]*len(tehai)
    sum_list = [0]*len(tehai)
    #mean_list = [0]*len(tehai)
    hai_list = find_yuukou_sutehai(janshi, init_shanten_suu, hash_table)
    #print(hai_list)
    #副露した時でアガリ役なしの場合
    if len(hai_list) == 0:
        return random.choice(range(len(janshi.tehai))), 0
    
    #バグ防止用
    for i in hai_list:
        sum_list[i] += 0.001
    
    #print(hai_list)
    itr = 25
    
    for i in hai_list:
        for j in range(itr):
            count = 1.      
            temp_janshi = copy.deepcopy(janshi)
            temp_tehai = tehai.copy()
            temp_yama = yama.copy()       
            temp_tehai[i] -= 1
            temp_janshi.tehai = function.tehai_convert_reverse(temp_tehai)
            a = yuukouhai_explore(temp_yama, init_shanten_suu, count, hash_table, temp_janshi, taku)
            #index_list[i] += 1
            sum_list[i] += a
        sum_list[i] /= float(itr)
        

    #for i in range(len(tehai)):
    #    mean_list[i] = sum_list[i]/float(itr)
    
    maximum_index_num = -1
    #print(janshi.tehai)
    #print(np.round(sum_list,2))
    
    maximum_expect = np.max(sum_list)
    return_hai_str = function.hai_convert_reverse(np.argmax(sum_list))
    #print(return_hai_str)
    
    for i in range(len(janshi.tehai)):
        if janshi.tehai[i] == return_hai_str:
            maximum_index_num = i
            break
    #print(maximum_index_num)
    assert maximum_index_num >= 0
    return maximum_index_num, maximum_expect

def yuukouhai_explore(yama, shanten_suu, count, hash_table, janshi, taku):
    
    nokori_tsumo_kaisuu = int(taku.yama_nokori/4)+1
    yuukouhai_boost = 1.45
    shanten_const = np.sum(yama) / nokori_tsumo_kaisuu * 10
    
    yuukouhai_list = find_yuukouhai(janshi, shanten_suu, hash_table)
    yuukouhai_prob_list = create_yuukouhai_prob_list(yuukouhai_list, yama)
    #yuukouhai_prob_listの要素がない場合
    if len(yuukouhai_prob_list) == 0:
        yuukouhai_prob_list = yuukouhai_list
    index = random.choice(yuukouhai_prob_list)
    janshi.tehai.append(function.hai_convert_reverse(index))
    yuukouhai_num = 0.001
    for i in yuukouhai_list:
        yuukouhai_num += yama[i]

    #ツモって来る牌が自身の捨て牌にあれば補正
    if function.hai_convert_reverse(index) in janshi.sutehai:
        furiten_hosei = 0.25
    else:
        furiten_hosei = 1.0

    #テンパイ時に待ち牌に対してブーストを行う
    if shanten_suu == 0:
        count *= yuukouhai_num**(yuukouhai_boost)/shanten_const*furiten_hosei
    else:
        count *= yuukouhai_num/shanten_const*furiten_hosei
    yama[index] -= 1
    
    shanten_suu -= 1
    
    if shanten_suu == -1:
        agarihai_str = function.hai_convert_reverse(index)
        #tehai_str = function.tehai_convert_reverse(tehai)
        ##temp_janshi = copy.deepcopy(janshi)
        #temp_janshi.tehai =  tehai_str
        #print(tehai_str)
        #print(temp_janshi.fuurohai)
        #print(count)
        point_temp = tensu_calc.tensu_calc(janshi, taku, agarihai_str)
        if len(point_temp) == 0:
            point = 0
        elif point_temp[0] == point_temp[1]:
            point  = point_temp[0]*3
        else:
            point = point_temp[0] * 2 + point_temp[1]
        #print(point)
        return count * point
        #return count*teyaku_check.teyaku_check(janshi, taku, agarihai_str)[0]
    
    yuukou_sutehai_index_list = find_yuukou_sutehai(janshi, shanten_suu, hash_table) 
    index2 = random.choice(yuukou_sutehai_index_list)
    janshi.tehai.remove(function.hai_convert_reverse(index2))
    return yuukouhai_explore(yama, shanten_suu, count, hash_table, janshi, taku)

#有効牌の枚数を考慮したリストを作る。例：4m3枚、7m4枚、1s2枚→[4,4,4,7,7,7,7,21,21]
def create_yuukouhai_prob_list(yuukouhai_list, yama):
    yuukouhai_list_prob = []
    for i in yuukouhai_list:
        for j in range(int(yama[i])):
            yuukouhai_list_prob.append(i)
    return yuukouhai_list_prob

#n枚の手牌に対してシャンテン数が向上する牌のindexリストを返す。赤ドラは含まない
def find_yuukouhai(janshi, old_shanten_suu, hash_table):
    yuukouhai_index_list = []
    tehai = function.tehai_convert(janshi.tehai)
    for i in range(len(tehai)):
        if (i !=30) and (tehai[i] < 4):
            temp_janshi = copy.deepcopy(janshi)
            temp_tehai = tehai.copy()
            temp_tehai[i] += 1
            temp_janshi.tehai = function.tehai_convert_reverse(temp_tehai)
            if shanten_check_new.shanten_check(temp_janshi, hash_table) < old_shanten_suu:
                yuukouhai_index_list.append(i)
    return yuukouhai_index_list

#n+1枚の手牌に対してシャンテン数が悪くならないための牌のindexリストを返す
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
    
    #普通の5があるときは赤ドラ5を除外
    if 0 in yuukou_sutehai_index_list and 5 in yuukou_sutehai_index_list:
        yuukou_sutehai_index_list.remove(0)
    if 10 in yuukou_sutehai_index_list and 15 in yuukou_sutehai_index_list:
        yuukou_sutehai_index_list.remove(10)
    if 20 in yuukou_sutehai_index_list and 25 in yuukou_sutehai_index_list:
        yuukou_sutehai_index_list.remove(20)
    return yuukou_sutehai_index_list


