# wiresharkインストール
# wiresharkインストール時にtsharkをインストールするチェックボックスを押す．
# "pip install pyshark"
# "tshark -D" で，自身のイーサネットのインターフェイスをコピーする

from pyshark import LiveCapture 
import sys,os
import time
import shutil

name = 10000 # 命名規則のID．1局終わったら，0に戻す．

# ファイルに保存
def write_packet(packet_data):
    global name
    #start = time.time()
    with open("./packet_data/{}.txt".format(name), "w") as f:
        f.write(packet_data)
        print(packet_data)
        name += 1
    #elapsed_time = time.time() - start
    #print(elapsed_time)

# パケット一つ一つに実行
def callback(packet):
    #1パケットに複数のデータがある可能性があるので，3つのデータまで取れるようにする．(packet5行目から2行ごとにデータがある)
    #start = time.time()
    for i in range(5, 31, 2):
        time.sleep(0.001)
        try:
            packet_str = str(packet[i])
        except IndexError:
            pass
        else:
            packet_split = packet_str.splitlines()
            try:
                write_packet(packet_split[1])
            except IndexError:
                pass
    #print(str(time.time()-start))

#スニファー 
def get_data():
    #interface = "イーサネットのインターフェイス"
    #cap = LiveCapture(interface="\\Device\\NPF_{7C999537-85AB-4220-B1F9-21D7B6EDA43F}") # itoh
    cap = LiveCapture(interface="\\Device\\NPF_{70B7AD93-4936-429F-9CD3-481AB236A4C0}") # itoh
    #cap = LiveCapture(interface="\\Device\\NPF_{B4C621AF-E6E9-4870-BA69-291B0CB317C5}") # genta
    # フィルタ
    cap._display_filter = "ip.dst == 192.168.11.4 && websocket" #itoh
    #cap._display_filter = "ip.dst == 192.168.1.4 && websocket" # genta
    
    #cap._display_filter = "ip.src == 160.16.234.177 || ip.src == 160.16.100.237 || ip.src == 160.16.123.55 || ip.src == 160.16.146.234 || ip.src == 160.16.102.148 || ip.src == 160.16.235.36 && ip.dst == 192.168.11.4 && websocket"
    # リアルタイムスニッフィング
    cap.apply_on_packets(callback, None, None)

if __name__ == "__main__":
    #リセット
    shutil.rmtree("./packet_data")
    time.sleep(0.5)
    os.mkdir("./packet_data")

    get_data()

#1300115	2515.881588	160.16.102.148	192.168.11.4	WebSocket	99	WebSocket Text [FIN] 
#1609800	3019.715095	160.16.235.36	192.168.11.4	WebSocket	99	WebSocket Text [FIN] 
#90247	147.557263	160.16.123.55	192.168.11.4	WebSocket	361	WebSocket Text [FIN] 
#67967	557.393422	160.16.100.237	192.168.11.4	WebSocket	356	WebSocket Text [FIN] 
#176128	4027.251648	160.16.234.177	192.168.11.4	WebSocket	165	WebSocket Text [FIN] 