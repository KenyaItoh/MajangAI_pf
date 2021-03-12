'''
Memo
    ポン，カン，チー，鳴きのクリック場所は同じ
'''

from pyautogui import click
import time

from TemplateMatching import TemplateMatching
from Cal_MinDistance import Cal_MinDistance
from TemplateMatching_for_fixed_time import TemplateMatching_for_fixed_time


# 鳴きをクリックする
def Click_Naki():
    time.sleep(0.1)
    click(1080, 830) # 鳴きクリック
    time.sleep(0.1)

# クリックする点の計算
def Search_ClickPoint(region_type, searchTime, *args):
    hais = args # わかりやすいように変数名を変更
    clickPoint_temp = [1800, 540]
    clickPoint = None

    # 引数が２つのときは，牌をクリックポイントにする．
    if len(hais) == 1:
        loc = TemplateMatching_for_fixed_time(region_type, searchTime, hais[0])

        if loc == None: #マッチがなかった
            clickPoint = clickPoint_temp
        else: #マッチがあった
            clickPoint = [loc[1][0], loc[0][0]] # クリックする点
        #print("clickPoint = {}".format(clickPoint))
    
    # 引数が２つのときは，２つの牌の間をクリックポイントにする．
    elif len(hais) == 2:
        # なきクリック
        Click_Naki()
        #print(hais[0])
        loc1 = TemplateMatching_for_fixed_time(region_type, searchTime, hais[0])
        if loc1 == None: #マッチがなかった
            clickPoint = clickPoint_temp
        
        else: #マッチがあった
            loc2 = TemplateMatching_for_fixed_time(region_type, searchTime, hais[1])

            clickPoint = Cal_MinDistance(loc1, loc2) # クリックする点
        #print(clickPoint)
    else:
        clickPoint = clickPoint_temp

    return clickPoint

if __name__ == '__main__':
    from Region import region
    Search_ClickPoint(region["all"], 0.5, "ok")