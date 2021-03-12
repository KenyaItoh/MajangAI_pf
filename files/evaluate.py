##評価用
import function
#import shanten_check
import numpy as np
import function_fuuro_convert
#import complete_sc
#import eval_yuukouhai
import eval_yuukouhai_for_naki
import eval_yuukouhai_for_naki2
import eval_yuukouhai_for_naki_kuikae
import eval_ensemble_for_kuikae
import shanten_check_new
import copy
import math
#import function_fuuro_convert

#新点数化方式
#flow.txtを参照
def eval_tehai5(janshi, taku):
    
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
    koritsu_yaochu_penalty = -0.03 #1,9
    koritsu_suuhai_penalty2 = -0.02 #2,8
    koritsu_suuhai_penalty3 = -0.01 #3~7
    koritsu_jihai_penalty = -0.04
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
    return np.argmax(eval_point_list)
                                       
        
        
        
        
        
#level1用
#maximum_indexを返す
#ドラも考慮
#鳴きは考慮しない
def eval_tehai4(janshi, taku):
    #まずシャンテン数を求める
    shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
    maximum_eval_index = False
    if shanten_suu > 2:
        maximum_eval_index = eval_tehai5(janshi, taku)
    elif shanten_suu <= 2:
        maximum_eval_index = eval_yuukouhai_for_naki.new_yuukouhai_explore(shanten_suu, janshi, taku)[0]
        
    #assert maximum_index_num
    return maximum_eval_index
    
    

#maximum_indexを返す level0用
def eval_tehai3(janshi, taku, imput_parameters): 

    #パラメータ群がFalseなら内蔵のパラメータを使う
    if imput_parameters == False:
        parameters = [6.049272498106422,
                      1.467532259578174,
                      0.9185793907656948,
                      1.2142240851561072,
                      -0.6299904909516113,
                      -0.29551434416531586,
                      -1.0,
                      4.6856576224468816,
                      4.061958]
    else:
        parameters = imput_parameters
    
    maximum_eval_point = 0.0
    maximum_eval_index = 0
    
    for i in range(len(janshi.tehai)):  
        temp_tehai = janshi.tehai.copy()
        del temp_tehai[i]
        temp_eval_point = eval_tehai2(janshi, temp_tehai, taku, parameters)
        if temp_eval_point > maximum_eval_point:
            maximum_eval_point = temp_eval_point
            maximum_eval_index = i
    return maximum_eval_index

def eval_tehai2(janshi, tehai_str, taku, parameters): #捨て牌も考慮(残り枚数も考慮)
    
    eval_point = 0.0
    tehai_eval = tehai_convert_eval(tehai_str)
    
    
    #トイツボーナス（要らないかも）
    for i in range(2, 42):
        if tehai_eval[i] >= 2:
            eval_point += parameters[7]
            break
    
    #数牌
    for i in range(2,33):
        if tehai_eval[i] > 0:
            #トイツ→1点 アンコ→5点
            if tehai_eval[i] >= 3:
                eval_point += parameters[0]
            elif tehai_eval[i] ==2:
                eval_point += parameters[1]
            
            #i-2について
            if tehai_eval[i-2] == -1:
                eval_point += parameters[5]
            elif tehai_eval[i-2] > 0: ##カンチャン
                eval_point += parameters[2]
            
            #i-1について
            if tehai_eval[i-1] == -1:
                eval_point += parameters[4]
            elif tehai_eval[i-1] > 0: #リャンメン
                eval_point += parameters[3]
            
            #i+1について
            if tehai_eval[i+1] == -1:
                eval_point += parameters[4]
            elif tehai_eval[i+1] > 0: #リャンメン
                eval_point += parameters[3]
            
            #i-2について
            if tehai_eval[i+2] == -1:
                eval_point += parameters[5]
            elif tehai_eval[i+2] > 0: ##カンチャン
                eval_point += parameters[2] 
    
    #字牌
    for i in range(35,42):
        if tehai_eval[i] > 0:       
            if tehai_eval[i] >= 3:
                eval_point += parameters[0]
            elif tehai_eval[i] == 2:
                eval_point += parameters[1]
            elif tehai_eval[i] == 1:
                eval_point += parameters[6]
    
    #テンパイボーナス　待ち牌の残り枚数に応じて減点
    if shanten_check_new.shanten_check(janshi,taku.hash_table):
        eval_point += parameters[8] #テンパイボーナス
        temp_tehai = function.tehai_convert(tehai_str)
        temp_sutehai = function.tehai_convert(taku.merge_kawa())
        tehai_plus_sutehai = [0]*38
        for i in range(len(tehai_plus_sutehai)):
            tehai_plus_sutehai[i] = temp_tehai[i] + temp_sutehai[i]
        machihai = function.find_machihai(janshi, taku.hash_table)
        nokori_maisuu = len(machihai) * 4.0
        for i in machihai:
            nokori_maisuu -= tehai_plus_sutehai[i]
        eval_point += np.sqrt(3.2*nokori_maisuu) - 5.0 #減点関数
        #print(machihai)       
    return eval_point

#2シャンテン以下でポンできる。２シャンテン以下でシャンテン維持も可
def eval_pon(janshi, taku, hai_str, janshi_list, bakyou_list):
    nokori_tsumo_kaisuu = int(taku.yama_nokori/4)
    if janshi.level == 1:
        pon_boost = 1.5
    else:
        pon_boost = math.exp((17-nokori_tsumo_kaisuu)/7.45)

    #このシャンテン数以下で鳴ける
    naki_kanou_shanten_suu = 3

    temp_shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
    if temp_shanten_suu >= naki_kanou_shanten_suu:
        shanten_iji_const = 0.5
        shanten_iji_flag = False
    else:
        shanten_iji_const = 0.7
        shanten_iji_flag = True

    akadora_flag = False
    hai_index = function.hai_convert(hai_str)
    tehai = function.tehai_convert(janshi.tehai)
    #切られた牌が赤ドラ（字牌の条件は省略できる）
    if hai_index%10 == 0:
        akadora_flag = True
        hai_index += 5
        old_shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
        
        #2シャンテン以下でポンできる
        if old_shanten_suu > naki_kanou_shanten_suu:
            return False, 0
        
        if tehai[hai_index] >= 2:
            temp_janshi = copy.deepcopy(janshi)      
            temp_janshi.fuurohai.append(function_fuuro_convert.pon_convert(temp_janshi, hai_str, 0, akadora_flag))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            
            if old_shanten_suu > new_shanten_suu:
                c = eval_yuukouhai_for_naki2.new_yuukouhai_explore(old_shanten_suu, janshi, taku) + 1  #鳴かなかったとき
                a, b = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list) #鳴いたとき
                #b = 210/(len(taku.yama)+200)*b ここの良い関数形

                #print(b*pon_boost)
                #print(c)
                if b * pon_boost > c:
                    return True, a
            if old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                c = eval_yuukouhai_for_naki2.new_yuukouhai_explore(old_shanten_suu, janshi, taku) + 1  #鳴かなかったとき
                a, b = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list) #鳴いたとき
                #b = 210/(len(taku.yama)+200)*b ここの良い関数形

                if b * shanten_iji_const > c:
                    return True, a
        
        return False, 0
    #切られた牌が5で同じ色の赤5を持っていたら（字牌の条件は省略できる）
    elif (hai_index % 10 == 5) and (tehai[hai_index-5] == 1):
        tehai[hai_index] += 1
        old_shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
        
        #2シャンテン以下でポンできる
        if old_shanten_suu > naki_kanou_shanten_suu:
            return False, 0
        
        if tehai[hai_index] >= 2:
            akadora_flag = True
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-5))
            temp_janshi.tehai.append(function.hai_convert_reverse(hai_index))
            temp_janshi.fuurohai.append(function_fuuro_convert.pon_convert(temp_janshi, hai_str, 0, akadora_flag))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            
            if old_shanten_suu > new_shanten_suu:
                c = eval_yuukouhai_for_naki2.new_yuukouhai_explore(old_shanten_suu, janshi, taku) + 1  #鳴かなかったとき
                a, b = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list) #鳴いたとき
                #b = 210/(len(taku.yama)+200)*b ここの良い関数形
                #print(b*pon_boost)
                #print(c)
                if b* pon_boost > c:
                    return True, a  

            if old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                c = eval_yuukouhai_for_naki2.new_yuukouhai_explore(old_shanten_suu, janshi, taku) + 1  #鳴かなかったとき
                a, b = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list) #鳴いたとき
                #b = 210/(len(taku.yama)+200)*b ここの良い関数形
    
                if b * shanten_iji_const > c:
                    return True, a

        return False, 0
    #その他
    else:
        old_shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
        
        #2シャンテン以下でポンできる
        if old_shanten_suu > naki_kanou_shanten_suu:
            return False, 0
        
        if tehai[hai_index] >= 2:
            temp_janshi = copy.deepcopy(janshi)      
            temp_janshi.fuurohai.append(function_fuuro_convert.pon_convert(temp_janshi, hai_str, 0, akadora_flag))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            
            if old_shanten_suu > new_shanten_suu:
                c = eval_yuukouhai_for_naki2.new_yuukouhai_explore(old_shanten_suu, janshi, taku) + 1  #鳴かなかったとき
                a, b = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list) #鳴いたとき
                #b = 210/(len(taku.yama)+200)*b ここの良い関数形
                #temp = [c, b*pon_boost]
                #print(temp)
                #print(b*pon_boost)
                #print(c)
                if b* pon_boost > c:
                    return True, a

            if old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                c = eval_yuukouhai_for_naki2.new_yuukouhai_explore(old_shanten_suu, janshi, taku) + 1  #鳴かなかったとき
                a, b = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list) #鳴いたとき
                #b = 210/(len(taku.yama)+200)*b ここの良い関数形
    
                if b * shanten_iji_const > c:
                    return True, a

        return False, 0

#[チー形式, チー後打牌, チー出しする手牌に赤があるか]
def eval_chii(janshi, taku, hai_str, janshi_list, bakyou_list):
    nokori_tsumo_kaisuu = int(taku.yama_nokori/4)
    if janshi.level == 1:
        chii_boost = 0.8
    else:
        chii_boost = math.exp(-(17-nokori_tsumo_kaisuu)/7.45)
    #print(chii_boost)

    shanten_iji_const = chii_boost * 0.7
    shanten_iji_flag = False
    #このシャンテン数以下で鳴ける
    naki_kanou_shanten_suu = 3
    
    hai_index = function.hai_convert(hai_str)
    if hai_index > 30:
        return -1, 0
    tehai = function.tehai_convert(janshi.tehai)
    akadora_flag = False
    #切られた牌が赤ドラ
    if hai_index%10 == 0:
        hai_index += 5
        akadora_flag = True
        #tehai[hai_index] += 1
        #tehai[hai_index-5] = 0
        
        old_shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)

        if old_shanten_suu > naki_kanou_shanten_suu:
            return -1, 0, False
        
        no_chii = eval_yuukouhai_for_naki2.new_yuukouhai_explore(old_shanten_suu, janshi, taku)*chii_boost + 1  #鳴かなかったとき0.9は鳴きブースト
        chii_array = np.array([no_chii, 0, 0, 0])
        dahai_array = [0, 0, 0, 0]
        
        if (tehai[hai_index -1] >= 1) and (tehai[hai_index -2] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 0, akadora_flag))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[1] = temp[1]
                dahai_array[1] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[1] = temp[1] * shanten_iji_const
                dahai_array[1] = temp[0]
                                
        if (tehai[hai_index -1] >= 1) and (tehai[hai_index +1] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 1, akadora_flag))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[2] = temp[1]
                dahai_array[2] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[2] = temp[1] * shanten_iji_const
                dahai_array[2] = temp[0]

        if (tehai[hai_index +1] >= 1) and (tehai[hai_index +2] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 2, akadora_flag))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[3] = temp[1]
                dahai_array[3] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[3] = temp[1] * shanten_iji_const
                dahai_array[3] = temp[0]

        #print(chii_array)
        max_chii_index = np.argmax(chii_array) - 1
        return max_chii_index, dahai_array[max_chii_index+1], False 
    
    #切られた牌が3でその色に赤ドラがある0→普通、1→普通、2→赤
    elif hai_index % 10 == 3 and tehai[hai_index-3] == 1:
        
        tehai[hai_index-3] = 0
        tehai[hai_index+2] += 1
        old_shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
        
        if old_shanten_suu > naki_kanou_shanten_suu:
            return -1, 0, False
        
        no_chii = eval_yuukouhai_for_naki2.new_yuukouhai_explore(old_shanten_suu, janshi, taku)*chii_boost + 1  #鳴かなかったとき
        chii_array = np.array([no_chii, 0, 0, 0])
        dahai_array = [0, 0, 0, 0]
        
        if (tehai[hai_index -1] >= 1) and (tehai[hai_index -2] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            #temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-3))
            #temp_janshi.tehai.append(function.hai_convert_reverse(hai_index+2))
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 0, False))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[1] = temp[1]
                dahai_array[1] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[1] = temp[1] * shanten_iji_const
                dahai_array[1] = temp[0]

        if (tehai[hai_index -1] >= 1) and (tehai[hai_index +1] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            #temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-3))
            #temp_janshi.tehai.append(function.hai_convert_reverse(hai_index+2))
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 1, False))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[2] = temp[1]
                dahai_array[2] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[2] = temp[1] * shanten_iji_const
                dahai_array[2] = temp[0]

        if (tehai[hai_index +1] >= 1) and (tehai[hai_index +2] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-3))
            temp_janshi.tehai.append(function.hai_convert_reverse(hai_index+2))
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 2, True))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[3] = temp[1]
                dahai_array[3] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[3] = temp[1] * shanten_iji_const
                dahai_array[3] = temp[0]

        #print(chii_array)
        max_chii_index = np.argmax(chii_array) - 1
        if max_chii_index == 2:
            return max_chii_index, dahai_array[max_chii_index+1], True
        else:
            return max_chii_index, dahai_array[max_chii_index+1], False
    
    #切られた牌が4でその色に赤ドラがある0→普通、1→赤、2→赤
    elif hai_index % 10 == 4 and tehai[hai_index-4] == 1:
        
        tehai[hai_index-4] = 0
        tehai[hai_index+1] += 1
        old_shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
        
        if old_shanten_suu > naki_kanou_shanten_suu:
            return -1, 0, False
        
        no_chii = eval_yuukouhai_for_naki2.new_yuukouhai_explore(old_shanten_suu, janshi, taku)*chii_boost + 1  #鳴かなかったとき
        chii_array = np.array([no_chii, 0, 0, 0])
        dahai_array = [0, 0, 0, 0]
        
        if (tehai[hai_index -1] >= 1) and (tehai[hai_index -2] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            #temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-4))
            #temp_janshi.tehai.append(function.hai_convert_reverse(hai_index+1))
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 0, False))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[1] = temp[1]
                dahai_array[1] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[1] = temp[1] * shanten_iji_const
                dahai_array[1] = temp[0]

        if (tehai[hai_index -1] >= 1) and (tehai[hai_index +1] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-4))
            temp_janshi.tehai.append(function.hai_convert_reverse(hai_index+1))
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 1, True))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[2] = temp[1]
                dahai_array[2] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[2] = temp[1] * shanten_iji_const
                dahai_array[2] = temp[0]

        if (tehai[hai_index +1] >= 1) and (tehai[hai_index +2] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-4))
            temp_janshi.tehai.append(function.hai_convert_reverse(hai_index+1))
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 2, True))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[3] = temp[1]
                dahai_array[3] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[3] = temp[1] * shanten_iji_const
                dahai_array[3] = temp[0]

        #print(chii_array)
        max_chii_index = np.argmax(chii_array) - 1
        if max_chii_index == 2 or max_chii_index == 1:
            return max_chii_index, dahai_array[max_chii_index+1], True
        else:
            return max_chii_index, dahai_array[max_chii_index+1], False
    
    #切られた牌が6でその色に赤ドラがある0→赤、1→赤、2→普通
    elif hai_index % 10 == 6 and tehai[hai_index-6] == 1:
        
        tehai[hai_index-6] = 0
        tehai[hai_index-1] += 1
        old_shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
        
        if old_shanten_suu > naki_kanou_shanten_suu:
            return -1, 0, False
        
        no_chii = eval_yuukouhai_for_naki2.new_yuukouhai_explore(old_shanten_suu, janshi, taku)*chii_boost + 1  #鳴かなかったとき
        chii_array = np.array([no_chii, 0, 0, 0])
        dahai_array = [0, 0, 0, 0]
        
        if (tehai[hai_index -1] >= 1) and (tehai[hai_index -2] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-6))
            temp_janshi.tehai.append(function.hai_convert_reverse(hai_index-1))
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 0, True))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[1] = temp[1]
                dahai_array[1] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[1] = temp[1] * shanten_iji_const
                dahai_array[1] = temp[0]

        if (tehai[hai_index -1] >= 1) and (tehai[hai_index +1] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-6))
            temp_janshi.tehai.append(function.hai_convert_reverse(hai_index-1))
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 1, True))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[2] = temp[1]
                dahai_array[2] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[2] = temp[1] * shanten_iji_const
                dahai_array[2] = temp[0]

        if (tehai[hai_index +1] >= 1) and (tehai[hai_index +2] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            #temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-6))
            #temp_janshi.tehai.append(function.hai_convert_reverse(hai_index-1))
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 2, False))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[3] = temp[1]
                dahai_array[3] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[3] = temp[1] * shanten_iji_const
                dahai_array[3] = temp[0]
                
        #print(chii_array)
        max_chii_index = np.argmax(chii_array) - 1
        if max_chii_index == 0 or max_chii_index == 1:
            return max_chii_index, dahai_array[max_chii_index+1], True
        else:
            return max_chii_index, dahai_array[max_chii_index+1], False
    
    #切られた牌が7でその色に赤ドラがある0→赤、1→普通、2→普通
    elif hai_index % 10 == 7 and tehai[hai_index-7] == 1:
        
        tehai[hai_index-7] = 0
        tehai[hai_index-2] += 1
        old_shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
        
        if old_shanten_suu > naki_kanou_shanten_suu:
            return -1, 0, False
        no_chii = eval_yuukouhai_for_naki2.new_yuukouhai_explore(old_shanten_suu, janshi, taku)*chii_boost + 1  #鳴かなかったとき
        chii_array = np.array([no_chii, 0, 0, 0])
        dahai_array = [0, 0, 0, 0]
        
        if (tehai[hai_index -1] >= 1) and (tehai[hai_index -2] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-7))
            temp_janshi.tehai.append(function.hai_convert_reverse(hai_index-2))
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 0, True))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[1] = temp[1]
                dahai_array[1] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[1] = temp[1] * shanten_iji_const
                dahai_array[1] = temp[0]

        if (tehai[hai_index -1] >= 1) and (tehai[hai_index +1] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            #temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-7))
            #temp_janshi.tehai.append(function.hai_convert_reverse(hai_index-2))
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 1, False))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[2] = temp[1]
                dahai_array[2] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[2] = temp[1] * shanten_iji_const
                dahai_array[2] = temp[0]

        if (tehai[hai_index +1] >= 1) and (tehai[hai_index +2] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            #temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-7))
            #temp_janshi.tehai.append(function.hai_convert_reverse(hai_index-2))
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 2, False))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[3] = temp[1]
                dahai_array[3] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[3] = temp[1] * shanten_iji_const
                dahai_array[3] = temp[0]

        #print(chii_array)
        max_chii_index = np.argmax(chii_array) - 1
        if max_chii_index == 0:
            return max_chii_index, dahai_array[max_chii_index+1], True
        else:
            return max_chii_index, dahai_array[max_chii_index+1], False
    
    #それ以外
    else:
        old_shanten_suu = shanten_check_new.shanten_check(janshi, taku.hash_table)
    
        if old_shanten_suu > naki_kanou_shanten_suu:
            return -1, 0, False
        
        no_chii = eval_yuukouhai_for_naki2.new_yuukouhai_explore(old_shanten_suu, janshi, taku)*chii_boost + 1  #鳴かなかったとき
        chii_array = np.array([no_chii, 0, 0, 0])
        dahai_array = [0, 0, 0, 0]
        
        if (hai_index % 10 >= 3) and (tehai[hai_index -1] >= 1) and (tehai[hai_index -2] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 0, False))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[1] = temp[1]
                dahai_array[1] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[1] = temp[1] * shanten_iji_const
                dahai_array[1] = temp[0]
                       
        if (hai_index % 10 >= 2) and (hai_index % 10 <= 8) and (tehai[hai_index -1] >= 1) and (tehai[hai_index +1] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 1, False))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[2] = temp[1]
                dahai_array[2] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[2] = temp[1] * shanten_iji_const
                dahai_array[2] = temp[0]

        if (hai_index % 10 <= 7) and (tehai[hai_index +1] >= 1) and (tehai[hai_index +2] >= 1):
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.fuurohai.append(function_fuuro_convert.chii_convert(temp_janshi, hai_str, 2, False))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            kuikae_list = function.kuikae_convert(temp_janshi.fuurohai[-1])
            if old_shanten_suu > new_shanten_suu:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[3] = temp[1]
                dahai_array[3] = temp[0]
            elif old_shanten_suu == new_shanten_suu and shanten_iji_flag:
                temp = eval_ensemble_for_kuikae.eval_tehai_ens(old_shanten_suu, temp_janshi, taku, kuikae_list, janshi_list, bakyou_list)
                chii_array[3] = temp[1] * shanten_iji_const
                dahai_array[3] = temp[0]

        #print(chii_array)
        max_chii_index = np.argmax(chii_array) - 1
        return max_chii_index, dahai_array[max_chii_index+1], False

def eval_ankan(janshi, taku):
    temp_tehai = function.tehai_convert(janshi.tehai)
    for i in range(len(temp_tehai)):
        if temp_tehai[i] == 4:
            temp_janshi = copy.deepcopy(janshi)
            old_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            temp_janshi.ankan_list.append(function_fuuro_convert.ankan_convert(temp_janshi, function.hai_convert_reverse(i)))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            if old_shanten_suu == new_shanten_suu:
                return i
        #5が3枚以上あって同じ色の赤ドラがある場合
        elif i%10 == 5 and temp_tehai[i] ==3 and temp_tehai[i-5] == 1:
            temp_janshi = copy.deepcopy(janshi)
            temp_janshi.tehai.remove(function.hai_convert_reverse(i-5))
            temp_janshi.tehai.append(function.hai_convert_reverse(i))
            old_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            temp_janshi.ankan_list.append(function_fuuro_convert.ankan_convert(temp_janshi, function.hai_convert_reverse(i)))
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            if old_shanten_suu == new_shanten_suu:
                return i
    return -1

#[カカンする副露インデックス, カカンする牌インデックス、カカンするのが赤ドラかどうか]
def eval_kakan(janshi, taku):
    temp_fuurohai = janshi.fuurohai
    temp_tehai = function.tehai_convert(janshi.tehai)
    for i in range(len(temp_fuurohai)):
        if temp_fuurohai[i][0] == 2 and temp_tehai[temp_fuurohai[i][1]] > 0:
            temp_janshi = copy.deepcopy(janshi)
            old_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            temp_janshi.fuurohai[i] = function_fuuro_convert.kakan_convert(temp_janshi, function.hai_convert_reverse(temp_fuurohai[i][1]), i)
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            if old_shanten_suu == new_shanten_suu:
                kakan_conducted_point = eval_yuukouhai_for_naki2.new_yuukouhai_explore(new_shanten_suu, temp_janshi, taku)
                temp_janshi2 = copy.deepcopy(janshi)
                kakan_not_conducted_point = eval_yuukouhai_for_naki.new_yuukouhai_explore(new_shanten_suu, temp_janshi2, taku)[1]
                if kakan_conducted_point >= kakan_not_conducted_point:
                    return [i, temp_fuurohai[i][1], False]
        #5をポンしていて同じ色の赤5を持ってきた場合
        elif temp_fuurohai[i][1]%5 == 5 and temp_fuurohai[i][0] == 2 and temp_tehai[temp_fuurohai[i][1]-5] == 1:
            temp_janshi = copy.deepcopy(janshi)
            old_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            hai_index = temp_fuurohai[i][1]
            temp_janshi.tehai.remove(function.hai_convert_reverse(hai_index-5))
            temp_janshi.tehai.append(function.hai_convert_reverse(hai_index))
            temp_janshi.fuurohai[i] = function_fuuro_convert.kakan_convert(temp_janshi, function.hai_convert_reverse(temp_fuurohai[i][1]), i)
            new_shanten_suu = shanten_check_new.shanten_check(temp_janshi, taku.hash_table)
            if old_shanten_suu == new_shanten_suu:
                kakan_conducted_point = eval_yuukouhai_for_naki2.new_yuukouhai_explore(new_shanten_suu, temp_janshi, taku)
                temp_janshi2 = copy.deepcopy(janshi)
                kakan_not_conducted_point = eval_yuukouhai_for_naki.new_yuukouhai_explore(new_shanten_suu, temp_janshi2, taku)[1]
                if kakan_conducted_point >= kakan_not_conducted_point:
                    return [i, temp_fuurohai[i][1], True]
    return [-1, 0, False]

#とりあえずダイミンカンはしない
def eval_daiminkan(janshi, taku, hai_str):
    return False
    
    
def str_to_num_eval(hai_str):
    str_to_num = {"1m":2, "2m":3, "3m":4, "4m":5, "5m":6, "6m":7, "7m":8, "8m":9, "9m":10, "1p":13, "2p":14, "3p":15, "4p":16, "5p":17, "6p":18, "7p":19, "8p":20, "9p":21, "1s":24, "2s":25, "3s":26, "4s":27, "5s":28, "6s":29, "7s":30, "8s":31, "9s":32, "1z":35, "2z":36, "3z":37, "4z":38, "5z":39, "6z":40, "7z":41}
    return str_to_num[hai_str]   

def tehai_convert_eval(tehai_str): #評価用の手牌コンバート
    
    #tehai_eval初期化
    tehai_eval = [0]*42
    #牌の入らないところには-1
    tehai_eval[0] = -1
    tehai_eval[1] = -1
    tehai_eval[11] = -1
    tehai_eval[12] = -1
    tehai_eval[22] = -1
    tehai_eval[23] = -1
    tehai_eval[33] = -1
    tehai_eval[34] = -1
    
    #書き換え
    for i in range(len(tehai_str)):
        tehai_eval[str_to_num_eval(tehai_str[i])] += 1
        
    return tehai_eval


##################以下使ってない
             
def eval_shanten(shanten_suu): #シャンテン数を評価（使ってない）
    
    if shanten_suu == 0:
        eval_point = 5
    elif shanten_suu == 1:
        eval_point = 3
    elif shanten_suu == 2:
        eval_point = 1
    else:
        eval_point = 0
        
    return eval_point            
                
    
    
def eval_tehai(tehai_str, parameters):
    
    eval_point = 0.0
    tehai_eval = tehai_convert_eval(tehai_str)
    
    
    for i in range(2, 42):
        if tehai_eval[i] >= 2:
            eval_point += parameters[7]
            break
    
    for i in range(2,33):
        if tehai_eval[i] > 0:
            #トイツ→1点 アンコ→5点
            if tehai_eval[i] >= 3:
                eval_point += parameters[0]
            elif tehai_eval[i] ==2:
                eval_point += parameters[1]
            
            #i-2について
            if tehai_eval[i-2] == -1:
                eval_point += parameters[5]
            elif tehai_eval[i-2] > 0: ##カンチャン
                eval_point += parameters[2]
            
            #i-1について
            if tehai_eval[i-1] == -1:
                eval_point += parameters[4]
            elif tehai_eval[i-1] > 0: #リャンメン
                eval_point += parameters[3]
            
            #i+1について
            if tehai_eval[i+1] == -1:
                eval_point += parameters[4]
            elif tehai_eval[i+1] > 0: #リャンメン
                eval_point += parameters[3]
            
            #i-2について
            if tehai_eval[i+2] == -1:
                eval_point += parameters[5]
            elif tehai_eval[i+2] > 0: ##カンチャン
                eval_point += parameters[2] 
    
    for i in range(35,42):
        if tehai_eval[i] > 0:
            #トイツ→1点 アンコ→4点
            if tehai_eval[i] >= 3:
                eval_point += parameters[0]
            elif tehai_eval[i] == 2:
                eval_point += parameters[1]
            elif tehai_eval[i] == 1:
                eval_point += parameters[6]
    
    if function.tenpai_hantei(tehai_str):
        eval_point += parameters[8]
    
    return eval_point
        
'''          
def evaluate_test(tehai_str, sutehai, parameters):
        maximam_eval_point = 0
        maximam_index = 0
        #self.shanten_suu = function.shanten_check(self.tehai)
        if function.agari_hantei(tehai_str):
            return -1
        else:
            for i in range(len(tehai_str)):
                temp_tehai = tehai_str.copy()                
                del temp_tehai[i]
                #temp_shanten_suu = function.shanten_check(temp_tehai)
                eval_point = eval_tehai2(temp_tehai, sutehai, parameters) # + evaluate.eval_shanten(temp_shanten_suu)
                if eval_point > maximam_eval_point:
                    maximam_eval_point = eval_point
                    maximam_index = i
        
        return maximam_index
'''

#parameters = [5.195317515099803, 1.304086483374882, 1.0428673149449136, 1.2432482015998434, -0.6789857316369717, -0.3190732524485256, -1.3291062522937311, 4.823759635706856, 3.0]
#sutehai = ['5z', '7z', '3z', '1p', '1m', '3s', '7s', '7m', '6s', '1m', '2m', '6m']
#print(evaluate_test(['6m', '7m', '8m', '3p', '4p', '5p', '7p', '8p', '9p', '9p', '8s', '8s', '8s', '4m'], sutehai, parameters))