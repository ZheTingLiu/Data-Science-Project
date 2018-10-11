# -*- coding: UTF-8 -*-  

# Form implementation generated from reading ui file '.\datascience.ui'
#
# Created: Sun May 20 15:48:20 2018
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
import random
from io import open
from bs4 import BeautifulSoup
from PyQt4 import QtCore, QtGui
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def __init__(self):
        self.author = []
        self.comment = []
        self.all_url = []
        self.read_file()
    def read_file(self):
        f = open('articles.txt','r')
        all_url = []
        for url in f.readlines():
            all_url.append(url.strip('\n'))
        f.close()
        random.shuffle(all_url)
        self.all_url = all_url
    def fetch_comment(self,url):
    	self.comment = []
    	self.author = []
        payload = {
        'from' : '/bbs/Gossiping/index.html',
        'yes' : 'yes'
        }
        rs = requests.session()
        response = rs.post('https://www.ptt.cc/ask/over18', verify = False, data = payload)
        response = rs.get('https://www.ptt.cc'+url)
        soup = BeautifulSoup(response.text,'html.parser')
        self.content = soup.find_all('div',id = 'main-content')[0].text.split('※ 發信站')[0]
        comment = soup.find_all('span','f3 push-content')
        author = soup.find_all('span','f3 hl push-userid')
        for comment_,author_ in zip(comment,author):
            self.comment.append(comment_.text[2:])
            self.author.append(author_.text)

        

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(729, 423)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(420, 220, 120, 40))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(420, 360, 120, 40))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(420, 290, 120, 40))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_2"))


        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(570, 290, 120, 40))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_2.setEnabled(False)
        self.pushButton.setEnabled(False)
        self.pushButton_4.setEnabled(False)

        # self.label = QtGui.QLabel(self.centralwidget)
        # self.label.setGeometry(QtCore.QRect(50, 270, 341, 71))
        # self.label.setObjectName(_fromUtf8("label"))

        self.textBrowser1 = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser1.setGeometry(QtCore.QRect(50, 270, 341, 71))
        self.textBrowser1.setObjectName(_fromUtf8("textBrowser"))

        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 10, 671, 211))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 729, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "Useful", None))
        self.pushButton_2.setText(_translate("MainWindow", "Useless", None))
        self.pushButton_3.setText(_translate("MainWindow", "Start", None))
        self.pushButton_4.setText(_translate("MainWindow", "neutral", None))
        # self.textBrowser1.setText(_translate("MainWindow", " ", None))

    
            




    
if __name__ == "__main__":
    global article_index,comment_index,comment_label
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    article_index = 0
    comment_index = 1
    def displayArticle():
        global article_index,comment_index
        f = open('comment_label.txt','a',encoding = 'utf8')
        f.write(ui.all_url[article_index]+'\n')
        f.close()
        ui.fetch_comment(ui.all_url[article_index])
        ui.textBrowser.setText(ui.content)
        article_index = article_index + 1
        comment_index = 1
        ui.pushButton_3.setText(_translate("MainWindow", "Next", None))
        # ui.pushButton_3.setEnabled(False)
        ui.pushButton_2.setEnabled(True)
        ui.pushButton.setEnabled(True)
        ui.pushButton_4.setEnabled(True)
        # print len(ui.comment)
        # if len(ui.comment) == 1:
        #     displayArticle()
        #     return
        ui.textBrowser1.setText(ui.author[0]+': '+ui.comment[0])
    def judgeComment(label):
    	writeToTxt(label,str(ui.textBrowser1.toPlainText()).decode('utf8'))
        global comment_index
        upper_bound = 50
        if len(ui.comment) < 50:
        	upper_bound = len(ui.comment)
        if comment_index == upper_bound:
            ui.pushButton_3.setEnabled(True)
            ui.pushButton_2.setEnabled(False)
            ui.pushButton.setEnabled(False)
            displayArticle()
            return
        comment = ui.author[comment_index]+': '+ui.comment[comment_index]
        # print type(ui.comment[comment_index])
        ui.textBrowser1.setText(comment)
        comment_index = comment_index + 1
    def writeToTxt(label,comment):
        f = open('comment_label.txt','a',encoding = 'utf8')
        f.write(str(label)+' '+comment+'\n')
        f.close()
    ui.pushButton_3.clicked.connect(lambda: displayArticle())
    ui.pushButton_2.clicked.connect(lambda: judgeComment(0))
    ui.pushButton.clicked.connect(lambda: judgeComment(1))   
    ui.pushButton_4.clicked.connect(lambda: judgeComment(-1))
    MainWindow.show()
    sys.exit(app.exec_())
    
