#鳴き対応
import function


#shanten_check用のハッシュテーブルファイルを読み込む。
def read_hash_table_for_shanten_check():
    hash_table = [[],[]]
    #数牌ハッシュテーブルの読み込み
    f = open('hashtable_for_shantencheck/index_s-1.txt')
    line = f.readline()
    while line:
        hash_table[0].append(line)
        line = f.readline()
    f.close
    f = open('hashtable_for_shantencheck/index_s-2.txt')
    line = f.readline()
    while line:
        hash_table[0].append(line)
        line = f.readline()
    f.close
    #字牌ハッシュテーブルの読み込み
    f = open('hashtable_for_shantencheck/index_z.txt')
    line = f.readline()
    while line:
        hash_table[1].append(line)
        line = f.readline()
    f.close
    return hash_table

#シャンテン計算。引数は、Janshiオブジェクトとread_hash_table_for_shanten_checkで読み込んだものを格納した配列。
def shanten_check(janshi,hash_table):
    tehai = function.tehai_convert(function.akadora_convert(janshi.tehai)[0])
    fuurosu = len(janshi.fuurohai) + len(janshi.ankan_list)

    #国士無双形
    Sh_kokushi = 13 # ここから1、9、字牌の数を引いていく
    kokushi_l = [1,9,11,19,21,29,31,32,33,34,35,36,37]
    kokushi_toitsu = 0
    for i in kokushi_l:
        if tehai[i] >= 1:
            Sh_kokushi -= 1
        if kokushi_toitsu == 0 and tehai[i] >= 2: #1，9、字牌の対子があれば1つだけシャンテン数が下がる
            kokushi_toitsu = 1
    Sh_kokushi -= kokushi_toitsu


    #七対子形
    Sh_chiitoi = 6 #ここから対子の数だけ引く
    haisyu = 0 #牌の種類
    for i in range(0,38):
        if tehai[i] >= 1:
            haisyu += 1
            if tehai[i] >= 2:
                Sh_chiitoi -= 1
    if haisyu < 7:
        Sh_chiitoi += 7- haisyu


    #4面子1雀頭形
    #tehaiを色ごとにハッシュ化
    manzu_hash = 0 #萬子部分のハッシュ値
    for i in range(1,10):
        manzu_hash = manzu_hash * 5 + tehai[i]
    pinzu_hash = 0 #筒子部分のハッシュ値
    for i in range(11,20):
        pinzu_hash = pinzu_hash * 5 + tehai[i]
    souzu_hash = 0 #索子部分のハッシュ値
    for i in range(21,30):
        souzu_hash = souzu_hash * 5 + tehai[i]
    zihai_hash = 0 #字牌部分のハッシュ値
    for i in range(31,38):
        zihai_hash = zihai_hash * 5 + tehai[i]
    
    #各ハッシュ値をキーにハッシュテーブルにある部分置換数t,uを取得
    t_manzu = [] #萬子部分の部分置換数tの配列
    u_manzu = [] #萬子部分の部分置換数uの配列
    for i in range(0,5):
        t_manzu.append(int(hash_table[0][manzu_hash].split()[i]))
    for i in range(5,10):
        u_manzu.append(int(hash_table[0][manzu_hash].split()[i]))
    t_pinzu = [] #筒子部分の部分置換数tの配列
    u_pinzu = [] #筒子部分の部分置換数uの配列
    for i in range(0,5):
        t_pinzu.append(int(hash_table[0][pinzu_hash].split()[i]))
    for i in range(5,10):
        u_pinzu.append(int(hash_table[0][pinzu_hash].split()[i]))
    t_souzu = [] #索子部分の部分置換数tの配列
    u_souzu = [] #索子部分の部分置換数uの配列
    for i in range(0,5):
        t_souzu.append(int(hash_table[0][souzu_hash].split()[i]))
    for i in range(5,10):
        u_souzu.append(int(hash_table[0][souzu_hash].split()[i]))
    t_zihai = [] #字牌部分の部分置換数tの配列
    u_zihai = [] #字牌部分の部分置換数uの配列
    for i in range(0,5):
        t_zihai.append(int(hash_table[1][zihai_hash].split()[i]))
    for i in range(5,10):
        u_zihai.append(int(hash_table[1][zihai_hash].split()[i]))

    t = [t_manzu,t_pinzu,t_souzu,t_zihai]
    u = [u_manzu,u_pinzu,u_souzu,u_zihai]

    #計算部分
    x = [[0 for m in range(0,5)] for n in range(0,4)]
    y = [[0 for m in range(0,5)] for n in range(0,4)]
    for m in range(0,5):
        x[0][m] = t[0][m]
        y[0][m] = u[0][m]
    for n in range(1,4):
        for m in range(0,5):
            x_temp = 15
            y_temp = 15
            for l in range(0,m+1):
                x_temp = min(x_temp, x[n-1][l] + t[n][m-l])
                y_temp = min(y_temp, min(y[n-1][l] + t[n][m-l], x[n-1][l] + u[n][m-l]))
            x[n][m] = x_temp
            y[n][m] = y_temp
    Th_temp = 15
    for l in range(0,5-fuurosu):
        Th_temp = min(Th_temp, min(x[2][l] + u[3][(4-fuurosu)-l], y[2][l] + t[3][(4-fuurosu)-l]))
    Sh_normal = Th_temp - 1


    #最終的なシャンテン数
    Shanten_su = min(Sh_normal,Sh_kokushi,Sh_chiitoi)
    return Shanten_su 
   
