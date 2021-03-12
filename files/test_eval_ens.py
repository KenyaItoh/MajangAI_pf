import eval_ensemble
import eval_ensemble2
import majang
import time
import mentsu_count
import function

janshi = majang.Janshi_p(1)
taku = majang.Taku()

janshi.kaze = 1
#janshi.sutehai = ["7s"]

#janshi.vertual_yama.remove("5z")
#janshi.vertual_yama.remove("5z")

#janshi.sutehai.append("5z")


taku.dorahyouji = ["8p"]

janshi.tehai = ['2m', '3m', '4m', '6m', '8m', '7m', '3p', '3p', '3p', '4p', '4p', 
'8s', '9s', '4p']
#janshi.fuurohai = [[2,31,1]]

#print(function.find_yuukouhai(janshi, 1, taku.hash_table))

janshi.init_vertual_yama(taku)

start = time.time()
#print(eval_ensemble.eval_tehai_ens(janshi, taku))
print("打: " + janshi.tehai[eval_ensemble.eval_tehai_ens(janshi, taku)])
elapsed_time = time.time() - start
print(elapsed_time)

#print(mentsu_count.mentsu_count(janshi))

