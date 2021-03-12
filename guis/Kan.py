from pyautogui import click
import time

from Region import region
from Search_ClickPoint import Search_ClickPoint

def Kan(str_template):
    # print("hai1 = {0}".format(str_template)
    clickPoint = Search_ClickPoint(region["naki"], 0.5, str_template, "kan")
    click(clickPoint)
    time.sleep(0.1)
    click(1800, 540) # テンプクリック
    time.sleep(0.1)

if __name__ == '__main__':
    Kan("9s") # カン