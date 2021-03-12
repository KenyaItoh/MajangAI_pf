import function

def mentsu_count(janshi):
    global mentsu_suu
    global maximum_mentsu_suu
    mentsu_suu = len(janshi.fuurohai)

    temp_tehai = function.tehai_convert(janshi.tehai)

    for j in range(31,38):
        if temp_tehai[j] >= 3:
            mentsu_suu += 1
    
    mentsu_suu_copy = mentsu_suu
    maximum_mentsu_suu = mentsu_suu
    
    for i in range(1, 30):
        mentsu_suu = mentsu_suu_copy
        mentsu_cut(temp_tehai, i)
    
    return maximum_mentsu_suu






def mentsu_cut(temp_tehai, i): #アガリ判定用
    
    global mentsu_suu
    global maximum_mentsu_suu
    
    for j in range(i, 30):
        
        #コーツ抜き出し
        if temp_tehai[j] >= 3:
            mentsu_suu +=1
            #print(j,j,j)
            temp_tehai[j] -= 3
            mentsu_cut(temp_tehai, j)
            mentsu_suu -=1
            temp_tehai[j] += 3
    
        #シュンツ抜き出し
        if temp_tehai[j] > 0 and temp_tehai[j+1] > 0 and temp_tehai[j+2] > 0 and j < 28:
            mentsu_suu += 1
            #print(j,j+1,j+2)
            temp_tehai[j] -= 1
            temp_tehai[j+1] -= 1
            temp_tehai[j+2] -= 1
            mentsu_cut(temp_tehai, j)
            mentsu_suu -= 1
            temp_tehai[j] += 1
            temp_tehai[j+1] += 1
            temp_tehai[j+2] += 1   

        if mentsu_suu > maximum_mentsu_suu:
            maximum_mentsu_suu = mentsu_suu
            