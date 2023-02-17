from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from common.collect import Collect
import base64


class Frame1Btn3F(object):
    def __init__(self):
        self.text1 = "输入uid"
        self.text2 = "输入设备ID"
        self.text3 = "输入设备名"
        self.text4 = "输入应用名"
        self.text5 = "输入collect服务的accessID"
        self.text6 = "输入collect服务的secretKey"
        pass

    def business(self, QDialog):
        # textbox
        self.label = QLabel(QDialog)
        self.label.setText("uid必填、其他选填，设备ID需保证唯一性\n设备ID和设备名结合使用\n可以仅添加设备信息或仅添加应用信息\n测试环境的密钥可以为空")
        QDialog.verticalLayoutRight3.addWidget(self.label)

        self.textbox1 = QLineEdit(QDialog)
        self.textbox1.setText(self.text1)
        QDialog.verticalLayoutRight3.addWidget(self.textbox1)
        self.textbox1.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox1, self.text1))

        self.textbox2 = QLineEdit(QDialog)
        self.textbox2.setText(self.text2)
        QDialog.verticalLayoutRight3.addWidget(self.textbox2)
        self.textbox2.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox2, self.text2))

        self.textbox3 = QLineEdit(QDialog)
        self.textbox3.setText(self.text3)
        QDialog.verticalLayoutRight3.addWidget(self.textbox3)
        self.textbox3.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox3, self.text3))

        self.textbox4 = QLineEdit(QDialog)
        self.textbox4.setText(self.text4)
        QDialog.verticalLayoutRight3.addWidget(self.textbox4)
        self.textbox4.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox4, self.text4))

        self.textbox5 = QLineEdit(QDialog)
        self.textbox5.setText(self.text5)
        QDialog.verticalLayoutRight3.addWidget(self.textbox5)
        self.textbox5.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox5, self.text5))

        self.textbox6 = QLineEdit(QDialog)
        self.textbox6.setText(self.text6)
        QDialog.verticalLayoutRight3.addWidget(self.textbox6)
        self.textbox6.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox6, self.text6))

        # 第一个按钮事件
        self.btn1 = QPushButton("create", QDialog)
        self.btn1.setGeometry(275, 150, 100, 50)
        QDialog.verticalLayoutRight3.addWidget(self.btn1)
        self.btn1.clicked.connect(lambda: self.click_btn1())

        # 第二个按钮事件
        self.btn2 = QPushButton("清空输入数据", QDialog)
        self.btn2.setGeometry(275, 150, 100, 50)
        QDialog.verticalLayoutRight3.addWidget(self.btn2)
        self.btn2.clicked.connect(lambda: self.click_btn2())

        # 控制台输出
        self.text_output = QTextBrowser(QDialog)
        QDialog.verticalLayoutRight3.addWidget(self.text_output)

    def textbox_click_color(self, textbox, text):
        if textbox.text() != text:
            textbox.setStyleSheet(
                "QLineEdit{font:75 15pt '黑体'}"
                "QLineEdit{color:rgb(94,221,224)}")

    def click_btn2(self):
        self.textbox1.setText(self.text1)
        self.textbox2.setText(self.text2)
        self.textbox3.setText(self.text3)
        self.textbox4.setText(self.text4)
        self.textbox5.setText(self.text5)
        self.textbox6.setText(self.text6)

    def click_btn1(self):
        # 点击
        uid = self.textbox1.text()
        device_id = str(self.textbox2.text())
        device_name = str(self.textbox3.text())
        request_channel = str(self.textbox4.text())
        accessID = str(self.textbox5.text())
        secretKey = str(self.textbox6.text())
        try:
            if "输入" in device_id or device_id == "":
                device_id = None
            if "输入" in device_name or device_name == "":
                device_name =None
            if "输入" in request_channel or request_channel == "":
                request_channel = None
            if "输入" in uid or uid == "":
                uid = None
            else:
                uid = int(uid)
            if "输入" in accessID or accessID == "":
                accessID = "123"
            if "输入" in secretKey or secretKey == "":
                secretKey = "123"
            if uid is None:
                self.text_output.setText("uid required!")
            else:
                res = Collect().api_v1_userdatachange("file_create", uid, accessID, secretKey, device_id, device_name, request_channel)
                if res.status_code == 200:
                    self.text_output.setText("add success!\n设备ID:{}\n设备名:{}\n应用名:{}".format(device_id, device_name, request_channel))
                else:
                    self.text_output.setText("add fail! please check params!")
        except:
            self.text_output.setText("create fail")

