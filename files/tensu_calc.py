import teyaku_check
import math

def tensu_calc(janshi,taku,agarihai_str):

    #アガリ手牌の点数を返す。
    #例:30符3翻 子ロン:[3900]、子ツモ:[1000,2000]、親ロン[5800]、親ツモ[2000,2000]

    #親かどうか
    if janshi.kaze == 0:
        oya = 1
    else:
        oya = 0

    #ツモかどうか
    fuurohai = janshi.fuurohai
    ankan = janshi.ankan_list
    fuurosu = len(fuurohai) + len(ankan)
    if len(janshi.tehai) + fuurosu * 3== 14:
        tsumo = True
    elif len(janshi.tehai) + fuurosu * 3== 13:
        tsumo = False

    #点数計算
    hanfu = teyaku_check.teyaku_check(janshi,taku,agarihai_str)
    hansu = hanfu[0]
    fusu = hanfu[1]

    if hansu < 0 or hansu >= 5:
        if hansu < 0 :
            s = 8000 * -hansu
        elif hansu >= 13:
            s = 8000
        elif hansu >= 11:
            s = 6000
        elif hansu >= 8:
            s = 4000
        elif hansu >= 6:
            s = 3000
        elif hansu >= 5:
            s = 2000
    elif hansu == 0:
        return []
    else:
        s = 2**(hansu + 2)*fusu
        if s >= 2000:
            s = 2000

    if tsumo:
        return [ceil_ten(s*2**oya),ceil_ten(s*2)]
    else:
        return [ceil_ten(s*4*1.5**oya)]

def ceil_ten(num):

    #10の位を切り上げた整数を返す

    num2 = num / 100
    return math.ceil(num2)*100







        
    