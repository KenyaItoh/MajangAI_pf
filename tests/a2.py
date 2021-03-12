import majang
import function
import time
import tensu_calc
import teyaku_check
import eval_ensemble_for_kuikae
import eval_ensemble
import eval_ensemble_parallel
import os
from multiprocessing import Pool
import multiprocessing as multi

janshi = majang.Janshi_p(2)
janshi1 = majang.Janshi_e(1)
janshi2 = majang.Janshi_e(2)
janshi3 = majang.Janshi_e(3)
taku = majang.Taku()
janshi_list= [janshi, janshi1, janshi2, janshi3]

janshi.janshi_reset()
taku.taku_reset()
taku.dorahyouji = ["1z"]
janshi.tehai = ['2m', '4m', '5m', '6m', '7m', '2p', '2p', '3p', '4p', '5p', '6p', '7p', '7p', '4s']
#janshi.fuurohai = [[2,2,1]]

janshi.init_vertual_yama(taku)
janshi.vertual_yama.remove("3p")
janshi.vertual_yama.remove("3p")
#janshi.vertual_yama.remove("3p")
#janshi.vertual_yama.remove("3p")
taku.yama_nokori = 58

start = time.time()
#print(eval_ensemble.new_yuukouhai_explore(1, janshi, taku))
print(eval_ensemble_parallel.eval_tehai_ens(janshi, taku, janshi_list, [0,0,0]))
print(str(time.time()-start))

#print(janshi.pon(taku, '6s', janshi_list, [0, 0, 0]))

#print(tensu_calc.tensu_calc(janshi, taku, "6m"))
#print(teyaku_check.teyaku_check(janshi, taku, "6m"))
#print(function.dama_hantei(janshi, taku, "5p"))