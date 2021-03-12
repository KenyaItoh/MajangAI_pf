#import re
import function_tenhou
import majang
import riichi_hantei
import decode_m
import read_packet
import time

taku = majang.Taku()

janshi0 = majang.Janshi_p(2) #プレイヤー(自家)
janshi1 = majang.Janshi_e(1) #下家
janshi2 = majang.Janshi_e(2) #対面
janshi3 = majang.Janshi_e(3) #上家

janshi = [janshi0, janshi1, janshi2, janshi3]
who_to_str = {0:"自家", 1:"下家", 2:"対面", 3:"上家"}
kaze_to_str = {0: "東", 1: "南", 2: "西", 3: "北"}

while True:
    time.sleep(0.5)
    read_text = read_packet.read_packet()
    splitted_read_text = function_tenhou.read_text_decomp(read_text)
    ingame_flag = False

    #print(splitted_read_text)

    #初期
    if len(splitted_read_text) > 0:
        if splitted_read_text[1] == "INIT":
            ingame_flag = True
            #卓
            taku.taku_reset()
            kaze_honba_index = function_tenhou.find_str(splitted_read_text, "seed")
            taku.kaze_honba[0] = int(splitted_read_text[kaze_honba_index])
            taku.kaze_honba[1] = int(splitted_read_text[kaze_honba_index + 1])
            taku.dorahyouji.append(function_tenhou.hai_convert_136_to_str(int(splitted_read_text[kaze_honba_index+5])))
            #雀士
            oya = int(splitted_read_text[function_tenhou.find_str(splitted_read_text, "oya")])
            ten_index = function_tenhou.find_str(splitted_read_text, "ten")
            for i in range(4):
                janshi[i].janshi_reset()
                janshi[i].kaze = (oya + i)%4
                janshi[i].tensuu = int(splitted_read_text[ten_index+i])*100
            janshi[0].tehai_136 = function_tenhou.get_haipai_136(splitted_read_text)
            janshi[0].tehai = function_tenhou.get_haipai_str(splitted_read_text)
            janshi[0].riipai()

            print("自家: " + kaze_to_str[janshi0.kaze] + "  点数: " + str(janshi0.tensuu))
            print("下家: " + kaze_to_str[janshi1.kaze] + "  点数: " + str(janshi1.tensuu))
            print("対面: " + kaze_to_str[janshi2.kaze] + "  点数: " + str(janshi2.tensuu))
            print("上家: " + kaze_to_str[janshi3.kaze] + "  点数: " + str(janshi3.tensuu))

            print()
            print("初期手牌")
            print(janshi0.tehai)
            #print(janshi0.tehai_136)

    #誰かが打牌したときに更新
    #last_dahai = 35 #直前の打牌。鳴きに利用する。
    #last_teban = 0  #直前の打牌をしたプレイヤー

    if ingame_flag:
        print("IN GAME")
        while True:
            time.sleep(0.1)
            read_text = read_packet.read_packet()
            if len(read_text) == 0:
                continue
            
            splitted_read_text = function_tenhou.read_text_decomp(read_text)

            #牌をツモってきたとき
            if splitted_read_text[1][0] == "T":
                
                hai_136 = int(splitted_read_text[1].strip("T"))
                #print(hai_136)
                print("ツモ牌: " + function_tenhou.hai_convert_136_to_str(hai_136))
                hai_str = function_tenhou.hai_convert_136_to_str(hai_136)
                janshi[0].tsumo(hai_str, hai_136) 
                
                #暗槓&カカン
                temp_ankan = janshi[0].ankan(taku)
                if temp_ankan:              
                    pass
                if janshi[0].kakan(taku):
                    pass
                
                #ツモアガリか立直
                if len(splitted_read_text) > 2:
                    #ツモアガリ
                    if splitted_read_text[3] == "16":
                        #とりあえずツモアガリする
                        print("プレイヤーのツモアガリ")
                        #天鳳に出力
                        continue
                    #立直
                    if splitted_read_text[3] == "32":
                        a, b, c = riichi_hantei.riichi_hantei(janshi[0], taku)
                        if a:
                            janshi[0].func_riichi(taku)
                            #riichi&dahai
                            #天鳳に出力
                            continue
                            pass
                
                #ツモアガリも立直もしない時
                max_index = janshi[0].dahai(taku)
                hai_str = janshi[0].tehai[max_index]
                #天鳳に出力
                continue

            #自家打牌時
            if splitted_read_text[1][0] == "D":
                hai_136 = int(splitted_read_text[1].strip("D"))
                print("自家 打: " + function_tenhou.hai_convert_136_to_str(hai_136))
                hai_str = function_tenhou.hai_convert_136_to_str(hai_136)
                
                #print(janshi0.tehai_136)
                #print(hai_136)

                janshi[0].tehai.remove(hai_str)
                janshi[0].tehai_136.remove(hai_136)

                last_dahai = hai_136 #直前の打牌。鳴きに利用する。
                last_teban = 0  #直前の打牌をしたプレイヤー

                continue

            #他家打牌家

            #下家
            if splitted_read_text[1][0] == "E":
                
                hai_136 = int(splitted_read_text[1].strip("E"))
                hai_str = function_tenhou.hai_convert_136_to_str(hai_136)
                janshi[0].vertual_yama.remove(hai_str)
                janshi[1].sutehai.append(hai_str)

                print("下家 打:" + hai_str)

                last_dahai = hai_136 #直前の打牌。鳴きに利用する。
                last_teban = 1  #直前の打牌をしたプレイヤー
                
                #以下鳴き　鳴きの基本方針→赤ドラを副露牌に含められるときは必ず含める
                if len(splitted_read_text) > 2:
                    #ロン通知
                    if int(splitted_read_text[3]) >= 8:
                        #あがる
                        pass
                    #ポン通知
                    elif splitted_read_text[3] == "1":
                        #ポン打診
                        if janshi[0].pon(taku, hai_str):
                            #ポンする
                            pass
                        else:
                            #鳴かない
                            pass
                    #チー通知
                    elif splitted_read_text[3] == "4":
                        #チー打診
                        chii_index = janshi[0].chii(taku, hai_str)
                        if chii_index != -1:
                            #チーする
                            pass
                        else:
                            #鳴かない
                            pass
                    #ポンチー通知#ポンチーダイミンカン通知
                    elif splitted_read_text[3] == "5" or splitted_read_text[3] == "7":
                        #ポンチー打診
                        if janshi[0].pon(taku, hai_str):
                            #ポンする
                            #continue
                            pass
                        chii_index = janshi[0].chii(taku, hai_str)
                        if chii_index != -1:
                            #チーする
                            #continue
                            pass
                        #鳴かない
                        continue   
                continue

            if splitted_read_text[1][0] == "e":
                hai_136 = int(splitted_read_text[1].strip("e"))
                hai_str = function_tenhou.hai_convert_136_to_str(hai_136)
                janshi[0].vertual_yama.remove(hai_str)
                janshi[1].sutehai.append(hai_str)

                print("下家 打:" + hai_str)

                last_dahai = hai_136 #直前の打牌。鳴きに利用する。
                last_teban = 1  #直前の打牌をしたプレイヤー
                
                #以下鳴き　鳴きの基本方針→赤ドラを副露牌に含められるときは必ず含める
                if len(splitted_read_text) > 2:
                    #ロン通知
                    if int(splitted_read_text[3]) >= 8:
                        #あがる
                        pass
                    #ポン通知
                    elif splitted_read_text[3] == "1":
                        #ポン打診
                        if janshi[0].pon(taku, hai_str):
                            #ポンする
                            pass
                        else:
                            #鳴かない
                            pass
                    #チー通知
                    elif splitted_read_text[3] == "4":
                        #チー打診
                        chii_index = janshi[0].chii(taku, hai_str)
                        if chii_index != -1:
                            #チーする
                            pass
                        else:
                            #鳴かない
                            pass
                    #ポンチー通知#ポンチーダイミンカン通知
                    elif splitted_read_text[3] == "5" or splitted_read_text[3] == "7":
                        #ポンチー打診
                        if janshi[0].pon(taku, hai_str):
                            #ポンする
                            #continue
                            pass
                        chii_index = janshi[0].chii(taku, hai_str)
                        if chii_index != -1:
                            #チーする
                            #continue
                            pass
                        #鳴かない
                        continue   
                continue

            #対面
            if splitted_read_text[1][0] == "F" and splitted_read_text[1] != "FURITEN":
                hai_136 = int(splitted_read_text[1].strip("F"))
                hai_str = function_tenhou.hai_convert_136_to_str(hai_136)
                janshi[0].vertual_yama.remove(hai_str)
                janshi[2].sutehai.append(hai_str)
                
                print("対面 打:" + hai_str)

                last_dahai = hai_136 #直前の打牌。鳴きに利用する。
                last_teban = 2  #直前の打牌をしたプレイヤー
                
                #以下鳴き　鳴きの基本方針→赤ドラを副露牌に含められるときは必ず含める
                if len(splitted_read_text) > 2:
                    #ロン通知
                    if int(splitted_read_text[3]) >= 8:
                        #あがる
                        pass
                    #ポン通知
                    elif splitted_read_text[3] == "1":
                        #ポン打診
                        if janshi[0].pon(taku, hai_str):
                            #ポンする
                            pass
                        else:
                            #鳴かない
                            pass
                    #チー通知
                    elif splitted_read_text[3] == "4":
                        #チー打診
                        chii_index = janshi[0].chii(taku, hai_str)
                        if chii_index != -1:
                            #チーする
                            pass
                        else:
                            #鳴かない
                            pass
                    #ポンチー通知#ポンチーダイミンカン通知
                    elif splitted_read_text[3] == "5" or splitted_read_text[3] == "7":
                        #ポンチー打診
                        if janshi[0].pon(taku, hai_str):
                            #ポンする
                            #continue
                            pass
                        chii_index = janshi[0].chii(taku, hai_str)
                        if chii_index != -1:
                            #チーする
                            #continue
                            pass
                        #鳴かない
                        continue   
                continue

            if splitted_read_text[1][0] == "f":
                hai_136 = int(splitted_read_text[1].strip("f"))
                hai_str = function_tenhou.hai_convert_136_to_str(hai_136)
                janshi[0].vertual_yama.remove(hai_str)
                janshi[2].sutehai.append(hai_str)

                print("対面 打:" + hai_str)

                last_dahai = hai_136 #直前の打牌。鳴きに利用する。
                last_teban = 2  #直前の打牌をしたプレイヤー
                
                #以下鳴き　鳴きの基本方針→赤ドラを副露牌に含められるときは必ず含める
                if len(splitted_read_text) > 2:
                    #ロン通知
                    if int(splitted_read_text[3]) >= 8:
                        #あがる
                        pass
                    #ポン通知
                    elif splitted_read_text[3] == "1":
                        #ポン打診
                        if janshi[0].pon(taku, hai_str):
                            #ポンする
                            pass
                        else:
                            #鳴かない
                            pass
                    #チー通知
                    elif splitted_read_text[3] == "4":
                        #チー打診
                        chii_index = janshi[0].chii(taku, hai_str)
                        if chii_index != -1:
                            #チーする
                            pass
                        else:
                            #鳴かない
                            pass
                    #ポンチー通知#ポンチーダイミンカン通知
                    elif splitted_read_text[3] == "5" or splitted_read_text[3] == "7":
                        #ポンチー打診
                        if janshi[0].pon(taku, hai_str):
                            #ポンする
                            #continue
                            pass
                        chii_index = janshi[0].chii(taku, hai_str)
                        if chii_index != -1:
                            #チーする
                            #continue
                            pass
                        #鳴かない
                        continue   
                continue
                
            #上家
            if splitted_read_text[1][0] == "G":
                hai_136 = int(splitted_read_text[1].strip("G"))
                hai_str = function_tenhou.hai_convert_136_to_str(hai_136)
                janshi[0].vertual_yama.remove(hai_str)
                janshi[3].sutehai.append(hai_str)

                print("上家 打:" + hai_str)

                last_dahai = hai_136 #直前の打牌。鳴きに利用する。
                last_teban = 3  #直前の打牌をしたプレイヤー
                
                #以下鳴き　鳴きの基本方針→赤ドラを副露牌に含められるときは必ず含める
                if len(splitted_read_text) > 2:
                    #ロン通知
                    if int(splitted_read_text[3]) >= 8:
                        #あがる
                        pass
                    #ポン通知
                    elif splitted_read_text[3] == "1":
                        #ポン打診
                        if janshi[0].pon(taku, hai_str):
                            #ポンする
                            pass
                        else:
                            #鳴かない
                            pass
                    #チー通知
                    elif splitted_read_text[3] == "4":
                        #チー打診
                        chii_index = janshi[0].chii(taku, hai_str)
                        if chii_index != -1:
                            #チーする
                            pass
                        else:
                            #鳴かない
                            pass
                    #ポンチー通知#ポンチーダイミンカン通知
                    elif splitted_read_text[3] == "5" or splitted_read_text[3] == "7":
                        #ポンチー打診
                        if janshi[0].pon(taku, hai_str):
                            #ポンする
                            #continue
                            pass
                        chii_index = janshi[0].chii(taku, hai_str)
                        if chii_index != -1:
                            #チーする
                            #continue
                            pass
                        #鳴かない
                        continue   
                continue

            if splitted_read_text[1][0] == "g":
                hai_136 = int(splitted_read_text[1].strip("g"))
                hai_str = function_tenhou.hai_convert_136_to_str(hai_136)
                janshi[0].vertual_yama.remove(hai_str)
                janshi[3].sutehai.append(hai_str)

                print("上家 打:" + hai_str)    

                last_dahai = hai_136 #直前の打牌。鳴きに利用する。
                last_teban = 3  #直前の打牌をしたプレイヤー
                
                #以下鳴き　鳴きの基本方針→赤ドラを副露牌に含められるときは必ず含める
                if len(splitted_read_text) > 2:
                    #ロン通知
                    if int(splitted_read_text[3]) >= 8:
                        #あがる
                        pass
                    #ポン通知
                    elif splitted_read_text[3] == "1":
                        #ポン打診
                        if janshi[0].pon(taku, hai_str):
                            #ポンする
                            pass
                        else:
                            #鳴かない
                            pass
                    #チー通知
                    elif splitted_read_text[3] == "4":
                        #チー打診
                        chii_index = janshi[0].chii(taku, hai_str)
                        if chii_index != -1:
                            #チーする
                            pass
                        else:
                            #鳴かない
                            pass
                    #ポンチー通知#ポンチーダイミンカン通知
                    elif splitted_read_text[3] == "5" or splitted_read_text[3] == "7":
                        #ポンチー打診
                        if janshi[0].pon(taku, hai_str):
                            #ポンする
                            #continue
                            pass
                        chii_index = janshi[0].chii(taku, hai_str)
                        if chii_index != -1:
                            #チーする
                            #continue
                            pass
                        #鳴かない
                        continue   
                continue


            #各種鳴き
            if splitted_read_text[1] == "N":
                who = int(splitted_read_text[3])
                m = int(splitted_read_text[5])
                m_decoded_list = decode_m.decode_m(m)
                
                if m_decoded_list[0] == 1:
                    #ポン
                    
                    #他家がポン→バーチャル山更新
                    if who:
                        print(who_to_str[who] + ": ポン")
                        for i in range(3):
                            if last_dahai != m_decoded_list[1][i]:
                                janshi[0].vertual_yama.remove(function_tenhou.hai_convert_136_to_str(m_decoded_list[1][i]))
                    
                    #自家がポン→副露リスト更新
                    else:
                        print(who_to_str[who] + ": ポン")
                        janshi[0].pon_add(taku, m_decoded_list[1], last_teban)
                

                elif m_decoded_list[0] == 2:
                    #ダイミンカン
                    #他家がダイミンカン→バーチャル山更新
                    if who:
                        for i in range(3):
                            janshi[0].vertual_yama.remove(function_tenhou.hai_convert_136_to_str(m_decoded_list[1][i]))
                    #自家がダイミンカン
                    else:
                        #しない
                        pass         
                
                elif m_decoded_list[0] == 3:
                    #チー
                    
                    #他家がチー→バーチャル山更新
                    if who:
                        print(who_to_str[who] + ": チー")
                        for i in range(3):
                            if last_dahai != m_decoded_list[1][i]:
                                janshi[0].vertual_yama.remove(function_tenhou.hai_convert_136_to_str(m_decoded_list[1][i]))
                    
                    #自家がチー→副露リスト更新
                    else:
                        print(who_to_str[who] + ": チー")
                        janshi[0].chii_add(taku, m_decoded_list[1], last_dahai)
                        
                elif m_decoded_list[0] == 4:
                    #アンカン
                    
                    #他家が暗槓→バーチャル山更新
                    if who:
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
                continue

            #ドラ追加
            if splitted_read_text[1] == "DORA":
                hai_136 = int(splitted_read_text[3])
                hai_str = function_tenhou.hai_convert_136_to_str(hai_136)
                taku.dorahyouji.append(hai_str)
                janshi[0].vertual_yama.remove(hai_str)
                continue

            #立直時
            if splitted_read_text[1] == "REACH":
                who = int(splitted_read_text[3])
                #自家
                if splitted_read_text[3] == "0":
                    print(who_to_str[who] + ": リーチ")
                    janshi[0].riichi = 1
                else:
                    print(who_to_str[who] + ": リーチ")
                continue

            #アガリ時
            if splitted_read_text[1] == "AGARI":
                who = int(splitted_read_text[function_tenhou.find_str(splitted_read_text, "who")])
                print(who_to_str[who] + ": アガリ")
                break
                

            #流局時
            if splitted_read_text[1] == "RYUUKYOKU":
                break
               