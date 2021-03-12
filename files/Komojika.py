def Komojika(_str):
    _str = _str.lower() # 5m
    _str += _str[1] #5mm
    return _str
    
if __name__ == '__main__':
    _str = '5M'
    komojika(_str)