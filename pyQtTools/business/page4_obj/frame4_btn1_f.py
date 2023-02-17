from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
from common.fileOperation import FileOperation
import threading


class Frame4Btn1F(object):
    def __init__(self):
        self.text1 = "输入sid"
        self.text2 = "输入deviceId"
        self.text3 = "输入文件生成数量，以200为倍数，最少200，最多不限制"

    def business(self, QDialog):
        # textbox
        self.label = QLabel(QDialog)
        self.label.setText("批量创建设备文件，生成的文件都是一样的。")
        QDialog.verticalLayoutFrame4Right1.addWidget(self.label)

        self.textbox1 = QLineEdit(QDialog)
        self.textbox1.setText(self.text1)
        QDialog.verticalLayoutFrame4Right1.addWidget(self.textbox1)
        self.textbox1.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox1, self.text1))

        self.textbox2 = QLineEdit(QDialog)
        self.textbox2.setText(self.text2)
        QDialog.verticalLayoutFrame4Right1.addWidget(self.textbox2)
        self.textbox2.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox2, self.text2))

        self.textbox3 = QLineEdit(QDialog)
        self.textbox3.setText(self.text3)
        QDialog.verticalLayoutFrame4Right1.addWidget(self.textbox3)
        self.textbox3.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox3, self.text3))

        # 第一个按钮事件
        self.btn1 = QPushButton("create", QDialog)
        self.btn1.setGeometry(275, 150, 100, 50)
        QDialog.verticalLayoutFrame4Right1.addWidget(self.btn1)
        self.btn1.clicked.connect(lambda: self.click_btn1())

        # 控制台输出
        self.text_output = QTextBrowser(QDialog)
        QDialog.verticalLayoutFrame4Right1.addWidget(self.text_output)

    def textbox_click_color(self, textbox, text):
        if textbox.text() != text:
            textbox.setStyleSheet(
                "QLineEdit{font:75 15pt '黑体'}"
                "QLineEdit{color:rgb(94,221,224)}")

    def click_btn1(self):
        t = threading.Thread(target=self.click_btn1_thread)
        t.start()

    def click_btn1_thread(self):
        # 点击
        sid = self.textbox1.text()
        device_id = self.textbox2.text()
        num = self.textbox3.text()
        loop_num = int(num)/200
        try:
            self.text_output.append("start create")
            assert_list = []
            for i in range(1, 201):
                t = threading.Thread(target=FileOperation().re_upload_device_file, args=(i, sid, device_id, loop_num, assert_list))
                t.start()
            while True:
                print(len(assert_list))
                if len(assert_list) == int(num):
                    self.text_output.append("create file sum: {}".format(len(assert_list)))
                    self.text_output.append("success!!")
                    self.text_output.moveCursor(self.text_output.textCursor().End)
                    break
                else:
                    self.text_output.append("create file sum: {}, loading...".format(len(assert_list)))
                    self.text_output.moveCursor(self.text_output.textCursor().End)
                    time.sleep(1)
                    continue
        except:
            self.text_output.append("create fail")