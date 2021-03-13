import shanten_check_new
from haihu_revival import Game,Janshi
import csv
import random
import sys
import time

#テンパイ予測用データセットの生成

class makeDataSet(Game):
    def __init__(self,kyoku_str):
        super().__init__(kyoku_str)
        self.probability = 1/4
        for janshi in self.janshi:
            janshi.doragiri = []
            janshi.akadoragiri = False
            janshi.fuurojunme = []

    def play(self):
        if super().play() == 1:
            return 0
        janshi = self.janshi[self.action_player_num]
        if self.action.tag[0] in ('D','E','F','G') and self.action.tag[1].isdecimal():
            if self.is_dora(int(self.action.tag[1:])):
                janshi.doragiri.append(int(self.action.tag[1:])//4)
            if int(self.action.tag[1:]) in (16,52,88):
                janshi.akadoragiri = True
        elif self.action.tag == 'N':
            janshi.fuurojunme.append((janshi.fuurosu,len(janshi.kawa)))     
        if random.randrange(int(1/self.probability)) == 0:
            self.record(janshi)

    def record(self,janshi):
        row = [0]*6888
        rowCnt = 0
        if janshi.reach == True:
            row[0] = 1
        rowCnt = 1
        a = len(janshi.kawa)+19*janshi.fuurosu
        row[rowCnt+a] = 1
        rowCnt += 5*19
        for i in janshi.fuurojunme:
            a = i[1] + 19*(i[0]-1)
            row[rowCnt+a] = 1
        rowCnt += 4*19
        tedasisu = 0
        last_tedasi = -1
        for d in janshi.kawa:
             if d[0] == 'd':
                tedasisu += 1
                last_tedasi = d[1:]
        a = tedasisu + 19*(janshi.fuurosu)
        row[rowCnt+a] = 1
        rowCnt += 5*19
        akadora_id = {'16':34,'52':35,'88':36}
        if last_tedasi in ('16','52','88'):
            last_tedasi = akadora_id[last_tedasi]
        else :
            last_tedasi = int(last_tedasi)//4
        a = last_tedasi + 37*(janshi.fuurosu)
        row[rowCnt+a] = 1
        rowCnt += 5*37
        if janshi.doragiri:
            for d in janshi.doragiri:
                row[rowCnt+d] = 1
        rowCnt += 34
        if janshi.akadoragiri:
            row[rowCnt+1] = 1
        rowCnt += 1
        tedasi_pare = -1
        for d in janshi.kawa:
            if d[0] == 'd':
                tedasi = d[1:]
                if tedasi in  ('16','52','88'):
                    tedasi = akadora_id[tedasi]
                else:
                    tedasi = int(tedasi)//4
                if tedasi_pare != -1:
                    a = tedasi_pare + tedasi*37
                    row[rowCnt+a] += 1
                tedasi_pare = tedasi
        rowCnt += 37*37
        if shanten_check_new.shanten_check(janshi,self.hash_table_for_shanten_check) == -1:
            row[rowCnt+1] = 1
        rowCnt += 1
        row = row[:rowCnt+1]

        writer = csv.writer(self.output_file)
        writer.writerow(row)

if __name__ == '__main__':
    t1 = time.time()
    hash_table = shanten_check_new.read_hash_table_for_shanten_check()
    with open(sys.argv[1]) as inp,open(sys.argv[2],'w',newline='') as out:
        line = inp.readline()
        cnt = 1
        while line:
            make = makeDataSet(line)
            make.hash_table_for_shanten_check = hash_table
            make.output_file = out
            while make.play() != 0:
                pass
            line = inp.readline()
            print(str(cnt)+'kyoku')
            cnt += 1
    t2 = time.time()
    elapsed_time = t2 -t1
    print(t2-t1)
        
