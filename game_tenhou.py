import sys,os
import time
sys.path.append(os.getcwd()+"\\files")
import function_tenhou
import majang
import riichi_hantei3
import decode_m
import read_packet
import shanten_check_new
import function
import ingame_func
sys.path.append(os.getcwd()+"\\guis")
from gui_hub import gui_click

if __name__ == "__main__":
    owari_flag = False
    itr = 100 #試合数
    taku = majang.Taku()

    sleep_time_thresh = taku.sleep_time_thresh
    sleep_time = taku.sleep_time

    janshi0 = majang.Janshi_p(2) #プレイヤー(自家)
    janshi1 = majang.Janshi_e(1) #下家
    janshi2 = majang.Janshi_e(2) #対面
    janshi3 = majang.Janshi_e(3) #上家

    janshi = [janshi0, janshi1, janshi2, janshi3]

    who_to_str = {0:"自家", 1:"下家", 2:"対面", 3:"上家"}
    kaze_to_str = {0: "東", 1: "南", 2: "西", 3: "北"}
    kyoku_to_str = {0:'東１局', 1:'東2局', 2:'東3局', 3:'東4局', 4:'南１局', 5:'南2局', 6:'南3局', 7:'南4局', 8:'西1局' , 9:'西2局' , 10:'西3局' , 11:'西4局'}
    dan_to_str = {0:"10級", 1:"9級", 2:"8級", 3:"7級", 4:"6級", 5:"5級", 6:"4級", 7:"3級", 8:"2級", 9:"1級", 10:"初段", 11:"二段", 12:"三段", 13:"四段", 14:"五段", 15:"六段", 16:"七段", 17:"八段", 18:"九段", 19:"十段", 20:"天鳳位"}

    #前処理
    while True:
        time.sleep(0.5)
        read_text = read_packet.read_packet()
        splitted_read_text = function_tenhou.read_text_decomp(read_text)
        if len(splitted_read_text) > 0:
            tag_index = function_tenhou.find_str(splitted_read_text, "tag")
            if splitted_read_text[tag_index] == "HELO":
                #段位等更新
                PF4_pos = function_tenhou.find_str(splitted_read_text, "PF4")
                if PF4_pos != -1:
                    janshi0.dan = dan_to_str[int(splitted_read_text[PF4_pos])]
                    janshi0.dan_point = int(splitted_read_text[PF4_pos+1])
                    janshi0.rating = int(float(splitted_read_text[PF4_pos+2]))
                    print()
                    print("======アカウント情報======")
                    print("アカウント名: DivyneDx")
                    print("段位： " + janshi0.dan)
                    print("ポイント: " + str(janshi0.dan_point))
                    print("レーティング: " + str(janshi0.rating))
                    print()
                    break
    begin_flag = True

    for itration in range(itr):
        print(str(itration+1) + "回目")
        print("マッチング開始")
        #ここで対戦予約ボタンを押す

        #owari_flagリセット
        owari_flag = False
        ranking_flag = False

        while True:
            time.sleep(0.5)
            if owari_flag:
                break
            read_text = read_packet.read_packet()
            splitted_read_text = function_tenhou.read_text_decomp(read_text)
            ingame_flag = False

            #最初だけ手動
            if not begin_flag:
                #OKを押す
                gui_click("Ok")
                gui_click("Yoyaku")

            #初期
            if len(splitted_read_text) > 0:
                tag_index = function_tenhou.find_str(splitted_read_text, "tag")

                if splitted_read_text[tag_index] == "HELO":
                    owari_flag = True
                    #段位等更新
                    PF4_pos = function_tenhou.find_str(splitted_read_text, "PF4")
                    if PF4_pos != -1:
                        janshi0.dan = dan_to_str[int(splitted_read_text[PF4_pos])]
                        janshi0.dan_point = int(splitted_read_text[PF4_pos+1])
                        janshi0.rating = int(float(splitted_read_text[PF4_pos+2]))
                        print()
                        print("======アカウント情報======")
                        print("アカウント名: DivyneDx")
                        print("段位： " + janshi0.dan)
                        print("ポイント: " + str(janshi0.dan_point))
                        print("レーティング: " + str(janshi0.rating))
                        print()
                        continue

                if splitted_read_text[tag_index] == "RANKING" and ranking_flag:
                    owari_flag = True
                    continue

                if splitted_read_text[tag_index] == "INIT":
                    begin_flag = False
                    time.sleep(1.0)
                    ingame_flag = True
                    ingame_func.init_game(janshi,taku,splitted_read_text)

            ############################INGAME####################################
            if ingame_flag:
                print("IN GAME")
                while True:
                    time.sleep(0.5)
                    read_text = read_packet.read_packet()
                    if len(read_text) == 0:
                        continue
                    
                    splitted_read_text = function_tenhou.read_text_decomp(read_text)
                    tag_index = function_tenhou.find_str(splitted_read_text, "tag")

                    if len(splitted_read_text) == 0:
                        continue

                    #他家ツモ時
                    if splitted_read_text[tag_index] == "U" or splitted_read_text[tag_index] == "V" or splitted_read_text[tag_index] == "W":
                        taku.yama_nokori -= 1

                    #牌をツモってきたとき
                    if splitted_read_text[1][0] == "T":
                        ingame_func.jicha_tsumo(janshi,taku,splitted_read_text)
                        continue

                    #自家打牌時
                    if splitted_read_text[1][0] == "D" and splitted_read_text[1] != "DORA":
                        hai_136 = int(splitted_read_text[1].strip("D"))
                        print("自家 打:" + function_tenhou.hai_convert_136_to_str(hai_136))
                        hai_str = function_tenhou.hai_convert_136_to_str(hai_136)
                        janshi[0].tehai.remove(hai_str)
                        janshi[0].tehai_136.remove(hai_136)
                        janshi[0].sutehai.append(hai_str)
                        taku.last_dahai = hai_136 #直前の打牌。鳴きに利用する。
                        taku.last_teban = 0  #直前の打牌をしたプレイヤー
                        continue

                    #他家打牌時

                    #下家
                    if splitted_read_text[1][0] == "E":
                        ingame_func.tacha_dahai("E",janshi,taku,splitted_read_text)
                        continue

                    if splitted_read_text[1][0] == "e":
                        ingame_func.tacha_dahai("e",janshi,taku,splitted_read_text)
                        continue

                    #対面
                    if splitted_read_text[1][0] == "F" and splitted_read_text[1] != "FURITEN":
                        ingame_func.tacha_dahai("e",janshi,taku,splitted_read_text)
                        continue

                    if splitted_read_text[1][0] == "f":
                        ingame_func.tacha_dahai("f",janshi,taku,splitted_read_text)
                        continue
                        
                    #上家
                    if splitted_read_text[1][0] == "G" and splitted_read_text[1] != "GO":
                        ingame_func.tacha_dahai("G",janshi,taku,splitted_read_text)
                        continue

                    if splitted_read_text[1][0] == "g":
                        ingame_func.tacha_dahai("g",janshi,taku,splitted_read_text)
                        continue

                    #各種鳴き
                    if splitted_read_text[1] == "N":
                        ingame_func.naki(janshi, taku, splitted_read_text)
                        continue

                    #ドラ追加
                    if splitted_read_text[1] == "DORA":
                        hai_136 = int(splitted_read_text[3])
                        hai_str = function_tenhou.hai_convert_136_to_str(hai_136)
                        taku.dorahyouji.append(hai_str)
                        janshi[0].vertual_yama.remove(hai_str)
                        print("新ドラ表示牌:" + hai_str)
                        continue

                    #立直時
                    if splitted_read_text[1] == "REACH":
                        start = time.time()
                        step_index = function_tenhou.find_str(splitted_read_text, "step")
                        if int(splitted_read_text[step_index]) == 1:
                            who = int(splitted_read_text[3])
                            #自家
                            if splitted_read_text[3] == "0":
                                #天鳳に出力
                                if time.time() - start < sleep_time_thresh:
                                    time.sleep(sleep_time)
                                gui_click("Dahai",taku.riichi_dahai)
                                print(who_to_str[who] + ": リーチ")
                                janshi[0].riichi = 1
                            else:
                                print(who_to_str[who] + ": リーチ")
                                janshi[who].riichi = 1
                        else:
                            taku.kyoutaku_tensuu += 1000
                        continue

                    #アガリ時
                    if splitted_read_text[tag_index] == "AGARI":
                        who = int(splitted_read_text[function_tenhou.find_str(splitted_read_text, "who")])
                        print(who_to_str[who] + ": アガリ")
                        ranking_flag = True
                        break            

                    #流局時
                    if splitted_read_text[tag_index] == "RYUUKYOKU":
                        print("流局")
                        ranking_flag = True
                        break

                    #HELO テスト対局途中退出用
                    if splitted_read_text[tag_index] == "HELO":
                        owari_flag = True
                        break
        print()
        print("終局")             