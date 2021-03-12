# packetファイルを読み込み，コマンドを選別して，操作につなげる．
# printの部分が操作につなげる部分．
# packetファイルは，./packet/下に保存される．
# packetの例は，./packetExample.txtにある．
# 「os.listdir(packetPath)[0]」で呼ばれるファイルは名前順なので，保存する側のプログラムはpacketの命名規則をよく考える．

import os
import time

# ファイル読み込み
def read_packet():
    packetPath = "./packet_data"
    if len(os.listdir(packetPath)) == 0: #packet_dataディレクトリにファイルがない
        #print("No update")
        return ""

    else: #packetディレクトリにファイルがある

        with open("{0}/{1}".format(packetPath, os.listdir(packetPath)[0]), "r") as f: #ファイルを開く
            read_text = f.read() #str
        time.sleep(0.01)
        os.remove("{0}/{1}".format(packetPath, os.listdir(packetPath)[0])) #ファイル削除
        #print(read_text)
        return read_text
    

#print(read_packet())