#game_tenhou.pyを整理
#import sys,os
import time
import function_tenhou
import decode_m
import shanten_check_new
import riichi_hantei3
#import majang
#import riichi_hantei3
#import decode_m
#import read_packet
#import shanten_check_new
import function
from gui_hub import gui_click

key_to_index = {"E":1, "e":1, "F":2, "f":2, "G":3, "g":3}
key_to_char = {"E":"下家", "e":"下家", "F":"対面", "f":"対面", "G":"上家", "g":"上家"}
who_to_str = {0:"自家", 1:"下家", 2:"対面", 3:"上家"}
kaze_to_str = {0: "東", 1: "南", 2: "西", 3: "北"}
kyoku_to_str = {0:'東１局', 1:'東2局', 2:'東3局', 3:'東4局', 4:'南１局', 5:'南2局', 6:'南3局', 7:'南4局', 8:'西1局' , 9:'西2局' , 10:'西3局' , 11:'西4局'}

def tacha_dahai(key, janshi, taku, splitted_read_text):

    output2 = ["",""]

    start = time.time()
    hai_136 = int(splitted_read_text[1].strip(key))
    hai_str = function_tenhou.hai_convert_136_to_str(hai_136)
    janshi[0].vertual_yama.remove(hai_str)
    janshi[key_to_index[key]].sutehai.append(hai_str)
    janshi[key_to_index[key]].tedashi_flag.append(key.isupper) #keyが大文字なら手出し
    janshi[key_to_index[key]].temp_genbutsu = []
    for k in range(1,4):
        janshi[k].temp_genbutsu.append(hai_str)

    print(key_to_char[key] + " 打:" + hai_str)

    taku.last_dahai = hai_136 #直前の打牌。鳴きに利用する。
    taku.last_teban = key_to_index[key] #直前の打牌をしたプレイヤー
    
    #以下鳴き　鳴きの基本方針→赤ドラを副露牌に含められるときは必ず含める
    if len(splitted_read_text) > 2:
        #ロン通知
        if int(splitted_read_text[3]) >= 8:
            #あがる
            print("AI ロン")
            #天鳳に出力
            if time.time() - start < taku.sleep_time_thresh:
                time.sleep(taku.sleep_time)
            gui_click("Agari")
            return None
        #ポン通知
        elif splitted_read_text[3] == "1" or splitted_read_text[3] == "3":
            #ポン打診
            pon_index = janshi[0].pon(taku, hai_str, janshi, taku.bakyou_list)
            if pon_index[0]:
                print("AI ポン")
                #ポンする
                #ポンする牌のindex
                pon_hai_index = function_tenhou.hai_convert_136_to_index(taku.last_dahai)
                
                #赤なら普通の5に書き換え
                if pon_hai_index % 10 == 0:
                    pon_hai_index += 5

                #もし赤じゃない5をポンするなら
                if pon_hai_index%10 == 5 and pon_hai_index < 30:
                    tehai_index = function.tehai_convert(janshi[0].tehai)
                    #もし同じ色の赤を持っていたら
                    if tehai_index[pon_hai_index-5] == 1:
                        output2 = [function.hai_convert_reverse(pon_hai_index - 5), function.hai_convert_reverse(pon_hai_index)]
                    else:
                        output2 = [function.hai_convert_reverse(pon_hai_index), function.hai_convert_reverse(pon_hai_index)]
                else:
                    output2 = [function.hai_convert_reverse(pon_hai_index), function.hai_convert_reverse(pon_hai_index)]

                #print("ポンする牌:" + output2)
                #天鳳に出力
                if time.time() - start < taku.sleep_time_thresh:
                    time.sleep(taku.sleep_time)
                print(output2)
                gui_click("Pon_Chii", output2)

                #打牌時の情報を追加
                taku.naki_dahai = pon_index[1]
                print("AI 打:" + taku.naki_dahai)
                return None

            else:
                #鳴かない
                print("AI スルー")
                #天鳳に出力
                if time.time() - start < taku.sleep_time_thresh:
                    time.sleep(taku.sleep_time)
                gui_click("Cancel")
                return None
        #チー通知
        elif splitted_read_text[3] == "4":
            #チー打診
            chii_index = janshi[0].chii(taku, hai_str, janshi, taku.bakyou_list)
            if chii_index[0] != -1:
                print("AI チー: index = " + str(chii_index[0]))
                #チーする

                #チーする牌のindex
                chii_hai_index = function_tenhou.hai_convert_136_to_index(taku.last_dahai)

                #赤をチー
                if chii_hai_index%10 == 0:
                    chii_hai_index += 5
                    if chii_index[0] == 0:
                        output2[0] = function.hai_convert_reverse(chii_hai_index - 2)
                        output2[1] = function.hai_convert_reverse(chii_hai_index - 1)
                    elif chii_index[0] == 1:
                        output2[0] = function.hai_convert_reverse(chii_hai_index - 1)
                        output2[1] = function.hai_convert_reverse(chii_hai_index + 1)
                    else:# chii_index[0] == 2:
                        output2[0] = function.hai_convert_reverse(chii_hai_index + 1)
                        output2[1] = function.hai_convert_reverse(chii_hai_index + 2)
                #赤以外をチー
                else:
                    if chii_index[0] == 0:
                        output2[0] = function.hai_convert_reverse(chii_hai_index - 2)
                        output2[1] = function.hai_convert_reverse(chii_hai_index - 1)
                    elif chii_index[0] == 1:
                        output2[0] = function.hai_convert_reverse(chii_hai_index - 1)
                        output2[1] = function.hai_convert_reverse(chii_hai_index + 1)
                    else: # chii_index[0] == 2:
                        output2[0] = function.hai_convert_reverse(chii_hai_index + 1)
                        output2[1] = function.hai_convert_reverse(chii_hai_index + 2)
                    
                    #赤の書き換え
                    if chii_index[2]:
                        for j in range(2):
                            if output2[j] == "5m":
                                output2[j] = "5M"
                            elif output2[j] == "5p":
                                output2[j] = "5P"
                            elif output2[j] == "5s":
                                output2[j] = "5S"
                #天鳳に出力
                print(output2)
                if time.time() - start < taku.sleep_time_thresh:
                    time.sleep(taku.sleep_time)
                gui_click("Pon_Chii",output2)
                
                #打牌時の情報を追加
                taku.naki_dahai = chii_index[1]
                print("AI 打:" + taku.naki_dahai)
                return None
            else:
                #鳴かない
                print("AI スルー")
                #天鳳に出力
                if time.time() - start < taku.sleep_time_thresh:
                    time.sleep(taku.sleep_time)
                gui_click("Cancel")
                return None
        #ポンチー通知#ポンチーダイミンカン通知
        elif splitted_read_text[3] == "5" or splitted_read_text[3] == "7":
            #ポンチー打診
            pon_index = janshi[0].pon(taku, hai_str, janshi, taku.bakyou_list)
            if pon_index[0]:
                print("AI ポン")
                #ポンする
                #ポンする牌のindex
                pon_hai_index = function_tenhou.hai_convert_136_to_index(taku.last_dahai)

                #赤なら普通の5に書き換え
                if pon_hai_index % 10 == 0:
                    pon_hai_index += 5

                #もし赤じゃない5をポンするなら
                if pon_hai_index%10 == 5 and pon_hai_index < 30:
                    tehai_index = function.tehai_convert(janshi[0].tehai)
                    #もし同じ色の赤を持っていたら
                    if tehai_index[pon_hai_index-5] == 1:
                        output2 = [function.hai_convert_reverse(pon_hai_index - 5), function.hai_convert_reverse(pon_hai_index)]
                    else:
                        output2 = [function.hai_convert_reverse(pon_hai_index), function.hai_convert_reverse(pon_hai_index)]
                else:
                    output2 = [function.hai_convert_reverse(pon_hai_index), function.hai_convert_reverse(pon_hai_index)]
                #print("ポンする牌:" + output)
                #天鳳に出力
                print(output2)
                if time.time() - start < taku.sleep_time_thresh:
                    time.sleep(taku.sleep_time)
                gui_click("Pon_Chii",output2)


                #打牌時の情報を追加
                taku.naki_dahai = pon_index[1]
                print("AI 打:" + taku.naki_dahai)
                return None
                
            chii_index = janshi[0].chii(taku, hai_str, janshi, taku.bakyou_list)
            if chii_index[0] != -1:
                print("AI チー: index = " + str(chii_index[0]))
                #チーする
                #チーする牌のindex
                chii_hai_index = function_tenhou.hai_convert_136_to_index(taku.last_dahai)

                #赤をチー
                if chii_hai_index%10 == 0:
                    chii_hai_index += 5
                    if chii_index[0] == 0:
                        output2[0] = function.hai_convert_reverse(chii_hai_index - 2)
                        output2[1] = function.hai_convert_reverse(chii_hai_index - 1)
                    elif chii_index[0] == 1:
                        output2[0] = function.hai_convert_reverse(chii_hai_index - 1)
                        output2[1] = function.hai_convert_reverse(chii_hai_index + 1)
                    else:# chii_index[0] == 2:
                        output2[0] = function.hai_convert_reverse(chii_hai_index + 1)
                        output2[1] = function.hai_convert_reverse(chii_hai_index + 2)
                #赤以外をチー
                else:
                    if chii_index[0] == 0:
                        output2[0] = function.hai_convert_reverse(chii_hai_index - 2)
                        output2[1] = function.hai_convert_reverse(chii_hai_index - 1)
                    elif chii_index[0] == 1:
                        output2[0] = function.hai_convert_reverse(chii_hai_index - 1)
                        output2[1] = function.hai_convert_reverse(chii_hai_index + 1)
                    else: # chii_index[0] == 2:
                        output2[0] = function.hai_convert_reverse(chii_hai_index + 1)
                        output2[1] = function.hai_convert_reverse(chii_hai_index + 2)
                    
                    #赤の書き換え
                    if chii_index[2]:
                        for j in range(2):
                            if output2[j] == "5m":
                                output2[j] = "5M"
                            elif output2[j] == "5p":
                                output2[j] = "5P"
                            elif output2[j] == "5s":
                                output2[j] = "5S"
                #天鳳に出力
                print(output2)
                if time.time() - start < taku.sleep_time_thresh:
                    time.sleep(taku.sleep_time)
                gui_click("Pon_Chii",output2)
                #打牌時の情報を追加
                taku.naki_dahai = chii_index[1]
                print("AI 打:" + taku.naki_dahai)
                return None
                
            #鳴かない
            print("AI スルー")
            #天鳳に出力
            if time.time() - start < taku.sleep_time_thresh:
                time.sleep(taku.sleep_time)
            gui_click("Cancel")
            return None
    return None

def naki(janshi,taku,splitted_read_text):
    who = int(splitted_read_text[3])
    m = int(splitted_read_text[5])
    m_decoded_list = decode_m.decode_m(m)
    
    if m_decoded_list[0] == 1:
        #ポン
        
        #他家がポン→バーチャル山更新
        if who:
            janshi[who].fuurosuu += 1
            print(who_to_str[who] + ": ポン")
            for i in range(3):
                if taku.last_dahai != m_decoded_list[1][i]:
                    janshi[0].vertual_yama.remove(function_tenhou.hai_convert_136_to_str(m_decoded_list[1][i]))
        
        #自家がポン→副露リスト更新
        else:
            print(who_to_str[who] + ": ポン")
            janshi[0].pon_add(taku, m_decoded_list[1], taku.last_teban)
            #打牌出力 naki_dahai
            gui_click("Dahai",taku.naki_dahai)
            #print(janshi[0].fuurohai)
    

    elif m_decoded_list[0] == 2:
        #ダイミンカン
        #他家がダイミンカン→バーチャル山更新
        if who:
            janshi[who].fuurosuu += 1
            print(who_to_str[who] + ": ダイミンカン")
            #最初の牌
            temp = m_decoded_list[1][0] - m_decoded_list[1][0] % 4
            for i in range(4):
                if function_tenhou.hai_convert_136_to_str(temp+i) in janshi[0].vertual_yama:
                    janshi[0].vertual_yama.remove(function_tenhou.hai_convert_136_to_str(temp+i))
        #自家がダイミンカン
        else:
            print(who_to_str[who] + ": ダイミンカン")
            janshi[0].daiminkan_add(taku, m_decoded_list[1], taku.last_dahai, taku.last_teban)   
    
    elif m_decoded_list[0] == 3:
        #チー
        
        #他家がチー→バーチャル山更新
        if who:
            janshi[who].fuurosuu += 1
            print(who_to_str[who] + ": チー")
            for i in range(3):
                if taku.last_dahai != m_decoded_list[1][i]:
                    janshi[0].vertual_yama.remove(function_tenhou.hai_convert_136_to_str(m_decoded_list[1][i]))
        
        #自家がチー→副露リスト更新
        else:
            print(who_to_str[who] + ": チー")
            janshi[0].chii_add(taku, m_decoded_list[1], taku.last_dahai)
            #打牌出力 naki_dahai
            gui_click("Dahai",taku.naki_dahai)
            #print(janshi[0].fuurohai)
            
    elif m_decoded_list[0] == 4:
        #アンカン
        
        #他家が暗槓→バーチャル山更新
        if who:
            janshi[who].fuurosuu += 1
            print(who_to_str[who] + ": 暗槓")
            #ソートされているので赤は最初に来る(はず)
            janshi[0].vertual_yama.remove(function_tenhou.hai_convert_136_to_str(m_decoded_list[1][0]))
            janshi[0].vertual_yama.remove(function_tenhou.hai_convert_136_to_str(m_decoded_list[1][1]))
            janshi[0].vertual_yama.remove(function_tenhou.hai_convert_136_to_str(m_decoded_list[1][1]))
            janshi[0].vertual_yama.remove(function_tenhou.hai_convert_136_to_str(m_decoded_list[1][1]))
        
        #自家が暗槓→暗槓リストを更新
        else:
            print(who_to_str[who] + ": 暗槓")
            janshi[0].ankan_add(taku, m_decoded_list[1])
    
    else: #m_decoded_list[0] == 5:
        #加カン
        
        #他家がカカン→バーチャル山更新
        if who:
            print(who_to_str[who] + ": 加槓")
            #カカンした牌IDを求める
            temp_arr = m_decoded_list[1]
            kakan_hai_id = 6 + temp_arr[0] - (temp_arr[0]%4)*2 - temp_arr[1] % 4 - temp_arr[2] % 4
            janshi[0].vertual_yama.remove(function_tenhou.hai_convert_136_to_str(kakan_hai_id))
        
        #自家がカカン→副露リストを更新
        else:
            print(who_to_str[who] + ": 加槓")
            janshi[0].kakan_add(taku, m_decoded_list[1])

def jicha_tsumo(janshi,taku,splitted_read_text):
    output = ""
    start = time.time()
    taku.yama_nokori -= 1
    hai_136 = int(splitted_read_text[1].strip("T"))
    #print(hai_136)
    print("ツモ牌:" + function_tenhou.hai_convert_136_to_str(hai_136))
    print("残りツモ回数:" + str(int(taku.yama_nokori/4)) + "回")
    hai_str = function_tenhou.hai_convert_136_to_str(hai_136)
    janshi[0].tsumo(hai_str, hai_136)
    print(janshi[0].tehai)

    print("シャンテン数: " + str(shanten_check_new.shanten_check(janshi[0], taku.hash_table)))

    #暗槓&カカン
    temp_ankan = janshi[0].ankan(taku)
    if temp_ankan != -1:
        print("AI 暗槓: " + function.hai_convert_reverse(temp_ankan))
        output = function.hai_convert_reverse(temp_ankan)
        #天鳳に出力
        if time.time() - start < taku.sleep_time_thresh:
            time.sleep(taku.sleep_time)
        gui_click("Kan", output)
        return None

    temp_kakan = janshi[0].kakan(taku)
    if temp_kakan[0] != -1:
        print("AI 加槓: " + function.hai_convert_reverse(temp_kakan[1]))
        if temp_kakan[2]:
            output = function.hai_convert_reverse(temp_kakan[1]-5)
        else:
            output = function.hai_convert_reverse(temp_kakan[1])
        
        #天鳳に出力
        if time.time() - start < taku.sleep_time_thresh:
            time.sleep(taku.sleep_time)
        gui_click("Kan", output)
        return None
    
    #ツモアガリか立直
    if len(splitted_read_text) > 2:
        #ツモアガリ
        if splitted_read_text[3] == "64":
            if shanten_check_new.shanten_check(janshi[0], taku.hash_table) >= 3:
                if time.time() - start < taku.sleep_time_thresh:
                    time.sleep(taku.sleep_time)
                print("AI 九種九牌流局")
                gui_click("Kyuusyu")
                return None

        if splitted_read_text[3] == "16" or splitted_read_text[3] == "48" or splitted_read_text[3] == "112":
            #とりあえずツモアガリする
            print("AI ツモアガリ")
            #天鳳に出力
            if time.time() - start < taku.sleep_time_thresh:
                time.sleep(taku.sleep_time)
            gui_click("Agari")
            return None
        #立直
        if splitted_read_text[3] == "32":
            #a→点数がthreshに届いてるか, b→立直時or保留時の打牌index, c→保留するかどうか
            a, b, c = riichi_hantei3.riichi_hantei(janshi[0], taku)               
            #オーラスなら条件考慮
            if taku.bakyou_list[0]:
                hai_str = function.hai_convert_reverse(b)
                #アガリ点の平均値
                dama_point = function.dama_hantei(janshi[0], taku, hai_str)
                if a:
                    #全ての待ち牌に対してダマでロンアガリできる
                    if dama_point:
                        if taku.bakyou_list[0] == 1 or taku.bakyou_list[0] == 3:
                            print("AI ダマテン")
                            print("AI 打:" + hai_str)
                            output = hai_str
                            if time.time() - start < taku.sleep_time_thresh:
                                time.sleep(taku.sleep_time)
                            gui_click("Dahai",output)
                            janshi[0].riipai()
                            return None
                        else:
                            #ダマでは点数が足りない
                            if taku.bakyou_list[1] > dama_point:
                                print("AI リーチ")
                                taku.riichi_dahai = hai_str
                                print("AI 打:" + taku.riichi_dahai)
                                #天鳳に出力
                                if time.time() - start < taku.sleep_time_thresh:
                                    time.sleep(taku.sleep_time)
                                gui_click("Riichi")
                                janshi[0].riipai()
                                return None
                            #ダマでも点数が足りる
                            else:
                                print("AI ダマテン")
                                print("AI 打:" + hai_str)
                                output = hai_str
                                if time.time() - start < taku.sleep_time_thresh:
                                    time.sleep(taku.sleep_time)
                                gui_click("Dahai",output)
                                janshi[0].riipai()
                                return None
                    #ダマでロンアガリできない待ち牌がある
                    else:
                        print("AI リーチ")
                        taku.riichi_dahai = hai_str
                        print("AI 打:" + taku.riichi_dahai)
                        #天鳳に出力
                        if time.time() - start < taku.sleep_time_thresh:
                            time.sleep(taku.sleep_time)
                        gui_click("Riichi")
                        janshi[0].riipai()   
                        return None
                elif c:
                    print("AI リーチ保留")
                    temp_index = 0
                    print("AI 打:" + hai_str)
                    output = hai_str
                    if time.time() - start < taku.sleep_time_thresh:
                        time.sleep(taku.sleep_time)
                    gui_click("Dahai",output)
                    janshi[0].riipai()
                    return None
                #threshに足りてない(aとほぼ同じ。ラスの時だけ立直)
                else:
                    pass
                    #全ての待ち牌に対してダマでロンアガリできる
                    if dama_point:
                        if taku.bakyou_list[0] == 1 or taku.bakyou_list[0] == 3:
                            print("AI ダマテン")
                            print("AI 打:" + hai_str)
                            output = hai_str
                            if time.time() - start < taku.sleep_time_thresh:
                                time.sleep(taku.sleep_time)
                            gui_click("Dahai",output)
                            janshi[0].riipai()
                            return None
                        else:
                            #ダマでは点数が足りない
                            if taku.bakyou_list[1] > dama_point:
                                print("AI リーチ")
                                taku.riichi_dahai = hai_str
                                print("AI 打:" + taku.riichi_dahai)
                                #天鳳に出力
                                if time.time() - start < taku.sleep_time_thresh:
                                    time.sleep(taku.sleep_time)
                                gui_click("Riichi")
                                janshi[0].riipai()
                                return None
                            #ダマでも点数が足りる
                            else:
                                print("AI ダマテン")
                                print("AI 打:" + hai_str)
                                output = hai_str
                                if time.time() - start < taku.sleep_time_thresh:
                                    time.sleep(taku.sleep_time)
                                gui_click("Dahai",output)
                                janshi[0].riipai()
                                return None
                    #ダマでロンアガリできない待ち牌がある
                    else:
                        #ラスの時だけ立直
                        if taku.bakyou_list[0] == 4:
                            print("AI リーチ")
                            taku.riichi_dahai = hai_str
                            print("AI 打:" + taku.riichi_dahai)
                            #天鳳に出力
                            if time.time() - start < taku.sleep_time_thresh:
                                time.sleep(taku.sleep_time)
                            gui_click("Riichi")
                            janshi[0].riipai()   
                            return None
            #オーラス以外
            else:
                if a:
                    print("AI リーチ")
                    b_str = function.hai_convert_reverse(b)
                    temp_index = 0
                    for j in range(len(janshi[0].tehai)):
                        if b_str == janshi[0].tehai[j]:
                            temp_index = j
                            break

                    taku.riichi_dahai = janshi[0].tehai[temp_index]
                    print("AI 打:" + taku.riichi_dahai)
                    #janshi[0].func_riichi(taku)
                    #天鳳に出力
                    if time.time() - start < taku.sleep_time_thresh:
                        time.sleep(taku.sleep_time)
                    gui_click("Riichi")
                    janshi[0].riipai()   
                    return None
                elif c:
                    print("AI リーチ保留")
                    b_str = function.hai_convert_reverse(b)
                    temp_index = 0
                    for j in range(len(janshi[0].tehai)):
                        if b_str == janshi[0].tehai[j]:
                            temp_index = j
                            break
                    print("AI 打:" + b_str)
                    output = b_str
                    if time.time() - start < taku.sleep_time_thresh:
                        time.sleep(taku.sleep_time)
                    gui_click("Dahai",output)
                    janshi[0].riipai()
                    return None        

    #ツモアガリも立直もしない時
    max_index = int(janshi[0].dahai(taku, janshi, taku.bakyou_list))
    hai_str = janshi[0].tehai[max_index]
    print("AI 打:" + hai_str)
    #天鳳に出力　立直時はしない
    if not janshi[0].riichi:
        output = hai_str
        if time.time() - start < taku.sleep_time_thresh:
            time.sleep(taku.sleep_time)

        gui_click("Dahai",output)
    janshi[0].riipai()

def init_game(janshi,taku,splitted_read_text):
    #卓
    taku.taku_reset()
    kaze_honba_index = function_tenhou.find_str(splitted_read_text, "seed")
    taku.kaze_honba[0] = int(splitted_read_text[kaze_honba_index])
    taku.kaze_honba[1] = int(splitted_read_text[kaze_honba_index + 1])
    taku.kyoutaku_tensuu = int(splitted_read_text[kaze_honba_index + 2])*1000
    taku.dorahyouji.append(function_tenhou.hai_convert_136_to_str(int(splitted_read_text[kaze_honba_index+5])))
    print()
    print()
    print(kyoku_to_str[int(splitted_read_text[kaze_honba_index])] + " " + splitted_read_text[kaze_honba_index+1] + "本場")
    print("ドラ表示牌: " + taku.dorahyouji[0])

    #雀士
    oya = int(splitted_read_text[function_tenhou.find_str(splitted_read_text, "oya")])
    ten_index = function_tenhou.find_str(splitted_read_text, "ten")
    for i in range(4):
        janshi[i].janshi_reset()
        janshi[i].kaze = (-oya + i)%4
        janshi[i].tensuu = int(splitted_read_text[ten_index+i])*100
    janshi[0].tehai_136 = function_tenhou.get_haipai_136(splitted_read_text)
    janshi[0].tehai = function_tenhou.get_haipai_str(splitted_read_text)
    janshi[0].riipai()
    janshi[0].init_vertual_yama(taku)

    taku.bakyou_list = function_tenhou.create_bakyou_list(janshi, taku)

    print("自家: " + kaze_to_str[janshi[0].kaze] + "  点数: " + str(janshi[0].tensuu) + "  段位: " + janshi[0].dan + "  レーティング: " + str(janshi[0].rating) + "  ポイント: " + str(janshi[0].dan_point))
    print("下家: " + kaze_to_str[janshi[1].kaze] + "  点数: " + str(janshi[1].tensuu))
    print("対面: " + kaze_to_str[janshi[2].kaze] + "  点数: " + str(janshi[2].tensuu))
    print("上家: " + kaze_to_str[janshi[3].kaze] + "  点数: " + str(janshi[3].tensuu))
    print()
    print("初期手牌")
    print(janshi[0].tehai)

