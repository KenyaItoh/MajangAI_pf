import function
import evaluate
import shanten_check_new
import function_fuuro_convert
import tensu_calc
import teyaku_check
import copy
import function_tenhou
import eval_ensemble

class Taku:
    def __init__(self):
        self.yama_nokori = 70
        self.kaze_honba = [0,0] #東２局１本場→[1,1] 南４局3本場　→[7,3]
        self.dorahyouji = []
        self.uradorahyouji = []
        self.chankan_flag = False
        self.haitei_flag = False
        self.kyoutaku_tensuu = 0
        self.hash_table = shanten_check_new.read_hash_table_for_shanten_check()
        self.last_dahai = None
        self.last_teban = None
        self.bakyou_list = [0,0,0]
        self.naki_dahai = ""
        self.riichi_dahai = ""

        self.sleep_time = 1.5
        self.sleep_time_thresh = 1.5
 
    def taku_reset(self):
        self.yama_nokori = 70
        self.kaze_honba = [0,0] #東２局１本場→[1,1] 南４局3本場　→[7,3]
        self.dorahyouji = []
        self.uradorahyouji = []
        self.chankan_flag = False
        self.haitei_flag = False
        self.kyoutaku_tensuu = 0
        self.last_dahai = None
        self.last_teban = None
        self.naki_dahai = ""
        self.riichi_dahai = ""
        
class Janshi_p:
    def __init__(self, janshi_level):
        self.tehai = []
        self.tehai_136 = [] #データやり取り用
        self.syoki_tehai = [] #データ出力用
        self.sutehai = []
        self.tsumohai_list = [] #今のところデータ出力用
        self.vertual_yama = list(['1m', '1m', '1m', '1m', '2m', '2m', '2m', '2m', '3m', '3m', '3m', '3m', '4m', '4m', '4m', '4m', '5M', '5m', '5m', '5m', '6m', '6m', '6m', '6m', '7m', '7m', '7m', '7m', '8m', '8m', '8m', '8m', '9m', '9m', '9m', '9m', '1p', '1p', '1p', '1p', '2p', '2p', '2p', '2p', '3p', '3p', '3p', '3p', '4p', '4p', '4p', '4p', '5P', '5p', '5p', '5p', '6p', '6p', '6p', '6p', '7p', '7p', '7p', '7p', '8p', '8p', '8p', '8p', '9p', '9p', '9p', '9p', '1s', '1s', '1s', '1s', '2s', '2s', '2s', '2s', '3s', '3s', '3s', '3s', '4s', '4s', '4s', '4s', '5S', '5s', '5s', '5s', '6s', '6s', '6s', '6s', '7s', '7s', '7s', '7s', '8s', '8s', '8s', '8s', '9s', '9s', '9s', '9s','1z','1z','1z','1z','2z','2z','2z','2z','3z','3z','3z','3z','4z','4z','4z','4z', '5z', '5z', '5z', '5z', '6z', '6z', '6z', '6z', '7z', '7z', '7z', '7z'])
        self.temp_furiten = []
        self.fuurohai= []
        self.fuuro_akadora_list = []
        self.ankan_list = []
        self.tensuu = 25000
        self.kaze = 0 #東→0 南→1...
        #level 1→メンゼン型 2→鳴き型
        self.level = janshi_level
        self.riichi = 0 #0→リーチしていない 1→リーチ状態 2→ダブリー状態
        self.temp_riichi_flag = False
        self.rinshan_flag = False
        self.ippatsu_flag = False
        self.first_tsumo_flag = False #True #テンホウ、チーホウ、九種、ダブリーなどに使う
        self.rating = 0
        self.dan = 0
        self.dan_point = 0
        
    def janshi_reset(self):
        self.tehai = []
        self.tehai_136 = []
        self.syoki_tehai = []
        self.sutehai = []
        self.tsumohai_list = []
        self.vertual_yama = list(['1m', '1m', '1m', '1m', '2m', '2m', '2m', '2m', '3m', '3m', '3m', '3m', '4m', '4m', '4m', '4m', '5M', '5m', '5m', '5m', '6m', '6m', '6m', '6m', '7m', '7m', '7m', '7m', '8m', '8m', '8m', '8m', '9m', '9m', '9m', '9m', '1p', '1p', '1p', '1p', '2p', '2p', '2p', '2p', '3p', '3p', '3p', '3p', '4p', '4p', '4p', '4p', '5P', '5p', '5p', '5p', '6p', '6p', '6p', '6p', '7p', '7p', '7p', '7p', '8p', '8p', '8p', '8p', '9p', '9p', '9p', '9p', '1s', '1s', '1s', '1s', '2s', '2s', '2s', '2s', '3s', '3s', '3s', '3s', '4s', '4s', '4s', '4s', '5S', '5s', '5s', '5s', '6s', '6s', '6s', '6s', '7s', '7s', '7s', '7s', '8s', '8s', '8s', '8s', '9s', '9s', '9s', '9s','1z','1z','1z','1z','2z','2z','2z','2z','3z','3z','3z','3z','4z','4z','4z','4z', '5z', '5z', '5z', '5z', '6z', '6z', '6z', '6z', '7z', '7z', '7z', '7z'])
        self.temp_furiten = []
        self.fuurohai = []
        self.fuuro_akadora_list = []
        self.ankan_list = []
        self.riichi = 0 #0→リーチしていない 1→リーチ状態 2→ダブリー状態
        self.temp_riichi_flag = False
        self.rinshan_flag = False
        self.ippatsu_flag = False
        self.first_tsumo_flag = False #True #テンホウ、チーホウ、九種などに使う
    
    def get_haipai(self, hai_str_list):
        self.tehai = hai_str_list
        self.riipai()
    
    def init_vertual_yama(self, taku):
        self.vertual_yama.remove(taku.dorahyouji[0])
        for i in range(len(self.tehai)):
            self.vertual_yama.remove(self.tehai[i])
    
    def renew_vertual_yama(self, hai_str):
        self.vertual_yama.remove(hai_str)
        
    def renew_vertual_yama_pon(self, hai_str, janshi_pon):
        hai_index = function.hai_convert(hai_str)
        
        #hai_strが5でjanshi_ponのfuuro_akadora_list[-1]がTrueなら赤ドラを追加
        if hai_index % 10 == 5 and janshi_pon.fuuro_akadora_list[-1]:
            self.vertual_yama.remove(hai_str)
            self.vertual_yama.remove(function.hai_convert_reverse(hai_index-5))
        #赤5が鳴かれたとき
        elif hai_index % 10 == 0:
            self.vertual_yama.remove(function.hai_convert_reverse(hai_index+5))
            self.vertual_yama.remove(function.hai_convert_reverse(hai_index+5))
        else:
            self.vertual_yama.remove(hai_str)
            self.vertual_yama.remove(hai_str)
    
    def renew_vertual_yama_chii(self, hai_str, chii_index, janshi_chii):
        hai_index = function.hai_convert(hai_str)
        
        #もし3が鳴かれてjanshi_chiiのfuuro_akadora_list[-1]がTrueならchii_indexは2で確定で5は赤
        if hai_index % 10 == 3 and janshi_chii.fuuro_akadora_list[-1]:
            hai_str1 = function.hai_convert_reverse(hai_index + 1)
            self.vertual_yama.remove(hai_str1)
            hai_str2 = function.hai_convert_reverse(hai_index - 3)
            self.vertual_yama.remove(hai_str2)
        #もし7が鳴かれてjanshi_chiiのfuuro_akadora_list[-1]がTrueならchii_indexは0で確定で5は赤
        elif hai_index % 10 == 7 and janshi_chii.fuuro_akadora_list[-1]:
            hai_str1 = function.hai_convert_reverse(hai_index - 1)
            self.vertual_yama.remove(hai_str1)
            hai_str2 = function.hai_convert_reverse(hai_index - 7)
            self.vertual_yama.remove(hai_str2)
        #もし4が鳴かれてjanshi_chiiのfuuro_akadora_list[-1]がTrueならchii_indexは1か2で5は赤
        elif hai_index % 10 == 4 and janshi_chii.fuuro_akadora_list[-1]:
            #345
            if chii_index == 1:
                hai_str1 = function.hai_convert_reverse(hai_index - 1)
                self.vertual_yama.remove(hai_str1)
                hai_str2 = function.hai_convert_reverse(hai_index - 4)
                self.vertual_yama.remove(hai_str2)
            else: #chii_index == 2
                hai_str1 = function.hai_convert_reverse(hai_index - 4)
                self.vertual_yama.remove(hai_str1)
                hai_str2 = function.hai_convert_reverse(hai_index + 2)
                self.vertual_yama.remove(hai_str2)
        #もし6が鳴かれてjanshi_chiiのfuuro_akadora_list[-1]がTrueならchii_indexは0か1で5は赤
        elif hai_index % 10 == 6 and janshi_chii.fuuro_akadora_list[-1]:
            if chii_index == 0:
                hai_str1 = function.hai_convert_reverse(hai_index - 6)
                self.vertual_yama.remove(hai_str1)
                hai_str2 = function.hai_convert_reverse(hai_index - 2)
                self.vertual_yama.remove(hai_str2)
            else: #chii_index = 1
                hai_str1 = function.hai_convert_reverse(hai_index - 6)
                self.vertual_yama.remove(hai_str1)
                hai_str2 = function.hai_convert_reverse(hai_index + 1)
                self.vertual_yama.remove(hai_str2)
        #もし赤5が鳴かれた場合
        elif hai_index % 10 == 0:
            hai_index += 5
            if chii_index == 0:
                hai_str1 = function.hai_convert_reverse(hai_index - 1)
                self.vertual_yama.remove(hai_str1)
                hai_str2 = function.hai_convert_reverse(hai_index - 2)
                self.vertual_yama.remove(hai_str2)
            elif chii_index == 1:
                hai_str1 = function.hai_convert_reverse(hai_index - 1)
                self.vertual_yama.remove(hai_str1)
                hai_str2 = function.hai_convert_reverse(hai_index + 1)
                self.vertual_yama.remove(hai_str2)
            elif chii_index == 2:
                hai_str1 = function.hai_convert_reverse(hai_index + 1)
                self.vertual_yama.remove(hai_str1)
                hai_str2 = function.hai_convert_reverse(hai_index + 2)
                self.vertual_yama.remove(hai_str2)
        #それ以外
        else:
            if chii_index == 0:
                hai_str1 = function.hai_convert_reverse(hai_index - 1)
                self.vertual_yama.remove(hai_str1)
                hai_str2 = function.hai_convert_reverse(hai_index - 2)
                self.vertual_yama.remove(hai_str2)
            elif chii_index == 1:
                hai_str1 = function.hai_convert_reverse(hai_index - 1)
                self.vertual_yama.remove(hai_str1)
                hai_str2 = function.hai_convert_reverse(hai_index + 1)
                self.vertual_yama.remove(hai_str2)
            elif chii_index == 2:
                hai_str1 = function.hai_convert_reverse(hai_index + 1)
                self.vertual_yama.remove(hai_str1)
                hai_str2 = function.hai_convert_reverse(hai_index + 2)
                self.vertual_yama.remove(hai_str2)
    
    def renew_vertual_yama_ankan(self, hai_str):
        hai_index = function.hai_convert(hai_str)
        if hai_index % 10 == 5 and hai_index < 30:
            aka_hai_str = function.hai_convert_reverse(hai_index - 5)
            self.vertual_yama.remove(aka_hai_str)
            self.vertual_yama.remove(hai_str)
            self.vertual_yama.remove(hai_str)
            self.vertual_yama.remove(hai_str)
        else:
            self.vertual_yama.remove(hai_str)
            self.vertual_yama.remove(hai_str)
            self.vertual_yama.remove(hai_str)
            self.vertual_yama.remove(hai_str)
    
    def renew_vertual_yama_kakan(self, hai_str):
        self.vertual_yama.remove(hai_str)
    
    def riipai(self):
        self.tehai_136.sort()
        self.tehai = sorted(self.tehai)
        manzu = [s for s in self.tehai if ('m' in s) or ('M' in s)]
        pinzu = [s for s in self.tehai if ('p' in s) or ('P' in s)]
        souzu = [s for s in self.tehai if ('s' in s) or ('S' in s)]
        zihai = [s for s in self.tehai if 'z' in s]
        self.tehai = manzu + pinzu + souzu + zihai
        
    def tsumo(self, hai_str, hai_136):        
        self.tehai.append(hai_str)
        self.tehai_136.append(hai_136)
        self.tsumohai_list.append(hai_str)
        self.renew_vertual_yama(hai_str)
    
    def dahai(self, taku, janshi_list, bakyou_list):
        if self.riichi != 0:
            return -1
        return eval_ensemble.eval_tehai_ens(self, taku, janshi_list, bakyou_list)
    
    def func_riichi(self, taku):
        self.riichi = 1
      
    def pon(self, taku, hai_str, janshi_list, bakyou_list):
        return evaluate.eval_pon(self, taku, hai_str, janshi_list, bakyou_list)
   
    def pon_add(self, taku, hai_arr, teban):
        
        #tehaiとtehai_136の操作
        for i in range(3):
            if hai_arr[i] in self.tehai_136:
                self.tehai_136.remove(hai_arr[i])
                self.tehai.remove(function_tenhou.hai_convert_136_to_str(hai_arr[i]))
                             
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
            self.fuuro_akadora_list.append(False)
            
    def daiminkan(self, taku, hai_str, teban, bakyou_list):
        return evaluate.eval_daiminkan(self, taku, hai_str)

    def daiminkan_add(self, taku, hai_arr, last_dahai, teban):
        last_hai_str = function_tenhou.hai_convert_136_to_str(last_dahai)
        last_hai_index = function.hai_convert(function.akadora_hai_convert(last_hai_str))
        
        #手牌から削除
        for i in range(3):
            if hai_arr[i] in self.tehai_136:
                self.tehai_136.remove(hai_arr[i])
                self.tehai.remove(function_tenhou.hai_convert_136_to_str(hai_arr[i]))

        #副露リストに追加
        self.fuurohai.append([3,last_hai_index ,teban])
        if last_hai_index%10 == 5 and last_hai_index < 30:
            self.fuuro_akadora_list.append(True)
        else:
            self.fuuro_akadora_list.append(False)

    def chii(self, taku, hai_str, janshi_list, bakyou_list): 
        #eval_chiiは[chii_index, その時の打牌（手牌の何番目か）を返す]
        return evaluate.eval_chii(self, taku, hai_str, janshi_list, bakyou_list)      
    
    def chii_add(self, taku, hai_arr, last_dahai):
        last_hai = function_tenhou.hai_convert_136_to_str(last_dahai)
        #tehaiとtehai_136の操作。tehai_136の中にhai_arrのIDがあれば削除
        #print(hai_arr)
        #print(self.tehai_136)

        for i in range(3):
            if hai_arr[i] in self.tehai_136:
                self.tehai_136.remove(hai_arr[i])
                self.tehai.remove(function_tenhou.hai_convert_136_to_str(hai_arr[i]))
        
        #print(self.tehai_136)
        #print(self.tehai)
        
        #副露リストへの追加
        last_hai_index = function.hai_convert(function.akadora_hai_convert(last_hai))
        temp = function.akadora_convert(function_tenhou.tehai_convert_136_to_str(hai_arr))
        #print(temp)
        temp_arr_str = temp[0]
        #print(temp_arr_str)
        akadora_flag = temp[1] #枚数
        hai_arr_index = sorted(function.tehai_convert2(temp_arr_str))
        #print(hai_arr_index)
        #print(last_hai_index)
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
    
    def ankan(self, taku):
        ankan_index = evaluate.eval_ankan(self, taku)
        return ankan_index
    
    def ankan_add(self, taku, hai_arr):
        for i in range(4):
            self.tehai_136.remove(hai_arr[0]+i)
            self.tehai.remove(function_tenhou.hai_convert_136_to_str(hai_arr[0]+i))
        ankan_index = function.hai_convert(function_tenhou.hai_convert_136_to_str(hai_arr[1]))
        self.ankan_list.append(ankan_index)   
    
    #kakan_index = [副露リストの番号, 副露牌の牌番号(例:5mポンなら5), 赤かどうか] ※カカンなしなら[-1,0]を返す
    def kakan(self, taku):
        kakan_index = evaluate.eval_kakan(self, taku)
        return kakan_index
    
    def kakan_add(self, taku, hai_arr):
        #元からソートされているはず
        #カカンした牌の種類(hai_arr[1]としているので赤の可能性なし)
        kakan_index = function.hai_convert(function_tenhou.hai_convert_136_to_str(hai_arr[1]))
        #実際に加えられた牌のID(赤の可能性あり)
        temp_arr = hai_arr
        kakan_hai_id = 6 + temp_arr[0] - (temp_arr[0]%4)*2 - temp_arr[1] % 4 - temp_arr[2] % 4
        kakan_hai_str = function_tenhou.hai_convert_136_to_str(kakan_hai_id)
        
        #remove
        self.tehai.remove(kakan_hai_str)
        self.tehai_136.remove(kakan_hai_id)
        
        #副露リスト更新
        for i in range(len(self.fuurohai)):
            if self.fuurohai[i][1] == kakan_index and self.fuurohai[i][0] == 2:
                self.fuurohai[i][0] = 3
                #kakan_indexが5,15,25なら赤ドラあり
                if kakan_index % 10 == 5 and kakan_index < 30:
                    self.fuuro_akadora_list[i] = True
    
    def tsumo_agari(self, teban, oya, kaze_honba, taku):
        point = [0,0,0,0,False]
        if shanten_check_new.shanten_check(self, taku.hash_table)== -1:
            point[4] = True
            hai = self.tehai[len(self.tehai)-1]
            temp_point = tensu_calc.tensu_calc(self, taku, hai)
            if len(temp_point) == 0:
                point[4] = False
            else:
                print(teyaku_check.teyaku_check(self, taku, hai))
                if self.kaze == 0:
                    for i in range(4):
                        if teban != i:
                            point[i] = temp_point[0]
                else:
                    #ここもっとましな書き方できるかも
                    for i in range(4):
                        if i == (4 -self.kaze + teban)%4:
                            point[i] = temp_point[1]
                        elif i == teban:
                            pass
                        else:
                            point[i] = temp_point[0]      
        return point
    
    #13枚の手牌とを受け取ってフリテンかどうかを判定。Trueならフリテン
    def furiten_hantei(self, taku):
        furiten_list = self.sutehai + self.temp_furiten
        machihai_list = function.find_machihai(self, taku.hash_table)
        for hai_str in furiten_list:
            if hai_str in machihai_list:
                return True
        return False
           
    def ron_agari(self, num_temp, oya, kaze_honba, hai, taku):
        point = 0
        if self.furiten_hantei(taku):
            print("フリテン")
        else:
            temp_tehai = self.tehai.copy()
            temp_tehai.append(hai)
            temp_janshi = copy.deepcopy(self)
            temp_janshi.tehai = temp_tehai
            if shanten_check_new.shanten_check(temp_janshi, taku.hash_table) == -1:
                point = tensu_calc.tensu_calc(self, taku, hai)
                if len(point) == 0:
                    point = 0
                else:
                    print(teyaku_check.teyaku_check(self, taku, hai))
                    point = point[0]
        return point

#enemy
class Janshi_e:
    def __init__(self, janshi_num):
        self.num = janshi_num
        self.sutehai = []
        self.tedashi_flag = []
        self.temp_genbutsu = []
        self.fuurohai= []
        self.fuurosuu = 0
        self.fuuro_akadora_list = []
        self.ankan_list = []
        self.tensuu = 25000
        self.kaze = 0 #東→0 南→1...
        self.riichi = 0 #0→リーチしていない 1→リーチ状態 2→ダブリー状態
        self.ippatsu_flag = False
        self.rating = 0
        self.dan = ""
        
    def janshi_reset(self):
        self.sutehai = []
        self.tedashi_flag = []
        self.temp_genbutsu = []
        self.fuurohai = []
        self.fuurosuu = 0
        self.fuuro_akadora_list = []
        self.ankan_list = []
        self.riichi = 0 #0→リーチしていない 1→リーチ状態 2→ダブリー状態
        self.ippatsu_flag = False
