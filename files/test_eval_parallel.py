import evaluate
#eval_yuukouhaiの鳴き対応版 戻り値は[index, 期待値]となる
import random
#import shanten_check
import shanten_check_new
import function
import numpy as np
import teyaku_check
import time
import majang
import tensu_calc
import copy
import mentsu_count
import defense
import eval_keiten
from multiprocessing import Pool
import multiprocessing as multi

sum_list, pure_point_sum = [], []
janshi_global = None
yama_global = None
taku_global = None
shanten_suu_global = None
itr_global = None
hash_table = shanten_check_new.read_hash_table_for_shanten_check()

def new_yuukouhai_explore(shanten_suu, janshi, taku):
    #print("aaaaaaaaaaaaaaaaaaaaa")
    global sum_list, pure_point_sum
    global janshi_global, yama_global, taku_global, shanten_suu_global, itr_global
    hash_table = taku.hash_table
    tehai = np.array(function.tehai_convert(janshi.tehai))

    #ツモって来る牌に赤ドラは考慮しない
    yama = np.array(function.tehai_convert(function.akadora_convert(janshi.vertual_yama)[0]))
    init_shanten_suu = shanten_suu
    #index_list = [0]*len(tehai)
    sum_list = [0]*len(tehai)
    pure_point_sum = [0]*len(tehai)
    print(len(sum_list))
    #mean_list = [0]*len(tehai)
    if shanten_suu >= 2:
        hai_list = find_yuukou_sutehai(janshi, init_shanten_suu, hash_table)
    #テンパイならシャンテン戻しも考える
    else:
        hai_list = function.tehai_convert3(janshi.tehai)

    #print(hai_list)
    #副露した時でアガリ役なしの場合
    if len(hai_list) == 0:
        #print("no_hai_list_error")
        return [0.001]*len(janshi.tehai), [0.001]*len(janshi.tehai), [0.001]*len(janshi.tehai)

    #バグ防止用
    for i in hai_list:
        sum_list[i] += 0.001

    #print(hai_list)
    if init_shanten_suu >= 2:
        itr = 25
    elif init_shanten_suu == 1:
        itr = 20
    else:
        itr = 15
    itr_global = itr

    janshi_global = janshi
    yama_global = yama
    taku_global = taku
    taku.hash_table = None
    shanten_suu_global = shanten_suu

    temp_list = [[hai_id, janshi, yama, taku, shanten_suu, itr] for hai_id in reversed(hai_list)]
    p = Pool(multi.cpu_count())
    print(multi.cpu_count())
    print(hai_list)
    #print(time.time())
    p.starmap(temp_process, temp_list)
    #p.map(test_process, hai_list)
    p.close()

    taku.hash_table = hash_table

    for i in hai_list:
        print(i)
        for j in range(itr):
            count = 1.0
            temp_janshi = copy.deepcopy(janshi)
            #temp_tehai = tehai.copy()
            temp_yama = yama.copy()
            #temp_tehai[i] -= 1
            temp_janshi.tehai.remove(function.hai_convert_reverse(i)) # = function.tehai_convert_reverse(temp_tehai)
            temp_janshi.sutehai.append(function.hai_convert_reverse(i))
            if j == 0:
                init_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            a, b = yuukouhai_explore(temp_yama, init_shanten_suu, count, hash_table, temp_janshi, taku)
            #index_list[i] += 1
            sum_list[i] += a
            pure_point_sum[i] += b
        #shanten_suu + 1で平均打点を割る
        pure_point_sum[i] /= max(init_shanten_suu + 1, 1)*itr

def y():
    global janshi_global, yama_global, taku_global, shanten_suu_global, itr_global
    return janshi_global, yama_global, taku_global, shanten_suu_global, itr_global

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
    yuukouhai_num = 0.001 + len(yuukouhai_prob_list)

    #ツモって来る牌が自身の捨て牌にあれば補正
    if function.hai_convert_reverse(index) in janshi.sutehai:
        furiten_hosei = 0.25
    else:
        furiten_hosei = 1.0

    #テンパイ時に待ち牌に対してブーストを行う
    if shanten_suu == 0:
        count *= yuukouhai_num**(yuukouhai_boost)/shanten_const * furiten_hosei
    else:
        count *= yuukouhai_num/shanten_const * furiten_hosei

    yama[index] -= 1
    
    shanten_suu -= 1
    
    if shanten_suu == -1:
        agarihai_str = function.hai_convert_reverse(index)
        point_temp = tensu_calc.tensu_calc(janshi, taku, agarihai_str)
        if len(point_temp) == 0:
            point = 0
        elif point_temp[0] == point_temp[1]:
            point  = point_temp[0]*3
        else:
            point = point_temp[0] * 2 + point_temp[1]
        #print(point)
        #print(count*point)
        if teyaku_check.teyaku_check(janshi, taku, agarihai_str)[1] == 25:
            point *= 0.5
        return count * point, point
    
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

def test_process(i):
    for janshi1 in range(1000000):
        i = i
    print(i)
    return i

def temp_process(hai_id, janshi, yama, taku, shanten_suu, itr):
#def temp_process(temp_list):
    global hash_table
    #temp_list = y()
    #print(time.time())
    #global pure_point_sum, sum_list
    #start = time.time()
    #hai_id = temp_list[0]
    #janshi = temp_list[1]
    #yama = temp_list[2]
    #taku = temp_list[3]
    #shanten_suu = temp_list[4]
    #itr = temp_list[5]
    taku.hash_table = hash_table
    itr = 50
    print(hai_id)
    #print(str(time.time()-start))
    print(itr)
    for j in range(itr):
        count = 1.0
        temp_janshi = copy.deepcopy(janshi)
        temp_yama = yama.copy()
        temp_janshi.tehai.remove(function.hai_convert_reverse(hai_id)) # = function.tehai_convert_reverse(temp_tehai)
        temp_janshi.sutehai.append(function.hai_convert_reverse(hai_id))
        if j == 0:
            init_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
        a, b = yuukouhai_explore(temp_yama, init_shanten_suu, count, taku.hash_table, temp_janshi, taku)
    
        #sum_list[hai_id] += a
        #pure_point_sum[hai_id] += b
    #shanten_suu + 1で平均打点を割る
    #pure_point_sum[hai_id] /= max(init_shanten_suu + 1, 1)*itr


if __name__ ==  "__main__":
    janshi = majang.Janshi_p(2)
    janshi1 = majang.Janshi_e(1)
    janshi2 = majang.Janshi_e(2)
    janshi3 = majang.Janshi_e(3)
    taku = majang.Taku()
    janshi_list= [janshi, janshi1, janshi2, janshi3]

    janshi.janshi_reset()
    taku.taku_reset()
    taku.dorahyouji = ["1z"]
    #taku.hash_table = None
    janshi.tehai = ['1m', '4m', '5m', '6m', '7m', '2p', '2p', '3p', '4p', '5p', '6p', '7p', '7p', '7p']
    #janshi.fuurohai = [[2,2,1]]

    janshi.init_vertual_yama(taku)
    janshi.vertual_yama.remove("3p")
    janshi.vertual_yama.remove("3p")
    #janshi.vertual_yama.remove("3p")
    #janshi.vertual_yama.remove("3p")
    taku.yama_nokori = 58
    shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)

    #start = time.time()
    #print(eval_ensemble.new_yuukouhai_explore(1, janshi, taku))
    new_yuukouhai_explore(shanten_suu, janshi, taku)
    #print(str(time.time()-start))