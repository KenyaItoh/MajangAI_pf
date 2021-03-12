from pyautogui import click
import time

from Region import region
from Search_ClickPoint import Search_ClickPoint

def Ok():
    clickPoint = Search_ClickPoint(region["all"], 0.1, "ok")
    if clickPoint != [1800, 540]:
        click(clickPoint)
    #time.sleep(0.1)
    #click(1800, 540) # テンプクリック

if __name__ == '__main__':
    Ok() # OK