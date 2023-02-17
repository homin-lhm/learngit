from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from common.fileOperation import FileOperation


class Frame1Btn1F(object):
    def __init__(self):
        self.text1 = "输入sid"

    def business(self, QDialog):
        # textbox
        self.label = QLabel(QDialog)
        self.label.setText("仅清空个人空间下的，根据sid清空！")
        QDialog.verticalLayoutRight1.addWidget(self.label)

        self.textbox1 = QLineEdit(QDialog)
        self.textbox1.setText(self.text1)
        QDialog.verticalLayoutRight1.addWidget(self.textbox1)
        self.textbox1.textEdited[str].connect(lambda: self.textbox1_click_color())

        # 第一个按钮事件
        self.btn1 = QPushButton("clear", QDialog)
        self.btn1.setGeometry(275, 150, 100, 50)
        QDialog.verticalLayoutRight1.addWidget(self.btn1)
        self.btn1.clicked.connect(lambda: self.click_btn1())

        # 控制台输出
        self.text_output = QTextBrowser(QDialog)
        QDialog.verticalLayoutRight1.addWidget(self.text_output)

    def textbox1_click_color(self):
        if self.textbox1.text() != self.text1:
            self.textbox1.setStyleSheet(
                "QLineEdit{font:75 15pt '黑体'}"
                "QLineEdit{color:rgb(94,221,224)}")

    def click_btn1(self):
        # 点击
        sid = self.textbox1.text()
        try:
            result = FileOperation().delete_all_file_and_folder(sid)
            if result is True:
                self.text_output.setText("clear success")
            else:
                self.text_output.setText("clear fail")
        except:
            self.text_output.setText("clear fail")