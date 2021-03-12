'''
require
    pip install opencv-python
    pip install pyautogui

Memo
    ポン，カン，チー，鳴きのクリック場所は同じ
'''

import cv2
import numpy as np
from pyautogui import click
import time

from TemplateMatching import TemplateMatching
from Cal_MinDistance import Cal_MinDistance
from sitei_zikan_dake_templatematching_suru_yatu import sitei_zikan_dake_templatematching_suru_yatu


# 鳴きをクリックする
def Click_Naki():
    time.sleep(0.1)
    click(1080, 830) # 鳴きクリック
    time.sleep(0.1)

# クリックする点の計算
def Set_ClickPoint(command, hais):
    clickPoint_temp = (1800, 540)
    clickPoint = None
    waitTime = 0.3

    # 打牌
    if command == "dahai" or command == "ok" or command == "yoyaku":
        loc = sitei_zikan_dake_templatematching_suru_yatu(waitTime, command, hais[0])
        if loc == None: #マッチがなかった
            clickPoint = clickPoint_temp
        else: #マッチがあった
            clickPoint = [loc[1][0], loc[0][0]] # クリックする点
            if(command == "dahai"):
                clickPoint[1] += 930

        print("clickPoint = {}".format(clickPoint))

        # -   -   -   -   出力    -   -   -   - #
        # cv2.circle(img_screen, clickPoint, 5, (0, 0, 255), thickness=3, lineType=cv2.LINE_AA)
        # cv2.imwrite("zimg_match.png", img_screen)

    # ポンチー
    elif(command == "pon_chii"):

        # なきクリック
        Click_Naki()
        print(hais[0])
        loc1 = sitei_zikan_dake_templatematching_suru_yatu(waitTime, command, hais[0])
        if loc1 == None: #マッチがなかった
            clickPoint = clickPoint_temp
        
        else: #マッチがあった
            loc2 = sitei_zikan_dake_templatematching_suru_yatu(waitTime, command, hais[1])

            clickPoint = Cal_MinDistance(loc1, loc2) # クリックする点
        print(clickPoint)

        # -   -   -   -   出力    -   -   -   - #
        # cv2.circle(img_screen, clickPoint, 5, (255, 255, 255), thickness=3, lineType=cv2.LINE_AA)
        # cv2.imwrite("zimg_match.png", img_screen)

    elif(command == "kan"):
        Click_Naki()
        loc1 = sitei_zikan_dake_templatematching_suru_yatu(waitTime, command, hais[0])
        if loc1 == None: #マッチがなかった
            clickPoint = clickPoint_temp
        else: #マッチがあった
            loc2 = sitei_zikan_dake_templatematching_suru_yatu(waitTime, command, hais[1])

            clickPoint = Cal_MinDistance(loc1, loc2) # クリックする点
        print(clickPoint)

        # -   -   -   -   出力    -   -   -   - #
        # cv2.circle(img_screen, clickPoint, 5, (255, 255, 255), thickness=3, lineType=cv2.LINE_AA)
        # cv2.imwrite("zimg_match.png", img_screen)

    # 立直
    elif(command == "riichi"):
        clickPoint = (825, 842) 
        print("riichi")

    # 和了
    elif(command == "agari"):
        clickPoint = (1324, 640)

    # キャンセル
    elif(command == "cancel"):
        clickPoint = (1326, 837)
    
    # 予約
    elif(command == "nanka"):
        pass
    # 追加があれば使う．
    elif(command == "nanka"):
        pass
    else:
        clickPoint = clickPoint_temp

    
    return clickPoint

# クリックする
def Click(command, *args):
    clickPoint = Set_ClickPoint(command, args) # クリックする点を算出
    click(clickPoint) # クリック
    time.sleep(0.1)
    if command != "ok":
        click(1800, 540) # tempクリック

if __name__ == '__main__':
    # Click("dahai", "5z")
    Click("ok", "ok")