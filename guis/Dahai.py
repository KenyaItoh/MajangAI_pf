from pyautogui import click
import time

from Region import region
from Search_ClickPoint import Search_ClickPoint

def Dahai(str_template):
    clickPoint = Search_ClickPoint(region["tehai"], 0.5, str_template)
    clickPoint[1] += 930
    click(clickPoint)
    time.sleep(0.1)
    click(1800, 540) # テンプクリック

if __name__ == '__main__':
    Dahai("1p") # 2s打牌