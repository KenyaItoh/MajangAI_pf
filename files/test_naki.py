import majang
import shanten_check_new
import time

janshi0 = majang.Janshi_p(2)
janshi1 = majang.Janshi_e(1)
janshi2 = majang.Janshi_e(2)
janshi3 = majang.Janshi_e(3)
janshi = [janshi0, janshi1, janshi2, janshi3]

taku = majang.Taku()

janshi0.janshi_reset()
taku.taku_reset()

janshi0.kaze = 1
taku.yama_nokori = 20
janshi0.tehai = ['4m', '5m', '2p', '3p', '7p', '8p', '2s', '3s', '7s', '1z', '2z', '2z', '6z']
janshi0.riipai()
taku.dorahyouji = ["2s"]
janshi0.init_vertual_yama(taku)
print(janshi0.tehai)
print(shanten_check_new.shanten_check(janshi0, taku.hash_table))




start = time.time()
#print(janshi0.pon(taku, "6z", janshi))
print(janshi0.chii(taku, "6p", janshi))
print(str(time.time()-start))
