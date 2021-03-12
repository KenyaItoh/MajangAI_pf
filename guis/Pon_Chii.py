from pyautogui import click
import time

from Region import region
from Search_ClickPoint import Search_ClickPoint

def Pon_Chii(str_templates):
    # print("hai1 = {0}, hai2 = {1}".format(str_templates[0], str_templates[1]))
    clickPoint = Search_ClickPoint(region["naki"], 0.5, str_templates[0], str_templates[1])
    click(clickPoint)
    time.sleep(0.1)
    click(1800, 540) # テンプクリック
    time.sleep(0.1)

if __name__ == '__main__':
    Pon_Chii(["6m", "8m"]) #6m, 8m