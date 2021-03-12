import PySimpleGUI as sg                                 # インポート
from tkinter import *
from tkinter import ttk
import csv
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
class MainDisplay:
    ''' ここからデータ取得 '''

    csv_file = open("pointer_tra.csv", "r", errors="", newline="" )
    #リスト形式
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    pointerlist = []
    for row in f: #全行分回す
        #rowはList
        #row[0]で必要な項目を取得することができる
        pointerlist.append(row) #2次元配列pointerlist


    '''ここから見た目'''
    # ウィンドウの内容を定義する
    #画面上部に縦7x横5=35個のbutton配置(150*150)

    layout = [ ]    # レイアウト->ウィンドウに設定するやつ
    #column = [ ]
    width = 1080  #nexus5の画面ピクセル比率(1080,1920)のまま縮小
    height = 1920
    bairitu = 1/3 #1/3倍にしている

    #button作成
    # ボタンを縦7横5=35個配置
    for j in range(7):
        #column.append([])
        layout.append([])
        for i in range(5):
            # ボタンの名前（テキスト）を設定
            button_name = "(" + str(j) + "," + str(i)+ ")"

            # ボタンのインスタンス作成
            button = sg.Button(
                button_text=button_name,
                image_filename='button_image.png',
                image_subsample=3, #1/3にしている
                #image_size=(500, 500), #width,height
                key= "button_"+str(j)+"_"+str(i)
            )
            #column[j].append(button)
            layout[j].append(button)


    #layout.append(column)
    # ウィンドウを作成する(button押下後に作成するsubDispley用関数も作成)
    window = sg.Window('MainDisplay', layout, finalize=True, size=(int(width*bairitu), int(height*bairitu))) # ウィンドウ定義（サイズとか）
    #第２画面設定->pointerの軌跡表示ウィンドウ
    def make_subdisplay(self):
        subdisp = SubDisplay()
        subdisp.make_trajectory()
        del subdisp   

    def main(self):
        while True: #リスナーの役割をしているらしい。何かのイベントが起きたらここの中の処理が動くように実装する

            '''window.read()はinput()のように入力待ちの状態です。
            入力を受け取るまではこの行でずっと待機していて、
            イベントが発生したら(key, value)のタプル形式でイベントを受け取ります'''
            event, values = self.window.read()  #  イベントループまたは Window.read 呼び出し->.readで[イベントが発生したよ]という情報をevent変数に伝えている
            print(event,values) #eventが'button_0_0'。valuesはよくわからんけど'{}'が出力

            if event.startswith("button"): #(今回の場合はevent)keyがbuttonから始まるなら->buttonを押した時の処理
                _,y,x = event.split("_") #eventを_区切りで分割 右側がlistになる　変数yとxに押されたボタンのindex的なものが入る

                #押されたbuttonの情報取得
                y = int(y)*150
                x = int(x)*150
                print("button座標",int(y),int(x))

                #押されたボタンに対応した軌跡データ行だけ抽出
                p_tra_array = [] 
                splitarray = []
                for plist in self.pointerlist: #リストの長さ分繰り返す。要素の一つめと"y""x"が一致している行だけ抜き出す
                    if plist[0] == (str(y)+" , "+str(x)): #リストの0要素目(ターゲット座標)がボタンと同じ行だけp_tra_arrayに抜き出した
                        p_tra_array.append(plist) ###この時点で、押したボタンの座標に対応した行(30行分)だけ入ってる
                        sarray = []
                        for pl in plist[2:]: #plistの3番目から(スライス)
                            #del pl[0],pl[1] ##ターゲット座標とポインター座標のテキストの要素を削除
                            if " , "in pl:
                                sarray.append(pl.split(" , ")) ##splitarrayの1次元目が[0]~[29]行情報、2次元目の0=x座標,1=y座標
                        splitarray.append(sarray)

                            
                #print(splitarray[5]) #splitarray[行][列][x座標 or y座標]が出力できる
                self.make_subdisplay()


            
            '''
            ・押されたbutton以外は非表示にしたい    ->よくわからん！layout[]の中にcolumn[]要素を入れて、そのcolumnを表示非表示するらしいけどできない
            └別ウィンドウを適宜作成するようにする

            ・画面下にリセットボタン(非表示などを初期状態に戻す)
            ・一行ずつ表示できるように仕様変えるべきかも？？？(後回し)
        ----- ここに処理を書く-----

            yとxに押されたbuttonの識別子が入っているから、各行の最初の文字と比較することで対応する軌跡の行を抽出できる(はず)
            30行分抽出できたら","で区切って、各行の要素を取り出してintにキャスト→直線引く用のlistにいれる
            直線用listの要素数分直線を引けば軌跡が出るはず->1/3にするの忘れない
            各タスクの軌跡は色か太さで区別
            '''
        

        # 画面から削除して終了
        self.window.close()                   # ウィンドウを閉じる55

class SubDisplay:
        maindis = MainDisplay()

        sublayout = [[sg.Canvas(background_color='WHITE', size=(int(maindis.width*maindis.bairitu), int(maindis.height*maindis.bairitu))],
                    [sg.Text("ウィンドウを閉じる")],
                    [sg.Button("Exit",key="-EXIT-",size=(10,1))]]
        #keep_on_top=Trueにする
        subwindow = sg.Window("SecondDisplay",sublayout,keep_on_top=True, size=(int(maindis.width*maindis.bairitu), int(maindis.height*maindis.bairitu)))
        
        def make_trajectory(self):
            while True:
                subevent, subvalue = self.subwindow.read()
                if subevent == "-EXIT-":
                    sg.Popup("このウィンドウを閉じます",keep_on_top=True)
                    break
            self.subwindow.close()


###ここが悪いのか？？？→2画面出るようになったけど、1回目のクリックしか反応しない。ループできるようにするべきなのか？？
disp1 = MainDisplay()
disp1.main()
