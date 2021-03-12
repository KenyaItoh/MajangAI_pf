import copy
import numpy as np
import function
import math

#危険度リストを作る（yuukouhai_explorer用）。indexリスト。
def create_danger_degree_list(janshi, taku, bakyou_list):   
    danger_degree_list = [0] * 38
    danger_degree_list_return = [1.0] * 38
    #オーラスで最下位ならぜんぶ1.0
    if bakyou_list[0] == 4:
        return danger_degree_list_return

    janshi_list = copy.deepcopy(janshi)
    janshi_p = janshi_list[0]
    nokori_tsumo_kaisuu = int(taku.yama_nokori/4)

    vertual_yama = janshi_p.vertual_yama
    vertual_yama_index = function.tehai_convert(vertual_yama)

    for i in range(1,4):
        #とりあえず立直者だけ警戒
        if janshi_list[i].riichi:
            tenpai_prob = 1.0
        elif janshi_list[i].fuurosuu != 0:
            tenpai_prob = janshi_list[i].fuurosuu * 0.09 * math.exp(((17 - nokori_tsumo_kaisuu)/17-1)*math.sqrt(5))
        else:
            continue

        #max_pointの設定
        genbutsu_list = function.akadora_convert(janshi_list[i].sutehai)[0] + function.akadora_convert(janshi_list[i].temp_genbutsu)[0]

        #手出しリスト作成
        tedashi_list = []
        for j in range(len(janshi_list[i].sutehai)):
            if janshi_list[i].tedashi_flag:
                tedashi_list.append(janshi_list[i].sutehai[j])

        ############メイン#########################
        temp_list = list(range(len(danger_degree_list)))
        temp_list.remove(0)
        temp_list.remove(10)
        temp_list.remove(20)
        temp_list.remove(30)
        for j in temp_list:
            hai_index = j
            #現物ならcontinue
            temp_hai_str = function.akadora_hai_convert(j)
            if temp_hai_str in genbutsu_list:
                continue

            #字牌
            if hai_index > 30:
                if vertual_yama_index[hai_index] == 0:
                    continue
                elif vertual_yama_index[hai_index] == 1:
                    continue
                elif vertual_yama_index[hai_index] == 2:
                    danger_degree_list[j] += 0.05
                    continue
                elif vertual_yama_index[hai_index] == 3:
                    danger_degree_list[j] += 0.2
                    continue

            #筋牌ならばcontinue
            if suji_hantei(genbutsu_list, hai_index):
                continue
            
            #序盤に切れた数牌の外側ならばcontinue
            sutehai_len = len(janshi_list[i].sutehai)
            if sutehai_len > 6:
                sotohai_list = sotohai_find(janshi_list[i].sutehai, min(int(sutehai_len/3), 4))
                if hai_index in sotohai_list:
                    continue
            
            #カベの外側continue
            if kabe_eval(vertual_yama_index, hai_index) != 0:
                continue

            #補正
            danger_degree_list[j] += tenpai_prob * 2.0
    
    danger_degree_list = np.array(danger_degree_list)
    danger_degree_list_return = np.array(danger_degree_list_return)

    return danger_degree_list + danger_degree_list_return
            


            

def suji_hantei(genbutsu_list, hai_index):
    genbutsu_index_list = function.tehai_convert3(genbutsu_list)
    suji_list = suji_henkan(hai_index)
    for i in range(len(suji_list)):
        if not (suji_list[i] in genbutsu_index_list):
            return False
    return True

#hai_indexが筋で安全となるための牌indexlistを返す
def suji_henkan(hai_index):
    suji_list = []
    if hai_index < 30:
        if hai_index%10 == 1:
            suji_list = [hai_index+3]
        elif hai_index%10 == 2:
            suji_list = [hai_index+3]
        elif hai_index%10 == 3:
            suji_list = [hai_index+3]
        elif hai_index%10 == 4:
            suji_list = [hai_index-3, hai_index+3]
        elif hai_index%10 == 4:
            suji_list = [hai_index-3, hai_index+3]
        elif hai_index%10 == 5:
            suji_list = [hai_index-3, hai_index+3]
        elif hai_index%10 == 6:
            suji_list = [hai_index-3, hai_index+3]
        elif hai_index%10 == 7:
            suji_list = [hai_index-3]
        elif hai_index%10 == 8:
            suji_list = [hai_index-3]
        elif hai_index%10 == 9:
            suji_list = [hai_index-3]
        elif hai_index%10 == 0:
            suji_list = [hai_index + 2, hai_index + 8]
    return suji_list

#hai_indexがマタギとなるhai_index_listを返す
def matagi_henkan(hai_index):
    matagi_list = []
    if hai_index < 30:
        if hai_index%10 == 1:
            matagi_list = [hai_index+1, hai_index+2]
        elif hai_index%10 == 2:
            matagi_list = [hai_index+1, hai_index+2]
        elif hai_index%10 == 3:
            matagi_list = [hai_index+1, hai_index+2]
        elif hai_index%10 == 4:
            matagi_list = [hai_index-2, hai_index-1, hai_index+1, hai_index+2]
        elif hai_index%10 == 5:
            matagi_list = [hai_index-2, hai_index-1, hai_index+1, hai_index+2]
        elif hai_index%10 == 6:
            matagi_list = [hai_index-2, hai_index-1, hai_index+1, hai_index+2]
        elif hai_index%10 == 7:
            matagi_list = [hai_index-2, hai_index-1]
        elif hai_index%10 == 8:
            matagi_list = [hai_index-2, hai_index-1]
        elif hai_index%10 == 9:
            matagi_list = [hai_index-2, hai_index-1]
        elif hai_index%10 == 0:
            matagi_list = [hai_index-3, hai_index-4, hai_index+6, hai_index+7]
    return matagi_list

#hai_indexが裏筋となるhai_index_listを返す
def urasuji_henkan(hai_index):
    urasuji_list = []
    if hai_index < 30:
        if hai_index%10 == 1:
            urasuji_list = [hai_index-1, hai_index+4]
        elif hai_index%10 == 2:
            urasuji_list = [hai_index-1, hai_index+4]
        elif hai_index%10 == 3:
            urasuji_list = [hai_index-1, hai_index+4]
        elif hai_index%10 == 4:
            urasuji_list = [hai_index-1, hai_index-4, hai_index+4]
        elif hai_index%10 == 5:
            urasuji_list = [hai_index-1, hai_index+1, hai_index-4, hai_index+4]
        elif hai_index%10 == 6:
            urasuji_list = [hai_index+1, hai_index-6, hai_index-4]
        elif hai_index%10 == 7:
            urasuji_list = [hai_index+1, hai_index-4]
        elif hai_index%10 == 8:
            urasuji_list = [hai_index+1, hai_index-4]
        elif hai_index%10 == 9:
            urasuji_list = [hai_index-9, hai_index-4]
        elif hai_index%10 == 0:
            urasuji_list = [hai_index+1, hai_index+9]
    return urasuji_list

#捨て牌が7枚以上あるとき、3枚目までの捨て牌について外側となる牌indexを返す。
def sotohai_find(sutehai, limit):
    sotohai_list = []
    for i in range(limit):
        sotohai_list = sotohai_list + sotohai_henkan(function.hai_convert(sutehai[i]))
    return sotohai_list
        
def sotohai_henkan(hai_index):
    sotohai_list = []
    if hai_index < 30:
        if hai_index%10 == 2:
            sotohai_list = [hai_index-1]
        elif hai_index%10 == 3:
            sotohai_list = [hai_index-2, hai_index-1]
        elif hai_index%10 == 4:
            sotohai_list = [hai_index-2, hai_index-1]
        elif hai_index%10 == 6:
            sotohai_list = [hai_index+1, hai_index+2]
        elif hai_index%10 == 7:
            sotohai_list = [hai_index+1, hai_index+2]
        elif hai_index%10 == 8:
            sotohai_list = [hai_index+1]
    return sotohai_list

#hai_indexとvertual_yama_index([0,4,3,4,1,2,...])から加点ポイントを出す。
def kabe_eval(vertual_yama_index, hai_index):
    #字牌は関係ない
    if hai_index > 30:
        return 0.0
    
    if hai_index%10 == 1:
        if vertual_yama_index[hai_index+1] == 0 or  vertual_yama_index[hai_index+2] == 0:
            if vertual_yama_index[hai_index] == 0:
                return 10.0
            elif vertual_yama_index[hai_index] == 1:
                return 5.0
            elif vertual_yama_index[hai_index] == 2:
                return 2.0
            elif vertual_yama_index[hai_index] == 3:
                return 1.0
        elif vertual_yama_index[hai_index+1] == 1 or  vertual_yama_index[hai_index+2] == 1:
            return 0.8
        else:
            return 0.0
    
    elif hai_index%10 == 2:
        if vertual_yama_index[hai_index+1] == 0 or  vertual_yama_index[hai_index+2] == 0:
            if vertual_yama_index[hai_index] == 0:
                return 10.0
            elif vertual_yama_index[hai_index] == 1:
                return 5.0
            elif vertual_yama_index[hai_index] == 2:
                return 2.0
            elif vertual_yama_index[hai_index] == 3:
                return 1.0
        elif vertual_yama_index[hai_index+1] == 1 or  vertual_yama_index[hai_index+2] == 1:
            return 0.7
        else:
            return 0.0
    
    elif hai_index%10 == 3:
        if vertual_yama_index[hai_index+1] == 0 or  vertual_yama_index[hai_index+2] == 0:
            if vertual_yama_index[hai_index] == 0:
                return 10.0
            elif vertual_yama_index[hai_index] == 1:
                return 5.0
            elif vertual_yama_index[hai_index] == 2:
                return 2.0
            elif vertual_yama_index[hai_index] == 3:
                return 1.0
        elif vertual_yama_index[hai_index+1] == 1 or  vertual_yama_index[hai_index+2] == 1:
            return 0.6
        else:
            return 0.0

    elif hai_index%10 == 4:
        if (vertual_yama_index[hai_index+1] == 0 or  vertual_yama_index[hai_index+2] == 0) and (vertual_yama_index[hai_index-1] == 0 or  vertual_yama_index[hai_index-2] == 0):
            if vertual_yama_index[hai_index] == 0:
                return 10.0
            elif vertual_yama_index[hai_index] == 1:
                return 5.0
            elif vertual_yama_index[hai_index] == 2:
                return 2.0
            elif vertual_yama_index[hai_index] == 3:
                return 1.0
        elif (vertual_yama_index[hai_index+1] == 1 or  vertual_yama_index[hai_index+2] == 1) and (vertual_yama_index[hai_index-1] == 1 or  vertual_yama_index[hai_index-2] == 1):
            return 0.5
        else:
            return 0.0

    elif hai_index%10 == 5:
        if (vertual_yama_index[hai_index+1] == 0 or  vertual_yama_index[hai_index+2] == 0) and (vertual_yama_index[hai_index-1] == 0 or  vertual_yama_index[hai_index-2] == 0):
            if vertual_yama_index[hai_index] == 0:
                return 10.0
            elif vertual_yama_index[hai_index] == 1:
                return 5.0
            elif vertual_yama_index[hai_index] == 2:
                return 2.0
            elif vertual_yama_index[hai_index] == 3:
                return 1.0
        elif (vertual_yama_index[hai_index+1] == 1 or  vertual_yama_index[hai_index+2] == 1) and (vertual_yama_index[hai_index-1] == 1 or  vertual_yama_index[hai_index-2] == 1):
            return 0.5
        else:
            return 0.0

    elif hai_index%10 == 0:
        hai_index += 5
        if (vertual_yama_index[hai_index+1] == 0 or  vertual_yama_index[hai_index+2] == 0) and (vertual_yama_index[hai_index-1] == 0 or  vertual_yama_index[hai_index-2] == 0):
            if vertual_yama_index[hai_index] == 0:
                return 10.0
            elif vertual_yama_index[hai_index] == 1:
                return 5.0
            elif vertual_yama_index[hai_index] == 2:
                return 2.0
            elif vertual_yama_index[hai_index] == 3:
                return 1.0
        elif (vertual_yama_index[hai_index+1] == 1 or  vertual_yama_index[hai_index+2] == 1) and (vertual_yama_index[hai_index-1] == 1 or  vertual_yama_index[hai_index-2] == 1):
            return 0.5
        else:
            return 0.0

    elif hai_index%10 == 6:
        if (vertual_yama_index[hai_index+1] == 0 or  vertual_yama_index[hai_index+2] == 0) and (vertual_yama_index[hai_index-1] == 0 or  vertual_yama_index[hai_index-2] == 0):
            if vertual_yama_index[hai_index] == 0:
                return 10.0
            elif vertual_yama_index[hai_index] == 1:
                return 5.0
            elif vertual_yama_index[hai_index] == 2:
                return 2.0
            elif vertual_yama_index[hai_index] == 3:
                return 1.0
        elif (vertual_yama_index[hai_index+1] == 1 or  vertual_yama_index[hai_index+2] == 1) and (vertual_yama_index[hai_index-1] == 1 or  vertual_yama_index[hai_index-2] == 1):
            return 0.5
        else:
            return 0.0

    elif hai_index%10 == 7:
        if vertual_yama_index[hai_index-1] == 0 or  vertual_yama_index[hai_index-2] == 0:
            if vertual_yama_index[hai_index] == 0:
                return 10.0
            elif vertual_yama_index[hai_index] == 1:
                return 5.0
            elif vertual_yama_index[hai_index] == 2:
                return 2.0
            elif vertual_yama_index[hai_index] == 3:
                return 1.0
        elif vertual_yama_index[hai_index-1] == 1 or  vertual_yama_index[hai_index-2] == 1:
            return 0.6
        else:
            return 0.0

    elif hai_index%10 == 8:
        if vertual_yama_index[hai_index-1] == 0 or  vertual_yama_index[hai_index-2] == 0:
            if vertual_yama_index[hai_index] == 0:
                return 10.0
            elif vertual_yama_index[hai_index] == 1:
                return 5.0
            elif vertual_yama_index[hai_index] == 2:
                return 2.0
            elif vertual_yama_index[hai_index] == 3:
                return 1.0
        elif vertual_yama_index[hai_index-1] == 1 or  vertual_yama_index[hai_index-2] == 1:
            return 0.7
        else:
            return 0.0
    
    elif hai_index%10 == 9:
        if vertual_yama_index[hai_index-1] == 0 or  vertual_yama_index[hai_index-2] == 0:
            if vertual_yama_index[hai_index] == 0:
                return 10.0
            elif vertual_yama_index[hai_index] == 1:
                return 5.0
            elif vertual_yama_index[hai_index] == 2:
                return 2.0
            elif vertual_yama_index[hai_index] == 3:
                return 1.0
        elif vertual_yama_index[hai_index-1] == 1 or  vertual_yama_index[hai_index-2] == 1:
            return 0.8
        else:
            return 0.0
    
    return 0.0
