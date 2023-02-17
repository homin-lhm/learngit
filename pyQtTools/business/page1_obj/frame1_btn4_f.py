from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from common.collect import Collect


class Frame1Btn4F(object):
    def __init__(self):
        self.text1 = "输入sid"
        self.text2 = "输入searchtag服务的accessID"
        self.text3 = "输入searchtag服务的secretKey"

    def business(self, QDialog):
        # textbox
        self.label = QLabel(QDialog)
        self.label.setText("需输入对应服务的输入accessID和secretKey")
        QDialog.verticalLayoutRight4.addWidget(self.label)

        self.textbox1 = QLineEdit(QDialog)
        self.textbox1.setText(self.text1)
        QDialog.verticalLayoutRight4.addWidget(self.textbox1)
        self.textbox1.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox1, self.text1))

        self.textbox2 = QLineEdit(QDialog)
        self.textbox2.setText(self.text2)
        QDialog.verticalLayoutRight4.addWidget(self.textbox2)
        self.textbox2.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox2, self.text2))

        self.textbox3 = QLineEdit(QDialog)
        self.textbox3.setText(self.text3)
        QDialog.verticalLayoutRight4.addWidget(self.textbox3)
        self.textbox3.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox3, self.text3))
        
        # 第一个按钮事件
        self.btn1 = QPushButton("query", QDialog)
        self.btn1.setGeometry(275, 150, 100, 50)
        QDialog.verticalLayoutRight4.addWidget(self.btn1)
        self.btn1.clicked.connect(lambda: self.click_btn1())

        # 第二个按钮事件
        self.btn2 = QPushButton("清空输入数据", QDialog)
        self.btn2.setGeometry(275, 150, 100, 50)
        QDialog.verticalLayoutRight4.addWidget(self.btn2)
        self.btn2.clicked.connect(lambda: self.click_btn2())

        # 控制台输出
        self.text_output = QTextBrowser(QDialog)
        QDialog.verticalLayoutRight4.addWidget(self.text_output)

    def textbox_click_color(self, textbox, text):
        if textbox.text() != text:
            textbox.setStyleSheet(
                "QLineEdit{font:75 15pt '黑体'}"
                "QLineEdit{color:rgb(94,221,224)}")

    def click_btn1(self):
        # 点击
        sid = self.textbox1.text()
        accessID = str(self.textbox2.text())
        secretKey = str(self.textbox3.text())
        try:
            result = Collect().searchtag_taginfo_v1_taginfo(accessID, secretKey, sid)
            if result.status_code == 200:
                self.text_output.setText("query success!\nresponse json: \n{}".format(result.json()))
            else:
                self.text_output.setText("query fail!\nresponse code:{} \nresponse json: \n{}".format(result.status_code, result.json()))
        except:
            self.text_output.setText("query fail!")

    def click_btn2(self):
        self.textbox1.setText(self.text1)
        self.textbox2.setText(self.text2)
        self.textbox3.setText(self.text3)