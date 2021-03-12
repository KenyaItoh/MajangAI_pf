import copy
import numpy as np
import function
import math

#戻り値→手牌n枚の防御評価値　すなわち要素数nのリスト
def eval_defense(janshi, taku, shanten_suu, temp_max, pure_point_list, bakyou_list):
    janshi_list = copy.deepcopy(janshi)
    janshi_p = janshi_list[0]
    nokori_tsumo_kaisuu = int(taku.yama_nokori/4)

    vertual_yama = janshi_p.vertual_yama
    vertual_yama_index = function.tehai_convert(vertual_yama)
    tehai_len = len(janshi_p.tehai)
    eval_defense_point = np.zeros(tehai_len)

    for i in range(1,4):
        #とりあえず立直者だけ警戒
        if janshi_list[i].riichi:
            tenpai_prob = 3.0
        elif janshi_list[i].fuurosuu != 0:
            tenpai_prob = janshi_list[i].fuurosuu * 0.1 * math.exp(((17 - nokori_tsumo_kaisuu)/17-1)*math.sqrt(5))
        else:
            continue
        
        #打点期待値を設定
        if janshi_list[i].kaze == 0:
            daten_expect = 10000
        else:
            daten_expect = 7000
        
        #max_pointの設定
        #オーラスで最下位なら防御をほとんどしない
        if bakyou_list[0] == 4:
            max_point = temp_max*0.1
        else:
            max_point = temp_max
        #3シャンテン以上は倍
        #if shanten_suu >= 3:
        #    max_point *= 1.0
        genbutsu_list = function.akadora_convert(janshi_list[i].sutehai)[0] + function.akadora_convert(janshi_list[i].temp_genbutsu)[0]

        #危険牌枚数を計上
        temp_list = ["1m", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "9m", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "1z", "2z", "3z", "4z", "5z", "6z", "7z"]
        for j in range(len(genbutsu_list)):
            if genbutsu_list[j] in temp_list:
                temp_list.remove(genbutsu_list[j])
        kikenhai_maisuu = len(temp_list)

        #save_max_point = max_point

        #手出しリスト作成
        tedashi_list = []
        for j in range(len(janshi_list[i].sutehai)):
            if janshi_list[i].tedashi_flag:
                tedashi_list.append(janshi_list[i].sutehai[j])

        ############メイン#########################
        max_pure = max(pure_point_list)
        yuuido = max((max_pure/(daten_expect*tenpai_prob/kikenhai_maisuu))**0.5, 0.66)
        print(yuuido)
        max_point /= yuuido

        for j in range(tehai_len):
            
            hai_index = function.hai_convert(janshi_p.tehai[j])

            #現物ならmax_point与えてcontinue
            temp_hai_str = function.akadora_hai_convert(janshi_p.tehai[j])
            if temp_hai_str in genbutsu_list:
                eval_defense_point[j] += max_point
                continue

            #字牌
            if hai_index > 30:
                if vertual_yama_index[hai_index] == 0:
                    eval_defense_point[j] += max_point
                    continue
                elif vertual_yama_index[hai_index] == 1:
                    eval_defense_point[j] += max_point*0.8
                    continue
                elif vertual_yama_index[hai_index] == 2:
                    eval_defense_point[j] += max_point*0.5
                    continue
                elif vertual_yama_index[hai_index] == 3:
                    eval_defense_point[j] += max_point*0.2
                    continue

            #牌の種類によって減点     
            if hai_index < 30:
                if hai_index % 10 == 1 or hai_index % 10 == 9:
                    eval_defense_point[j] -= max_point * 0.1
                elif hai_index % 10 == 2 or hai_index % 10 == 2:
                    eval_defense_point[j] -= max_point * 0.2
                elif hai_index % 10 == 3  or hai_index % 10 == 4 or hai_index % 10 == 5 or hai_index % 10 == 6 or hai_index % 10 == 7:
                    eval_defense_point[j] -= max_point * 0.3
                #赤ドラ
                else:
                    eval_defense_point[j] -= max_point * 0.5

            #筋牌ならば加点。宣言牌の筋は知らん
            if suji_hantei(genbutsu_list, hai_index):
                eval_defense_point[j] += max_point * 0.5

            #最終手出しおよびその一つ前の手出しのマタギならば減点。マタギは赤ドラを考えない。
            matagi_list = matagi_henkan(hai_index)
            if len(tedashi_list) >= 1:
                if function.hai_convert(tedashi_list[-1]) in matagi_list:
                    eval_defense_point[j] -= max_point * 0.5
            if len(tedashi_list) >= 2:
                if function.hai_convert(tedashi_list[-2]) in matagi_list:
                    eval_defense_point[j] -= max_point * 0.5
            
            #裏筋ならば減点
            urasuji_list = urasuji_henkan(hai_index)
            sutehai_index_list = function.akadora_convert3(function.tehai_convert3(tedashi_list))[0]
            for k in range(len(urasuji_list)):
                if urasuji_list[k] in sutehai_index_list:
                    eval_defense_point[j] -= max_point * 0.4
            
            #序盤に切れた数牌の外側に対して加点
            sutehai_len = len(janshi_list[i].sutehai)
            if sutehai_len > 6:
                sotohai_list = sotohai_find(janshi_list[i].sutehai, min(int(sutehai_len/3), 4))
                if hai_index in sotohai_list:
                    eval_defense_point[j] += max_point * 0.5
            
            #カベの外側に対して加点
            eval_defense_point[j] += max_point * kabe_eval(vertual_yama_index, hai_index)

            #max_pointに補正
            if abs(eval_defense_point[j]) > max_point:
                eval_defense_point[j] *= max_point/abs(eval_defense_point[j])
    
    return eval_defense_point
            


            

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
