from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from common.fileOperation import FileOperation
import base64


class Frame1Btn2F(object):
    def __init__(self):
        self.text1 = "输入sid"
        self.text2 = "输入设备ID"
        self.text3 = "输入设备名"
        self.text4 = "输入应用名"

        pass

    def business(self, QDialog):
        # textbox
        self.label = QLabel(QDialog)
        self.label.setText("文件生成在'testProject'文件夹下\nsid必填、其他选填\n设备ID和设备名结合使用")
        QDialog.verticalLayoutRight2.addWidget(self.label)

        self.textbox1 = QLineEdit(QDialog)
        self.textbox1.setText(self.text1)
        QDialog.verticalLayoutRight2.addWidget(self.textbox1)
        self.textbox1.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox1, self.text1))

        self.textbox2 = QLineEdit(QDialog)
        self.textbox2.setText(self.text2)
        QDialog.verticalLayoutRight2.addWidget(self.textbox2)
        self.textbox2.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox2, self.text2))

        self.textbox3 = QLineEdit(QDialog)
        self.textbox3.setText(self.text3)
        QDialog.verticalLayoutRight2.addWidget(self.textbox3)
        self.textbox3.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox3, self.text3))

        self.textbox4 = QLineEdit(QDialog)
        self.textbox4.setText(self.text4)
        QDialog.verticalLayoutRight2.addWidget(self.textbox4)
        self.textbox4.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox4, self.text4))

        # 第一个按钮事件
        self.btn1 = QPushButton("create", QDialog)
        self.btn1.setGeometry(275, 150, 100, 50)
        QDialog.verticalLayoutRight2.addWidget(self.btn1)
        self.btn1.clicked.connect(lambda: self.click_btn1())

        # 第二个按钮事件
        self.btn2 = QPushButton("清空输入数据", QDialog)
        self.btn2.setGeometry(275, 150, 100, 50)
        QDialog.verticalLayoutRight2.addWidget(self.btn2)
        self.btn2.clicked.connect(lambda: self.click_btn2())

        # 控制台输出
        self.text_output = QTextBrowser(QDialog)
        QDialog.verticalLayoutRight2.addWidget(self.text_output)

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

    def click_btn1(self):
        # 点击
        sid = str(self.textbox1.text())
        device_id = str(self.textbox2.text())
        device_name = str(self.textbox3.text())
        request_channel = str(self.textbox4.text())
        try:
            if "输入" in device_id or device_id == "":
                device_id = None
            if "输入" in device_name or device_name == "":
                device_name = None
            if "输入" in request_channel or request_channel == "":
                request_channel = None
            headers = self.create_headers(device_id, device_name, request_channel)
            file_id, group_id, file_name = FileOperation().uploadCloudFile_update_header(sid, headers)
            if file_id is None:
                self.text_output.setText("create fail, please check params!")
            else:
                self.text_output.setText("create success!\nfile_id:{}\ngroup_id:{}\nfile_name:{}".format(file_id, group_id, file_name))
        except Exception as err:
            self.text_output.setText("create fail!! error: {}".format(err))

    def create_headers(self, device_id, device_name, request_channel):
        if device_id is None and request_channel is not None:
            headers = {"x-kso-request-channel": base64.b64encode(request_channel.encode("utf-8"))}
        elif device_id is not None and request_channel is None:
            headers = {"x-kso-device-name": base64.b64encode(device_name.encode("utf-8")), "x-kso-device-id": base64.b64encode(device_id.encode("utf-8"))}
        elif device_id is not None and request_channel is not None:
            headers = {"x-kso-device-name": base64.b64encode(device_name.encode("utf-8")), "x-kso-device-id": base64.b64encode(device_id.encode("utf-8")), "x-kso-request-channel": base64.b64encode(request_channel.encode("utf-8"))}
        else:
            headers = {}
        return headers
