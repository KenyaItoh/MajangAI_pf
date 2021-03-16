# MajangAI_pf
整理版<br><br>
主な流れ<br>
①write_packet.pyで天鳳とのパケット通信を取ってくる<br>
②game_tenhou.pyで天鳳のデータを再現、打牌や鳴きなどをAIに検討させる<br>
③AIが出した答えをテンプレートマッチングによるGUI操作で天鳳に出力<br>
<br>
Template -> 画像テンプレート<br>
files -> 各アルゴリズムや補助機能など（要整理）<br>
guis -> テンプレートマッチングに使用<br>
hashtable_for_shantencheck -> シャンテン数計算用のハッシュテーブル<br>
game_tenhou.py -> メイン<br>
write_packet.py -> 天鳳からのパケットを受信してpacket_dataフォルダに保存<br>
hitori-majang-learning -> 一人麻雀機械学習<br>
majang-learning -> 四人麻雀機械学習（未完成）<br>
