#天鳳に使う機能用
import re
import function
import numpy as np

#[オーラスの場況インデックス1~4, 1位になるのに必要点数(正), ラスらないために失ってはいけない点数(正)]を返す
def create_bakyou_list(janshi_list, taku):
    #東風を想定
    if taku.kaze_honba[0] <=2:
        return [0, 0, 0]
    #オーラス想定 kazeを足すことで同点に対応　北→3、西→2、...
    tensuu_list = np.array([janshi_list[0].tensuu + janshi_list[0].kaze, janshi_list[1].tensuu + janshi_list[1].kaze, janshi_list[2].tensuu + janshi_list[2].kaze, janshi_list[3].tensuu + janshi_list[3].kaze])
    tensuu_list_argsort = tensuu_list.argsort()
    #トップ①
    if tensuu_list_argsort.tolist().index(0) == 3:
        loss_point = janshi_list[0].tensuu - janshi_list[tensuu_list_argsort.tolist().index(2)].tensuu
        return [1, 0, loss_point]
    #ラス④
    elif tensuu_list_argsort.tolist().index(0) == 0:
        necessary_point =  janshi_list[tensuu_list_argsort.tolist().index(1)].tensuu - janshi_list[0].tensuu
        return [4, necessary_point, 0]
    else: #2,3着
        necessary_point = janshi_list[tensuu_list_argsort[3]].tensuu - janshi_list[0].tensuu
        loss_point = janshi_list[0].tensuu - janshi_list[tensuu_list_argsort[0]].tensuu
        #③ラス回避
        if necessary_point >= loss_point:
            return [3, necessary_point, loss_point]
        else:
            return [2, necessary_point, loss_point]

def riipai(tehai_str):
    tehai_str = sorted(tehai_str)
    manzu = [s for s in tehai_str if 'm' in s]
    pinzu = [s for s in tehai_str if 'p' in s]
    souzu = [s for s in tehai_str if 's' in s]
    zihai = [s for s in tehai_str if 'z' in s]
    tehai = manzu + pinzu + souzu + zihai
    return tehai

def tehai_convert_136_to_str(tehai_136):
    tehai_str = []
    for i in range(len(tehai_136)):
        tehai_str.append(hai_convert_136_to_str(tehai_136[i]))
    return tehai_str
    
def hai_convert_136_to_str(index):
    _136_to_str = {0:"1m",1:"1m",2:"1m",3:"1m",4:"2m",5:"2m",6:"2m",7:"2m",8:"3m",9:"3m",10:"3m",11:"3m",12:"4m",13:"4m",14:"4m",15:"4m",16:"5M",17:"5m",18:"5m",19:"5m",20:"6m",21:"6m",22:"6m",23:"6m",24:"7m",25:"7m",26:"7m",27:"7m",28:"8m",29:"8m",30:"8m",31:"8m",32:"9m",33:"9m",34:"9m",35:"9m",36:"1p",37:"1p",38:"1p",39:"1p",40:"2p",41:"2p",42:"2p",43:"2p",44:"3p",45:"3p",46:"3p",47:"3p",48:"4p",49:"4p",50:"4p",51:"4p",52:"5P",53:"5p",54:"5p",55:"5p",56:"6p",57:"6p",58:"6p",59:"6p",60:"7p",61:"7p",62:"7p",63:"7p",64:"8p",65:"8p",66:"8p",67:"8p",68:"9p",69:"9p",70:"9p",71:"9p",72:"1s",73:"1s",74:"1s",75:"1s",76:"2s",77:"2s",78:"2s",79:"2s",80:"3s",81:"3s",82:"3s",83:"3s",84:"4s",85:"4s",86:"4s",87:"4s",88:"5S",89:"5s",90:"5s",91:"5s",92:"6s",93:"6s",94:"6s",95:"6s",96:"7s",97:"7s",98:"7s",99:"7s",100:"8s",101:"8s",102:"8s",103:"8s",104:"9s",105:"9s",106:"9s",107:"9s",108:"1z",109:"1z",110:"1z",111:"1z",112:"2z",113:"2z",114:"2z",115:"2z",116:"3z",117:"3z",118:"3z",119:"3z",120:"4z",121:"4z",122:"4z",123:"4z",124:"5z",125:"5z",126:"5z",127:"5z",128:"6z",129:"6z",130:"6z",131:"6z",132:"7z",133:"7z",134:"7z",135:"7z"}
    return _136_to_str[index]

def hai_convert_136_to_index(hai_136):
    _136_to_str = {0:"1m",1:"1m",2:"1m",3:"1m",4:"2m",5:"2m",6:"2m",7:"2m",8:"3m",9:"3m",10:"3m",11:"3m",12:"4m",13:"4m",14:"4m",15:"4m",16:"5M",17:"5m",18:"5m",19:"5m",20:"6m",21:"6m",22:"6m",23:"6m",24:"7m",25:"7m",26:"7m",27:"7m",28:"8m",29:"8m",30:"8m",31:"8m",32:"9m",33:"9m",34:"9m",35:"9m",36:"1p",37:"1p",38:"1p",39:"1p",40:"2p",41:"2p",42:"2p",43:"2p",44:"3p",45:"3p",46:"3p",47:"3p",48:"4p",49:"4p",50:"4p",51:"4p",52:"5P",53:"5p",54:"5p",55:"5p",56:"6p",57:"6p",58:"6p",59:"6p",60:"7p",61:"7p",62:"7p",63:"7p",64:"8p",65:"8p",66:"8p",67:"8p",68:"9p",69:"9p",70:"9p",71:"9p",72:"1s",73:"1s",74:"1s",75:"1s",76:"2s",77:"2s",78:"2s",79:"2s",80:"3s",81:"3s",82:"3s",83:"3s",84:"4s",85:"4s",86:"4s",87:"4s",88:"5S",89:"5s",90:"5s",91:"5s",92:"6s",93:"6s",94:"6s",95:"6s",96:"7s",97:"7s",98:"7s",99:"7s",100:"8s",101:"8s",102:"8s",103:"8s",104:"9s",105:"9s",106:"9s",107:"9s",108:"1z",109:"1z",110:"1z",111:"1z",112:"2z",113:"2z",114:"2z",115:"2z",116:"3z",117:"3z",118:"3z",119:"3z",120:"4z",121:"4z",122:"4z",123:"4z",124:"5z",125:"5z",126:"5z",127:"5z",128:"6z",129:"6z",130:"6z",131:"6z",132:"7z",133:"7z",134:"7z",135:"7z"}
    return function.hai_convert(_136_to_str[hai_136])

def read_text_decomp(read_text):
    splitted_read_text = re.split('[,|:|"|{|}|[|]| |\t]', read_text)
    #print(splitted_read_text)
    count = splitted_read_text.count("")
    for i in range(count):
        splitted_read_text.remove("")
    
    #truncatedをtruncateする
    if len(splitted_read_text) != 0:
        while True:
            if len(splitted_read_text) == 0:
                break
            if splitted_read_text[0] != "tag":
                del splitted_read_text[0]
            else:
                break
    return splitted_read_text

def get_haipai_str(srt):
    tehai = []
    for i in range(17,30):
        tehai.append(int(srt[i]))
    return tehai_convert_136_to_str(tehai)

def get_haipai_136(srt):
    tehai_136 = []
    for i in range(17,30):
        tehai_136.append(int(srt[i]))
    return tehai_136

#string型のリストから特定の文字列を見つけてそのインデックス+1を返す
def find_str(str_list, str_to_find):
    index = 0
    for i in range(len(str_list)):
        if str_list[i] == str_to_find:
            index = i
            return index + 1
    return -1
    

#使い方↓
#text = '{"tag":"AGARI","ba":"0,1","hai":"14,16,20,22,23,38,43,47,54,56,60,77,80,84","machi":"84","ten":"30,8000,1","yaku":"1,1,2,1,7,1,52,1,54,1,53,0","doraHai":"78","doraHaiUra":"32","who":"0","fromWho":"1","sc":"240,90,250,-80,250,0,250,0"}'
#text = '{"tag":"g54","t":"4"}'
#split = read_text_decomp(text)
#print(split)
#index = find_str(split, "who")
#print("プレイヤー"+split[index]+"のアガリ")

#ead_text ='[truncated]{"tag":"AGARI","ba":"1,1","hai":"49,50,77,82,84,86,90,95,121,122,123","m":"1024","machi":"82","ten":"60,18000,2","yaku":"1,1,52,2,53,4","doraHai":"73,76","doraHaiUra":"103,0","who":"3","fromWho":"1","sc":"302,0,130,-183,250,0,'
#print(read_text_decomp(read_text))
