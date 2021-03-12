import function
import math
from copy import deepcopy as copy

#本体

def teyaku_check(janshi,taku,agarihai_str:[str]):

    #janshi,takuオブジェクトを引数に、そのjanshiのアガリ手牌の[符数,翻数,役リスト]を出力する。翻数（n倍役満:-n、役なし:0)
    #アガリ牌はjanshi.tehaiに含めて入力。
    fusuu = 20
    hansuu = 0
    yaku_list = []
    
    #変数の整理
    tehai_akadora = function.akadora_convert(janshi.tehai)[1]
    tehai_str = function.akadora_convert(janshi.tehai)[0]
    fuurohai = janshi.fuurohai
    ankan = janshi.ankan_list
    fuurosu = len(fuurohai) + len(ankan)
    tehai_plus_fuuro_len = len(tehai_str) + fuurosu * 3
    assert 13 <= tehai_plus_fuuro_len <= 14
    if  tehai_plus_fuuro_len == 13:
        if function.hai_convert(agarihai_str) % 10 == 0:
            tehai_akadora += 1
            agarihai_str = function.akadora_hai_convert(agarihai_str)
        tehai_str.append(agarihai_str)
        tsumoagari = False
    else :
        assert agarihai_str in janshi.tehai
        if function.hai_convert(agarihai_str) % 10 == 0:
            agarihai_str = function.akadora_hai_convert(agarihai_str)
        tsumoagari = True
    tehai = tehai_fuuro_mix_convert(tehai_str,janshi.fuurohai,janshi.ankan_list)
    tehai_exc_fuuro = tehai_str
    riichi = janshi.riichi
    ippatsu = janshi.ippatsu_flag
    rinshan = janshi.rinshan_flag
    zikaze = janshi.kaze
    first_tsumo = janshi.first_tsumo_flag
    fuuro_akadora = janshi.fuuro_akadora_list
    chankan = taku.chankan_flag
    haitei = taku.haitei_flag
    is_fuuro = Is_fuuro(fuurohai)
    #場風
    cnv = [0,0,0,0,1,1,1,1,2,2,2,2]
    bakaze = cnv[taku.kaze_honba[0]]
    #ドラ表示→ドラ
    str_to_num = {"5M":0, "5P":10, "5S":20, "1m":1, "2m":2, "3m":3, "4m":4, "5m":5, "6m":6, "7m":7, "8m":8, "9m":9, "1p":11, "2p":12, "3p":13, "4p":14, "5p":15, "6p":16, "7p":17, "8p":18, "9p":19, "1s":21, "2s":22, "3s":23, "4s":24, "5s":25, "6s":26, "7s":27, "8s":28, "9s":29, "1z":31, "2z":32, "3z":33, "4z":34, "5z":35, "6z":36, "7z":37}
    dorah = [taku.dorahyouji,taku.uradorahyouji]
    #dora = [[ドラリスト],[裏ドラリスト]]
    dora = [[],[]]
    for i in range(0,2):
        for j in dorah[i]:
            j2 = str_to_num[j]
            if (j2 == 9) or (j2 == 19) or(j2 == 29):
                dora[i].append(j2-8)
            elif j2 == 34:
                dora[i].append(31)
            elif j2 == 37:
                dora[i].append(35)
            elif j2 % 10 == 0:
                dora[i].append(j2+6)
            else:
                dora[i].append(j2+1)              
    agarihai = str_to_num[agarihai_str]
    fanpai = [tehai[31],tehai[32],tehai[33],tehai[34]]
    sangenpai = [tehai[35],tehai[36],tehai[37]]
        

    #アガリ形の判別（国士形:2、七対形:1、四面子一雀頭形:0、アガってない:-1)
    agari_kei = -1
    #国士形かどうか
    kokushi_flag = True
    kokushi_l = [1,9,11,19,21,29,31,32,33,34,35,36,37]
    for i in kokushi_l:
        if tehai[i] == 0:
            kokushi_flag = False
    if kokushi_flag == True:
        agari_kei = 2
    #七対形かどうか
    chiitoi_flag = True
    for i in range(1,38):
        if tehai[i] == 1 or tehai[i] >= 3 :
            chiitoi_flag = False
    if chiitoi_flag == True:
        agari_kei = 1    
    #四面子一雀頭形の場合、雀頭と面子に分解して変換
    jm_list = jm_convert(tehai_exc_fuuro,fuurohai,ankan)
    if jm_list != []:
        agari_kei = 0
    if agari_kei == -1:
        return [0,0,[]]

    #個別の役について判定する
    #役満役
    yakuman = 0
    #天和
    if first_tsumo:
        yaku_list.append("天和")
        yakuman += 1
    #字一色
    if inc(tehai,'000000000 000000000 000000000 1111111'):
        yaku_list.append("字一色")
        yakuman += 1
    #緑一色
    if inc(tehai,'000000000 000000000 011101010 0000010'):
        yaku_list.append("緑一色")
        yakuman += 1
    #清老頭
    if inc(tehai,'100000001 100000001 100000001 0000000'):
        yaku_list.append("清老頭")
        yakuman += 1
    #大三元
    sangenpai = [tehai[35],tehai[36],tehai[37]]
    if sangenpai[0] >= 3 and sangenpai[1] >= 3 and sangenpai[2] >= 3:
        yaku_list.append("大三元")
        yakuman += 1
    #小四喜
    fanpai = [tehai[31],tehai[32],tehai[33],tehai[34]]
    if (fanpai[0] == 2 and fanpai[1] >= 3 and fanpai[2] >= 3 and fanpai[3] >= 3) or\
        (fanpai[0] >= 3 and fanpai[1] == 2 and fanpai[2] >= 3 and fanpai[3] >= 3) or\
            (fanpai[0] >= 3 and fanpai[1] >= 3 and fanpai[2] == 2 and fanpai[3] >= 3) or\
                (fanpai[0] >= 3 and fanpai[1] >= 3 and fanpai[2] >= 3 and fanpai[3] == 2):
        yaku_list.append("小四喜")
        yakuman +=1
    #大四喜
    fanpai = [tehai[31],tehai[32],tehai[33],tehai[34]]
    if fanpai[0] >= 3 and fanpai[1] >= 3 and fanpai[2] >= 3 and fanpai[3] >= 3:
        yaku_list.append("大四喜")
        yakuman +=1
    #九蓮宝橙:萬子
    tyuuren_flag = True
    if not inc(tehai,'111111111 000000000 000000000 0000000'):
        tyuuren_flag = False
    for i in range(1,10):
        if i == (1 or 9):
            if tehai[i] < 3:
                tyuuren_flag = False
        if tehai[i] == 0:
            tyuuren_flag = False
    if tyuuren_flag == True and is_fuuro == False:
        yaku_list.append("九蓮宝橙")
        yakuman += 1
    #九蓮宝橙:筒子
    tyuuren_flag = True
    if not inc(tehai,'000000000 111111111 000000000 0000000'):
        tyuuren_flag = False
    for i in range(11,20):
        if i == (11 or 19):
            if tehai[i] < 3:
                tyuuren_flag = False
        if tehai[i] == 0:
            tyuuren_flag = False
    if tyuuren_flag == True and is_fuuro == False:
        yaku_list.append("九蓮宝橙")
        yakuman += 1
    #九蓮宝橙:索子
    tyuuren_flag = True
    if not inc(tehai,'000000000 000000000 111111111 0000000'):
        tyuuren_flag = False
    for i in range(21,30):
        if i == (21 or 29):
            if tehai[i] < 3:
                tyuuren_flag = False
        if tehai[i] == 0:
            tyuuren_flag = False
    if tyuuren_flag == True and is_fuuro == False:
        yaku_list.append("九蓮宝橙")
        yakuman += 1
    #四槓子
    if agari_kei == 0:
        for jm in jm_list:    
            suukantsu_flag = True
            for m in jm[1]:
                if m[1] != 2:
                    suukantsu_flag = False
            if suukantsu_flag ==True:
                yaku_list.append("四槓子")
                yakuman += 1
    #四暗刻
    if agari_kei == 0:
        for jm in jm_list:           
            suuankou_flag = True
            for m in jm[1]:
                if m[0]!=0 or m[1] == 0:
                    suuankou_flag = False
            if not tsumoagari and jm[0] != agarihai:
                suuankou_flag = False
            if suuankou_flag ==True:
                yaku_list.append("四暗刻")
                yakuman += 1
    #国士無双
    if kokushi_flag == True:
        yaku_list.append("国士無双")
        yakuman += 1
    #役満があったとき
    if yakuman != 0:
        return [-yakuman,0, yaku_list]

    #役満以外の役
    #立直、ダブル立直
    if riichi == 1:
        yaku_list.append("立直")
        hansuu += 1
    if riichi == 2:
        yaku_list.append("ダブル立直")
        hansuu += 2
    #一発
    if ippatsu:
        yaku_list.append("一発")
        hansuu += 1
    #メンゼン自摸
    if tsumoagari and not is_fuuro:
        yaku_list.append("門前清自摸和")
        hansuu += 1
    #嶺上開花
    if rinshan:
        yaku_list.append("嶺上開花")
        hansuu += 1
    #海底、河底
    if haitei:
        yaku_list.append("ハイテイ")
        hansuu += 1
    #槍槓
    if chankan:
        yaku_list.append("槍槓")
        hansuu += 1
    #断么九
    if inc(tehai,'011111110 011111110 011111110 0000000'):
        yaku_list.append("断么九")
        hansuu += 1
    #混老頭
    if inc(tehai,'100000001 100000001 100000001 1111111'):
        yaku_list.append("混老頭")
        hansuu += 2
    #清一色
    tinitsu_flag = False
    if inc(tehai,'111111111 000000000 000000000 0000000') or inc(tehai,'000000000 1111111111 000000000 0000000')\
    or inc(tehai,'000000000 000000000 111111111 0000000'):
        yaku_list.append("清一色")
        tinitsu_flag = True
        if is_fuuro:
            hansuu += 5
        else:
            hansuu += 6
    #混一色
    if tinitsu_flag == False and ( inc(tehai,'111111111 000000000 000000000 1111111')\
    or inc(tehai,'000000000 111111111 000000000 1111111') or inc(tehai,'000000000 000000000 111111111 1111111')):
        yaku_list.append("混一色")
        if is_fuuro:
            hansuu += 2
        else:
            hansuu += 3
    #白、發、中
    sangenpai = [tehai[35],tehai[36],tehai[37]]
    if sangenpai[0] >= 3:
        yaku_list.append("白")
        hansuu += 1
    if sangenpai[1] >= 3:
        yaku_list.append("發")
        hansuu += 1
    if sangenpai[2] >= 3:
        yaku_list.append("中")
        hansuu += 1
    #小三元
    sangenpai = [tehai[35],tehai[36],tehai[37]]
    if (sangenpai[0] >= 3 and sangenpai[1] >= 3 and sangenpai[2] == 2) or\
        (sangenpai[0] >= 3 and sangenpai[1] == 2 and sangenpai[2] >= 3) or\
            (sangenpai[0] == 2 and sangenpai[1] >= 3 and sangenpai[2] >= 3):
            yaku_list.append("小三元")
            hansuu += 2
    #場風、自風
    if tehai[31+bakaze] >= 3:
        yaku_list.append("場風")
        hansuu += 1
    if tehai[31+zikaze] >= 3:
        yaku_list.append("自風")
        hansuu +=1
    #七対子
    if agari_kei == 1:
        yaku_list.append("七対子")
        hansuu += 2
        fusuu = 25
    #三槓子
    if agari_kei == 0:
        kantsu_num = 0
        for jm in jm_list:
            for m in jm[1]:
                if m[1] == 2:
                    kantsu_num += 1
            if kantsu_num >= 3:
                yaku_list.append("三槓子")
                hansuu += 2

    #面子の分解パターンによってついたりつかなかったりする役(四暗刻をのぞく)
    #すべての分解パターンについて求め、最も翻数、符数が高いものをえらぶ。
    if agari_kei == 0:    
        han_fu_candidate =[]
        for jm in jm_list:
            hansuu_tmp = hansuu
            fusuu_tmp = fusuu
            yaku_list_tmp = copy(yaku_list)
            
            #符計算
            shuntsu_lis = [i for i in jm[1] if i[1] == 0]#順子を入れた配列
            #符（雀頭）
            yakuhai_jantou_flag = False
            if jm[0] == 35 or jm[0] == 36 or jm[0] == 37 or jm[0] == 31+zikaze or jm[0] == 31+bakaze:
                fusuu_tmp += 2
                yakuhai_jantou_flag = True
            #符（待ち）
            #待ち方が複数解釈できる場合平和がつく（符数20）なら両面。それ以外は符がつく待ちを選ぶ。(シャボvs両面は両面（for三暗刻))
            #順子数>3の時、両面待ちがあるならピンフ。ないなら符数＋2
            pinfu_flag = False
            ryanmen = [[],[1],[2,4],[3,5],[4,6],[5,7],[6,8],[9],[],[],[],[11],[12,14],[13,15],[14,16],[15,17],[16,18],[19],[],[],[],[21],[22,24],[23,25],[24,26],[25,27],[26,28],[29],[],[]]
            if len(shuntsu_lis) > 3:
                for i in shuntsu_lis:
                    r = ryanmen[i[2]]
                    if len(r) > 0:
                        for j in r:
                            if agarihai < 30 and agarihai == j and yakuhai_jantou_flag == False:
                                pinfu_flag = True
                if pinfu_flag == False:
                    fusuu_tmp += 2
            #順子数<=3の時、符が付く待ち→両面の順に探す。どれもなければシャボ。シャボの場合、ロンアガリならjmのその暗刻を明刻に変える。
            else:
                tanki_flag = False
                penchan_flag = False
                kanchan_flag = False
                ryanmen_flag = False
                penchan = [0,3,0,0,0,0,0,7,0,0,0,13,0,0,0,0,0,17,0,0,0,23,0,0,0,0,0,27,0,0]
                kanchan = [0,2,3,4,5,6,7,8,0,0,0,12,13,14,15,16,17,18,0,0,0,22,23,24,25,26,27,28,0,0]
                if agarihai == jm[0]:
                    tanki_flag = True
                elif len(shuntsu_lis) > 0 and agarihai < 30:
                    for i in shuntsu_lis:
                        if agarihai == penchan[i[2]]:
                            penchan_flag = True
                        elif agarihai == kanchan[i[2]]:
                            kanchan_flag = True
                        else:
                            r = ryanmen[i[2]]
                            if len(r) > 0:
                                for j in r:
                                    if agarihai == j:
                                        ryanmen_flag = True
                if tanki_flag == True or penchan_flag == True or kanchan_flag == True:
                    fusuu_tmp += 2
                elif ryanmen_flag == False and not tsumoagari:
                    for l in jm[1]:
                        if l[1] == 1 and l[2] == agarihai:
                            l[0] = 1
            #刻子、暗刻を入れた配列
            koutsu_lis = [i for i in jm[1] if i[1] == 1 or i[1] == 2] #槓子含む
            anko_lis = [i for i in koutsu_lis if i[0] == 0] #槓子含む
            #符（刻子、槓子）
            if len(koutsu_lis) > 0:
                for l in koutsu_lis:
                    if (1 < l[2] < 9) or (11 < l[2] < 19) or (21 < l[2] < 29):
                        yaotyu = 0
                    else:
                        yaotyu = 1
                    if l[0] == 1:
                        ank = 0
                    else:
                        ank = 1
                    if l[1] == 1:
                        kant = 0
                    else:
                        kant = 1
                    fusuu_tmp += 2*(2**yaotyu)*(2**ank)*(4**kant)
            #符（上がり方）
            if tsumoagari and pinfu_flag == False:
                fusuu_tmp += 2
            elif not tsumoagari and not is_fuuro:
                fusuu_tmp += 10
        
            #順子が3個以上ならすべての三順子のインデックスを抜き出す。同順、イッツー用
            if len(shuntsu_lis) >=3:
                san_shuntsu_id = []
                if len(shuntsu_lis) ==3:
                    san_shuntsu_id.append([i[2] for i in shuntsu_lis])
                else:
                    yon_shuntsu_id = [i[2] for i in shuntsu_lis]
                    for i in range(0,4):
                        san_shuntsu_id.append(yon_shuntsu_id[:i]+yon_shuntsu_id[(i+1):])
                for i in san_shuntsu_id:
                    i.sort()
            #刻子が3個以上ならすべての三刻子のインデックスを抜き出す。同刻用。
            if len(koutsu_lis) >=3:
                san_koutsu_id = []
                if len(koutsu_lis) ==3:
                    san_koutsu_id.append([i[2] for i in koutsu_lis])
                else:
                    yon_koutsu_id = [i[2] for i in koutsu_lis] 
                    for i in range(0,4):
                        san_koutsu_id.append(yon_koutsu_id[:i]+yon_koutsu_id[(i+1):])
                for i in san_koutsu_id:
                    i.sort()
            #一盃口、二盃口
            if not is_fuuro:
                l = len(shuntsu_lis)
                if l >= 2:
                    peko_num = 0
                    for i in range(0,l-1):
                        for j in range(i+1,l):
                            if shuntsu_lis[i][2] == shuntsu_lis[j][2]:
                                peko_num += 1
                    if peko_num == 1:
                        yaku_list_tmp.append("一盃口")
                        hansuu_tmp += 1
                    elif peko_num == 2:
                        yaku_list_tmp.append("二盃口")
                        hansuu_tmp += 3
            #三暗刻
            if len(anko_lis) == 3:
                yaku_list_tmp.append("三暗刻")
                hansuu_tmp += 2
            #三色同刻
            if len(koutsu_lis) >= 3:
                doukou_flag = False
                for s in san_koutsu_id:
                    if s[1] == s[0]+10 and s[2] == s[0]+20 and s[2] < 30:
                        doukou_flag = True
                if doukou_flag == True:
                    yaku_list_tmp.append("三色同刻")
                    hansuu_tmp += 2
            #三色同順
            if len(shuntsu_lis) >= 3:
                doujun_flag = False
                for s in san_shuntsu_id:
                    if s[1] == s[0]+10 and s[2] == s[0]+20:
                        doujun_flag = True
                if doujun_flag == True:
                    yaku_list_tmp.append("三色同順")
                    if is_fuuro:
                        hansuu_tmp += 1
                    else:
                        hansuu_tmp += 2
            #対々和
            if len(koutsu_lis) >= 4:
                yaku_list_tmp.append("対々和")
                hansuu_tmp += 2
            #一気通貫
            if len(shuntsu_lis) >= 3:
                ittsu_flag = False
                for s in san_shuntsu_id:
                    if s == ([1,4,7] or [11,14,17] or [21,24,27]):
                        ittsu_flag = True
                if ittsu_flag == True:
                    yaku_list_tmp.append("一気通貫")
                    if is_fuuro:
                        hansuu_tmp += 1
                    else:
                        hansuu_tmp += 2
            #純全帯么九、混全帯么九
            junchan_flag = True
            chanta_flag = True
            if len(shuntsu_lis) >= 1:
                for l in shuntsu_lis:
                    if (1 < l[2] < 7) or (11 < l[2] < 17) or (21 < l[2] < 27):
                        junchan_flag = False
                        chanta_flag = False
            if len(koutsu_lis) >= 1:
                for l in koutsu_lis:
                    if (1 < l[2] < 9) or (11 < l[2] < 19) or (21 < l[2] < 29):
                        junchan_flag = False
                        chanta_flag = False
                    elif 30 < l[2]:
                        junchan_flag = False
            if (1 < jm[0] < 7) or (11 < jm[0] < 17) or (21 < jm[0] < 27):
                junchan_flag = False
                chanta_flag = False
            elif 30 < jm[0]:
                junchan_flag = False
            if junchan_flag == True:
                yaku_list_tmp.append("純全帯么九")
                if is_fuuro:
                    hansuu_tmp += 2
                else:
                    hansuu_tmp += 3
            elif chanta_flag == True:
                yaku_list_tmp.append("混全帯么九")
                if is_fuuro:
                    hansuu_tmp += 1
                else:
                    hansuu_tmp += 2
            #平和
            if pinfu_flag == True and not is_fuuro:
                yaku_list_tmp.append("平和")
                hansuu_tmp += 1
            han_fu_candidate.append([hansuu_tmp,fusuu_tmp,yaku_list_tmp])

        for i in han_fu_candidate:
            if i[0] > hansuu:
                hansuu = i[0]
                fusuu = i[1]
                yaku_list = i[2]
            elif i[0] == hansuu:
                if i[1] > fusuu:
                    fusuu = i[1]
                    yaku_list = i[2]

    if hansuu > 0:
        od = 0
        for i in dora[0]:
            od += tehai[i]
        if od > 0:
            yaku_list.append("ドラ"+str(od))
            hansuu += od
        ad = tehai_akadora
        if len(fuuro_akadora) > 0:
            for i in fuuro_akadora:
                if i:
                    ad += 1
        if len(ankan) > 0:
            for i in ankan:
                if i == 5 or i== 15 or i == 25:
                    ad += 1
        if ad > 0:
            yaku_list.append("赤ドラ"+str(ad))
            hansuu += ad
        if riichi > 0:
            ud = 0
            for i in dora[1]:
                ud += tehai[i]
            if ud > 0:
                yaku_list.append("裏ドラ"+str(ud))
                hansuu += ud
    if fusuu != 25:
        fusuu2 = fusuu / 10.0
        fusuu = math.ceil(fusuu2)*10

    return [hansuu,fusuu,yaku_list]
            

#サブの関数
def jm_convert(tehai_exc_fuuro,fuurohai,ankan):

    #手牌を面子と雀頭に分解し、フウロしている面子とともに手役計算用表示に変換したリストにする。
    #出力は可能なすべての分解パターンのリスト。
    #ひとつの分解パターン[n,[[i1,j1,k1],[i2,j2,k2],[i3,j2,k2],[i3,j3,k3]]]
    #(雀頭):n (n=牌のインデックス)
    #(面子):[i,j,k]
    # i=0(暗) ,1(明)
    # j=0(順子),1(刻子),2(槓子)
    # k=(順子なら)先頭の牌のインデックス,(刻子なら)その牌のインデックス
    tehai = function.tehai_convert(tehai_exc_fuuro)
    fuurosu = len(fuurohai) + len(ankan)

    rets = decomp_tehai(tehai,fuurosu)
    for ret in rets:
        if len(fuurohai) >= 1:  
            for f in fuurohai:
                if f[0] == 1:
                    ret[1].append([1,0,f[1]-2+f[2]])
                elif f[0] == 2:
                    ret[1].append([1,1,f[1]])
                elif f[0] == 3:
                    ret[1].append([1,2,f[1]])
        if len(ankan) >= 1:
            for a in ankan:
                ret[1].append([0,2,a])
        
    return rets

def decomp_tehai(tehai,fuurosu):  

    #convert用。
    #手牌を可能なn面子1雀頭に分解する。複数ある場合すべて並べる。
    ans = []
    for i in range(0,38): 
        if tehai[i] >= 2: 
            t = tehai.copy()
            t[i] -= 2
            lis = [[0,[i,[]],t]]
            lis_nxt = []
            while lis:
                lis2 = []
                for l in lis:
                    a = pick_koutsu(l)
                    for j in a:    
                        if j[0] == 38:
                            if len(j[1][1]) == 4-fuurosu:
                                ans.append(j[1])
                            else:
                                lis_nxt.append(j)
                        else:
                            lis2.append(j)
                lis = lis2
            lis = lis_nxt
            for l in lis:
                l[0] = 0
            while lis:
                lis2 = []
                for l in lis:
                    a = pick_shuntsu(l)
                    for j in a:         
                        if j[0] == 30:
                            if len(j[1][1]) == 4-fuurosu:
                                ans.append(j[1])           
                        else:
                            lis2.append(j)
                lis = lis2
    
    return ans

def pick_koutsu(lis): 

    #decomp_tehai用。手牌から刻子を抜き出し手役計算用表示にする。

    n = lis[0]
    m_lis = lis[1]
    tehai_r = lis[2]
    for i in range(n,38):
        if tehai_r[i] >= 3:
            tehai_r2 = copy(tehai_r)
            tehai_r2[i] -= 3
            m_lis2 = copy(m_lis)
            m_lis2[1].append([0,1,i])
            return [[i+1,m_lis,tehai_r],[i,m_lis2,tehai_r2]]
    return [[38,m_lis,tehai_r]]

def pick_shuntsu(lis):

    #decomp_tehai用。手牌から順子を抜き出し手役計算用表示にする。

    n = lis[0]
    m_lis = lis[1]
    tehai_r = lis[2]
    for i in range(n,30):
        if tehai_r[i] >= 1 and tehai_r[i+1] >= 1 and tehai_r[i+2] >= 1:
            tehai_r2 = copy(tehai_r)
            tehai_r2[i] -= 1
            tehai_r2[i+1] -= 1
            tehai_r2[i+2] -= 1
            m_lis2 = copy(m_lis)
            m_lis2[1].append([0,0,i])
            return [[i+1,m_lis,tehai_r],[i,m_lis2,tehai_r2]]
    return [[30,m_lis,tehai_r]]

def inc(tehai_all,compair_str): 

    #tehai_all:手牌とフウロ混ぜた[0,0,1,2,0,...]形式。
    #compair_strの例"110000011 110111101 111101111 1111101"。
    #萬子、筒子、索子、字牌の並びで1になってる牌だけ含むならtrue,それ以外も含むならfalse。

    tehai = tehai_all
    compair_list = compair_str.split()
    for i in range(1,10):
        if int(compair_list[0][i-1]) == 0 and tehai[i] >= 1:
            return False
    for i in range(11,20):
        if int(compair_list[1][i-11]) == 0 and tehai[i] >= 1:
            return False
    for i in range(21,30):
        if int(compair_list[2][i-21]) == 0 and tehai[i] >= 1:
            return False
    for i in range(31,38):
        if int(compair_list[3][i-31]) == 0 and tehai[i] >= 1:
            return False
    return True

def Is_fuuro(fuurohai): 

    #フウロ牌（暗槓除く）があるならTrueないならFalse

    if len(fuurohai) >= 1:
        return True
    else:
        return False

def tehai_fuuro_mix_convert(tehai_str,fuurohai,ankan):
    
    #手牌と副露牌を混ぜて[0,0,1,2,0,...]形式にする

    mix = function.tehai_convert(tehai_str)
    for f in fuurohai:
        if f[0] == 1:
            mix[f[1]-2+f[2]] += 1
            mix[f[1]-1+f[2]] += 1
            mix[f[1]  +f[2]] += 1
        elif f[0] == 2:
            mix[f[1]] +=3
        elif f[0] == 3:
            mix[f[1]] +=4
    if len(ankan) >= 1:
        for a in ankan:
            mix[a] += 4
    
    return mix




    


    


    
        