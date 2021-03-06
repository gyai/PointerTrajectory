from itertools import count
from traceback import print_tb
import PySimpleGUI as sg                                 # インポート
from tkinter import *
from tkinter import ttk
import csv
import colorsys
import math
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

        csv_file = open("Trajectory.csv", "r", errors="", newline="",encoding="shift_jis")
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
        subdisp.make_trajectory()
        del subdisp   

    def main(self):
        while True: #リスナーの役割をしているらしい。何かのイベントが起きたらここの中の処理が動くように実装する

            '''window.read()はinput()のように入力待ちの状態です。
            入力を受け取るまではこの行でずっと待機していて、
            イベントが発生したら(key, value)のタプル形式でイベントを受け取ります'''
            event, values = self.window.read()  #  イベントループまたは Window.read 呼び出し->.readで[イベントが発生したよ]という情報をevent変数に伝えている
            print(event) #eventが'button_0_0'。valuesはよくわからんけど'{}'が出力
            tarpoii = event
            if event.startswith("button"): #(今回の場合はevent)keyがbuttonから始まるなら->buttonを押した時の処理
                _,x,y = event.split("_") #eventを_区切りで分割 右側がlistになる　変数yとxに押されたボタンのindex的なものが入る

                #押されたbuttonの情報取得
                self.y = int(y)*150
                self.x = int(x)*150

                #押されたボタンに対応した軌跡データ行だけ抽出
                self.p_tra_array = [] 
                self.splitarray = []
                for plist in self.pointerlist: #リストの長さ分繰り返す。要素の一つめと"y""x"が一致している行だけ抜き出す
                    if plist[0] == (str(self.x)+" , "+str(self.y)): #リストの0要素目(ターゲット座標)がボタンと同じ行だけp_tra_arrayに抜き出した
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
        self.x,self.y = maindis.x,maindis.y


    def make_trajectory(self):

#ここで生成するsubdisplayにcanvasを使って軌跡を表示したい。
#そのためにsublayoutに、軌跡を入れたcanvasを作る
    
        self.sublayout = [[sg.Canvas(key='-canvas-', background_color='white', size=(int(self.maindis.width*self.maindis.bairitu), int(self.maindis.height*self.maindis.bairitu)))],
                    [sg.Button("all補正off", key="-offall-",size=(10,1)),sg.Button("補正off(奇数セクション)", key="-off-",size=(10,1)), sg.Button("all補正on", key="-onall-",size=(10,1)), sg.Button("補正on(偶数セクション)", key="-on-",size=(10,1))],
                    [sg.Text("ウィンドウを閉じる"), sg.Button("Exit",key="-EXIT-",size=(10,1))]
                    ]

        #keep_on_top=Trueにする->画面を最前面に

        self.subwindow = sg.Window("SecondDisplay",self.sublayout, element_justification='center', keep_on_top=True, size=(int(self.maindis.width*self.maindis.bairitu)+50, int(self.maindis.height*self.maindis.bairitu)+100))
        self.canvas = self.subwindow['-canvas-']    
        self.subwindow.finalize()  

        #ここにMainクラスで作成した座標リストを入れる
        #print(self.maindis.splitarray[0])
        for i, slist in enumerate(self.maindis.splitarray):
            #splitarrayの各行の長さ(ポインター座標の数)をcountで取得
            code = '#'+''.join(list(map(lambda x: '{:02x}'.format(int(x * 255)), colorsys.hsv_to_rgb(i/len(self.maindis.splitarray) , 1, 1))))
            #slistの中に50,50があったらそれを消して詰める
            slist = [s for s in slist if (s != ['50.0', '50.0'])]
            for c in range(len(slist)-1):
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
        self.target = self.canvas.TKCanvas.create_rectangle(int(self.maindis.x/3), int(self.maindis.y/3), int(self.maindis.x/3)+int(150/3), int(self.maindis.y/3)+int(150/3))
        self.canvas.TKCanvas.itemconfig(self.target)

        self.count = 0
        
        while True:
            subevent, subvalue = self.subwindow.read()
            if subevent == "-EXIT-":
                sg.Popup("このウィンドウを閉じます",keep_on_top=True)
                break

            if subevent == "-off-":#奇数セクション→偶数行目
                self.canvas.TKCanvas.delete("all")
                #クリックされたボタンのターゲット座標
                x__ = float(self.x) 
                y__ = float(self.y)
                print('{}_{}'.format(math.floor((self.count/3)+1),math.floor((self.count%3)+1)))   
                for self.i, slist in enumerate(self.maindis.splitarray):
                    #count行目のみ表示
                    if self.i==self.count:
                        code = '#'+''.join(list(map(lambda x: '{:02x}'.format(int(x * 255)), colorsys.hsv_to_rgb(i/len(self.maindis.splitarray) , 1, 1))))
                        #slistの中に50,50があったらそれを消して詰める
                        slist = [s for s in slist if (s != ['50.0', '50.0'])]
                        for c in range(len(slist)-1):
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
                                if (x__>=float(slist[c+1][0]) or float(slist[c+1][0])>=x__+149)or(y__>=float(slist[c+1][1]) or float(slist[c+1][1])>=y__+149)  :
                                    print('error:target({},{})~({},{})|pointer({},{})'.format(x__,y__,x__+149,y__+149,slist[c+1][0],slist[c+1][1]))
                            self.canvas.TKCanvas.itemconfig(self.trajectory, fill=code)  #各行をグラデーションで表示したい
                        self.canvas.TKCanvas.itemconfig(self.endpoint, fill=code)  #各行をグラデーションで表示したい                                      
                
                self.count = self.count+1
                if self.count > 44:
                    self.count = 0
                self.target = self.canvas.TKCanvas.create_rectangle(int(self.maindis.x/3), int(self.maindis.y/3), int(self.maindis.x/3)+int(150/3), int(self.maindis.y/3)+int(150/3))
                self.canvas.TKCanvas.itemconfig(self.target)
            
            if subevent == "-on-":#偶数セクション→奇数行目   
                self.canvas.TKCanvas.delete("all")
                for self.i, slist in enumerate(self.maindis.splitarray):
                    #count行目のみ表示
                    if self.i==self.count:
                        code = '#'+''.join(list(map(lambda x: '{:02x}'.format(int(x * 255)), colorsys.hsv_to_rgb(i/len(self.maindis.splitarray) , 1, 1))))
                        for c in range(len(slist)-1):
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
                self.count = self.count+1
                self.target = self.canvas.TKCanvas.create_rectangle(int(self.maindis.x/3), int(self.maindis.y/3), int(self.maindis.x/3)+int(150/3), int(self.maindis.y/3)+int(150/3))
                self.canvas.TKCanvas.itemconfig(self.target)
            if subevent == "-onall-":
                self.canvas.TKCanvas.delete("all")
                for self.i, slist in enumerate(self.maindis.splitarray):
                    #奇数行目のみ表示
                    if self.i%2==1:
                        code = '#'+''.join(list(map(lambda x: '{:02x}'.format(int(x * 255)), colorsys.hsv_to_rgb(i/len(self.maindis.splitarray) , 1, 1))))
                        for c in range(len(slist)-1):
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
                self.target = self.canvas.TKCanvas.create_rectangle(int(self.maindis.x/3), int(self.maindis.y/3), int(self.maindis.x/3)+int(150/3), int(self.maindis.y/3)+int(150/3))
                self.canvas.TKCanvas.itemconfig(self.target)

            if subevent == "-offall-":
                self.canvas.TKCanvas.delete("all")
                for self.i, slist in enumerate(self.maindis.splitarray):
                    #偶数行目のみ表示
                    if self.i%2==0:
                        code = '#'+''.join(list(map(lambda x: '{:02x}'.format(int(x * 255)), colorsys.hsv_to_rgb(i/len(self.maindis.splitarray) , 1, 1))))
                        for c in range(len(slist)-1):
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
                self.target = self.canvas.TKCanvas.create_rectangle(int(self.maindis.x/3), int(self.maindis.y/3), int(self.maindis.x/3)+int(150/3), int(self.maindis.y/3)+int(150/3))
                self.canvas.TKCanvas.itemconfig(self.target)
               

            
        self.subwindow.close()


disp1 = MainDisplay()
disp1.main()
