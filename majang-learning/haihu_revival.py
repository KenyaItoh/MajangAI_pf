import function
import function_tenhou
import xml.etree.ElementTree as ET

#天鳳ログの一局を読み込んで疑似的に再現する

#使い方
#game=Game(kyoku_str)のようにgameインスタンスを作る．kyoku_strは<INIT ~ /INIT>
#で囲まれた，一局の牌譜ログ文字列．
#gameの各プロパティで，現在の状況を取得できる(最初は配牌時の状況)．
#game.play()で，牌譜を一つ読み進めて状況を更新する（＝次の< />を読み込んで反映する）

class Game():
    def __init__(self,kyoku_str):
        self.log = ET.fromstring('<root>'+kyoku_str+'</root>')
        seed = self.log[0].attrib['seed'].split(',')
        self.kyoku = int(seed[0])#東1=0 ~ 南4=7
        self.honba = int(seed[1])
        self.reabou = int(seed[2])
        self.dorahyouji = [int(seed[5])]
        
        #各プレイヤーのオブジェクト．手牌や捨て牌・点数などが確認可能
        self.janshi = []
        for i in range(4):
            self.janshi.append(Janshi(i,self.log[0].attrib['hai'+str(i)], True if str(i) == self.log[0].attrib['oya'] else False))
        self.proceed_count = 1

    def play(self):
        self.action = self.log[self.proceed_count]
        tsumo_alphabet_to_player_num = {'T':0,'U':1,'V':2,'W':3}
        dahai_alphabet_to_player_num = {'D':0,'E':1,'F':2,'G':3}
        #ドラ
        if self.action.tag == 'DORA':
            self.dorahyouji.append(self.action.attrib['hai'])
        #ツモ
        elif self.action.tag[0] in ('T','U','V','W') and self.action.tag[1].isdecimal():
            #ツモプレイヤー
            self.action_player_num = tsumo_alphabet_to_player_num[self.action.tag[0]]
            #tsumoメソッドの実行
            self.janshi[self.action_player_num].tsumo(int(self.action.tag[1:]))
        #打
        elif self.action.tag[0] in ('D','E','F','G') and self.action.tag[1].isdecimal():
            #打プレイヤー
            self.action_player_num = dahai_alphabet_to_player_num[self.action.tag[0]]
            #dahaiメソッドの実行
            self.janshi[self.action_player_num].dahai(int(self.action.tag[1:]))
        #鳴き
        elif self.action.tag == 'N':
            #鳴いたプレイヤー
            self.action_player_num = int(self.action.attrib['who'])
            #Nの前のlast_dahaiを探す。
            last_dahai_cnt = self.proceed_count-1
            last_dahai = self.log[last_dahai_cnt].tag
            while last_dahai[0] not in ('D','E','F','G') or not last_dahai[1].isdecimal():
                last_dahai_cnt -= 1
                last_dahai = self.log[last_dahai_cnt].tag
            #last_dahaiを打ったプレイヤーlast_player_numを特定する。
            last_player_num = dahai_alphabet_to_player_num[last_dahai[0]]
            #nakiメソッドの実行
            self.janshi[self.action_player_num].naki(int(self.action.attrib['m'])\
                ,last_dahai[1:],(last_player_num - self.action_player_num) % 4)
        #リーチ
        elif self.action.tag == 'REACH':
            self.action_player_num = int(self.action.attrib['who'])
            if self.action.attrib['step'] == '1':#REACHタグは2ステップに分かれてる
                self.janshi[self.action_player_num].reach = True  #リーチフラグ
            else:
                self.janshi[self.action_player_num].tensu -= 1000 #リーチ棒
        #ドラ
        elif self.action.tag == 'DORA':
            self.dorahyouji.append(self.action.attrib['DORA'])
        elif self.action.tag in ('AGARI','RYUUKYOKU'):
            return 1
        
        #デバッグ用
        # print(self.action_player_num,self.janshi[self.action_player_num].tsumoAndNaki,\
        #     self.janshi[self.action_player_num].kawa,self.janshi[self.action_player_num]\
        #         .tehai,self.janshi[self.action_player_num].reach,self.janshi[self.action_player_num].fuurohai,self.janshi[self.action_player_num].fuuro_akadora_list)
        
        
        # #牌譜の読み込みを一つ進める
        self.proceed_count += 1
     
    #haiがドラならTrue，非ドラならFalse    
    def is_dora(self,hai):
        hai_type = int(hai/4)
        for h2 in self.dorahyouji:
            hai2_type = int(int(h2)/4)
            if hai2_type < 8 or 8 < hai2_type < 17 or 17 < hai2_type < 26\
                or 26 < hai2_type < 30 or 30 < hai2_type <33:
                if hai_type == hai2_type + 1:
                    return True
            elif hai2_type in (8,17,26):
                if hai_type == hai2_type - 8:
                    return True
            elif hai2_type == 30:
                if hai_type == 26:
                    return True
            else:
                if hai_type == 30:
                    return True
        return False


#Gameで使う牌譜再現用の仮想プレイヤー
class Janshi():
    def __init__(self,player_num,haipai,is_oya):
        self.tehai = [] #いつものインデックス形式
        for h in haipai.split(','):
            self.tehai.append(int(h))
        self.fuurohai = [] #[i,j,k]i:チー１、ポン２、加カン３、暗槓４、j:牌index、k:誰から鳴いた（player_num)
        self.fuuro_akadora_list = []
        self.fuurosu = 0
        self.tsumoAndNaki = [] #[str]
        self.kawa = [] #[int]自摸切りならD、手出しならｄで表す
        self.reach = False
        self.tenpai = False
        self.player_num = player_num
        self.ankan_list = []
        self.tensu = 25000
        self.is_oya = is_oya
        self.tsumoHai = -1
    
    def tsumo(self,hai):
        self.tehai.append(hai)
        self.tsumoAndNaki.append('t'+str(hai))
        self.tsumoHai = hai

    def dahai(self,hai):
        self.tehai.remove(hai)
        if hai == self.tsumoHai:#自摸切りならD、手出しならｄで表す
            self.kawa.append('D'+str(hai))
        else :
            self.kawa.append('d'+str(hai))    
            
    #last_dahai→136表記の最後の打牌、last_teban→selfから見た手番。下:1、対:2、上:3
    def naki(self, m, last_dahai, last_teban):
        naki_info = decode_m(m)
        self.fuurosu += 1
        self.tsumoHai = -1 #自摸切りかどうかの確認。鳴きなのでリセット。
        #アンカン
        if naki_info[0] == 4:
            #[1][0]だと赤ドラになる可能性があるため[1][1]
            self.ankan_list.append(convert_mjlog_to_index(naki_info[1][1]))
            for h in naki_info[1]:
                if h in self.tehai:
                    self.tehai.remove(h)

        #チー
        elif naki_info[0] == 3:
            hai_arr = naki_info[1]
            #tehaiから鳴きに使った牌の削除
            for h in naki_info[1]:
                if h in self.tehai:
                    self.tehai.remove(h)
            
            #副露リストへの追加
            last_hai_index = convert_mjlog_to_index(int(last_dahai))
            temp = function.akadora_convert(function_tenhou.tehai_convert_136_to_str(hai_arr))
            temp_arr_str = temp[0]
            akadora_flag = temp[1] 
            hai_arr_index = sorted(function.tehai_convert2(temp_arr_str))
            if hai_arr_index[0] == last_hai_index:
                self.fuurohai.append([1,last_hai_index,2])
            elif hai_arr_index[1] == last_hai_index:
                self.fuurohai.append([1,last_hai_index,1])
            else: #hai_arr_index[2] == last_hai_index:
                self.fuurohai.append([1,last_hai_index,0])
            if akadora_flag:
                self.fuuro_akadora_list.append(True)
            else:
                self.fuuro_akadora_list.append(False)

        #ポン
        elif naki_info[0] == 1:
            hai_arr = naki_info[1]
            teban = last_teban
            #tehaiの操作
            for h in naki_info[1]:
                if h in self.tehai:
                    self.tehai.remove(h)

            #副露リストへの追加
            #先頭が赤ドラ
            if hai_arr[0] == 16 or hai_arr[0] == 52 or hai_arr[0] == 88:
                hai_str = function_tenhou.hai_convert_136_to_str(hai_arr[1])
                hai_index = function.hai_convert(hai_str)
                self.fuurohai.append([2,hai_index,teban])
                self.fuuro_akadora_list.append(True)
            #真ん中が赤ドラ
            elif hai_arr[1] == 16 or hai_arr[1] == 52 or hai_arr[1] == 88:
                hai_str = function_tenhou.hai_convert_136_to_str(hai_arr[2])
                hai_index = function.hai_convert(hai_str)
                self.fuurohai.append([2,hai_index,teban])
                self.fuuro_akadora_list.append(True)
            #最後が赤ドラ
            elif hai_arr[2] == 16 or hai_arr[2] == 52 or hai_arr[2] == 88:
                hai_str = function_tenhou.hai_convert_136_to_str(hai_arr[0])
                hai_index = function.hai_convert(hai_str)
                self.fuurohai.append([2,hai_index,teban])
                self.fuuro_akadora_list.append(True)
            #赤ドラなし
            else:
                hai_str = function_tenhou.hai_convert_136_to_str(hai_arr[0])
                hai_index = function.hai_convert(hai_str)
                self.fuurohai.append([2,hai_index,teban])
                self.fuuro_akadora_list.append(True)

        #ダイミンカン
        elif naki_info[0] == 2:
            hai_arr = naki_info[1]
            teban = last_teban
            last_hai_str = function_tenhou.hai_convert_136_to_str(int(last_dahai))
            last_hai_index = function.hai_convert(function.akadora_hai_convert(last_hai_str))
            
            #手牌から削除
            for h in naki_info[1]:
                if h in self.tehai:
                    self.tehai.remove(h)

            #副露リストに追加
            self.fuurohai.append([3,last_hai_index ,teban])
            if last_hai_index%10 == 5 and last_hai_index < 30:
                self.fuuro_akadora_list.append(True)
            else:
                self.fuuro_akadora_list.append(False)

        #カカン
        elif naki_info[0] == 5:
            hai_arr = naki_info[1]
            #元からソートされているはず
            #カカンした牌の種類(hai_arr[1]としているので赤の可能性なし)
            kakan_index = function.hai_convert(function_tenhou.hai_convert_136_to_str(hai_arr[1]))
            #実際に加えられた牌のID(赤の可能性あり)
            temp_arr = hai_arr.copy()
            kakan_hai_id = 6 + temp_arr[0] - (temp_arr[0]%4)*2 - temp_arr[1] % 4 - temp_arr[2] % 4
            
            #remove
            self.tehai.remove(kakan_hai_id)
            
            #副露リスト更新
            for i in range(len(self.fuurohai)):
                if self.fuurohai[i][1] == kakan_index and self.fuurohai[i][0] == 2:
                    self.fuurohai[i][0] = 3
                    #kakan_indexが5,15,25なら赤ドラあり
                    if kakan_index % 10 == 5 and kakan_index < 30:
                        self.fuuro_akadora_list[i] = True

            

    
#mjlog方式(天鳳ログの形式)からよく使う方式に変換
#各種の自作メソッドtensu_calcなどに必要   
def convert_mjlog_to_index(hai):
    if hai == 16:
        return 0
    elif hai == 52:
        return 10
    elif hai == 88:
        return 20
    else:
        hai1 = hai >> 2 
        idx = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37]
        return idx[hai1]
 
#mjlog方式の面子を変換
def decode_m(m):
    kui = (m & 3)
    fuuro_label = 0
    # 順子
    if m & (1<<2):
        fuuro_label = 3
        t = (m & 0xFC00) >> 10
        r = t % 3
        t = int(t / 3)
        t = int(t / 7) * 9 + (t % 7)
        t *= 4
        h = [t + 4 * 0 + ((m & 0x0018) >> 3), t + 4 * 1 + ((m & 0x0060) >> 5), t + 4 * 2 + ((m & 0x0180) >> 7)]
        
        # 牌の並び替え
        if r == 1:
            h.insert(0, h[1])
            del(h[2])
        elif r == 2:
            h.insert(2, h[1])
            del(h[1])

    # 刻子
    elif m & (1<<3):
        fuuro_label = 1
        unused = (m & 0x0060) >> 5
        t = (m & 0xFE00) >> 9
        r = t % 3
        t = int(t / 3)
        t  *= 4
        h = [t, t, t]
        if unused == 0:
            h[0]  += 1;h[1]  += 2;h[2]  += 3
        elif unused == 1:
            h[0]  += 0;h[1]  += 2;h[2]  += 3
        elif unused == 2:
            h[0]  += 0;h[1]  += 1;h[2]  += 3
        elif unused == 3:
            h[0]  += 0;h[1]  += 1;h[2]  += 2
        # 牌の並び替え
        if r == 1:
            h.insert(0, h[1])
            del(h[2])
        elif r == 2:
            h.insert(2, h[1])
            del(h[1])

        if kui < 3:
            h.insert(2, h[1])
            del(h[1])
        elif kui < 2:
            h.insert(2, h[1])
            del(h[1])

    # 加槓
    elif m & (1<<4):
        fuuro_label = 5
        added = (m & 0x0060) >> 5
        t = (m & 0xFE00) >> 9
        r = t % 3
        t = int(t / 3)
        t *= 4
        h = [t, t, t]
        if added == 0:
            h[0]  += 1;h[1]  += 2;h[2]  += 3
        elif added == 1:
            h[0]  += 0;h[1]  += 2;h[2]  += 3
        elif added == 2:
            h[0]  += 0;h[1]  += 1;h[2]  += 3
        elif added == 3:
            h[0]  += 0;h[1]  += 1;h[2]  += 2
        # 牌の並び替え
        if r == 1:
            h.insert(0, h[1])
            del(h[2])
        elif r == 2:
            h.insert(2, h[1])
            del(h[1])
        
    # 北抜き
    elif m & (1<<5):
        return "未実装"

    # 暗槓, 明槓
    else:   
        hai0 = (m & 0xFF00) >> 8
        if not kui:
            hai0 = (hai0 & ~3) + 3 # 暗槓
            fuuro_label = 4
        else:
            fuuro_label = 2       
        t = int(hai0 / 4) * 4
        h = [t, t+1, t+2, t+3]

    return fuuro_label, h

