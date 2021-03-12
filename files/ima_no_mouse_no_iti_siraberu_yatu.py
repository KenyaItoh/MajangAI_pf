import pyautogui

pos = None
while(True):
    nowpos = pyautogui.position()
    if not pos == nowpos:
        pos = nowpos
        print(pos)