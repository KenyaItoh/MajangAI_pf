import urllib.request as urlr
import re
import os
import time
import sys

#天鳳の過去の牌譜ログを取得する

#使い方．

#１．天鳳の牌譜ログサイトhttps://tenhou.net/sc/raw/にアクセスする．
#2."過去ログ"から好きなもの（1年分など）ダウンロードし，中のhtmlファイルを解凍(ssaなど
# のファイル名の意味は上記サイト参照．）（logファイルはいらないので注意)
#3.読み込みたいログのhtmlファイルをフォルダ(input_Folder)にまとめる.
#4.ログを書き込むxmlファイル(output_file)を新規作成する．
#5.mainに引数１:input_Folderのパス，引数2:output_fileのパスを渡して実行．おわり！(数時間かかるので注意)

#できたxmlファイルは一行が一局に対応している．同じ半荘は隣り合う行に存在する．
#天鳳のログの形式や解析は，http://m77.hatenablog.com/entry/2017/05/21/214529や
#https://blog.kobalab.net/entry/20170225/1488036549参照．




#main．引数 input_Folder:天鳳からダウンロードしたhtmlファイルの入ってるフォルダ
#                       もしフォルダが階層構造になっていても，recursiveにすべてのhtmlファイルを読み込む
#          output_file:牌譜データを書き込むxmlファイル
def main(input_Folder,output_file):
    with open(output_file,mode='w') as fo:
        recursiveFileExploreAndProsess(input_Folder,fo)
    print('全ファイル終わり')
    
#実質の本体.pathがディレクトリならその子要素すべてにrecursiveFileE(略)を適用し，
#ファイルならその内容を読み込み，記載されたurlにアクセスしてログをダウンロードし，
#局に分割してoutput_fileに書き込む．
#どのルールの牌譜をとってくるかはdownloadLogのrequirement引数参照．
def recursiveFileExploreAndProsess(path,output_file):
        cnt = 0
        if os.path.isdir(path):
            contents = os.listdir(path)
            for item in contents:
                recursiveFileExploreAndProsess(path + "\\" + item,output_file)
        else:
            with open(path,encoding='utf-8') as fi:
                line = fi.readline()
                while line:
                    raw_log = downloadLog(line)
                    if raw_log:
                        splitted_log = splitLog(raw_log)
                        for elm in splitted_log:
                            output_file.write(elm + '\n')
                    line = fi.readline()
                cnt += 1
                print(str(cnt)+" htmlファイル終わり")

#recursiveFileExploreAndProsess内で呼ぶ
#lineIncludingHTMLに含まれるurlにアクセスして天鳳から牌譜ログをとってくる
#ルールがrequirementの時のみアクセスする（デフォルト：四鳳南喰赤）
def downloadLog(lineIncludingHTML,requirement="四鳳東喰赤"):
    if requirement not in str(lineIncludingHTML):   
        return False
    else:
        raw_link = re.search("(?<=\").*?(?=\")",lineIncludingHTML).group()
        prosessed_link = raw_link.replace('?log=','log/?')
        i = 0
        with urlr.urlopen(prosessed_link) as response:
            while True:
                try:
                    raw_log = response.read()
                    break
                except:
                    i += 1
                    print('url('+prosessed_link+')のアクセスに '+str(i)+'回失敗（20回まで挑戦）')
                    time.sleep(1)
                    if i >= 20:
                        print('失敗')
                        return False
                    pass
        return raw_log

#recursiveFileExploreAndProsess内で呼ぶ
#ダウンロードしてきた牌譜ログは半荘(東風)ごとになっているので
#局の始まりが<INITであることを利用して，元のログを局ごとに分解する．
def splitLog(mjlog_str):
    logListSplitedByKyoku = re.findall("<INIT.*?(?=<INIT|</mjloggm)",str(mjlog_str))
    return logListSplitedByKyoku
        



if __name__ == '__main__':
    #args = sys.argv
    #if len(args) != 3:
    #    print('ERROR:2 arguments required ( input_Folder , output_file), please retry')
    #else:
    start = time.time()
    #main(args[1],args[2])
    main("input_folder","output.xml")
    elapsed_time = time.time() - start
    print(elapsed_time)
