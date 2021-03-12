import numpy as np
import shanten_check_new
import copy

def eval_keiten(shanten_suu, janshi, taku, temp_max):
    keiten_point_list = np.zeros(len(janshi.tehai))
    nokori_tsumo_kaisuu = int(taku.yama_nokori/4)
    if shanten_suu != 0 or nokori_tsumo_kaisuu >= 4:
        return keiten_point_list
    else:
        for i in range(len(janshi.tehai)):
            temp_janshi = copy.deepcopy(janshi)
            del temp_janshi.tehai[i]
            if shanten_check_new.shanten_check(temp_janshi, taku.hash_table) == 0:
                keiten_point_list[i] += temp_max/float(max(nokori_tsumo_kaisuu+1, 1))**0.6
        return keiten_point_list

def create_keiten_list(shanten_suu, janshi, taku):
    nokori_tsumo_kaisuu = int(taku.yama_nokori/4)
    keiten_list = np.zeros(len(janshi.tehai))
    if shanten_suu != 0 or nokori_tsumo_kaisuu >= 4:
        return keiten_list
    for i in range(len(janshi.tehai)):
        temp_janshi = copy.deepcopy(janshi)
        del temp_janshi.tehai[i]
        if shanten_check_new.shanten_check(temp_janshi, taku.hash_table) == 0:
            #keiten_list[i] += 1500/float(max(nokori_tsumo_kaisuu+1, 1))
            keiten_list[i] += 100000
    return keiten_list