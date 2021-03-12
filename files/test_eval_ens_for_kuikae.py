import majang
import eval_ensemble_for_kuikae
import eval_yuukouhai_for_naki2

janshi = majang.Janshi_p(2)
taku = majang.Taku()

janshi.kaze = 1

taku.dorahyouji = ["9s"]

janshi.tehai = ["1m", "1m", "7m", "7m", "7m", "5p", "5p", "6p", "2s", "3s"]
janshi.fuurohai = [[1,4,2]]


janshi.init_vertual_yama(taku)

#print(eval_ensemble_for_kuikae.eval_tehai_ens(1, janshi, taku, []))

#janshi = majang.Janshi_p(1)
#taku = majang.Taku()

##janshi.kaze = 1

#taku.dorahyouji = ["9s"]

#janshi.tehai = ["8m", "8m", "9m", "5P", "7p", "9p", "2s", "3s", "9s", "7s", "8s", "1z", "1z"]

#print(eval_yuukouhai_for_naki2.new_yuukouhai_explore(2, janshi, taku))

#janshi.vertual_yama.append("6p")
#janshi.vertual_yama.append("6p")

print(janshi.chii(taku, "4p"))
