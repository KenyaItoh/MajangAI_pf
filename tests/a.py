import numpy as np
import majang
import function
import function_tenhou

temp_list = list(range(10))
print(temp_list)

janshi0 = majang.Janshi_p(2)
janshi1 = majang.Janshi_e(1)
janshi2 = majang.Janshi_e(2)
janshi3 = majang.Janshi_e(3)
janshi = [janshi0, janshi1, janshi2, janshi3]
taku = majang.Taku()
taku.kaze_honba[0] = 3

janshi0.tensuu = 12000
janshi1.tensuu = 31000
janshi2.tensuu = 30000
janshi3.tensuu = 27000


print(function_tenhou.create_bakyou_list(janshi, taku))