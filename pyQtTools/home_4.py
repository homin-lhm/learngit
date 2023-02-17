from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import sys
from business.page3 import Page3
from business.page1_obj.frame1_btn1_f import Frame1Btn1F
from business.page1_obj.frame1_btn2_f import Frame1Btn2F
from business.page1_obj.frame1_btn3_f import Frame1Btn3F
from business.page1_obj.frame1_btn4_f import Frame1Btn4F


class Home(QDialog):

    def __init__(self, parent=None):
        super(Home, self).__init__(parent)
        # 窗口定义
        self.setWindowOpacity(1)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setObjectName("home_win")
        self.setStyleSheet("#home_win{border-image:url(./picture/background3.png);}"
                           "QPushButton{color:rgb(139,141,141)}"
                           "QPushButton:hover{color:rgb(255,190,173)}"
                           "QPushButton{border:2px solid rgb(226,250,246)}"
                           "QPushButton{font:75 15pt '黑体'}"
                           "QPushButton{border-radius:5px}"
                           "QPushButton{padding:2px 4px}"
                           "QLabel{font:75 15pt '黑体'}"
                           "QLabel{font-size:200%}"
                           "QLabel{color:rgb(163,92,94)}"
                           "QLineEdit{font:75 15pt '黑体'}"
                           "QLineEdit{color:rgb(249,251,250)}"
                           "QLineEdit{background-color:rgb(171,235,232)}"
                           "QLineEdit{border:2px solid rgb(226,250,246)}"
                           "QTextBrowser{font:75 15pt '黑体'}"
                           "QTextBrowser{color:rgb(190,233,214)}"
                           "QTextBrowser{background-color: rgb(202,202,202);}"
                           "QTextBrowser{border:2px solid rgb(226,250,246)}"
                           )
        self.resize(1050, 650)
        self.move(800, 400)
        self.setWindowTitle("miniTools")
        self.setWindowIcon(QIcon('./picture/lhm.ico'))
        self.home_page()

        # 标题栏
        self.title_label = QLabel(self)
        self.title_label.resize(1050, 30)
        self.title_label.setStyleSheet("QLabel{border-image:url(./picture/title_background2.png)}"
                                       "QLabel{border:2px solid rgb(10,20,18)}"
                                       )

        # 关闭按钮
        self.close_btn = QPushButton(self)
        self.close_btn.setText("X")
        self.close_btn.resize(30, 30)
        self.close_btn.setStyleSheet("QPushButton{color:rgb(139,141,141)}"
                                     "QPushButton{border:2px solid rgb(255,255,255)}"
                                     )

        # 窗口最大化按钮
        self.max_btn = QPushButton(self)
        self.max_btn.setText("口")
        self.max_btn.resize(30, 30)
        self.max_btn.setStyleSheet("QPushButton{color:rgb(139,141,141)}"
                                   "QPushButton{border:2px solid rgb(255,255,255)}"
                                   )

        # 窗口隐藏按钮
        self.hide_btn = QPushButton(self)
        self.hide_btn.setText("—")
        self.hide_btn.resize(30, 30)
        self.hide_btn.setStyleSheet("QPushButton{color:rgb(139,141,141)}"
                                    "QPushButton{border:2px solid rgb(255,255,255)}"
                                    )

        self.close_btn.pressed.connect(self.close)
        self.max_btn.pressed.connect(self.max_normal)
        self.hide_btn.pressed.connect(self.showMinimized)

    def home_page(self):

        # 【Frame】主页按钮
        self.frame = QFrame(self)
        self.frame.resize(200, 620)
        self.frame.move(0, 30)
        self.frame.setStyleSheet("QFrame{border:2px solid rgb(226,250,244)}")
        self.verticalLayout = QVBoxLayout(self.frame)

        # 第一个按钮事件
        btn1 = QPushButton("标签相关", self)
        self.verticalLayout.addWidget(btn1)

        # 第二个按钮事件
        btn2 = QPushButton("文件处理", self)
        self.verticalLayout.addWidget(btn2)

        # 第三个按钮事件
        btn3 = QPushButton("pdf转换", self)
        self.verticalLayout.addWidget(btn3)

        # 第四个按钮事件
        btn4 = QPushButton("接需求。。", self)
        self.verticalLayout.addWidget(btn4)

        # 第五个按钮事件
        btn5 = QPushButton("接需求。。", self)
        self.verticalLayout.addWidget(btn5)

        # 第六个按钮事件
        btn6 = QPushButton("接需求。。", self)
        self.verticalLayout.addWidget(btn6)

        # 第七个按钮事件
        btn7 = QPushButton("接需求。。", self)
        self.verticalLayout.addWidget(btn7)

        # 第八个按钮事件
        btn8 = QPushButton("接需求。。", self)
        self.verticalLayout.addWidget(btn8)

        btn1.clicked.connect(self.click_btn1)
        btn3.clicked.connect(self.click_btn3)

        # 【Frame】点击云文档后的
        self.frame1 = QFrame(self)
        self.frame1.resize(200, 620)
        self.frame1.move(0, 30)
        self.frame1.setStyleSheet("QFrame{border:2px solid rgb(226,250,244)}")
        self.verticalLayout_1 = QVBoxLayout(self.frame1)

        # 【Frame】云文档操作btn1，右侧的功能页
        self.frameRight1 = QFrame(self)
        self.frameRight1.resize(850, 620)
        self.frameRight1.move(200, 30)
        self.verticalLayoutRight1 = QVBoxLayout(self.frameRight1)

        # 【Frame】云文档操作btn2，右侧的功能页
        self.frameRight2 = QFrame(self)
        self.frameRight2.resize(850, 620)
        self.frameRight2.move(200, 30)
        self.verticalLayoutRight2 = QVBoxLayout(self.frameRight2)

        # 【Frame】云文档操作btn3，右侧的功能页
        self.frameRight3 = QFrame(self)
        self.frameRight3.resize(850, 620)
        self.frameRight3.move(200, 30)
        self.verticalLayoutRight3 = QVBoxLayout(self.frameRight3)

        # 【Frame】云文档操作btn4，右侧的功能页
        self.frameRight4 = QFrame(self)
        self.frameRight4.resize(850, 620)
        self.frameRight4.move(200, 30)
        self.verticalLayoutRight4 = QVBoxLayout(self.frameRight4)

        # 按钮frame下添加按钮，云文档操作BTN
        # 返回主页按钮
        back_btn = QPushButton("<- 回到主页", self)
        self.verticalLayout_1.addWidget(back_btn)
        back_btn.clicked.connect(self.click_back_btn)

        # 第一个按钮事件
        frame1_btn1 = QPushButton("sid清空文\n件及文件夹", self)
        self.verticalLayout_1.addWidget(frame1_btn1)
        frame1_btn1.clicked.connect(self.click_frame1_btn1)

        # 第二个按钮事件
        frame1_btn2 = QPushButton("创建有对应\n设备应用信\n息的云文档", self)
        self.verticalLayout_1.addWidget(frame1_btn2)
        frame1_btn2.clicked.connect(self.click_frame1_btn2)

        # 第三个按钮事件
        frame1_btn3 = QPushButton("给用户添加\n设备标签或\n应用标签", self)
        self.verticalLayout_1.addWidget(frame1_btn3)
        frame1_btn3.clicked.connect(self.click_frame1_btn3)

        # 第四个按钮事件
        frame1_btn4 = QPushButton("查看用户下\n的设备标签\n和应用标签", self)
        self.verticalLayout_1.addWidget(frame1_btn4)
        frame1_btn4.clicked.connect(self.click_frame1_btn4)

        # 业务初始化
        Frame1Btn1F().business(self)
        Frame1Btn2F().business(self)
        Frame1Btn3F().business(self)
        Frame1Btn4F().business(self)

        self.frame1.setVisible(False)
        self.frameRight1.setVisible(False)
        self.frameRight2.setVisible(False)
        self.frameRight3.setVisible(False)
        self.frameRight4.setVisible(False)

    """max_normal | resizeEvent 重写了标题栏"""
    def max_normal(self):
        if self.isMaximized():
            self.showNormal()
            self.max_btn.setText("口")
        else:
            self.showMaximized()
            self.max_btn.setText("O")

    def resizeEvent(self, QResizeEvent):
        self.close_btn_x = self.width() - self.close_btn.width()
        self.close_btn.move(self.close_btn_x, 0)

        self.max_btn_x = self.close_btn_x - self.max_btn.width()
        self.max_btn.move(self.max_btn_x - 5, 0)

        self.hide_btn_x = self.max_btn_x - self.hide_btn.width()
        self.hide_btn.move(self.hide_btn_x - 10, 0)

    """mouseMoveEvent | mousePressEvent | mouseReleaseEvent 重写了鼠标拖动事件"""
    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    # def mouseReleaseEvent(self, e: QMouseEvent):
    #     if e.button() == Qt.LeftButton:
    #         self._isTracking = False
    #         self._startPos = None
    #         self._endPos = None

    # ---------------------------- 按钮触发事件 ----------------------------
    def click_btn1(self):
        self.frame1.setVisible(True)
        self.frame.setVisible(False)

    def click_back_btn(self):
        self.frame.setVisible(True)
        self.frameRight1.setVisible(False)
        self.frameRight2.setVisible(False)
        self.frameRight3.setVisible(False)
        self.frameRight4.setVisible(False)
        self.frame1.setVisible(False)

    def click_btn3(self):
        Page3().get_web()

    def click_frame1_btn1(self):
        self.frameRight1.setVisible(True)
        self.frameRight2.setVisible(False)
        self.frameRight3.setVisible(False)
        self.frameRight4.setVisible(False)

    def click_frame1_btn2(self):
        self.frameRight1.setVisible(False)
        self.frameRight2.setVisible(True)
        self.frameRight3.setVisible(False)
        self.frameRight4.setVisible(False)

    def click_frame1_btn3(self):
        self.frameRight1.setVisible(False)
        self.frameRight2.setVisible(False)
        self.frameRight3.setVisible(True)
        self.frameRight4.setVisible(False)

    def click_frame1_btn4(self):
        self.frameRight1.setVisible(False)
        self.frameRight2.setVisible(False)
        self.frameRight3.setVisible(False)
        self.frameRight4.setVisible(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windows = Home()
    windows.show()
    sys.exit(app.exec_())
