import PySimpleGUI as sg                                 # インポート
from tkinter import *
from tkinter import ttk
import csv
import colorsys
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
#---------class1で最初のターゲットたくさんの画面と、押した時のデータ
class MainDisplay:
    def __init__(self):
        ''' ここからデータ取得 '''

        csv_file = open("pointer_tra.csv", "r", errors="", newline="" )
        #リスト形式
        f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
        self.pointerlist = []
        for row in f: #全行分回す
            i=0
            while i<len(row):
                if '\n' in row[i]:
                    tmp=list(map(lambda x:x.replace(',', ' , '), row[i].replace('"', ' ').replace('\n', ' ').replace(' , ', ',').split()))
                    row=row[:i]+tmp+(row[i+1:] if i<len(row) else [])
                    i=0
                    continue
                i=i+1
            #rowはList
            #row[0]で必要な項目を取得することができる
            self.pointerlist.append(row) #2次元配列pointerlist


        '''ここから見た目'''
        # ウィンドウの内容を定義する
        #画面上部に縦5x横7=35個のbutton配置(150*150)

        self.layout = [ ]    # レイアウト->ウィンドウに設定するやつ
        #column = [ ]
        self.width = 1080  #nexus5の画面ピクセル比率(1080,1920)のまま縮小
        self.height = 1920
        self.bairitu = 1/3 #1/3倍にしている

        #button作成
        # ボタンを縦5横7=35個配置
        for j in range(5):
            #column.append([])
            self.layout.append([])
            for i in range(7):
                # ボタンの名前（テキスト）を設定
                button_name = "(" + str(i) + "," + str(j)+ ")"

                # ボタンのインスタンス作成
                button = sg.Button(
                    button_text=button_name,
                    image_filename='button_image.png',
                    image_subsample=5, #1/3にしている
                    image_size=(500, 500), #width,height
                    key= "button_"+str(i)+"_"+str(j)
                )
                #column[j].append(button)
                self.layout[j].append(button)


        #layout.append(column)
        # ウィンドウを作成する(button押下後に作成するsubDispley用関数も作成)
        self.window = sg.Window('MainDisplay', self.layout, size=(int(self.width*self.bairitu), int(self.height*self.bairitu))) # ウィンドウ定義（サイズとか）

    #第２画面設定->pointerの軌跡表示ウィンドウ
    def make_subdisplay(self):
        subdisp = SubDisplay(self)
        subdisp.make_trajectory() #現状、ここが呼び出された場合SubDisplayのwhileが永遠に回って、MainDisplayのwhileがストップしてしまう
        del subdisp   

    def main(self):
        while True: #リスナーの役割をしているらしい。何かのイベントが起きたらここの中の処理が動くように実装する

            '''window.read()はinput()のように入力待ちの状態です。
            入力を受け取るまではこの行でずっと待機していて、
            イベントが発生したら(key, value)のタプル形式でイベントを受け取ります'''
            event, values = self.window.read()  #  イベントループまたは Window.read 呼び出し->.readで[イベントが発生したよ]という情報をevent変数に伝えている
            print(event) #eventが'button_0_0'。valuesはよくわからんけど'{}'が出力

            if event.startswith("button"): #(今回の場合はevent)keyがbuttonから始まるなら->buttonを押した時の処理
                _,x,y = event.split("_") #eventを_区切りで分割 右側がlistになる　変数yとxに押されたボタンのindex的なものが入る

                #押されたbuttonの情報取得
                y = int(y)*150
                x = int(x)*150

                #押されたボタンに対応した軌跡データ行だけ抽出
                self.p_tra_array = [] 
                self.splitarray = []
                for plist in self.pointerlist: #リストの長さ分繰り返す。要素の一つめと"y""x"が一致している行だけ抜き出す
                    if plist[0] == (str(x)+" , "+str(y)): #リストの0要素目(ターゲット座標)がボタンと同じ行だけp_tra_arrayに抜き出した
                        self.p_tra_array.append(plist) ###この時点で、押したボタンの座標に対応した行(30行分)だけ入ってる
                        sarray = []
                        for pl in plist[2:]: #plistの3番目から(スライス)
                            if " , "in pl:
                                sarray.append(pl.split(" , ")) ##splitarrayの1次元目が[0]~[29]行情報、2次元目の0=x座標,1=y座標
                        self.splitarray.append(sarray)

                            
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

#----------第2画面----------
class SubDisplay:
    def __init__(self,maindis):
        self.maindis = maindis

        
    def make_trajectory(self):

#ここで生成するsubdisplayにcanvasを使って軌跡を表示したい。
#そのためにsublayoutに、軌跡を入れたcanvasを作る
    
        self.sublayout = [[sg.Canvas(key='-canvas-', background_color='white', size=(int(self.maindis.width*self.maindis.bairitu), int(self.maindis.height*self.maindis.bairitu)))],
                    [sg.Text("タスク番目"), sg.Button("count", key="-count-",size=(10,1))],
                    [sg.Text("ウィンドウを閉じる"), sg.Button("Exit",key="-EXIT-",size=(10,1))]
                    ]

        #keep_on_top=Trueにする->画面を最前面に

        self.subwindow = sg.Window("SecondDisplay",self.sublayout, element_justification='center', keep_on_top=True, size=(int(self.maindis.width*self.maindis.bairitu)+50, int(self.maindis.height*self.maindis.bairitu)+100))
        self.canvas = self.subwindow['-canvas-']    
        self.subwindow.finalize()  
        self.count = 0
        #ここにMainクラスで作成した座標リストを入れる
        print(self.maindis.splitarray[0])
        for i, slist in enumerate(self.maindis.splitarray):
            #splitarrayの各行の長さ(ポインター座標の数)をcountで取得
            code = '#'+''.join(list(map(lambda x: '{:02x}'.format(int(x * 255)), colorsys.hsv_to_rgb(i/len(self.maindis.splitarray) , 1, 1))))
            for c in range(len(slist)-1):
                #print(int(float(slist[c][0])*self.maindis.bairitu))
                #print(type(float(int(slist[c][0])*self.maindis.bairitu)))
                self.trajectory = self.canvas.TKCanvas.create_line(
                    int(float(slist[c][0])*self.maindis.bairitu),
                    int(float(slist[c][1])*self.maindis.bairitu), 
                    int(float(slist[c+1][0])*self.maindis.bairitu), 
                    int(float(slist[c+1][1])*self.maindis.bairitu)
                )
                if c==0:
                    self.startpoint = self.canvas.TKCanvas.create_rectangle(
                        int(float(slist[c][0])*self.maindis.bairitu),
                        int(float(slist[c][1])*self.maindis.bairitu), 
                        int(float(slist[c][0])*self.maindis.bairitu)+5,
                        int(float(slist[c][1])*self.maindis.bairitu)+5 
                    )
                    self.canvas.TKCanvas.itemconfig(self.startpoint, fill=code)  #各行をグラデーションで表示したい
                if c==int(len(slist)-3):
                    self.endpoint = self.canvas.TKCanvas.create_oval(
                        int(float(slist[c+1][0])*self.maindis.bairitu),
                        int(float(slist[c+1][1])*self.maindis.bairitu), 
                        int(float(slist[c+1][0])*self.maindis.bairitu)+5,
                        int(float(slist[c+1][1])*self.maindis.bairitu)+5 
                    )
                self.canvas.TKCanvas.itemconfig(self.trajectory, fill=code)  #各行をグラデーションで表示したい
            self.canvas.TKCanvas.itemconfig(self.endpoint, fill=code)  #各行をグラデーションで表示したい
        
         

        while True:
            subevent, subvalue = self.subwindow.read()
            if subevent == "-EXIT-":
                sg.Popup("このウィンドウを閉じます",keep_on_top=True)
                break
            if subevent == "-count-":
                self.count = self.count+1
                self.canvas.TKCanvas.delete("all")
                for self.i, slist in enumerate(self.maindis.splitarray):
                    #count行目のみ表示
                    if self.i==self.count:
                        code = '#'+''.join(list(map(lambda x: '{:02x}'.format(int(x * 255)), colorsys.hsv_to_rgb(i/len(self.maindis.splitarray) , 1, 1))))
                        for c in range(len(slist)-1):
                            #print(int(float(slist[c][0])*self.maindis.bairitu))
                            #print(type(float(int(slist[c][0])*self.maindis.bairitu)))
                            self.trajectory = self.canvas.TKCanvas.create_line(
                                int(float(slist[c][0])*self.maindis.bairitu),
                                int(float(slist[c][1])), 
                                int(float(slist[c+1][0])*self.maindis.bairitu), 
                                int(float(slist[c+1][1])))
                            if c==0:
                                self.startpoint = self.canvas.TKCanvas.create_rectangle(
                                    int(float(slist[c][0])*self.maindis.bairitu),
                                    int(float(slist[c][1])), 
                                    int(float(slist[c][0])*self.maindis.bairitu)+5,
                                    int(float(slist[c][1]))+5 
                                )
                                self.canvas.TKCanvas.itemconfig(self.startpoint, fill=code)  #各行をグラデーションで表示したい
                            if c==int(len(slist)-3):
                                self.endpoint = self.canvas.TKCanvas.create_oval(
                                    int(float(slist[c+1][0])*self.maindis.bairitu),
                                    int(float(slist[c+1][1])), 
                                    int(float(slist[c+1][0])*self.maindis.bairitu)+5,
                                    int(float(slist[c+1][1]))+5
                                )
                            self.canvas.TKCanvas.itemconfig(self.trajectory, fill=code)  #各行をグラデーションで表示したい
                        self.canvas.TKCanvas.itemconfig(self.endpoint, fill=code)  #各行をグラデーションで表示したい
        self.subwindow.close()


disp1 = MainDisplay()
disp1.main()
