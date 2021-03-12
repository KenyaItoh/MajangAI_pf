#食い変え対応版　引数に食い変えリストを取る
#戻り値は[normalized_sum_list, sum_list]
import evaluate
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
import mentsu_count
import defense
import eval_keiten
import danger_degree

def eval_tehai_ens(old_shanten_suu, janshi, taku, kuikae_list, janshi_list_taple, bakyou_list):
    janshi_list = copy.deepcopy(janshi_list_taple)
    janshi_list[0] = janshi
    #まずシャンテン数を求める
    shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
    maximum_eval_index = False 
    if shanten_suu > 2:
        maximum_eval_index = np.argmax(eval_tehai_point(janshi, taku))

    else: # shanten_suu <= 2:
        point = np.array(eval_tehai_point(janshi, taku))
        point_temp = copy.deepcopy(point)
        top4_list = []
        if shanten_suu == 2:
            yuukou_sutehai_temp = find_yuukou_sutehai(janshi, 2, taku.hash_table)
            temp_count = 0
            while temp_count < 4:
                if max(point_temp) == 0:
                    break
                max_arg = np.argmax(point_temp)
                add_index = function.hai_convert(janshi.tehai[max_arg])
                if add_index in top4_list or not (add_index in yuukou_sutehai_temp):
                    point_temp[max_arg] = 0
                else:
                    top4_list.append(add_index)
                    point_temp[max_arg] = 0
                    temp_count += 1
                
        #print(top4_list)
        yuukouhai = new_yuukouhai_explore(shanten_suu, janshi, taku, kuikae_list, top4_list, janshi_list, bakyou_list)

        for i in range(len(yuukouhai[0])):
            if yuukouhai[0][i] == 0:
                point[i] = 0

        point = point/np.sum(point)
        point = point**3
        point = point/np.sum(point)
        point = point**3
        point = point/np.sum(point)

        temp = yuukouhai[0] + point
        temp_max = np.max(temp)
        pure_point_list = yuukouhai[5]

        #temp_minを求める
        temp_min = 10000
        for i in range(len(pure_point_list)):
            if temp_min > pure_point_list[i] and pure_point_list[i] != 0:
                temp_min = pure_point_list[i]
        
        for i in range(len(pure_point_list)):
            if pure_point_list[i] == 0:
                pure_point_list[i] = temp_min

        defense_point = np.array(defense.eval_defense(janshi_list, taku, shanten_suu, temp_max, pure_point_list, bakyou_list))
        keiten_point = np.array(eval_keiten.eval_keiten(shanten_suu, janshi, taku, temp_max))
        keiten_list = np.array(eval_keiten.create_keiten_list(shanten_suu, janshi, taku))
        #元からテンパイしてたとき
        if old_shanten_suu == 0:
            keiten_list *= 0

        #print(keiten_list)

        tehai_point_list = yuukouhai[0] + point + defense_point + keiten_point
        #print(yuukouhai)
        #print(point)
        #print(tehai_point_list)
        maximum_eval_index = np.argmax(tehai_point_list)
        maximum_eval_index = int(maximum_eval_index)
        maximum_eval_hai_str = janshi.tehai[maximum_eval_index]
        maximum_eval_expect = yuukouhai[2][maximum_eval_index] + keiten_list[maximum_eval_index]

        #print(yuukouhai)

        if bakyou_list[0]:
            #オーラスでラス目
            if bakyou_list[0] == 4:
                if yuukouhai[3][maximum_eval_index] > bakyou_list[1] and yuukouhai[4][maximum_eval_index] > bakyou_list[1]*0.5:
                    maximum_eval_expect += 100000

        #print(type(maximum_eval_index))
    return maximum_eval_hai_str, maximum_eval_expect


#切る前の状態から始める 食い変え対応
def new_yuukouhai_explore(shanten_suu, janshi, taku, kuikae_list, top4_list, janshi_list, bakyou_list):
    hash_table = taku.hash_table
    tehai = np.array(function.tehai_convert(janshi.tehai))
    danger_degree_list = danger_degree.create_danger_degree_list(janshi_list, taku, bakyou_list)
    #print(danger_degree_list)
    
    #ツモって来る牌に赤ドラは考慮しない
    yama = np.array(function.tehai_convert(function.akadora_convert(janshi.vertual_yama)[0]))    
    init_shanten_suu = shanten_suu
    #index_list = [0]*len(tehai)
    sum_list = [0]*len(tehai)
    pure_point_sum = [0]*len(tehai)
    pure_pure_point_sum = [0]*len(tehai)
    max_point = [0]*len(tehai)
    #mean_list = [0]*len(tehai)
    if init_shanten_suu >= 2:
        hai_list = top4_list
    else:
        hai_list = find_yuukou_sutehai(janshi, init_shanten_suu, hash_table)
    #print(hai_list)

    #hai_listからkuikae_listを削除
    temp_hai_list = hai_list.copy()
    for i in range(len(hai_list)):
        if temp_hai_list[i] in kuikae_list:
            hai_list.remove(temp_hai_list[i])

    #副露した時でアガリ役なしの場合
    if len(hai_list) == 0:
        #print("no_hai_list_error")
        return [0.001]*len(janshi.tehai), [0.001]*len(janshi.tehai), [0.001]*len(janshi.tehai), [0.001]*len(janshi.tehai), [0.001]*len(janshi.tehai), [0.001]*len(janshi.tehai)
    
    #バグ防止用
    for i in hai_list:
        sum_list[i] += 0.001
    
    #print(hai_list)
    if init_shanten_suu >= 2:
        itr = 20
    else:
        itr = 25

    for i in hai_list:
        for j in range(itr):
            count = 1.
            temp_janshi = copy.deepcopy(janshi)
            temp_yama = yama.copy()      
            temp_janshi.tehai.remove(function.hai_convert_reverse(i))
            temp_janshi.sutehai.append(function.hai_convert_reverse(i))
            #評価用の修正されたpoint, 普通の点数
            a, b, c = yuukouhai_explore(temp_yama, init_shanten_suu, count, hash_table, temp_janshi, taku , janshi_list, bakyou_list, danger_degree_list)
            #オーラス用max_pointの更新など
            if b > max_point[i]:
                max_point[i] = b
            pure_point_sum[i] += b
            pure_pure_point_sum[i] += c
                        
            #index_list[i] += 1
            sum_list[i] += a
        pure_pure_point_sum[i] /= max(init_shanten_suu + 1, 1)*itr


    normalized_index_list = np.array(sum_list)/np.sum(np.array(sum_list))
    normalized_list = np.zeros(len(janshi.tehai))
    sum_list_for_tehai_str = np.zeros(len(janshi.tehai))
    pure_point_mean = np.array(pure_point_sum)/float(itr)
    max_point_list = np.zeros(len(janshi.tehai))
    pure_point_mean_list = np.zeros(len(janshi.tehai))
    pure_point_sum_for_tehai_str = np.zeros(len(janshi.tehai))

    for i in range(len(janshi.tehai)):
        normalized_list[i] = normalized_index_list[function.hai_convert(janshi.tehai[i])]
        sum_list_for_tehai_str[i] = sum_list[function.hai_convert(janshi.tehai[i])]
        max_point_list[i] = max_point[function.hai_convert(janshi.tehai[i])]
        pure_point_mean_list[i] = pure_point_mean[function.hai_convert(janshi.tehai[i])]
        pure_point_sum_for_tehai_str[i] = pure_pure_point_sum[function.hai_convert(janshi.tehai[i])]

    mean_list_for_tehai_str = sum_list_for_tehai_str/float(itr)
   
    return normalized_list, sum_list_for_tehai_str, mean_list_for_tehai_str, max_point_list, pure_point_mean_list, pure_point_sum_for_tehai_str

def yuukouhai_explore(yama, shanten_suu, count, hash_table, janshi, taku , janshi_list, bakyou_list, danger_degree_list):
    
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
        count *= yuukouhai_num**(yuukouhai_boost)/shanten_const/danger_degree_list[function.akadora_hai_convert2(index)]*furiten_hosei
        #print(yuukouhai_num)
        #print(np.sum(yama))
    else:
        count *= yuukouhai_num/shanten_const/danger_degree_list[function.akadora_hai_convert2(index)]*furiten_hosei
    yama[index] -= 1
    
    shanten_suu -= 1
    
    if shanten_suu == -1:
        agarihai_str = function.hai_convert_reverse(index)
        #ロンアガリを想定（三暗刻防止）
        del janshi.tehai[-1]
        point_temp = tensu_calc.tensu_calc(janshi, taku, agarihai_str)
        if len(point_temp) == 0:
            point = 0
        else:
            point = point_temp[0]
        #print(point)
        #print(count*point)
        if point > 0:
            #条件判断用
            fixed_point = point + taku.kyoutaku_tensuu + taku.kaze_honba[1] * 300.0
        else:
            fixed_point = point
        return count * point, fixed_point, point
    
    yuukou_sutehai_index_list = find_yuukou_sutehai(janshi, shanten_suu, hash_table) 
    index2 = random.choice(yuukou_sutehai_index_list)
    janshi.tehai.remove(function.hai_convert_reverse(index2))
    return yuukouhai_explore(yama, shanten_suu, count, hash_table, janshi, taku, janshi_list, bakyou_list, danger_degree_list)


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

    #デバッグモード
    debug_mode = False
    
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
    dora_bonus0 = 1.1   #ドラインデックスの牌
    dora_bonus1 = 0.6 #ドラインデックス前後の牌
    dora_bonus2 = 0.3 #ドラインデックスから2枚離れた牌
    yakuhai_bonus = [0, 0.2, 0.7, 1.2] #0枚～3枚以上
    ryanmen_bonus = 0.3
    penchan_penalty = -0.5
    koritsu_yaochu_penalty = -0.25 #1,9
    koritsu_suuhai_penalty2 = -0.05 #2,8
    koritsu_suuhai_penalty3 = -0.01 #3~7
    koritsu_jihai_penalty = -0.33
    koritsu_nokori_yakuhai_penalty = [-0.5, -0.35, -0.2, 0.0]
    toitsu_nokori_yakuhai_penalty = [-1.2, -0.7, 0.0, 0.0]
    koritsu_nokori_jihai_penalty = [-0.3, -0.2, -0.1, 0.0]
    toitsu_nokori_jihai_penalty = [-0.4, -0.3, 0.0, 0.0]
    tanyao_bonus = [0,0,0,0,0,0,0,0,0,0,0,0.3,0.6,1.0]
    ittsuu_bonus = [0,0,0,0,0,0,0.3,0.7,1.1,1.4]
    sansyoku_bonus = [0,0,0,0,0,0,0.2,0.8,1.2,1.55]
    honitsu_bonus = [0,0,0,0,0,0,0,0,0,0,1.0,2.0,4.0,6.0]
    yipeko_param1 = 1.0 #222
    yipeko_param2 = 0.8 #122, 221
    yipeko_param3 = 0.6 #212
    yipeko_param4 = 0.5 #212(1,9含む)
    yipeko_param5 = 0.4 #221, 122(1,9含む)
    furiten_penalty = [-0.2, -0.5, -0.2]
    furiten_penalty_for_yuukouhai = -0.4
    mentsu_bonus = 1.0
    
    #メイン
    eval_point_list = [0]*len(janshi.tehai)
    old_shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
    for i in range(len(janshi.tehai)):
        
        if debug_mode:
            print("捨てる牌: " + janshi.tehai[i])
        
        #コピーして手牌を1つ削除
        temp_janshi = copy.deepcopy(janshi)
        temp_janshi.sutehai.append(temp_janshi.tehai[i])
        del temp_janshi.tehai[i]
        
        #赤ドラだけ抜き出してあとは赤ナシで考える
        temp = function.akadora_convert(temp_janshi.tehai)
        akadora_maisuu = temp[1]
        temp_janshi.tehai = temp[0]
        tehai = function.tehai_convert(temp_janshi.tehai)
        
        #vertual_yama
        vertual_yama_index = function.tehai_convert(temp_janshi.vertual_yama)
        #print(vertual_yama_index)
        
        #メンツカウント
        mentsu_suu = mentsu_count.mentsu_count(temp_janshi)
        mentsu_point = mentsu_suu*mentsu_bonus
        eval_point_list[i] += mentsu_point
        if debug_mode:
            print("メンツボーナス: " + str(mentsu_point))

        #シャンテン数関連
        
        new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
        if old_shanten_suu == new_shanten_suu:
            eval_point_list[i] += shanten_bonus
            if debug_mode:
                print("シャンテンアップボーナス: " + str(shanten_bonus))
        else:
            if debug_mode:
                print("シャンテンアップボーナス: " + str(0))
        #print(eval_point_list[i])
        
        #有効牌関連
        yuukouhai_maisuu = function.calc_yuukouhai_maisuu(temp_janshi, new_shanten_suu, taku.hash_table)
        yuukouhai_point = ((yuukouhai_maisuu/(len(temp_janshi.vertual_yama)/123.0*mean_list[new_shanten_suu]))**yuukouhai_pow_const)*yuukouhai_bonus
        eval_point_list[i] += yuukouhai_point
        if debug_mode:
            print("有効牌ボーナス: " + str(yuukouhai_point))
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
        if debug_mode:
            print("ドラボーナス: " +str(dora_point))
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
        if debug_mode:
            print("役牌ボーナス: " + str(yakuhai_point))
        #print(eval_point_list[i])
        
        #リャンメンボーナス（テスト）
        ryanmen_point = 0
        for j in range(30):
            if 2 <= j % 10 <= 7:
                if tehai[j-1] == 0 and tehai[j] >= 1 and tehai[j+1] >= 1 and tehai[j+2] ==0:
                    ryanmen_point += ryanmen_bonus
        eval_point_list[i] += ryanmen_point
        if debug_mode:
            print("リャンメンボーナス: " + str(ryanmen_point))
        #print(eval_point_list[i])
        
        #ペンチャンペナルティ
        penchan_point = 0
        for j in range(30):
            if j%10 == 1 or j%10 == 8:
                if tehai[j-1] == 0  and tehai[j] == 1 and tehai[j+1] == 1 and tehai[j+2] ==0:
                    penchan_point += penchan_penalty
                elif tehai[j-1] == 0  and tehai[j] >= 1 and tehai[j+1] >= 1 and tehai[j+2] ==0:
                    penchan_point += penchan_penalty*0.1
        if debug_mode:
            print("ペンチャンペナルティ: " + str(penchan_point))
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
        if debug_mode:
            print("孤立数牌ペナルティ: " + str(koritsu_suuhai_point))
        eval_point_list[i] += koritsu_jihai_point
        if debug_mode:
            print("孤立字牌ペナルティ: " + str(koritsu_jihai_point))
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
        if debug_mode:
            print("フリテンペナルティ: " + str(furiten_point))      
           
        #タンヤオボーナス
        tanyao_point = 0
        tanyao_sum = function.tanyao_sum_up(temp_janshi)
        tanyao_point = tanyao_bonus[tanyao_sum]
        eval_point_list[i] += tanyao_point
        if debug_mode:
            print("タンヤオボーナス: " + str(tanyao_point))
        #print(eval_point_list[i])
        
        #一通ボーナス
        ittsuu_point = 0
        for j in range(3):
            ittsuu_point += ittsuu_bonus[function.ittsuu_sum_up(temp_janshi,j)]
        eval_point_list[i] += ittsuu_point 
        if debug_mode:
            print("一通ボーナス: " + str(ittsuu_point))
        #print(eval_point_list[i])
        
        #三色ボーナス
        sansyoku_point = 0
        for j in range(1,8):
            sansyoku_point += sansyoku_bonus[function.sansyoku_sum_up(temp_janshi,j)]
        eval_point_list[i] += sansyoku_point
        if debug_mode:
            print("三色ボーナス: " + str(sansyoku_point))
        
        #ホンイツボーナス
        honitsu_point = 0
        for j in range(3):
            honitsu_point += honitsu_bonus[function.honitsu_sum_up(temp_janshi,j)]
        eval_point_list[i] += honitsu_point
        if debug_mode:
            print("ホンイツボーナス: " + str(honitsu_point))
        
        #一盃口ボーナス
        yipeko_point = 0
        for j in range(3):
            yipeko_point += function.yipeko_eval(janshi, j, yipeko_param1, yipeko_param2, yipeko_param3, yipeko_param4, yipeko_param5)
        eval_point_list[i] += yipeko_point
        if debug_mode:
            print("一盃口ボーナス: " + str(yipeko_point))    
        
        if debug_mode:
            print("  トータルポイント: " + str(eval_point_list[i]))
            print()
    eval_point_array = np.array(eval_point_list)
    normalized_eval_point_array = eval_point_array/np.sum(eval_point_array)
    return normalized_eval_point_array


