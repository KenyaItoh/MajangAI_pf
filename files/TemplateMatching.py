import cv2
import numpy as np

from Komojika import Komojika

similar = 0.9   # マッチングのしきい値

def TemplateMatching(img_screen, str_template):

    # 赤の文字列を変換
    if str_template[0] == "5" and str_template[1].isupper():
        str_template = Komojika(str_template)

    #print("str_template = {0}, type = {1}".format(str_template, type(str_template)))
        
    img_template = cv2.imread("./Template/{}.png".format(str_template)) #テンプレート画像

    if(str_template[0] == "5" and not str_template[1] == "z"): # 5m, 5s, 5p,5mm, 5ss, 5ppのとき
        # HSV変換
        img_screen_hsv = cv2.cvtColor(img_screen, cv2.COLOR_BGR2HSV)
        img_template_hsv = cv2.cvtColor(img_template, cv2.COLOR_RGB2HSV)
        # H
        img_screen_temp = cv2.split(img_screen_hsv)[0]
        img_template_temp = cv2.split(img_template_hsv)[0]
    else: # それ以外
        # GRAY
        img_screen_temp = cv2.cvtColor(img_screen, cv2.COLOR_BGR2GRAY)
        img_template_temp = cv2.cvtColor(img_template, cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(img_screen_temp,img_template_temp,cv2.TM_CCOEFF_NORMED) # マッチング
    loc = np.where( result >= similar) # しきい値より高いマッチ点を求める．


    # print("loc = {}".format(loc))

    height, width, _ = img_template.shape #テンプレート画像の高さと幅
    try:
        loc[0][0]
    except IndexError: # マッチが見つからなかった
        return_str = "no match"
    else: # マッチが見つかった
        return_str = "Found matching"
        
        # 真ん中押すようにする．
        loc[1][0] += (width // 2) 
        loc[0][0] += (height // 2)
        
    #print(return_str)

    # -   -   -   -   出力    -   -   -   - #
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_screen, pt, (pt[0] + width, pt[1] + height), (100,255,0), 2) #マッチした点に矩形を描く
    cv2.imwrite("z_img_screen.png", img_screen) # 入力画像
    cv2.imwrite("z_img_processed.png", img_template) # テンプレート画像
    cv2.imwrite("z_img_screen_temp.png", img_screen_temp) #入力画像加工後
    cv2.imwrite("z_img_template_processed.png", img_template_temp) #テンプレート画像加工後
    cv2.imwrite("z_match.png", img_screen) # マッチング表示

    return loc, return_str

if __name__ == '__main__':
    hai = "7z"
    from pyautogui import screenshot
    img_screen = np.array(screenshot())[920:1080, 0:1920]
    # img_screen = cv2.imread("test.png")[920:1080, 0:1920] 
    str_template = hai
    TemplateMatching(img_screen, str_template)