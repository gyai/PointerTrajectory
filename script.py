import PySimpleGUI as sg                                 # インポート
from tkinter import *
from tkinter import ttk

'''
#データ取得
 ストレージの.csvファイルを開いて中身を取得
 csvの各行1次元に,csvの各列をその中の2次元目の要素として、二次元配列orリストに格納
# 画面
 スマホ画面を模したウィンドウ作成
 その上部分には各地点にターゲットが敷き詰められている(button35個)
 buttonをタップすると対応する地点のターゲット(button)だけが残り
 そのターゲットに対応する軌跡が30行(タスク数)分表示される->なにかしら使って直線描く
 
'''
''' ここからデータ取得 '''


'''ここから見た目'''
# ウィンドウの内容を定義する
#画面上部に縦7x横5=35個のbutton配置(150*150)
layout = [ ]    # レイアウト->ウィンドウに設定するやつ
width = 1080  #nexus5の画面ピクセル比率(1080,1920)のまま縮小
height = 1920
bairitu = 1/3 #1/4倍にしている

#button作成
# ボタンを縦7横5=35個配置
for j in range(7):
    layout.append([])
    for i in range(5):
        # ボタンの名前（テキスト）を設定
        button_name = "(" + str(j) + "," + str(i)+ ")"

        # ボタンのインスタンス作成
        button = sg.Button(
            button_text=button_name,
            image_filename='button_image.png',
            image_subsample=3,
            #image_size=(500, 500), #width,height
            key= "button_"+str(j)+"_"+str(i)
        )
        layout[j].append(button)


# ウィンドウを作成する

window = sg.Window('ウィンドウタイトル', layout, size=(int(width*bairitu), int(height*bairitu))) # ウィンドウ定義（サイズとか）
       
# ウィンドウを表示し、対話する
'''window.read()はinput()のように入力待ちの状態です。
入力を受け取るまではこの行でずっと待機していて、
イベントが発生したら(key, value)のタプル形式でイベントを受け取ります'''
while True:
    event, values = window.read()  #  イベントループまたは Window.read 呼び出し
    print(event)
# 収集された情報で何かをする


# 画面から削除して終了
window.close()                                  # ウィンドウを閉じる55