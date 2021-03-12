import copy
import random
import shanten_check_new
import function
import tensu_calc
import numpy as np
import majang

#立直の場合は[True, 牌インデックス、期待値]
def riichi_hantei(janshi, taku):
    nokori_tsumo_kaisuu = int(taku.yama_nokori/4)
    nokori_tsumo_kaisuu2 = nokori_tsumo_kaisuu - 1

    #閾値　場況によって変える予定
    thresh = 1000
    
    yuukou_sutehai = find_yuukou_sutehai(janshi, 0, taku.hash_table)

    itr = int(3000.0 / (len(yuukou_sutehai) * max(nokori_tsumo_kaisuu, 1)))
    itr2 = itr
    #print(itr)

    agari_sum_list = np.zeros(38)
    agari_sum_list2 = np.zeros(38)
    #agari_sum_list[yuukou_sutehai] = 0.1
    temp_taku = copy.deepcopy(taku)
    dora_mem = temp_taku.dorahyouji.copy()
    len_dora = len(temp_taku.dorahyouji)
    dora_memory_list = []
    yama_memory_list = []

    #裏ドラリストを作成
    for j in range(itr):
        temp_vertual_yama = janshi.vertual_yama.copy()
        dora_temp = []
        for k in range(len_dora):
            rand_index = random.randrange(len(temp_vertual_yama))
            dora_temp.append(temp_vertual_yama[rand_index])
            del temp_vertual_yama[rand_index]
        dora_memory_list.append(dora_temp)
        random.shuffle(temp_vertual_yama)
        yama_memory_list.append(temp_vertual_yama[0:nokori_tsumo_kaisuu])

    #保存用
    yama_memory_list2 = copy.deepcopy(yama_memory_list)
    
    for index in yuukou_sutehai:
        #バグ防止
        agari_sum_list[index] += 1
        yama_memory_list = copy.deepcopy(yama_memory_list2)
        for j in range(itr):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.tehai.remove(function.hai_convert_reverse(index))
            temp_janshi.riichi = 1
            temp_taku.dorahyouji = dora_mem.copy()
            #フリテンの場合は減点
            #furiten_flag = function.furiten_hantei(temp_janshi, temp_taku)

            #裏ドラをランダムで設定
            temp_taku.dorahyouji.extend(dora_memory_list[j])
            
            #if furiten_flag:
            #    furiten_penalty = 0.7
            #else:
            #    furiten_penalty = 1.0
                              
            agari_sum_list[index] += monte_carlo_riichi(temp_janshi, temp_taku, nokori_tsumo_kaisuu, yama_memory_list[j])#*furiten_penalty
    
    mean_list = agari_sum_list/float(itr)
    max_index = np.argmax(mean_list)
    print("立直時打点期待値: " + str(mean_list[max_index]) + "点") 


    for index in yuukou_sutehai:
        yama_memory_list = copy.deepcopy(yama_memory_list2)
        #バグ防止
        agari_sum_list2[index] += 1
        for j in range(itr2):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.tehai.remove(function.hai_convert_reverse(index))
            temp_taku.dorahyouji = dora_mem.copy()

            #裏ドラをランダムで設定
            temp_taku.dorahyouji.extend(dora_memory_list[j])
            
            temp_janshi.tehai.append(yama_memory_list[j][0])
            del yama_memory_list[j][0]

            if shanten_check_new.shanten_check(temp_janshi, taku.hash_table) == -1:
                point = tensu_calc.tensu_calc(temp_janshi, temp_taku, temp_janshi.tehai[-1])
                if janshi.kaze == 0:
                    agari_point = point[0]*3
                else:
                    agari_point =  point[0]*2+point[1]
                agari_sum_list2[index] += agari_point
            else:
                yuukou_sutehai2 = find_yuukou_sutehai(temp_janshi, 0, taku.hash_table)
                temp2 = random.choice(yuukou_sutehai2)
                temp_janshi.tehai.remove(function.hai_convert_reverse(temp2))
                temp_janshi.riichi = 1
                #フリテンの場合は減点
                #furiten_flag = function.furiten_hantei(temp_janshi, temp_taku)
                #if furiten_flag:
                #   furiten_penalty = 0.7
                #else:
                #    furiten_penalty = 1.0
                agari_sum_list2[index] += monte_carlo_riichi(temp_janshi, temp_taku, nokori_tsumo_kaisuu2, yama_memory_list[j])#*furiten_penalty
   
    mean_list2 = agari_sum_list2/float(itr2)

    max_index2 = np.argmax(mean_list2)

    print("立直保留時打点期待値: " + str(mean_list2[max_index2]) + "点") 

    if max(mean_list2[max_index2], mean_list[max_index]) < thresh:
        return [False, max_index, 0]

    if mean_list2[max_index2] > mean_list[max_index] + 175:
        return [False, max_index2, mean_list2[max_index]]
    else:
        if mean_list[max_index] > thresh:
            return [True, max_index, mean_list[max_index]]
    return [False, max_index, 0]

def monte_carlo_riichi(janshi, taku, nokori_tsumo_kaisuu, yama):  
    count = 0
    while count < nokori_tsumo_kaisuu:
        count += 1
        janshi.tehai.append(yama[0])
        del yama[0]
        if shanten_check_new.shanten_check(janshi, taku.hash_table) == -1:
            point = tensu_calc.tensu_calc(janshi, taku, janshi.tehai[-1])
            if janshi.kaze == 0:
                agari_point = point[0]*3
            else:
                agari_point =  point[0]*2+point[1]
            agari_point = agari_point * (1.0-0.4*(count-1)/18.0)
            #print(agari_point)
            return agari_point
        del janshi.tehai[-1]
    return 0

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

if __name__ == '__main__':
    janshi = majang.Janshi_p(0)
    taku = majang.Taku()

    taku.taku_reset()
    taku.dorahyouji =["9m"]
    taku.yama_nokori = 30
    #taku.uradorahyouji = ["1z"]
    for i in range(len(janshi.tehai)):
        janshi.vertual_yama.remove(janshi.tehai[i])
    janshi.vertual_yama.remove("1z")
    janshi.vertual_yama.remove("4p")
    janshi.vertual_yama.remove("8p")
    janshi.vertual_yama.remove("7p")
    janshi.vertual_yama.remove("9p")

    janshi.first_tsumo_flag = False
    janshi.tehai = ["1m", "2m", "3m", "4m", "5m", "6m", "4s", "5s", "6s", "4p", "4p", "4p", "2p", "4p"]

    import time

    start = time.time()
    print(riichi_hantei(janshi, taku))
    print(str(time.time()-start))