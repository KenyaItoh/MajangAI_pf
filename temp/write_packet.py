# wiresharkインストール
# wiresharkインストール時にtsharkをインストールするチェックボックスを押す．
# "pip install pyshark"
# "tshark -D" で，自身のイーサネットのインターフェイスをコピーする
from pyshark import LiveCapture 
import os
import time
import shutil



name = 1000000 # 命名規則のID．1局終わったら，0に戻す．

# ファイルに保存
def write_packet(packet_data):
    global name
    with open("./packet_data/{}.txt".format(name), "w") as f:
        f.write(packet_data)
        print(packet_data)
        name += 1

# パケット一つ一つに実行
def callback(packet):
    #1パケットに複数のデータがある可能性があるので，3つのデータまで取れるようにする．(packet5行目から2行ごとにデータがある)
    for i in range(5, 31, 2):
        try:
            packet_str = str(packet[i])
        except IndexError:
            pass
        else:
            packet_split = packet_str.splitlines()
            # -   -   -   -   これを別のにつなげる．    -   -   -   - #
            write_packet(packet_split[1])
            # -   -   -   -   これを別のにつなげる．    -   -   -   - #


#スニファー 
def get_data():
    #interface 
    cap = LiveCapture(interface='\\Device\\NPF_{7C999537-85AB-4220-B1F9-21D7B6EDA43F}')
    # フィルタ
    cap._display_filter =   "ip.dst == 192.168.11.4 && websocket"
    #cap._display_filter =   "websocket"
    # リアルタイムスニッフィング
    cap.apply_on_packets(callback)

#リセット
shutil.rmtree("./packet_data")
time.sleep(0.5)
os.mkdir("./packet_data")

get_data()
    