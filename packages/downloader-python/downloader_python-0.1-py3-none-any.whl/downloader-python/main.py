from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.uic import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from downloader import *
import sys
import requests
import os
import datetime
import time
from colorama import *
init(autoreset=True)
print(f'[{time.ctime()}][main/Info] module colorama inited')
print(f'[{time.ctime()}][main/Info] modules initlazed')

Ui_MainWindow,_ = loadUiType('downloader.ui')
Ui_MainWindow2,_ = loadUiType('about.ui')
class window2(QtWidgets.QMainWindow,Ui_MainWindow2):
    def __init__(self):
        super(window2,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)
        self.setWindowIcon(QIcon('icon.bmp'))




class window(QtWidgets.QMainWindow,Ui_MainWindow):
    signal = pyqtSignal()
    def __init__(self):
        print(f'[{time.ctime()}][main/Info] loading')
        super(window,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.download)
        self.te = ''
        self.progressBar.setValue(0)
        self.pushButton_2.clicked.connect(self.fwa)
        self.pushButton_3.clicked.connect(self.about)


        self.setWindowIcon(QIcon('icon.bmp'))
        print(f'[{time.ctime()}][main/Info] icon loaded')

        try:
            self.load()
            print(f'[{time.ctime()}][main/Info] load settings.properties sucsess')
        except BaseException as e:


            print(f'{Fore.YELLOW}[{time.ctime()}][main/Error] error in initlazing:{e}')

            print(Fore.RED+r'*\**:( Downloader Crashed! ):**/*')
            sys.exit(self.show())

        self.timer = QTimer()
        self.timer.timeout.connect(self.write)
        self.timer.start(500)
        print(f'[{time.ctime()}][main/Info] timer initlazing sucsess')
    def about(self):
        self.signal.emit()
    def opencmd(self):
        os.system('cmd')
    def fwa(self):
        self.print()
        self.close()
    def print(self):
        print(f'[{time.ctime()}][main/Info] stopping!')

    def load(self):

        a = open('properties/settings.properties')

        dic = eval(a.read())
        if dic[0]:
            self.checkBox.toggle()
        if dic[1]:
            self.checkBox_2.toggle()
        if dic[2]:
            self.checkBox_3.toggle()
        self.lineEdit.setText(dic[3])
        self.lineEdit_2.setText(dic[4])
    def write(self):

        a = open('properties/settings.properties','w')
        dic = [None,None,None,None,None]
        if self.checkBox.isChecked():
            dic[0] = True
        else:
            dic[0] = False

        if self.checkBox_2.isChecked():
            dic[1] = True
        else:
            dic[1] = False

        if self.checkBox_3.isChecked():
            dic[2] = True
        else:
            dic[2] = False
        dic[3] = self.lineEdit.text()
        dic[4] = self.lineEdit_2.text()

        a.write(str(dic))


    def download(self):
        print(f'[{time.ctime()}][main/Info] Downloading')
        self.u(0)
        a = datetime.datetime.now()
        self.u(1)
        self.te = ''
        self.u(3)
        self.textBrowser.setText(self.te)
        self.u(4)
        self.update('initlazing')
        self.u(5)

        try:
            self.u(10)
            self.update('getting')
            self.u(20)
            if not self.checkBox.isChecked():
                if self.lineEdit_3.text() == '':
                    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78'}
                else:
                    header = header = {'user-agent':self.lineEdit_3.text()}

                r = requests.get(self.lineEdit.text(),headers = header)
            else:
                r = requests.get(self.lineEdit.text())
            self.u(30)
            con = r.content
            self.u(40)
            text = self.lineEdit.text().split('/')
            self.u(50)
            self.update('downloading')
            self.u(60)
            aaaaa = self.lineEdit_2.text()+text[-1].replace('/','')\
            .replace(r'\\', '')\
            .replace(':', '')\
            .replace('*', '')\
            .replace('?', '')\
            .replace('"','') \
            .replace('<', '') \
            .replace('>', '') \
            .replace('|', '') \

            aaa = str(time.time())
            with open(aaaaa,'ab+') as f:
                self.u(70)
                self.update('writing')
                self.u(80)
                f.write(con)
                self.u(90)
            self.u(101)
            b = datetime.datetime.now()
            x = b-a
            x = x.total_seconds()
            if not self.checkBox_2.isChecked():
                print(f'[{time.ctime()}][main/Info] Download from {self.lineEdit.text()} sucsess')
                size = float(os.path.getsize(aaaaa))
                if size >= 1024 and size <= 1024*1024:
                    self.update(f'sucsess in {x}s({size/1024}KB,{size/1024/x}KB/s)')
                elif size >= 1024*1024 and size <= 1024*1024*1024:
                    self.update(f'sucsess in {x}s({size/1024/1024}MB,{size/1024/1024/x}MB/s)')
                elif size >= 1024*1024*1024 and size <= 1024*1024*1024*1024:
                    self.update(f'sucsess in {x}s({size/1024/1024/1024}GB,{size/1024/1024/1024/x}GB/s)')
                elif size >= 1024*1024*1024*1024:
                    self.update(f'sucsess in {x}s({size/1024/1024/1024/1024}TB,{size/1024/1024/1024/1024/x}TB/s)')
                else:
                    self.update(f'sucsess in {x}s({size}B,{size/x}B/s)')
            else:
                self.update(f'sucsess in {x}s')
                print(f'[{time.ctime()}][main/Info] Download from {self.lineEdit.text()} sucsess')

        except BaseException as e:
            self.u(0)
            if not self.checkBox_3.isChecked():
                self.update(f'error:{e}')
            else:
                self.update(f'failed')


            print(f'{Fore.YELLOW}[{time.ctime()}][main/Error] error in download:{e},ignored')







    def update(self,t):
        self.te += t + '\n'
        self.textBrowser.setText(self.te)
    def u(self,v):
        a = self.progressBar.value()
        if v > a:
            for i in range(a,v):
                self.progressBar.setValue(i)
                time.sleep(0.001)
        else:

            self.progressBar.setValue(v)

from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import QT_VERSION_STR
print(f'[{time.ctime()}][main/Info] backend library:PyQt5 version {PYQT_VERSION_STR} build {QT_VERSION_STR}')
app = QtWidgets.QApplication(sys.argv)
window = window()
window.show()
window2=window2()
window.signal.connect(window2.show)
sys.exit(app.exec_())



