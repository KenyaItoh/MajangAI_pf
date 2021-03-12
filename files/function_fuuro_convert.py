import function

def pon_convert(janshi, hai_str,teban, akadora_flag):
    janshi.tsumohai_list.append(hai_str + "ポン")
    janshi.fuuro_akadora_list.append(akadora_flag)
    temp_tehai = function.tehai_convert(janshi.tehai)
    hai_index = function.hai_convert(function.akadora_hai_convert(hai_str))
    temp_tehai[hai_index] -= 2
    janshi.tehai = function.tehai_convert_reverse(temp_tehai)
    return [2,hai_index,teban]

def chii_convert(janshi, hai_str, chii_index, akadora_flag):
    janshi.tsumohai_list.append(hai_str + "チー")
    janshi.fuuro_akadora_list.append(akadora_flag)
    temp_tehai = function.tehai_convert(janshi.tehai)
    hai_index = function.hai_convert(function.akadora_hai_convert(hai_str))
    
    if chii_index == 0:
        temp_tehai[hai_index-2] -= 1
        temp_tehai[hai_index-1] -= 1
        janshi.tehai = function.tehai_convert_reverse(temp_tehai)
        return [1, hai_index, chii_index]
    elif chii_index == 1:
        temp_tehai[hai_index-1] -= 1
        temp_tehai[hai_index+1] -= 1
        janshi.tehai = function.tehai_convert_reverse(temp_tehai)
        return [1, hai_index, chii_index]
    elif chii_index == 2:
        temp_tehai[hai_index+1] -= 1
        temp_tehai[hai_index+2] -= 1
        janshi.tehai = function.tehai_convert_reverse(temp_tehai)
        return [1, hai_index, chii_index]

def daiminkan_convert(janshi, hai_str, teban):
    janshi.tsumohai_list.append(hai_str + "大明槓")
    temp_tehai = function.tehai_convert(janshi.tehai)
    hai_index = function.hai_convert(hai_str)
    temp_tehai[hai_index] -= 3
    janshi.tehai = function.tehai_convert_reverse(temp_tehai)
    return [3,hai_index,teban]

def kakan_convert(janshi, hai_str, fuuro_index):  
    if janshi.fuurohai[fuuro_index][1]%10 == 5 and janshi.fuurohai[fuuro_index][1] < 30:
        janshi.fuuro_akadora_list[fuuro_index] = True
    janshi.tsumohai_list.append(hai_str + "加槓")
    temp_tehai = function.tehai_convert(janshi.tehai)
    hai_index = function.hai_convert(hai_str)
    temp_tehai[hai_index] -= 1
    janshi.tehai = function.tehai_convert_reverse(temp_tehai)
    return [3,hai_index,0]

def ankan_convert(janshi, hai_str):
    janshi.tsumohai_list.append(hai_str + "暗槓")
    temp_tehai = function.tehai_convert(janshi.tehai)
    hai_index = function.hai_convert(hai_str)
    temp_tehai[hai_index] -= 4
    janshi.tehai = function.tehai_convert_reverse(temp_tehai)
    return hai_index