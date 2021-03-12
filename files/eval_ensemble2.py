import evaluate
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

#全探索（テスト）
def eval_tehai_ens(janshi, taku):
    #まずシャンテン数を求める
    shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
    #print("シャンテン" + str(shanten_suu))
    maximum_eval_index = False 
    if shanten_suu > 2:
        maximum_eval_index = eval_tehai_point(janshi, taku)

    elif shanten_suu == 2:
        yuukouhai = np.array(new_yuukouhai_explore(shanten_suu, janshi, taku))
        point = np.array(eval_tehai_point(janshi, taku))

        for i in range(len(yuukouhai)):
            if yuukouhai[i] == 0:
                point[i] = 0
        
        point = point/np.sum(point)

        tehai_point_list = yuukouhai + point
        print(yuukouhai)
        print(point)
        print(tehai_point_list)
        maximum_eval_index = np.argmax(tehai_point_list)
    
    elif shanten_suu <= 1:
        yuukouhai = np.array(new_yuukouhai_zenexplore(shanten_suu, janshi, taku))
        point = np.array(eval_tehai_point(janshi, taku))

        for i in range(len(yuukouhai)):
            if yuukouhai[i] == 0:
                point[i] = 0
        
        point = point/np.sum(point)

        tehai_point_list = yuukouhai + point
        print(yuukouhai)
        print(point)
        print(tehai_point_list)
        maximum_eval_index = np.argmax(tehai_point_list)

    return maximum_eval_index


#全探索
def new_yuukouhai_zenexplore(shanten_suu, janshi, taku):
    hash_table = taku.hash_table
    tehai = np.array(function.tehai_convert(janshi.tehai))

    #ツモって来る牌に赤ドラは考慮しない
    yama = np.array(function.tehai_convert(function.akadora_convert(janshi.vertual_yama)[0]))    
    init_shanten_suu = shanten_suu
    #index_list = [0]*len(tehai)
    sum_list = [0]*len(tehai)
    count_sum_list = [0.001]*len(tehai)
    #mean_list = [0]*len(tehai)
    hai_list = find_yuukou_sutehai(janshi, init_shanten_suu, hash_table)
    #print(hai_list)
    #副露した時でアガリ役なしの場合
    if len(hai_list) == 0:
        return [0.001]*len(janshi.tehai)
    
    #バグ防止用
    for i in hai_list:
        sum_list[i] += 0.001
    
    #print(hai_list)
    itr = 10

    #print(hai_list)

    for j in range(itr):
        count = 1.      
        for i in hai_list:
            temp_janshi = copy.deepcopy(janshi)
            temp_tehai = tehai.copy()
            temp_yama = yama.copy()       
            temp_tehai[i] -= 1
            temp_janshi.tehai = function.tehai_convert_reverse(temp_tehai)
            yuukouhai_zenexplore(temp_yama, init_shanten_suu, count, hash_table, temp_janshi, taku, sum_list, count_sum_list,i)

    print(sum_list)
    print(count_sum_list)

    #sum_list = np.array(sum_list)/np.array(count_sum_list)

    tehai_sum_list = np.zeros(len(janshi.tehai))

    for i in range(len(janshi.tehai)):
        tehai_sum_list[i] = sum_list[function.hai_convert(janshi.tehai[i])]
    
    normalized_list = np.array(tehai_sum_list)/np.sum(np.array(tehai_sum_list))
    print(np.sum(normalized_list))
    return normalized_list

def yuukouhai_zenexplore(yama, shanten_suu, count, hash_table, janshi, taku, sum_list, count_sum_list, i_const):
    
    yuukouhai_boost = 1.0
    yuukouhai_list = find_yuukouhai(janshi, shanten_suu, hash_table)

    #print("有効牌")
    #print(yuukouhai_list)

    for index in yuukouhai_list:
        #print("ツモ牌")
        #print(index)
        yama_copy = yama.copy()
        count_copy = count
        shanten_suu_copy = shanten_suu 
        temp_janshi = copy.deepcopy(janshi)
        tehai = function.tehai_convert(temp_janshi.tehai)
        tehai[index] += 1  
        yuukouhai_num = yama_copy[index] + 0.001
        #テンパイ時に待ち牌に対してブーストを行う
        if shanten_suu_copy == 0:
            count_copy *= (yuukouhai_num**(yuukouhai_boost))/len(yama_copy)
        else:
            count_copy *= yuukouhai_num/len(yama_copy)
        yama_copy[index] -= 1
    
        shanten_suu_copy -= 1

        #print(shanten_suu)
    
        if shanten_suu_copy == -1:
            agarihai_str = function.hai_convert_reverse(index)
            tehai_str = function.tehai_convert_reverse(tehai)
            temp_janshi.tehai =  tehai_str
            #print(temp_janshi.tehai)
            point_temp = tensu_calc.tensu_calc(temp_janshi, taku, agarihai_str)
            if len(point_temp) == 0:
                point = 0
            elif point_temp[0] == point_temp[1]:
                point  = point_temp[0]*3
            else:
                point = point_temp[0] * 2 + point_temp[1]
            #print(point)
            #print(count_copy * point)
            sum_list[i_const] += count_copy * point
            #print(sum_list)
            #count_sum_list[i_const] += 1
            #return count*teyaku_check.teyaku_check(janshi, taku, agarihai_str)
            continue
        
        temp_janshi.tehai = function.tehai_convert_reverse(tehai)
        yuukou_sutehai_index_list = find_yuukou_sutehai(temp_janshi, shanten_suu_copy, hash_table)

        #print("有効捨て牌")
        #print(yuukou_sutehai_index_list)

        index2 = random.choice(yuukou_sutehai_index_list)
        temp_janshi2 = copy.deepcopy(temp_janshi)
        tehai = function.tehai_convert(temp_janshi2.tehai)
        tehai[index2] -= 1
        temp_janshi2.tehai = function.tehai_convert_reverse(tehai)
        yuukouhai_zenexplore(yama_copy, shanten_suu_copy, count_copy, hash_table, temp_janshi2, taku, sum_list, count_sum_list, i_const)

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
        return [0.001]*len(janshi.tehai)
    
    #バグ防止用
    for i in hai_list:
        sum_list[i] += 0.001
    
    #print(hai_list)
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
            #index_list[i] += 1
            sum_list[i] += a

    tehai_sum_list = np.zeros(len(janshi.tehai))

    for i in range(len(janshi.tehai)):
        tehai_sum_list[i] = sum_list[function.hai_convert(janshi.tehai[i])]
    
    normalized_list = np.array(tehai_sum_list)/np.sum(np.array(tehai_sum_list))
    print(np.sum(normalized_list))
    return normalized_list

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
        #print(tehai_str)
        #print(temp_janshi.fuurohai)
        #print(count)
        point_temp = tensu_calc.tensu_calc(temp_janshi, taku, agarihai_str)
        if len(point_temp) == 0:
            point = 0
        elif point_temp[0] == point_temp[1]:
            point  = point_temp[0]*3
        else:
            point = point_temp[0] * 2 + point_temp[1]
        #print(point)
        return count * point
        #return count*teyaku_check.teyaku_check(janshi, taku, agarihai_str)[0]
    
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

def eval_tehai_point(janshi, taku):
    
    #パラメータ関連
    
    #各シャンテン数に対する平均有効牌枚数
    mean_list = [4.575752953784895,
                 12.18668553881974,
                 23.338351152742664,
                 40.50627978155267,
                 60.56931288649266,
                 77.81782501846193,
                 100.03097486813587]
    
    shanten_bonus = 5
    yuukouhai_bonus = 2.0
    yuukouhai_pow_const = 1.0
    dora_bonus0 = 1.0   #ドラインデックスの牌
    dora_bonus1 = 0.5 #ドラインデックス前後の牌
    dora_bonus2 = 0.3 #ドラインデックスから2枚離れた牌
    yakuhai_bonus = [0, 0.2, 0.6, 1.0] #0枚～3枚以上
    ryanmen_bonus = 0.3
    penchan_penalty = -0.3
    koritsu_yaochu_penalty = -0.1 #1,9
    koritsu_suuhai_penalty2 = -0.05 #2,8
    koritsu_suuhai_penalty3 = -0.01 #3~7
    koritsu_jihai_penalty = -0.2
    koritsu_nokori_yakuhai_penalty = [-0.5, -0.3, -0.2, 0.0]
    toitsu_nokori_yakuhai_penalty = [-0.6, -0.3, 0.0, 0.0]
    koritsu_nokori_jihai_penalty = [-0.3, -0.2, -0.1, 0.0]
    toitsu_nokori_jihai_penalty = [-0.4, -0.3, 0.0, 0.0]
    tanyao_bonus = [0,0,0,0,0,0,0,0,0,0,0,0.27,0.6,1.0]
    ittsuu_bonus = [0,0,0,0,0,0,0,0.5,0.9,1.4]
    sansyoku_bonus = [0,0,0,0,0,0,0.3,0.6,1.0,1.4]
    honitsu_bonus = [0,0,0,0,0,0,0,0,0,0,0,2.0,4.0,6.0]
    yipeko_param1 = 1.0 #222
    yipeko_param2 = 0.8 #122, 221
    yipeko_param3 = 0.6 #212
    yipeko_param4 = 0.5 #212(1,9含む)
    yipeko_param5 = 0.4 #221, 122(1,9含む)
    furiten_penalty = [-0.2, -0.55, -0.3]
    furiten_penalty_for_yuukouhai = -0.4
    
    #メイン
    eval_point_list = [0]*len(janshi.tehai)
    old_shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
    for i in range(len(janshi.tehai)):
        
        #print("捨てる牌: " + janshi.tehai[i])
        
        #コピーして手牌を1つ削除
        temp_janshi = copy.deepcopy(janshi)
        del temp_janshi.tehai[i]
        
        #赤ドラだけ抜き出してあとは赤ナシで考える
        temp = function.akadora_convert(temp_janshi.tehai)
        akadora_maisuu = temp[1]
        temp_janshi.tehai = temp[0]
        tehai = function.tehai_convert(temp_janshi.tehai)
        
        #vertual_yama
        vertual_yama_index = function.tehai_convert(temp_janshi.vertual_yama)
        #print(vertual_yama_index)
        
        #シャンテン数関連
        
        new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
        if old_shanten_suu == new_shanten_suu:
            eval_point_list[i] += shanten_bonus
            #print("シャンテンアップボーナス: " + str(shanten_bonus))
        else:
            pass
            #print("シャンテンアップボーナス: " + str(0))
        #print(eval_point_list[i])
        
        #有効牌関連
        yuukouhai_maisuu = function.calc_yuukouhai_maisuu(temp_janshi, new_shanten_suu, taku.hash_table)
        yuukouhai_point = ((yuukouhai_maisuu/(len(temp_janshi.vertual_yama)/123.0*mean_list[new_shanten_suu]))**yuukouhai_pow_const)*yuukouhai_bonus
        eval_point_list[i] += yuukouhai_point
        #print("有効牌ボーナス: " + str(yuukouhai_point))
        #print(eval_point_list[i])
        
        #ドラ関連とりあえず1枚の時だけ
        dora_index = []
        dora_hyouji_index = function.tehai_convert2(function.akadora_convert(taku.dorahyouji)[0]).copy()
        for j in range(len(taku.dorahyouji)):     
            ##まずドラのインデックスを求める
            if dora_hyouji_index[j] < 30:
                if dora_hyouji_index[j]%10 == 9:
                    dora_index.append(dora_hyouji_index[j] - 8)
                else:
                    dora_index.append(dora_hyouji_index[j] + 1)
            else:
                if dora_hyouji_index[j] == 34:
                    dora_index.append(31)
                elif dora_hyouji_index[j] == 37:
                    dora_index.append(35)
                else:
                    dora_index.append(dora_hyouji_index[j] + 1)
        
        dora_point = 0
        
        #赤ドラ
        dora_point += akadora_maisuu * dora_bonus0
        
        for j in range(len(dora_index)):
            if dora_index[j] < 30:
                if dora_index[j] % 10 == 1:
                    dora_point += tehai[dora_index[j]] * dora_bonus0
                    dora_point += bool(tehai[dora_index[j]+1]) * dora_bonus1
                    dora_point += bool(tehai[dora_index[j]+2]) * dora_bonus2
                elif dora_index[j] % 10 == 2:
                    dora_point += bool(tehai[dora_index[j]-1]) * dora_bonus2
                    dora_point += tehai[dora_index[j]] * dora_bonus0
                    dora_point += bool(tehai[dora_index[j]+1]) * dora_bonus1
                    dora_point += bool(tehai[dora_index[j]+2]) * dora_bonus2
                elif dora_index[j] % 10 == 8:
                    dora_point += bool(tehai[dora_index[j]-2]) * dora_bonus2
                    dora_point += bool(tehai[dora_index[j]-1]) * dora_bonus1
                    dora_point += tehai[dora_index[j]] * dora_bonus0
                    dora_point += bool(tehai[dora_index[j]+1]) * dora_bonus2
                elif dora_index[j] % 10 == 1:
                    dora_point += tehai[dora_index[j]] * dora_bonus0
                    dora_point += bool(tehai[dora_index[j]-1]) * dora_bonus1
                    dora_point += bool(tehai[dora_index[j]-2]) * dora_bonus2 
                else:
                    dora_point += bool(tehai[dora_index[j]-2]) * dora_bonus2
                    dora_point += bool(tehai[dora_index[j]-1]) * dora_bonus1
                    dora_point += tehai[dora_index[j]] * dora_bonus0
                    dora_point += bool(tehai[dora_index[j]+1]) * dora_bonus1
                    dora_point += bool(tehai[dora_index[j]+2]) * dora_bonus2
            else:
                dora_point += tehai[dora_index[j]] * dora_bonus0
        
        eval_point_list[i] += dora_point
        #print("ドラボーナス: " +str(dora_point))
        #print(eval_point_list[i])
        
        #役牌
        if taku.kaze_honba[0] < 4:
            bakaze_index = 31
        else:
            bakaze_index = 32
        jikaze_index = temp_janshi.kaze + 31
        
        yakuhai_point = 0
        yakuhai_point += yakuhai_bonus[tehai[bakaze_index]]
        yakuhai_point += yakuhai_bonus[tehai[jikaze_index]]
        yakuhai_point += yakuhai_bonus[tehai[35]]
        yakuhai_point += yakuhai_bonus[tehai[36]]
        yakuhai_point += yakuhai_bonus[tehai[37]]
        
          #ペナ
        if tehai[bakaze_index] == 1:
            yakuhai_point += koritsu_nokori_yakuhai_penalty[vertual_yama_index[bakaze_index]]
        elif tehai[bakaze_index] == 2:
            yakuhai_point += toitsu_nokori_yakuhai_penalty[vertual_yama_index[bakaze_index]]

        if tehai[jikaze_index] == 1:
            yakuhai_point += koritsu_nokori_yakuhai_penalty[vertual_yama_index[jikaze_index]]
        elif tehai[jikaze_index] == 2:
            yakuhai_point += toitsu_nokori_yakuhai_penalty[vertual_yama_index[jikaze_index]]
        
        for j in range(3):
            if tehai[35+j] == 1:
                yakuhai_point += koritsu_nokori_yakuhai_penalty[vertual_yama_index[35+j]]
            elif tehai[35+j] == 2:
                yakuhai_point += toitsu_nokori_yakuhai_penalty[vertual_yama_index[35+j]]

        #役牌以外の字牌に対するペナ
        for j in range(4):
            if 31+j != bakaze_index and 31+j != jikaze_index:
                if tehai[31+j] == 1:
                    yakuhai_point += koritsu_nokori_jihai_penalty[vertual_yama_index[31+j]]
                elif tehai[31+j] == 2:
                    yakuhai_point += toitsu_nokori_jihai_penalty[vertual_yama_index[31+j]]

        eval_point_list[i] += yakuhai_point
        #print("役牌ボーナス: " + str(yakuhai_point))
        #print(eval_point_list[i])
        
        #リャンメンボーナス（テスト）
        ryanmen_point = 0
        for j in range(30):
            if 2 <= j % 10 <= 7:
                if tehai[j-1] == 0 and tehai[j] >= 1 and tehai[j+1] >= 1 and tehai[j+2] ==0:
                    ryanmen_point += ryanmen_bonus
        eval_point_list[i] += ryanmen_point
        #print("リャンメンボーナス: " + str(ryanmen_point))
        #print(eval_point_list[i])
        
        #ペンチャンペナルティ
        penchan_point = 0
        for j in range(30):
            if j%10 == 1 or j%10 == 8:
                if tehai[j-1] == 0  and tehai[j] == 1 and tehai[j+1] == 1 and tehai[j+2] ==0:
                    penchan_point += penchan_penalty
                elif tehai[j-1] == 0  and tehai[j] >= 1 and tehai[j+1] >= 1 and tehai[j+2] ==0:
                    penchan_point += penchan_penalty*0.1
        #print("ペンチャンペナルティ: " + str(penchan_point))
        eval_point_list[i] += penchan_point
        
        #孤立牌ペナルティandフリテンペナルティ
        koritsu_suuhai_point = 0
        koritsu_jihai_point = 0
        koritsu_list = function.tehai_koritsu_hantei(temp_janshi.tehai)
        for j in koritsu_list:
            koritsu_index = function.hai_convert(temp_janshi.tehai[j])
            if koritsu_index < 30:
                if (koritsu_index%10 == 2) or (koritsu_index%10 ==8):
                    koritsu_suuhai_point += koritsu_suuhai_penalty2
                elif 3 <= koritsu_index%10 <= 7:
                    koritsu_suuhai_point += koritsu_suuhai_penalty3
                else:
                    koritsu_suuhai_point += koritsu_yaochu_penalty
            else:
                koritsu_jihai_point += koritsu_jihai_penalty
    
        eval_point_list[i] += koritsu_suuhai_point
        #print("孤立数牌ペナルティ: " + str(koritsu_suuhai_point))
        eval_point_list[i] += koritsu_jihai_point
        #print("孤立字牌ペナルティ: " + str(koritsu_jihai_point))
        #print(eval_point_list[i])
        
        #フリテンペナルティ　孤立牌がフリテン絡みand有効牌がフリテン絡み
        furiten_point = 0
        kawa_no_akadora = function.tehai_convert(function.akadora_convert(temp_janshi.sutehai)[0])
        for j in range(len(kawa_no_akadora)):
            kawa_no_akadora[j] = bool(kawa_no_akadora[j])
        
        #孤立牌に対して
        for j in koritsu_list:
            koritsu_index = function.hai_convert(temp_janshi.tehai[j])
            if koritsu_index < 30:
                if 2 <= koritsu_index%10 <= 8:
                    if kawa_no_akadora[koritsu_index-2]:
                        furiten_point += furiten_penalty[2]
                    if kawa_no_akadora[koritsu_index-1]:
                        furiten_point += furiten_penalty[1]
                    if kawa_no_akadora[koritsu_index]:
                        furiten_point += furiten_penalty[0]
                    if kawa_no_akadora[koritsu_index+1]:
                        furiten_point += furiten_penalty[1]
                    if kawa_no_akadora[koritsu_index+2]:
                        furiten_point += furiten_penalty[2]
                elif koritsu_index % 10 == 1:
                    if kawa_no_akadora[koritsu_index]:
                        furiten_point += furiten_penalty[0]
                    if kawa_no_akadora[koritsu_index+1]:
                        furiten_point += furiten_penalty[1]
                    if kawa_no_akadora[koritsu_index+2]:
                        furiten_point += furiten_penalty[2]
                elif koritsu_index % 10 == 9:
                    if kawa_no_akadora[koritsu_index-2]:
                        furiten_point += furiten_penalty[2]
                    if kawa_no_akadora[koritsu_index-1]:
                        furiten_point += furiten_penalty[1]
                    if kawa_no_akadora[koritsu_index]:
                        furiten_point += furiten_penalty[0]
            else:
                if kawa_no_akadora[koritsu_index]:
                    furiten_point += furiten_penalty[0]
        
        #有効牌に対して
        yuukouhai_index_list = function.find_yuukouhai(temp_janshi, new_shanten_suu, taku.hash_table)
        for index in yuukouhai_index_list:
            if kawa_no_akadora[index]:
                furiten_point += furiten_penalty_for_yuukouhai 
        eval_point_list[i] += furiten_point
        #print("フリテンペナルティ: " + str(furiten_point))      
           
        #タンヤオボーナス
        tanyao_point = 0
        tanyao_sum = function.tanyao_sum_up(temp_janshi)
        tanyao_point = tanyao_bonus[tanyao_sum]
        eval_point_list[i] += tanyao_point
        #print("タンヤオボーナス: " + str(tanyao_point))
        #print(eval_point_list[i])
        
        #一通ボーナス
        ittsuu_point = 0
        for j in range(3):
            ittsuu_point += ittsuu_bonus[function.ittsuu_sum_up(temp_janshi,j)]
        eval_point_list[i] += ittsuu_point 
        #print("一通ボーナス: " + str(ittsuu_point))
        #print(eval_point_list[i])
        
        #三色ボーナス
        sansyoku_point = 0
        for j in range(1,8):
            sansyoku_point += sansyoku_bonus[function.sansyoku_sum_up(temp_janshi,j)]
        eval_point_list[i] += sansyoku_point
        #print("三色ボーナス: " + str(sansyoku_point))
        
        #ホンイツボーナス
        honitsu_point = 0
        for j in range(3):
            honitsu_point += honitsu_bonus[function.honitsu_sum_up(temp_janshi,j)]
        eval_point_list[i] += honitsu_point
        #print("ホンイツボーナス: " + str(honitsu_point))
        
        #一盃口ボーナス
        yipeko_point = 0
        for j in range(3):
            yipeko_point += function.yipeko_eval(janshi, j, yipeko_param1, yipeko_param2, yipeko_param3, yipeko_param4, yipeko_param5)
        eval_point_list[i] += yipeko_point
        #print("一盃口ボーナス: " + str(yipeko_point))    
        
        #print("  トータルポイント: " + str(eval_point_list[i]))
        #print()
    eval_point_array = np.array(eval_point_list)
    normalized_eval_point_array = eval_point_array/np.sum(eval_point_array)
    return normalized_eval_point_array


