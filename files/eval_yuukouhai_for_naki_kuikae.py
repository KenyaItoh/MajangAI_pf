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

#切る前の状態から始める。食い変え防止版
def new_yuukouhai_explore(shanten_suu, janshi, taku, kuikae_list):
    hash_table = taku.hash_table
    tehai = np.array(function.tehai_convert(janshi.tehai))
    yama = np.array(function.tehai_convert(function.akadora_convert(janshi.vertual_yama)[0]))
    init_shanten_suu = shanten_suu
    sum_list = [0]*len(tehai)
    hai_list = find_yuukou_sutehai(janshi, init_shanten_suu, hash_table)
    
    #hai_listからkuikae_listを削除
    temp_hai_list = hai_list.copy()
    for i in range(len(hai_list)):
        if temp_hai_list[i] in kuikae_list:
            hai_list.remove(temp_hai_list)
    
    #副露した時でアガリ役なしの場合
    if len(hai_list) == 0:
        return random.choice(range(len(janshi.tehai))), 0
    
    #バグ防止用
    for i in hai_list:
        sum_list[i] += 0.001
    
    itr = 25
    
    for j in range(itr):
        count = 1.      
        for i in hai_list:
            temp_janshi = copy.deepcopy(janshi)
            temp_tehai = tehai.copy()
            temp_yama = yama.copy()       
            temp_tehai[i] -= 1
            temp_janshi.tehai = function.tehai_convert_reverse(temp_tehai)
            a = yuukouhai_explore(temp_yama, init_shanten_suu, count, hash_table, temp_janshi, taku)
            sum_list[i] += a
    
    maximum_index_num = -1
    
    maximum_expect = np.max(sum_list)
    return_hai_str = function.hai_convert_reverse(np.argmax(sum_list))
    
    for i in range(len(janshi.tehai)):
        if janshi.tehai[i] == return_hai_str:
            maximum_index_num = i
            break
    assert maximum_index_num >= 0
    return maximum_index_num, maximum_expect

def yuukouhai_explore(yama, shanten_suu, count, hash_table, janshi, taku):
    
    yuukouhai_boost = 1.45
    
    yuukouhai_list = find_yuukouhai(janshi, shanten_suu, hash_table)
    yuukouhai_prob_list = create_yuukouhai_prob_list(yuukouhai_list, yama)
    #yuukouhai_prob_listの要素がない場合
    if len(yuukouhai_prob_list) == 0:
        yuukouhai_prob_list = yuukouhai_list
    index = random.choice(yuukouhai_prob_list)
    tehai = function.tehai_convert(janshi.tehai)
    tehai[index] += 1  
    yuukouhai_num = 0
    for i in yuukouhai_list:
        yuukouhai_num += yama[i]
    #テンパイ時に待ち牌に対してブーストを行う
    if shanten_suu == 0:
        count *= yuukouhai_num**(yuukouhai_boost)/len(yama)
    else:
        count *= yuukouhai_num/len(yama)
    yama[index] -= 1
    
    shanten_suu -= 1
    
    if shanten_suu == -1:
        agarihai_str = function.hai_convert_reverse(index)
        tehai_str = function.tehai_convert_reverse(tehai)
        temp_janshi = copy.deepcopy(janshi)
        temp_janshi.tehai =  tehai_str
        point_temp = tensu_calc.tensu_calc(temp_janshi, taku, agarihai_str)
        if len(point_temp) == 0:
            point = 0
        elif point_temp[0] == point_temp[1]:
            point  = point_temp[0]*3
        else:
            point = point_temp[0] * 2 + point_temp[1]
        return count * point
    
    temp_janshi2 = copy.deepcopy(janshi)
    temp_tehai = tehai.copy()
    temp_janshi2.tehai = function.tehai_convert_reverse(temp_tehai)
    
    yuukou_sutehai_index_list = find_yuukou_sutehai(temp_janshi2, shanten_suu, hash_table) 
    index2 = random.choice(yuukou_sutehai_index_list)
    tehai[index2] -= 1
    temp_tehai = tehai.copy()
    temp_janshi2.tehai = function.tehai_convert_reverse(temp_tehai)
    return yuukouhai_explore(yama, shanten_suu, count, hash_table, temp_janshi2, taku)

#有効牌の枚数を考慮したリストを作る。例：4m3枚、7m4枚、1s2枚→[4,4,4,7,7,7,7,21,21]
def create_yuukouhai_prob_list(yuukouhai_list, yama):
    yuukouhai_list_prob = []
    for i in yuukouhai_list:
        for j in range(int(yama[i])):
            yuukouhai_list_prob.append(i)
    return yuukouhai_list_prob

#n枚の手牌に対してシャンテン数が向上する牌のindexリストを返す
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
                
    #普通の5があるときは赤5を切らない
    if 0 in yuukou_sutehai_index_list and 5 in yuukou_sutehai_index_list:
        yuukou_sutehai_index_list.remove(0)
    if 10 in yuukou_sutehai_index_list and 15 in yuukou_sutehai_index_list:
        yuukou_sutehai_index_list.remove(10)
    if 20 in yuukou_sutehai_index_list and 25 in yuukou_sutehai_index_list:
        yuukou_sutehai_index_list.remove(20)
    return yuukou_sutehai_index_list


