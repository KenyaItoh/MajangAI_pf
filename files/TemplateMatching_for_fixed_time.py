'''
指定の時間(waitTime)だけ，whileを回す．
    指定時間内にマッチが見つかったら，breakし，マッチの情報(loc)を戻す
    指定時間内にマッチが見つからなかったら，Noneを戻す

'''

import time
import numpy as np
from pyautogui import screenshot

from TemplateMatching import TemplateMatching


def TemplateMatching_for_fixed_time(region, searchTime, hai):

    startTime=time.time()
    return_loc = None

    # テンプレートマッチング
    while time.time() - startTime <= searchTime:
        img_screen = np.array(screenshot())[region[0]:region[1], region[2]:region[3]]  # スクショ
        loc, _str = TemplateMatching(img_screen, hai)
        if _str == "Found matching":
            return_loc = loc
            break

    return return_loc

if __name__ == '__main__':
    from Region import region
    TemplateMatching_for_fixed_time(region["tehai"], 5, "1p")