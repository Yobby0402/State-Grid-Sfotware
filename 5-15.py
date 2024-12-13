import cv2
import os
import shutil
import sys
import threading
import time
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class login_window(QDialog):  # 登录界面
    def __init__(self):
        super().__init__()

        self.data_class = None
        self.__setup_ui__()

    def __setup_ui__(self):  # 登录界面的所有控件
        self.setWindowTitle("用户管理界面")
        # 窗口大小
        self.resize(500, 400)
        self.setFixedSize(self.width(), self.height())
        # 工具栏
        self.frame_tool = QFrame(self)
        self.frame_tool.setGeometry(0, 0, self.width(), 40)
        self.frame_tool.setFrameShape(QFrame.Panel)
        self.frame_tool.setFrameShadow(QFrame.Raised)

        # 1.1 界面1按钮
        self.log_win_btn = QToolButton(self.frame_tool)
        self.log_win_btn.setCheckable(True)
        self.log_win_btn.setText("登录界面")
        self.log_win_btn.resize(int(self.width() / 2), 40)
        self.log_win_btn.setStyleSheet("QToolButton{background-color:lightgray}"
                                       "QToolButton:hover{color:red}"
                                       "QToolButton:pressed{background-color:gray;border: None;}"
                                       "QToolButton{font-size:30px}"
                                       )
        self.log_win_btn.clicked.connect(self.click_log_win)
        self.log_win_btn.setAutoRaise(True)

        # 1.2 界面2按钮
        self.resign_win_btn = QToolButton(self.frame_tool)
        self.resign_win_btn.setCheckable(True)
        self.resign_win_btn.setText("注册界面")
        self.resign_win_btn.resize(int(self.width() / 2), 40)
        self.resign_win_btn.setStyleSheet("QToolButton{background-color:lightgray}"
                                          "QToolButton:hover{color:red}"
                                          "QToolButton:pressed{background-color:gray;border: None;}"
                                          "QToolButton{font-size:30px}"
                                          )
        self.resign_win_btn.move(self.log_win_btn.width(), 0)
        self.resign_win_btn.clicked.connect(self.click_resign_win)
        self.resign_win_btn.setAutoRaise(True)

        self.btn_group = QButtonGroup(self.frame_tool)
        self.btn_group.addButton(self.log_win_btn, 1)
        self.btn_group.addButton(self.resign_win_btn, 2)

        # 2. 工作区域
        self.manage_frame = QFrame(self)
        self.manage_frame.setGeometry(0, 40, self.width(), self.height() - self.frame_tool.height())

        # 创建堆叠布局
        self.stacked_layout = QStackedLayout(self.manage_frame)

        # 第一个布局界面
        self.manage_frame1 = QMainWindow()

        self.login_frame = QWidget(self.manage_frame1)
        self.login_frame.setGeometry(0, 0, self.width(), self.manage_frame.height())

        self.login_hint = QLabel(self.manage_frame1)
        self.login_hint.setText("用户登录")
        self.login_hint.setStyleSheet("font-size:40px;font-weight:bold;font-family:Roman times;")
        self.login_hint.setGeometry(170, 20, 180, 35)

        self.user_name_hint = QLabel(self.manage_frame1)
        self.user_name_hint.setText('账号:')
        self.user_name_hint.setStyleSheet("font-size:30px;font-weight:bold;font-family:Roman times;")
        self.user_name_hint.setGeometry(100, 100, 150, 30)
        self.user_name_text = QLineEdit(self.manage_frame1)
        self.user_name_text.setGeometry(220, 100, 200, 30)
        self.user_name_text.setClearButtonEnabled(True)
        self.user_name_text.setPlaceholderText("请输入用户名")

        self.user_code_hint = QLabel(self.manage_frame1)
        self.user_code_hint.setText('密码:')
        self.user_code_hint.setStyleSheet("font-size:30px;font-weight:bold;font-family:Roman times;")
        self.user_code_hint.setGeometry(100, 150, 150, 30)
        self.user_code_text = QLineEdit(self.manage_frame1)
        self.user_code_text.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.user_code_text.setClearButtonEnabled(True)
        self.user_code_text.setGeometry(220, 150, 200, 30)
        self.user_code_text.setPlaceholderText("请输入密码")

        self.login_button = QPushButton(self.manage_frame1)
        self.login_button.setText("登录")
        self.login_button.setStyleSheet("QPushButton{background-color:lightblue}"
                                        "QPushButton:hover{color:red}"
                                        "QPushButton{border-radius:6px}"
                                        "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                        "QPushButton{font-size:30px}"
                                        )
        self.login_button.setGeometry(150, 250, 200, 50)
        self.login_button.clicked.connect(self.click_login_fun)

        self.error_hint_login = QLabel(self.manage_frame1)
        self.error_hint_login.setGeometry(220, 190, 200, 50)
        self.error_hint_login.setStyleSheet("font-size:20px;color:red;font-weight:bold;font-family:Roman times;")

        # 第二个布局界面
        self.manage_frame2 = QMainWindow()

        resign_frame = QFrame(self.manage_frame2)
        resign_frame.setGeometry(0, 0, self.width(), self.manage_frame.height())
        self.resign_hint = QLabel(self.manage_frame2)
        self.resign_hint.setText("用户注册")
        self.resign_hint.setStyleSheet("font-size:40px;font-weight:bold;font-family:Roman times;")
        self.resign_hint.setGeometry(170, 20, 180, 35)

        self.user_name_hint_resign = QLabel(self.manage_frame2)
        self.user_name_hint_resign.setText('账号:')
        self.user_name_hint_resign.setStyleSheet("font-size:30px;font-weight:bold;font-family:Roman times;")
        self.user_name_hint_resign.setGeometry(100, 100, 150, 30)
        self.user_name_text_resign = QLineEdit(self.manage_frame2)
        self.user_name_text_resign.setGeometry(220, 100, 200, 30)
        self.user_name_text_resign.setClearButtonEnabled(True)
        self.user_name_text_resign.setPlaceholderText("请设置用户名")

        self.user_code_hint_resign = QLabel(self.manage_frame2)
        self.user_code_hint_resign.setText('密码:')
        self.user_code_hint_resign.setStyleSheet("font-size:30px;font-weight:bold;font-family:Roman times;")
        self.user_code_hint_resign.setGeometry(100, 150, 150, 30)
        self.user_code_text_resign = QLineEdit(self.manage_frame2)
        self.user_code_text_resign.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.user_code_text_resign.setClearButtonEnabled(True)
        self.user_code_text_resign.setGeometry(220, 150, 200, 30)
        self.user_code_text_resign.setPlaceholderText("请设置密码")

        self.user_code2_hint_resign = QLabel(self.manage_frame2)
        self.user_code2_hint_resign.setText('确认密码:')
        self.user_code2_hint_resign.setStyleSheet("font-size:30px;font-weight:bold;font-family:Roman times;")
        self.user_code2_hint_resign.setGeometry(35, 200, 150, 30)
        self.user_code2_text_resign = QLineEdit(self.manage_frame2)
        self.user_code2_text_resign.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.user_code2_text_resign.setClearButtonEnabled(True)
        self.user_code2_text_resign.setGeometry(220, 200, 200, 30)
        self.user_code2_text_resign.setPlaceholderText("请再次输入密码")

        self.resign_button = QPushButton(self.manage_frame2)
        self.resign_button.setText("注册")
        self.resign_button.setStyleSheet("QPushButton{background-color:lightgreen}"
                                         "QPushButton:hover{color:red}"
                                         "QPushButton{border-radius:6px}"
                                         "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                         "QPushButton{font-size:30px}"
                                         )
        self.resign_button.setGeometry(150, 270, 200, 50)
        self.resign_button.clicked.connect(self.click_resign_fun)

        self.error_hint_resign = QLabel(self.manage_frame2)
        self.error_hint_resign.setGeometry(200, 220, 200, 50)
        self.error_hint_resign.setStyleSheet("font-size:20px;color:red;font-weight:bold;font-family:Roman times;")

        # 把两个布局界面放进去
        self.stacked_layout.addWidget(self.manage_frame1)
        self.stacked_layout.addWidget(self.manage_frame2)

    def click_log_win(self):  # 切换到登录窗口的按钮函数
        self.error_hint_login.clear()
        self.error_hint_resign.clear()
        if self.stacked_layout.currentIndex() != 0:
            self.stacked_layout.setCurrentIndex(0)

    def click_resign_win(self):  # 切换到注册窗口的按钮函数
        self.error_hint_login.clear()
        self.error_hint_resign.clear()
        if self.stacked_layout.currentIndex() != 1:
            self.stacked_layout.setCurrentIndex(1)

    def click_login_fun(self):  # 登录按钮
        self.data_class = data_pro()
        self.get_user_name = self.user_name_text.text()
        self.get_user_code = self.user_code_text.text()
        self.all_user_name = self.data_class.username_check()
        self.all_user_code = self.data_class.usercode_check()
        if self.get_user_name in self.all_user_name:
            if self.get_user_code == self.all_user_code[self.all_user_name.index(self.get_user_name)]:
                self.error_hint_login.setText("登录成功")
                self.accept()
            else:
                self.error_hint_login.setText("密码错误")
        else:
            self.error_hint_login.setText("用户名不存在")

    def click_resign_fun(self):  # 注册按钮
        self.data_class = data_pro()
        self.get_user_name_resign = self.user_name_text_resign.text()
        self.get_user_code_resign = self.user_code_text_resign.text()
        self.get_user_code2_resign = self.user_code2_text_resign.text()
        self.all_user_name_resign = self.data_class.username_check()
        if len(self.get_user_name_resign) == 0 or len(self.get_user_code_resign) == 0 or len(
                self.get_user_code2_resign) == 0:
            self.error_hint_resign.setText("输入有误！")
        elif self.get_user_name_resign in self.all_user_name_resign:
            self.error_hint_resign.setText("用户名已存在")
        elif not self.get_user_code_resign == self.get_user_code2_resign:
            self.error_hint_resign.setText("密码不一致")
        else:
            self.error_hint_resign.setText("注册成功!")
            self.new_username = self.get_user_name_resign
            self.new_usercode = self.get_user_code_resign
            self.data_class.userdata_write(self.new_username, self.new_usercode)


class main_window(QMainWindow):  # 软件主界面
    def __init__(self):
        super().__init__()
        self.information_generate_stack = None
        self.statusBar = QStatusBar()
        self.statusBar.showMessage("欢迎使用二次作业智能辅助系统！", 5000)
        self.statusBar.setFont(QFont("NSimSong", 15))
        self.statusBar.setFixedHeight(50)
        self.setStatusBar(self.statusBar)

        self.initui()

    def initui(self):  # 初始化ui
        self.setGeometry(0, 0, 1920, 1080)
        self.main_frame_sidebar_initui()

        # 添加堆叠界面
        self.terminal_inquire_stack = QWidget()
        self.terminal_recognize_stack = QWidget()
        self.terminal_input_stack = QWidget()
        self.terminal_index_stack = QWidget()
        self.fault_assisted_solve_stack = QWidget()
        self.information_generate_stack = QWidget()

        # 设置界面里的内容
        self.terminal_inquire_stack_initui()
        self.terminal_recognize_stack_initui()
        self.terminal_index_stack_initui()
        self.fault_assisted_solve_stack_initui()
        self.information_generate_stack_initui()

        self.main_stack = QStackedWidget(self)

        self.main_stack.addWidget(self.terminal_index_stack)
        self.main_stack.addWidget(self.terminal_recognize_stack)
        self.main_stack.addWidget(self.information_generate_stack)
        self.main_stack.addWidget(self.fault_assisted_solve_stack)
        self.main_stack.addWidget(self.terminal_inquire_stack)

        self.main_stack.setCurrentIndex(0)

        self.main_stack.setGeometry(200, 100, 1720, 930)

    def main_frame_sidebar_initui(self):  # 全局侧边栏
        self.main_stack_locate_area = QFrame(self)
        self.main_stack_locate_area.setGeometry(0, 100, 200, 930)
        self.main_stack_locate_area.setStyleSheet('background-color:#339ca3')

        self.main_stack_hint_area = QFrame(self)
        self.main_stack_hint_area.setGeometry(0, 0, 1920, 100)
        self.main_stack_hint_area.setStyleSheet('background-color:#216e73')

        self.main_stack_logo_area = QLabel(self)
        self.main_stack_logo_area.setScaledContents(True)
        self.main_stack_logo_area.setGeometry(50, 0, 100, 100)
        self.main_stack_logo_area.setStyleSheet('background-color:#216e73')
        self.main_stack_logo_area.setPixmap(QPixmap('电网logo.png'))

        self.main_stack_hint = QLabel('二次作业智能辅助系统', self)
        self.main_stack_hint.setFont(QFont('STZhongsong', 30, QFont.Bold))
        self.main_stack_hint.setStyleSheet('background-color:#216e73;color:#ffffff')
        self.main_stack_hint.setGeometry(300, 0, 1620, 100)

        self.main_stack_button1 = QPushButton(self)
        self.main_stack_button1.setText('首页')
        self.main_stack_button1.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.main_stack_button1.setStyleSheet("QPushButton{background-color:orange}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button1.setGeometry(0, 150, 200, 100)
        self.main_stack_button1.clicked.connect(self.stack_change_index)

        self.main_stack_button2 = QPushButton(self)
        self.main_stack_button2.setText('图实一致核查')
        self.main_stack_button2.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.main_stack_button2.setStyleSheet("QPushButton{color:#ffffff}"
                                              "QPushButton{background-color:#339ca3}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button2.setGeometry(0, 250, 200, 100)
        self.main_stack_button2.clicked.connect(self.stack_change_recognize)

        self.main_stack_button3 = QPushButton(self)
        self.main_stack_button3.setText('作业文本生成')
        self.main_stack_button3.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.main_stack_button3.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button3.setGeometry(0, 350, 200, 100)
        self.main_stack_button3.clicked.connect(self.stack_change_generate)

        self.main_stack_button4 = QPushButton(self)
        self.main_stack_button4.setText('故障诊断')
        self.main_stack_button4.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.main_stack_button4.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button4.setGeometry(0, 450, 200, 100)
        self.main_stack_button4.clicked.connect(self.stack_change_fas)

        self.main_stack_button5 = QPushButton(self)
        self.main_stack_button5.setText('图纸查询')
        self.main_stack_button5.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.main_stack_button5.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button5.setGeometry(0, 550, 200, 100)
        self.main_stack_button5.clicked.connect(self.stack_change_inquire)

    def terminal_index_stack_initui(self):  # 端子号索引界面
        self.terminal_index_stack_substation_area = QLabel(self.terminal_index_stack)
        self.terminal_index_stack_substation_area.setStyleSheet('border:2px solid #339ca3;border-radius:10px')
        self.terminal_index_stack_substation_area.setGeometry(50, 50, 260, 850)

        self.terminal_index_stack_substation_hint = QLabel('变电站', self.terminal_index_stack)
        self.terminal_index_stack_substation_hint.setAlignment(Qt.AlignCenter)
        self.terminal_index_stack_substation_hint.setStyleSheet(
            'background-color:#339ca3;border-radius:10px;color:white')
        self.terminal_index_stack_substation_hint.setFont(QFont('Microsoft YaHei', 20, QFont.Bold))

        self.terminal_index_stack_substation_hint.setGeometry(50, 50, 260, 75)

        self.substation_button1 = QPushButton(self.terminal_index_stack)
        self.substation_button1.setText('石北站')
        self.substation_button1.setStyleSheet("QPushButton{background-color:lightblue}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton{border-radius:6px}"
                                              "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                              "QPushButton{font-size:20px}"
                                              )

        self.substation_button2 = QPushButton(self.terminal_index_stack)
        self.substation_button2.setText('辛集站')
        self.substation_button2.setStyleSheet("QPushButton{background-color:lightblue}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton{border-radius:6px}"
                                              "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                              "QPushButton{font-size:20px}"
                                              )

        self.substation_button3 = QPushButton(self.terminal_index_stack)
        self.substation_button3.setText('辛安站')
        self.substation_button3.setStyleSheet("QPushButton{background-color:lightblue}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton{border-radius:6px}"
                                              "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                              "QPushButton{font-size:20px}"
                                              )

        self.substation_button4 = QPushButton(self.terminal_index_stack)
        self.substation_button4.setText('冶陶站')
        self.substation_button4.setStyleSheet("QPushButton{background-color:lightblue}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton{border-radius:6px}"
                                              "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                              "QPushButton{font-size:20px}"
                                              )

        self.substation_button5 = QPushButton(self.terminal_index_stack)
        self.substation_button5.setText('彭村站')
        self.substation_button5.setStyleSheet("QPushButton{background-color:lightblue}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton{border-radius:6px}"
                                              "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                              "QPushButton{font-size:20px}"
                                              )

        self.substation_button6 = QPushButton(self.terminal_index_stack)
        self.substation_button6.setText('宗州站')
        self.substation_button6.setStyleSheet("QPushButton{background-color:lightblue}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton{border-radius:6px}"
                                              "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                              "QPushButton{font-size:20px}"
                                              )

        self.substation_button7 = QPushButton(self.terminal_index_stack)
        self.substation_button7.setText('武邑站')
        self.substation_button7.setStyleSheet("QPushButton{background-color:lightblue}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton{border-radius:6px}"
                                              "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                              "QPushButton{font-size:20px}"
                                              )

        self.substation_button8 = QPushButton(self.terminal_index_stack)
        self.substation_button8.setText('沧西站')
        self.substation_button8.setStyleSheet("QPushButton{background-color:lightblue}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton{border-radius:6px}"
                                              "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                              "QPushButton{font-size:20px}"
                                              )

        self.substation_button9 = QPushButton(self.terminal_index_stack)
        self.substation_button9.setText('宣惠河站')
        self.substation_button9.setStyleSheet("QPushButton{background-color:lightblue}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton{border-radius:6px}"
                                              "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                              "QPushButton{font-size:20px}"
                                              )

        self.substation_button10 = QPushButton(self.terminal_index_stack)
        self.substation_button10.setText('赢洲站')
        self.substation_button10.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button11 = QPushButton(self.terminal_index_stack)
        self.substation_button11.setText('慈云站')
        self.substation_button11.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button12 = QPushButton(self.terminal_index_stack)
        self.substation_button12.setText('易水站')
        self.substation_button12.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button13 = QPushButton(self.terminal_index_stack)
        self.substation_button13.setText('保定站')
        self.substation_button13.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button1.setGeometry(70, 150, 100, 45)
        self.substation_button2.setGeometry(70, 200, 100, 45)
        self.substation_button3.setGeometry(70, 250, 100, 45)
        self.substation_button4.setGeometry(70, 300, 100, 45)
        self.substation_button5.setGeometry(70, 350, 100, 45)
        self.substation_button6.setGeometry(70, 400, 100, 45)
        self.substation_button7.setGeometry(70, 450, 100, 45)
        self.substation_button8.setGeometry(70, 500, 100, 45)
        self.substation_button9.setGeometry(70, 550, 100, 45)
        self.substation_button10.setGeometry(70, 600, 100, 45)
        self.substation_button11.setGeometry(70, 650, 100, 45)
        self.substation_button12.setGeometry(70, 700, 100, 45)
        self.substation_button13.setGeometry(70, 750, 100, 45)

        self.substation_button14 = QPushButton(self.terminal_index_stack)
        self.substation_button14.setText('桂山')
        self.substation_button14.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button15 = QPushButton(self.terminal_index_stack)
        self.substation_button15.setText('元氏站')
        self.substation_button15.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button16 = QPushButton(self.terminal_index_stack)
        self.substation_button16.setText('蔺河站')
        self.substation_button16.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button17 = QPushButton(self.terminal_index_stack)
        self.substation_button17.setText('管路站')
        self.substation_button17.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button18 = QPushButton(self.terminal_index_stack)
        self.substation_button18.setText('广元站')
        self.substation_button18.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button19 = QPushButton(self.terminal_index_stack)
        self.substation_button19.setText('卧牛城站')
        self.substation_button19.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button20 = QPushButton(self.terminal_index_stack)
        self.substation_button20.setText('深州站')
        self.substation_button20.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button21 = QPushButton(self.terminal_index_stack)
        self.substation_button21.setText('黄骅站')
        self.substation_button21.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button22 = QPushButton(self.terminal_index_stack)
        self.substation_button22.setText('东光站')
        self.substation_button22.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button23 = QPushButton(self.terminal_index_stack)
        self.substation_button23.setText('保北站')
        self.substation_button23.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button24 = QPushButton(self.terminal_index_stack)
        self.substation_button24.setText('清苑站')
        self.substation_button24.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button25 = QPushButton(self.terminal_index_stack)
        self.substation_button25.setText('廉州站')
        self.substation_button25.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button26 = QPushButton(self.terminal_index_stack)
        self.substation_button26.setText('邢台站')
        self.substation_button26.setStyleSheet("QPushButton{background-color:lightblue}"
                                               "QPushButton:hover{color:red}"
                                               "QPushButton{border-radius:6px}"
                                               "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"
                                               "QPushButton{font-size:20px}"
                                               )

        self.substation_button14.setGeometry(190, 150, 100, 45)
        self.substation_button15.setGeometry(190, 200, 100, 45)
        self.substation_button16.setGeometry(190, 250, 100, 45)
        self.substation_button17.setGeometry(190, 300, 100, 45)
        self.substation_button18.setGeometry(190, 350, 100, 45)
        self.substation_button19.setGeometry(190, 400, 100, 45)
        self.substation_button20.setGeometry(190, 450, 100, 45)
        self.substation_button21.setGeometry(190, 500, 100, 45)
        self.substation_button22.setGeometry(190, 550, 100, 45)
        self.substation_button23.setGeometry(190, 600, 100, 45)
        self.substation_button24.setGeometry(190, 650, 100, 45)
        self.substation_button25.setGeometry(190, 700, 100, 45)
        self.substation_button26.setGeometry(190, 750, 100, 45)

        self.substation_button1.setFont(QFont('微软雅黑'))
        self.substation_button2.setFont(QFont('微软雅黑'))
        self.substation_button3.setFont(QFont('微软雅黑'))
        self.substation_button4.setFont(QFont('微软雅黑'))
        self.substation_button5.setFont(QFont('微软雅黑'))
        self.substation_button6.setFont(QFont('微软雅黑'))
        self.substation_button7.setFont(QFont('微软雅黑'))
        self.substation_button8.setFont(QFont('微软雅黑'))
        self.substation_button9.setFont(QFont('微软雅黑'))
        self.substation_button10.setFont(QFont('微软雅黑'))
        self.substation_button11.setFont(QFont('微软雅黑'))
        self.substation_button12.setFont(QFont('微软雅黑'))
        self.substation_button13.setFont(QFont('微软雅黑'))
        self.substation_button14.setFont(QFont('微软雅黑'))
        self.substation_button15.setFont(QFont('微软雅黑'))
        self.substation_button16.setFont(QFont('微软雅黑'))
        self.substation_button17.setFont(QFont('微软雅黑'))
        self.substation_button18.setFont(QFont('微软雅黑'))
        self.substation_button19.setFont(QFont('微软雅黑'))
        self.substation_button20.setFont(QFont('微软雅黑'))
        self.substation_button21.setFont(QFont('微软雅黑'))
        self.substation_button22.setFont(QFont('微软雅黑'))
        self.substation_button23.setFont(QFont('微软雅黑'))
        self.substation_button24.setFont(QFont('微软雅黑'))
        self.substation_button25.setFont(QFont('微软雅黑'))
        self.substation_button26.setFont(QFont('微软雅黑'))

        self.terminal_index_stack_map_area = QLabel(self.terminal_index_stack)
        self.terminal_index_stack_map_area.setGeometry(380, 50, 800, 550)
        self.terminal_index_stack_map_area.setScaledContents(True)
        self.terminal_index_stack_map_area.setPixmap(QPixmap('中心图.png'))
        self.terminal_index_stack_map_area.setStyleSheet('border:1px solid #339ca3')

        self.info_area_fault_hint = QLabel('  缺陷信息', self.terminal_index_stack)
        self.info_area_fault_hint.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.info_area_fault_hint.setStyleSheet('background-color:#339ca3;color:white')
        self.info_area_fault_hint.setGeometry(1255, 50, 400, 50)

        self.info_area_fault = QTextEdit(self.terminal_index_stack)
        self.info_area_fault.setReadOnly(True)
        self.info_area_fault.setGeometry(1255, 100, 400, 350)
        self.info_area_fault.setStyleSheet('border:1px solid #339ca3')
        self.info_area_fault.setFont(QFont('Microsoft YaHei', 10))
        self.info_area_fault.setText('缺陷1：石北站：2021年4月12日10时27分53秒报忻石1线控制回路断线')

        self.info_area_fault_hint = QLabel('  跳闸信息', self.terminal_index_stack)
        self.info_area_fault_hint.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.info_area_fault_hint.setStyleSheet('background-color:#339ca3;color:white')
        self.info_area_fault_hint.setGeometry(1255, 500, 400, 50)

        self.info_area_else = QTextEdit(self.terminal_index_stack)
        self.info_area_else.setReadOnly(True)
        self.info_area_else.setGeometry(1255, 550, 400, 350)
        self.info_area_else.setStyleSheet('border:1px solid #339ca3')
        self.info_area_else.setFont(QFont('Microsoft YaHei', 10))
        self.info_area_else.setText('石北站：2021年4月12日10时27分报忻石I线PCS931线路保护动作')

        self.info_area_cur_fix_hint = QLabel('  当前检修工作', self.terminal_index_stack)
        self.info_area_cur_fix_hint.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.info_area_cur_fix_hint.setStyleSheet('background-color:#339ca3;color:white')
        self.info_area_cur_fix_hint.setGeometry(380, 650, 800, 50)

        self.info_area_cur_fix = QTextEdit(self.terminal_index_stack)
        self.info_area_cur_fix.setReadOnly(True)
        self.info_area_cur_fix.setGeometry(380, 700, 800, 200)
        self.info_area_cur_fix.setStyleSheet('border:1px solid #339ca3')
        self.info_area_cur_fix.setFont(QFont('Microsoft YaHei', 10))
        self.info_area_cur_fix.setText('石北站：2021年4月12日忻石I线保护检验')

    def terminal_recognize_stack_initui(self):  # 端子号识别界面
        self.terminal_recognize_substation_box = QComboBox(self.terminal_recognize_stack)
        self.terminal_recognize_substation_box.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.terminal_recognize_substation_box.setStyleSheet("border-radius:10px;border:2px solid black")
        self.terminal_recognize_substation_item_list = self.combobox_item_changed('substation')
        self.terminal_recognize_substation_box.addItems(self.terminal_recognize_substation_item_list)
        self.terminal_recognize_substation_box.setStatusTip("选择变电站")
        self.terminal_recognize_substation_box.setGeometry(50, 50, 250, 75)

        # 添加一个电压选择框
        self.terminal_recognize_voltage_box = QComboBox(self.terminal_recognize_stack)
        self.terminal_recognize_voltage_box.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.terminal_recognize_voltage_box.setStyleSheet("border-radius:10px;border:2px solid black")
        self.terminal_recognize_voltage_box.setStatusTip("选择电压类型")
        self.terminal_recognize_voltage_item_list = self.combobox_item_changed('voltage')
        self.terminal_recognize_voltage_box.addItems(self.terminal_recognize_voltage_item_list)
        self.terminal_recognize_voltage_box.activated.connect(self.recognize_voltage_box_changed)
        self.terminal_recognize_voltage_box.setGeometry(350, 50, 200, 75)

        # 添加一个下拉框选择要查询的号码索引
        self.terminal_recognize_index_box = QComboBox(self.terminal_recognize_stack)
        self.terminal_recognize_index_box.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.terminal_recognize_index_box.setStatusTip("选择二次回路类型")
        self.terminal_recognize_index_box.setStyleSheet("border-radius:10px;border:2px solid black")
        # self.terminal_recognize_index_box.addItem('忻石一线间隔')
        self.terminal_recognize_index_box.setGeometry(600, 50, 250, 75)
        self.terminal_recognize_index_box.activated.connect(self.recognize_index_box_changed)

        self.terminal_recognize_interval_name = QComboBox(self.terminal_recognize_stack)
        self.terminal_recognize_interval_name.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.terminal_recognize_interval_name.setStyleSheet("border-radius:10px;border:2px solid black")
        self.terminal_recognize_interval_name.setGeometry(900, 50, 250, 75)
        # self.terminal_recognize_interval_name.addItem('线路保护1')
        self.terminal_recognize_interval_name.activated.connect(self.recognize_interval_box_changed)

        self.terminal_recognize_side_box = QComboBox(self.terminal_recognize_stack)
        self.terminal_recognize_side_box.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.terminal_recognize_side_box.setStyleSheet("border-radius:10px;border:2px solid black")
        self.terminal_recognize_side_box.setGeometry(1200, 50, 250, 75)
        self.terminal_recognize_side_box.activated.connect(self.set_standard_number)

        self.terminal_recognize_camera_button = QPushButton(self.terminal_recognize_stack)
        self.terminal_recognize_camera_button.setText("打开相机")
        self.terminal_recognize_camera_button.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.terminal_recognize_camera_button.clicked.connect(self.recognize_open_camera)
        self.terminal_recognize_camera_button.setStyleSheet("QPushButton{background-color:lightblue}"
                                                            "QPushButton{color:#ffffff}"
                                                            "QPushButton{border:1px solid black}"
                                                            "QPushButton{border-radius:10px}"
                                                            "QPushButton:hover{color:red}"
                                                            "QPushButton:pressed{background-color:orange;border: None;}")
        self.terminal_recognize_camera_button.setGeometry(50, 175, 200, 75)

        self.terminal_recognize_photo_button = QPushButton(self.terminal_recognize_stack)
        self.terminal_recognize_photo_button.setText("拍摄图片")
        self.terminal_recognize_photo_button.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.terminal_recognize_photo_button.clicked.connect(self.recognize_take_photo)
        self.terminal_recognize_photo_button.setStyleSheet("QPushButton{background-color:gray}"
                                                           "QPushButton{color:#ffffff}"
                                                           "QPushButton{border:1px solid black}"
                                                           "QPushButton{border-radius:10px}"
                                                           "QPushButton:hover{color:red}"
                                                           "QPushButton:pressed{background-color:orange;border: None;}")
        self.terminal_recognize_photo_button.setEnabled(False)
        self.terminal_recognize_photo_button.setGeometry(300, 175, 200, 75)

        self.terminal_recognize_select_button = QPushButton(self.terminal_recognize_stack)
        self.terminal_recognize_select_button.setText("选择图片")
        self.terminal_recognize_select_button.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.terminal_recognize_select_button.clicked.connect(self.open_file_fun)
        self.terminal_recognize_select_button.setStyleSheet("QPushButton{background-color:green}"
                                                            "QPushButton{color:#ffffff}"
                                                            "QPushButton{border:1px solid black}"
                                                            "QPushButton{border-radius:10px}"
                                                            "QPushButton:hover{color:red}"
                                                            "QPushButton:pressed{background-color:orange;border: None;}")
        self.terminal_recognize_select_button.setGeometry(550, 175, 200, 75)

        self.terminal_recognize_picture_area_hint = QLabel('现场接线:', self.terminal_recognize_stack)
        self.terminal_recognize_picture_area_hint.setFont(QFont('Microsoft YaHei', 15))
        self.terminal_recognize_picture_area_hint.setGeometry(50, 250, 200, 50)

        # 添加待识别图片显示区域
        self.terminal_recognize_picture_area = QLabel(self.terminal_recognize_stack)
        self.terminal_recognize_picture_area.setScaledContents(True)
        self.terminal_recognize_picture_area.setStyleSheet("border: 2px dashed black")
        self.terminal_recognize_picture_area.setGeometry(50, 300, 640, 360)

        # 开始识别按钮
        self.terminal_recognize_button = QPushButton(self.terminal_recognize_stack)
        self.terminal_recognize_button.setText("开始比对")
        self.terminal_recognize_button.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.terminal_recognize_button.setStyleSheet("QPushButton{background-color:lightblue}"
                                                     "QPushButton{color:#ffffff}"
                                                     "QPushButton{border:1px solid black}"
                                                     "QPushButton{border-radius:10px}"
                                                     "QPushButton:hover{color:red}"
                                                     "QPushButton:pressed{background-color:orange;border: None;}")
        self.terminal_recognize_button.clicked.connect(self.terminal_recognize_start)
        self.terminal_recognize_button.setGeometry(760, 380, 200, 75)

        self.recognize_result_hint = QLabel('图纸基准:', self.terminal_recognize_stack)
        self.recognize_result_hint.setFont(QFont('微软雅黑', 15))
        self.recognize_result_hint.setGeometry(1030, 250, 590, 50)

        # 添加识别结果区域
        self.recognize_result = QTextEdit(self.terminal_recognize_stack)
        # self.recognize_result=QTextEdit(self.terminal_recognize_stack)
        self.recognize_result.setStyleSheet("border: 2px solid black")
        self.recognize_result.setGeometry(1030, 300, 590, 360)

        # 错误区域
        self.recognize_error_sum = QTextEdit(self.terminal_recognize_stack)
        self.recognize_error_sum.setStyleSheet("border: 2px solid black")
        self.recognize_error_sum.setFont(QFont('微软雅黑', 15))
        self.recognize_error_sum.setGeometry(50, 710, 1570, 200)
        self.recognize_error_sum.setText("""<table border="1">
								<tr>
								<td bgcolor='green'width='200'>序号</td>
								<td bgcolor='green' width='500'>错误类型</td>
								<td bgcolor='green' width='230'>端子排号</td>
								<td bgcolor='green' width='300'>端子排线号</td>
								<td bgcolor='green' width='300'>图纸线号</td>
								</tr>
								</table>
								""")

    def fault_assisted_solve_stack_initui(self):  # 故障辅助决策页面
        self.fas_stack_frame = QStackedWidget(self.fault_assisted_solve_stack)
        self.fas_stack_frame1 = QWidget()
        self.fas_stack_frame2 = QWidget()
        self.fas_stack_frame.addWidget(self.fas_stack_frame1)
        self.fas_stack_frame.addWidget(self.fas_stack_frame2)
        self.frame_tool = QFrame(self.fault_assisted_solve_stack)
        self.frame_tool.setGeometry(50, 200, 510, 75)
        self.frame_tool.setFrameShape(QFrame.Panel)
        self.frame_tool.setFrameShadow(QFrame.Raised)

        self.fas_frame_button1 = QToolButton(self.frame_tool)
        self.fas_frame_button1.setCheckable(True)
        self.fas_frame_button1.setText("失压继电器回路")
        self.fas_frame_button1.resize(250, 75)
        self.fas_frame_button1.setStyleSheet("QToolButton{background-color:green;color:#ffffff;}"
                                             "QToolButton:hover{color:red}"
                                             "QToolButton:pressed{background-color:orange;border:2px solid black;}"
                                             "QToolButton{font-size:30px}"
                                             )
        self.fas_frame_button1.clicked.connect(self.fas_stack_change1)
        self.fas_frame_button1.setAutoRaise(True)

        self.fas_frame_button2 = QToolButton(self.frame_tool)
        self.fas_frame_button2.setCheckable(True)
        self.fas_frame_button2.setText("失压信号回路")
        self.fas_frame_button2.resize(250, 75)
        self.fas_frame_button2.setStyleSheet("QToolButton{background-color:green;color:#ffffff}"
                                             "QToolButton:hover{color:red}"
                                             "QToolButton:pressed{background-color:orange;border:2px solid black;}"
                                             "QToolButton{font-size:30px}"
                                             )
        self.fas_frame_button2.move(self.fas_frame_button1.width() + 10, 0)
        self.fas_frame_button2.clicked.connect(self.fas_stack_change2)
        self.fas_frame_button2.setAutoRaise(True)

        self.btn_group = QButtonGroup(self.frame_tool)
        self.btn_group.addButton(self.fas_frame_button1, 1)
        self.btn_group.addButton(self.fas_frame_button2, 2)

        self.fault_assisted_solve_stack_hint1 = QLabel('当前缺陷:', self.fault_assisted_solve_stack)
        self.fault_assisted_solve_stack_hint1.setFont(QFont("微软雅黑", 18))
        self.fault_assisted_solve_stack_hint1.setStyleSheet('background-color:green;color:white;border:2px solid black')
        self.fault_assisted_solve_stack_hint1.setGeometry(50, 25, 200, 50)

        self.fault_assisted_solve_stack_hint2 = QLabel('故障定位:', self.fault_assisted_solve_stack)
        self.fault_assisted_solve_stack_hint2.setFont(QFont("微软雅黑", 18))
        self.fault_assisted_solve_stack_hint2.setStyleSheet('background-color:green;color:white;border:2px solid black')
        self.fault_assisted_solve_stack_hint2.setGeometry(50, 100, 200, 50)

        self.current_fault_line = QLineEdit(self.fault_assisted_solve_stack)
        self.current_fault_line.setGeometry(250, 25, 1420, 50)
        self.current_fault_line.setFont(QFont("微软雅黑", 18))
        self.current_fault_line.setStyleSheet('border:2px solid black')
        self.current_fault_line.setText('2021年4月15日9时38分，石北站忻石Ⅰ线PT断线危急缺陷')
        self.current_fault_line.setReadOnly(True)

        self.fault_locate_line = QLineEdit(self.fault_assisted_solve_stack)
        self.fault_locate_line.setGeometry(250, 100, 1420, 50)
        self.fault_locate_line.setFont(QFont("微软雅黑", 18))
        self.fault_locate_line.setStyleSheet('border:2px solid black')
        self.fault_locate_line.setText('电压回路')
        self.fault_locate_line.setReadOnly(True)

        self.fault_demo_area = QLabel(self.fas_stack_frame1)
        self.fault_demo_area.setGeometry(0, 0, 1620, 325)
        self.fault_demo_area.setScaledContents(True)
        self.fault_demo_area.setPixmap(QPixmap('失压继电器回路.png'))

        self.fault_demo_area1 = QLabel(self.fas_stack_frame2)
        self.fault_demo_area1.setGeometry(0, 0, 1620, 325)
        self.fault_demo_area1.setScaledContents(True)
        self.fault_demo_area1.setPixmap(QPixmap('失压信号回路.png'))

        self.voltage_measure = QPushButton(self.fault_assisted_solve_stack)
        self.voltage_measure.setText('测量电压')
        self.voltage_measure.setGeometry(900, 200, 200, 75)
        self.voltage_measure.clicked.connect(self.voltage_measure_fun)

        self.fas_stack_frame.setGeometry(50, 275, 1620, 325)

        self.fault_demo_list_area = QTextEdit(self.fault_assisted_solve_stack)
        self.fault_demo_list_area.setStyleSheet('color:white;border:2px solid black')
        self.fault_demo_list_area.setGeometry(50, 625, 1620, 280)
        self.fault_demo_list_area.setFont(QFont("微软雅黑", 15))
        self.fault_demo_list_area.setText(
            """
								<table border="1">
								<tr>
								<td bgcolor='green'>序号</td>
								<td bgcolor='green'>可能故障点</td>
								<td bgcolor='green'>现象分析</td>
								<td bgcolor='green'>处理方法分析</td>
								</tr>
								<tr>
								<td bgcolor="darkred">1</td>
								<td bgcolor="darkred">继电器损坏</td>
								<td bgcolor="darkred">保护装置正常，后台电压显示正常，后台报文：忻石Ⅰ线线路测控告警信息：忻石Ⅰ线PT断线</td>
								<td bgcolor="darkred">经检查发现为电压互感器端子箱继电器损坏，更换新的继电器后，恢复正常</td>
								</tr>
								<tr>
								<td bgcolor='red'>2</td>
								<td bgcolor='red'>电压空开辅助接点损坏</td>
								<td bgcolor='red'>保护装置正常，继电器无励磁，电压空开合位，后台光子“忻石Ⅰ线PT断线”</td>
								<td bgcolor='red'>经检查发现为保护1电压空开辅助接点损坏，更换新的节点后，恢复正常</td>
								</tr>
								<tr>
								<td bgcolor="pink">3</td>
								<td bgcolor="pink">空开损坏</td>
								<td bgcolor="pink">保护装置正常，后台无B相电压，后台报文：忻石Ⅰ线线路测控告警信息：忻石Ⅰ线电压异常</td>
								<td bgcolor="pink">经检查发现为测量用PT空开B相损坏，更换新空开后，恢复正常</td>
								</tr>
								</table>
										"""
        )

    def information_generate_stack_initui(self):  # 信息生成界面
        self.information_generate_substation_box = QComboBox(self.information_generate_stack)
        self.information_generate_substation_box.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.information_generate_substation_box.setStyleSheet("border-radius:10px;border:2px solid black")
        self.information_generate_substation_item_list = self.combobox_item_changed('substation')
        # self.information_generate_substation_box.addItems(self.information_generate_substation_item_list)
        self.information_generate_substation_box.addItem('石北站')
        self.information_generate_substation_box.setStatusTip("选择变电站与对应文件夹")
        self.information_generate_substation_box.setGeometry(50, 50, 250, 75)

        # 添加一个电压选择框
        self.information_generate_voltage_box = QComboBox(self.information_generate_stack)
        self.information_generate_voltage_box.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.information_generate_voltage_box.setStyleSheet("border-radius:10px;border:2px solid black")
        self.information_generate_voltage_box.setStatusTip("选择电压类型")
        # self.information_generate_voltage_item_list=self.combobox_item_changed('voltage')
        # self.information_generate_voltage_box.addItems(self.information_generate_voltage_item_list)
        self.information_generate_voltage_box.addItem('500KV部分')
        self.information_generate_voltage_box.setGeometry(350, 50, 250, 75)

        # 添加一个下拉框选择要查询的号码索引
        self.information_generate_index_box = QComboBox(self.information_generate_stack)
        self.information_generate_index_box.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.information_generate_index_box.setStatusTip("选择二次回路类型")
        self.information_generate_index_box.setStyleSheet("border-radius:10px;border:2px solid black")
        self.information_generate_index_box.setGeometry(650, 50, 250, 75)
        # self.information_generate_index_item_list=self.combobox_item_changed('index',self.information_generate_voltage_box.currentIndex())
        self.information_generate_index_box.addItem('线路二次线')
        # self.information_generate_index_box.addItems(self.information_generate_index_item_list)

        self.information_generate_interval_name = QComboBox(self.information_generate_stack)
        self.information_generate_interval_name.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.information_generate_interval_name.setStyleSheet("border-radius:10px;border:2px solid black")
        self.information_generate_interval_name.setGeometry(950, 50, 250, 75)
        self.information_generate_interval_name.addItem('忻石一线')

        self.information_generate_wire = QComboBox(self.information_generate_stack)
        self.information_generate_wire.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.information_generate_wire.setStyleSheet("border-radius:10px;border:2px solid black")
        self.information_generate_wire.setGeometry(1250, 50, 250, 75)
        self.information_generate_wire.addItem('线路保护1')

        self.generate_securate_button = QPushButton(self.information_generate_stack)
        self.generate_securate_button.setText('生成二次安全措施票')
        self.generate_securate_button.setStyleSheet("border-radius:20px;background-color:lightblue")
        self.generate_securate_button.setFont(QFont('微软雅黑', 13))
        self.generate_securate_button.setGeometry(150, 200, 240, 75)

        self.generate_standard_card_button = QPushButton(self.information_generate_stack)
        self.generate_standard_card_button.setText('生成标准作业流程卡')
        self.generate_standard_card_button.setStyleSheet("border-radius:20px;background-color:lightblue")
        self.generate_standard_card_button.setGeometry(690, 200, 240, 75)
        self.generate_standard_card_button.setFont(QFont('微软雅黑', 13))

        self.generate_wire_record_button = QPushButton(self.information_generate_stack)
        self.generate_wire_record_button.setText('生成拆线记录')
        self.generate_wire_record_button.setStyleSheet("border-radius:20px;background-color:lightblue")
        self.generate_wire_record_button.setGeometry(1230, 200, 240, 75)
        self.generate_wire_record_button.setFont(QFont('微软雅黑', 13))

        self.generate_securate_area = QLabel(self.information_generate_stack)
        self.generate_securate_area.setStyleSheet('border:2px dashed black')
        self.generate_securate_area.setGeometry(25, 300, 490, 550)
        self.generate_securate_area.setScaledContents(True)
        self.generate_securate_area.setPixmap(QPixmap('安措票.png'))

        self.generate_securate_output = QPushButton(self.information_generate_stack)
        self.generate_securate_output.setText('导出文件')
        self.generate_securate_output.setGeometry(315, 852, 200, 75)
        self.generate_securate_output.setStyleSheet("border-radius:20px;background-color:lightblue")
        self.generate_securate_output.setFont(QFont('微软雅黑', 15))

        self.generate_standard_card_area = QLabel(self.information_generate_stack)
        self.generate_standard_card_area.setStyleSheet('border:2px dashed black')
        self.generate_standard_card_area.setGeometry(565, 300, 490, 550)
        self.generate_standard_card_area.setScaledContents(True)
        self.generate_standard_card_area.setPixmap(QPixmap('标准卡.png'))

        self.generate_standard_card_output = QPushButton(self.information_generate_stack)
        self.generate_standard_card_output.setText('导出文件')
        self.generate_standard_card_output.setGeometry(855, 852, 200, 75)
        self.generate_standard_card_output.setStyleSheet("border-radius:20px;background-color:lightblue")
        self.generate_standard_card_output.setFont(QFont('微软雅黑', 15))

        self.generate_wire_record_area = QLabel(self.information_generate_stack)
        self.generate_wire_record_area.setStyleSheet('border:2px dashed black')
        self.generate_wire_record_area.setGeometry(1105, 300, 490, 550)
        self.generate_wire_record_area.setScaledContents(True)
        self.generate_wire_record_area.setPixmap(QPixmap('拆线记录.png'))

        self.generate_wire_record_output = QPushButton(self.information_generate_stack)
        self.generate_wire_record_output.setText('导出文件')
        self.generate_wire_record_output.setGeometry(1395, 852, 200, 75)
        self.generate_wire_record_output.setStyleSheet("border-radius:20px;background-color:lightblue")
        self.generate_wire_record_output.setFont(QFont('微软雅黑', 15))

    def terminal_inquire_stack_initui(self):  # 图纸查询界面
        # 端子号查询输入框
        self.terminal_inquire_number_input = QLineEdit(self.terminal_inquire_stack)
        self.terminal_inquire_number_input.setClearButtonEnabled(True)
        self.terminal_inquire_number_input.setStyleSheet("border-radius:10px;border:2px solid blue")
        self.terminal_inquire_number_input.setFont(QFont("STKaiti", 20))
        self.terminal_inquire_number_input.setPlaceholderText("请输入查询的图纸名或索引号")
        self.terminal_inquire_number_input.setGeometry(50, 175, 1570, 100)
        # self.terminal_inquire_number_input.textChanged.connect(self.terminal_inquire_input_change)

        self.terminal_inquire_substation_box = QComboBox(self.terminal_inquire_stack)
        self.terminal_inquire_substation_box.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.terminal_inquire_substation_box.setStyleSheet("border-radius:10px;border:2px solid black")
        self.terminal_inquire_substation_item_list = ['石北站', '辛集站', '桂山站', '元氏站', '廉州站', '管路站',
                                                      '辛安站', '蔺河站', '冶陶站', '广元站', '宗州站', '卧牛城站',
                                                      '彭村站', '深州站', '武邑站', '沧西站', '黄骅站', '宣惠河站',
                                                      '瀛州站', '东光站', '保北站', '慈云站', '清苑站', '易水站',
                                                      '保定站', '邢台站']
        self.terminal_inquire_substation_box.addItems(self.terminal_inquire_substation_item_list)
        self.terminal_inquire_substation_box.setStatusTip("选择变电站与对应文件夹")
        # self.terminal_inquire_substation_box.currentIndexChanged.connect(self.terminal_inquire_substation_change)
        self.terminal_inquire_substation_box.setGeometry(50, 50, 355, 75)

        # 添加一个电压选择框
        self.terminal_inquire_voltage_box = QComboBox(self.terminal_inquire_stack)
        self.terminal_inquire_voltage_box.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.terminal_inquire_voltage_box.setStyleSheet("border-radius:10px;border:2px solid black")
        self.terminal_inquire_voltage_box.setStatusTip("选择电压类型")
        # self.terminal_inquire_voltage_box.currentIndexChanged.connect(self.terminal_inquire_voltage_change)
        self.terminal_inquire_voltage_box.setGeometry(455, 50, 355, 75)
        self.terminal_inquire_voltage_box.addItem('500KV')

        # 添加一个下拉框选择要查询的号码索引
        self.terminal_inquire_index_box = QComboBox(self.terminal_inquire_stack)
        self.terminal_inquire_index_box.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.terminal_inquire_index_box.setStatusTip("选择二次回路类型")
        self.terminal_inquire_index_box.setStyleSheet("border-radius:10px;border:2px solid black")
        self.terminal_inquire_index_box.setGeometry(860, 50, 355, 75)
        self.terminal_inquire_index_box.addItem('线路二次线')

        # 更改下拉框则清除输入框内容,并获取相应的图纸列表
        # self.terminal_inquire_index_box.currentIndexChanged.connect(self.terminal_inquire_index_change)

        self.terminal_inquire_interval_name = QComboBox(self.terminal_inquire_stack)
        self.terminal_inquire_interval_name.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        self.terminal_inquire_interval_name.setStyleSheet("border-radius:10px;border:2px solid black")
        self.terminal_inquire_interval_name.setGeometry(1265, 50, 355, 75)
        self.terminal_inquire_interval_name.addItem('忻石一线')

        # 添加一个label用于放置查询结果，双击打开
        self.terminal_inquire_pdf_area = QListWidget(self.terminal_inquire_stack)
        self.terminal_inquire_pdf_area.setFont(QFont("KaiTi", 15))
        self.terminal_inquire_pdf_area.setStyleSheet("border-radius:4px;border:3px solid black")
        self.terminal_inquire_pdf_area.setStatusTip("双击打开查询到的图纸文件")
        self.terminal_inquire_pdf_area.setGeometry(50, 325, 700, 600)
        # self.terminal_inquire_pdf_area.addItems(os.listdir(r'D:\Desktop\pyQT2\terminal\图纸\HZB18W05S-D0201 500KV二次线总的部分'))
        # self.terminal_inquire_pdf_area.itemClicked.connect(self.terminal_inquire_result_clicked)
        # self.terminal_inquire_pdf_area.itemDoubleClicked.connect(self.terminal_inquire_result_double_clicked)

        self.terminal_inquire_pdf_show_area = QLabel(self.terminal_inquire_stack)
        self.terminal_inquire_pdf_show_area.setStyleSheet("border-radius:4px;border:3px solid black")
        self.terminal_inquire_pdf_show_area.setGeometry(800, 325, 800, 600)
        self.terminal_inquire_pdf_show_area.setScaledContents(True)
        self.terminal_inquire_pdf_show_area.setPixmap(QPixmap('pdf.png'))

    def fas_stack_change1(self):
        self.fas_stack_frame.setCurrentIndex(0)

    def fas_stack_change2(self):
        self.fas_stack_frame.setCurrentIndex(1)

    def open_file_fun(self):  # 打开文件函数
        self.open_file_name = QFileDialog.getOpenFileName(self, "请选择要打开的文件", os.getcwd(),
                                                          'Image files (*.png *.jpeg)')
        try:
            shutil.copyfile(self.open_file_name[0], os.getcwd() + r'\photo.png')
        except:
            pass
        self.terminal_recognize_picture_area.setPixmap(QPixmap('photo.png'))

    def terminal_inquire_substation_change(self):  # 当点击选择变电站的时候弹出文件夹选择对话框,此外需要根据选择的文件夹扫描
        self.cur_pdf_dir = QFileDialog.getExistingDirectory(self, "请选择图纸所在文件夹", os.getcwd())
        self.substation_dir = os.listdir(self.cur_pdf_dir)
        self.dir_500KV_list = []
        self.dir_220KV_list = []
        self.dir_35KV_list = []
        for dir_name in self.substation_dir:
            if '500' in dir_name:
                self.dir_500KV_list.append(dir_name)
            elif '220' in dir_name:
                self.dir_220KV_list.append(dir_name)
            elif '35' in dir_name:
                self.dir_35KV_list.append(dir_name)
        self.terminal_inquire_voltage_box.addItem("500KV")
        self.terminal_inquire_voltage_box.addItem("220KV")
        self.terminal_inquire_voltage_box.addItem("35KV")
        self.all_voltage_dir = [self.dir_500KV_list, self.dir_220KV_list, self.dir_35KV_list]

    def terminal_inquire_voltage_change(self):  # 当电压选择下拉框选项发生改变时，改变索引框内的选项
        self.terminal_inquire_index_box.clear()
        self.terminal_inquire_number_input.clear()
        self.terminal_inquire_pdf_area.clear()
        self.index_500_list = ["线路二次线", "断路器二次线", "母线及公用二次线", "主变二次线"]
        self.index_220_list = ["线路二次线", "母联分段二次线", "母线及公用二次线"]
        self.index_35_list = ["电容器二次线", "电抗器二次线", "站变二次线"]
        self.all_index_list = [self.index_500_list, self.index_220_list, self.index_35_list]
        self.terminal_inquire_index_box.addItems(self.all_index_list[self.terminal_inquire_voltage_box.currentRow()])

    def terminal_inquire_index_change(self):  # 索引选择框发生变化时，判断选择的项目，返回相应的文件夹列表
        self.terminal_inquire_number_input.clear()
        self.terminal_inquire_pdf_area.clear()
        try:
            self.cur_voltage_dir = self.all_voltage_dir[self.terminal_inquire_voltage_box.currentRow()]
        except:
            self.terminal_inquire_pdf_area.addItem("查询无结果")
        if self.cur_voltage_dir != []:
            for index_dir_name in self.cur_voltage_dir:
                if '线路二次线' in index_dir_name:
                    self.route_dir = self.cur_pdf_dir + '/' + index_dir_name
                    self.rout_pdf_all = os.listdir(self.route_dir)
                elif '断路器二次线' in index_dir_name:
                    self.breaker_dir = self.cur_pdf_dir + '/' + index_dir_name
                    self.breaker_pdf_all = os.listdir(self.breaker_dir)
                elif '总的部分' in index_dir_name:
                    self.mainpart_dir = self.cur_pdf_dir + '/' + index_dir_name
                    self.mainpart_pdf_all = os.listdir(self.mainpart_dir)
            self.all_dir_path = [self.route_dir, self.breaker_dir, self.mainpart_dir]
            self.all_dir_list = [self.rout_pdf_all, self.breaker_pdf_all, self.mainpart_pdf_all]
            try:
                self.terminal_inquire_pdf_area.addItems(self.all_dir_list[self.terminal_inquire_index_box.currentRow()])
            except:
                pass
        else:
            self.terminal_inquire_pdf_area.addItem("查询无结果")

    def terminal_inquire_input_change(self):  # 输入的内容变化时自动改变结果框中的内容
        self.cur_input = self.terminal_inquire_number_input.text()
        self.terminal_inquire_pdf_area.clear()
        self.result_now = []  # 如果有输入则清空列表
        self.cur_index_all = self.all_dir_list[self.terminal_inquire_index_box.currentRow()]
        for item in self.cur_index_all:
            if self.cur_input in item:
                self.result_now.append(item)
        self.terminal_inquire_pdf_area.addItems(self.result_now)

    def terminal_inquire_result_clicked(self):  # 单击显示要打开的文件，用于校对
        self.cur_open_dir = self.all_dir_path[self.terminal_inquire_index_box.currentRow()]
        # 为了防止在没有输入的情况下点击输出结果产生的错误，这里判断有没有输入
        if self.terminal_inquire_number_input.text() == '':
            self.wait_to_open = self.cur_open_dir + '/' + \
                                self.all_dir_list[self.terminal_inquire_index_box.currentRow()][
                                    self.terminal_inquire_pdf_area.currentRow()]
        else:
            self.wait_to_open = self.cur_open_dir + '/' + self.result_now[self.terminal_inquire_pdf_area.currentRow()]

        self.statusBar.showMessage(self.wait_to_open, 3000)

    def terminal_inquire_result_double_clicked(self):  # 双击打开结果框中的文件
        try:
            os.startfile(self.wait_to_open)
        except Exception as e:
            print(e)

    def combobox_item_changed(self, combobox_name, index=0):  # combobox变化
        self.substation_item_list = ['', '石北站', '辛集站', '桂山站', '元氏站', '廉州站', '管路站', '辛安站', '蔺河站',
                                     '冶陶站', '广元站', '宗州站', '卧牛城站', '彭村站', '深州站', '武邑站', '沧西站',
                                     '黄骅站', '宣惠河站', '瀛州站', '东光站', '保北站', '慈云站', '清苑站', '易水站',
                                     '保定站', '邢台站']
        self.voltage_level_item_list = ['', '500kV部分', '220kV部分', '35kV部分', '主变部分']
        self.index_500kv_item_list = ['', '线路二次线', '断路器二次线', '母线及公用部分']
        self.index_220kv_item_list = ['', '线路二次线', '母联分段二次线', '母线及公用部分']
        self.index_35kv_item_list = ['', '电容器二次线', '电抗器二次线', '站用变二次线']
        self.index_main_item_list = ['', '主变保护二次线', '汇控柜二次线']
        self.voltage_level_all = [self.index_500kv_item_list, self.index_220kv_item_list, self.index_35kv_item_list,
                                  self.index_main_item_list]
        if (combobox_name == 'substation'):
            return self.substation_item_list
        elif (combobox_name == 'voltage'):
            return self.voltage_level_item_list
        elif (combobox_name == 'index'):
            return self.voltage_level_all[index]

    def recognize_open_camera(self):  # 打开相机
        self.timer_camera = QTimer()
        self.timer_camera.timeout.connect(self.show_camera)
        self.cap = cv2.VideoCapture(0)
        if self.terminal_recognize_camera_button.text() == '打开相机':
            self.terminal_recognize_camera_button.setStyleSheet("QPushButton{background-color:orange}"
                                                                "QPushButton{color:#ffffff}"
                                                                "QPushButton{border:1px solid black}"
                                                                "QPushButton{border-radius:10px}"
                                                                "QPushButton:hover{color:red}"
                                                                "QPushButton:pressed{background-color:orange;border: None;}")
            self.terminal_recognize_photo_button.setEnabled(True)
            self.terminal_recognize_photo_button.setStyleSheet("QPushButton{background-color:red}"
                                                               "QPushButton{color:#ffffff}"
                                                               "QPushButton{border-radius:10px}"
                                                               "QPushButton{border:1px solid black}"
                                                               "QPushButton:hover{color:green}"
                                                               "QPushButton:pressed{background-color:orange;border: None;}")
            self.flag = self.cap.open(0)
            if self.flag == False:
                self.msg = QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                               buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
                self.terminal_recognize_camera_button.setText('关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.terminal_recognize_picture_area.clear()
            self.terminal_recognize_camera_button.setText('打开相机')
            self.terminal_recognize_picture_area.setStyleSheet("border: 2px dashed black")
            self.terminal_recognize_photo_button.setEnabled(False)
            self.terminal_recognize_camera_button.setStyleSheet("QPushButton{background-color:lightblue}"
                                                                "QPushButton{color:#ffffff}"
                                                                "QPushButton{border-radius:10px}"
                                                                "QPushButton{border:1px solid black}"
                                                                "QPushButton:hover{color:red}"
                                                                "QPushButton:pressed{background-color:orange;border: None;}")
            self.terminal_recognize_photo_button.setStyleSheet("QPushButton{background-color:gray}"
                                                               "QPushButton{color:#ffffff}"
                                                               "QPushButton{border:1px solid black}"
                                                               "QPushButton{border-radius:10px}"
                                                               "QPushButton:hover{color:red}"
                                                               "QPushButton:pressed{background-color:orange;border: None;}")

    def show_camera(self):  # 展示相片
        self.flag, self.image = self.cap.read()
        self.terminal_recognize_picture_area.setStyleSheet("border: 2px dashed red")
        self.show = cv2.resize(self.image, (640, 480))
        self.show = cv2.cvtColor(self.show, cv2.COLOR_BGR2RGB)
        self.showImage = QImage(self.show.data, 640, 480, QImage.Format_RGB888)
        self.terminal_recognize_picture_area.setPixmap(QPixmap.fromImage(self.showImage))

    def recognize_take_photo(self):  # 拍摄图片
        if self.timer_camera.isActive() == False:
            self.msg = QMessageBox.warning(self, "警告", "请先打开相机", buttons=QMessageBox.Ok,
                                           defaultButton=QMessageBox.Ok)
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.terminal_recognize_camera_button.setText('打开相机')
            cv2.imwrite('photo.png', self.image)
            self.terminal_recognize_picture_area.setPixmap(QPixmap.fromImage(self.showImage))
            self.terminal_recognize_picture_area.setStyleSheet("border: 2px solid black")

    def terminal_recognize_start(self):  # 图片识别按钮函数,放入识别程序实现识别功能，也可以用thread加线程放在后台识别防止前端界面卡死
        with open('photo.png', 'rb') as self.fp:
            self.image = self.fp.read()
        self.results = client.handwriting(self.image)["words_result"]
        self.img = cv2.imread('photo.png')
        self.recognize_result_list = []
        for result in self.results:
            text = result["words"]
            location = result["location"]
            self.recognize_result_list.append(text)
            cv2.rectangle(self.img, (location["left"], location["top"]),
                          (location["left"] + location["width"], location["top"] + location["height"]), (0, 255, 0), 2)
        cv2.imwrite('photo' + "_result.png", self.img)
        # self.number_comprasion(['1K1D','133A/5051/9W-141A','133B/5051/9W-141A','133B/505119W-141A','J31A/505/9W142A','J31B1505719W-142A','J31c/5051/9W-142A'])
        self.number_comprasion(self.recognize_result_list)
        self.terminal_recognize_picture_area.clear()
        self.terminal_recognize_picture_area.setPixmap(QPixmap('photo_result.png'))

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def stack_change_index(self):  # 端子号索引界面切换按钮
        self.main_stack.setCurrentIndex(0)
        self.main_stack_button1.setStyleSheet("QPushButton{background-color:orange}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button2.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button3.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button4.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button5.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")

    def stack_change_recognize(self):  # 端子号识别界面切换按钮
        self.main_stack.setCurrentIndex(1)
        self.main_stack_button1.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button2.setStyleSheet("QPushButton{background-color:orange}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button3.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button4.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button5.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")

    def stack_change_generate(self):  # 信息生成
        self.main_stack.setCurrentIndex(2)
        self.main_stack_button1.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button2.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button3.setStyleSheet("QPushButton{background-color:orange}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button4.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button5.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")

    def stack_change_fas(self):  # 故障辅助决策页面
        self.main_stack.setCurrentIndex(3)
        self.main_stack_button1.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button2.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button3.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button4.setStyleSheet("QPushButton{background-color:orange}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button5.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")

    def stack_change_inquire(self):  # 端子号查询界面切换按钮
        self.main_stack.setCurrentIndex(4)
        self.main_stack_button1.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button2.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button3.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button4.setStyleSheet("QPushButton{background-color:#339ca3}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")
        self.main_stack_button5.setStyleSheet("QPushButton{background-color:orange}"
                                              "QPushButton{color:#ffffff}"
                                              "QPushButton{border:1px solid #339ca3}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton:pressed{background-color:orange;border: None;}")

    def recognize_voltage_box_changed(self):
        self.terminal_recognize_index_box.clear()
        self.terminal_recognize_index_box.addItems(
            self.combobox_item_changed('index', self.terminal_recognize_voltage_box.currentIndex()))

    def recognize_index_box_changed(self):
        self.terminal_recognize_interval_name.clear()
        if self.terminal_recognize_voltage_box.currentIndex() == 1:
            if self.terminal_recognize_index_box.currentIndex() == 1:
                self.terminal_recognize_interval_name.addItems(['', '忻石一线', '忻石二线', '忻石三线', '忻石四线'])
            elif self.terminal_recognize_index_box.currentIndex() == 2:
                self.terminal_recognize_interval_name.addItems(['', '第一串二次线', '第二串二次线', '第三串二次线'])
        if self.terminal_recognize_voltage_box.currentIndex() == 2:
            if self.terminal_recognize_index_box.currentIndex() == 1:
                self.terminal_recognize_interval_name.addItems(['', '201二次线', '203二次线', '204二次线'])
            elif self.terminal_recognize_index_box.currentIndex() == 1:
                self.terminal_recognize_interval_name.addItems(['', '1号电容器', '2号电容器', '3号电容器'])

    def recognize_interval_box_changed(self):
        self.terminal_recognize_side_box.clear()
        self.terminal_recognize_side_box.addItems(['', '左侧端子排', '右侧端子排'])

    def terminal_number_read(self, data_index):
        with open('terminal_number.txt', 'r') as terminal_data:
            self.all_terminal_data_read = terminal_data.readlines()
        self.terminal_row_name = []
        for line in self.all_terminal_data_read:
            self.terminal_row_name.append(line.split(',')[0])
        self.terminal_row_name = list(set(self.terminal_row_name))
        self.all_terminal_data = []
        for i in range(len(self.terminal_row_name)):
            self.all_terminal_data.append([])
        for line in self.all_terminal_data_read:
            self.all_terminal_data[self.terminal_row_name.index(line.split(',')[0])].append(
                line.replace('\n', '').split(',')[2])
        if data_index == 0:
            return self.terminal_row_name
        elif data_index == 1:
            return self.all_terminal_data

    def set_standard_number(self):
        self.html_part = []
        self.terminal_name = self.terminal_number_read(0)[0]
        self.all_number = self.terminal_number_read(1)[0]
        self.html_part.append(
            "<tr><td bgcolor='lightgreen' style='font-size:20pt'>端子排名称</td><td bgcolor='lightgreen' style='font-size:20pt'>端子号</td><td bgcolor='lightgreen' style='font-size:20pt'>线号1</td></tr>")
        for i in range(len(self.all_number)):
            self.html_part.append(
                "<tr><td bgcolor='lightgray' width='200' height='100px' style='font-size:20pt'>" + self.terminal_name + "</td><td bgcolor='lightgray' width='130' height='100px' style='font-size:20pt'>" + str(
                    i + 1) + "</td><td bgcolor='lightgray' width='240' height='100px' style='font-size:20pt'>" +
                self.all_number[i] + '</td></tr>')
        self.recognize_result.setText(''.join(self.html_part))

    def voltage_measure_fun(self):
        self.stack_voltage_hint1 = QLabel('正在连接......', self.fault_assisted_solve_stack)
        self.stack_voltage_hint1.setFont(QFont('微软雅黑', 13))
        self.stack_voltage_hint1.setGeometry(600, 200, 510, 75)
        time.sleep(2)
        self.stack_voltage_hint1.clear()
        self.stack_voltage_hint1.setText('正在测量点位1')
        self.stack_voltage_number1 = QLabel('V1', self.fas_stack_frame1)
        self.stack_voltage_number1.setGeometry(100, 100, 100, 100)

    def number_comprasion(self, pic_number):
        self.recognize_result_hint.setText('比对结果')
        self.html_part = []
        self.all_terminal_name = self.terminal_number_read(0)
        self.all_number = self.terminal_number_read(1)
        self.html_part.append(
            "<tr><td bgcolor='lightgreen' style='font-size:20pt'>端子排名称</td><td bgcolor='lightgreen' style='font-size:20pt'>端子号</td><td bgcolor='lightgreen' style='font-size:20pt'>线号1</td></tr>")
        if pic_number[0].replace(' ', '') in self.all_terminal_name:
            self.file_number = self.all_number[0]
            self.pic_terminal_row = pic_number[0]
            del (pic_number[0])
        for i in range(len(self.file_number)):
            if self.file_number[i] == '/':
                pic_number.insert(i, '/')
        for i in range(len(self.file_number)):
            if self.file_number[i] == '/':
                self.html_part.append(
                    "<tr><td bgcolor='lightgray' width='200' height='100px' style='font-size:20pt'>" + self.pic_terminal_row + "</td><td bgcolor='lightgray' width='130' height='100px' style='font-size:20pt'>" + str(
                        i + 1) + "</td><td bgcolor='lightgray' width='240' height='100px' style='font-size:20pt'>/</td></tr>")
            elif (pic_number[i][0:4].upper() == self.file_number[i]):
                self.html_part.append(
                    "<tr><td bgcolor='lightgray' width='200' height='100px' style='font-size:20pt'>" + self.pic_terminal_row + "</td><td bgcolor='lightgray' width='130' height='100px' style='font-size:20pt'>" + str(
                        i + 1) + "</td><td bgcolor='lightgray' width='240' height='100px' style='font-size:20pt'>" +
                    self.file_number[i] + '</td></tr>')
            else:
                self.html_part.append(
                    "<tr><td bgcolor='red' width='200' height='100px' style='font-size:20pt'>" + self.pic_terminal_row + "</td><td bgcolor='red' width='130' height='100px' style='font-size:20pt'>" + str(
                        i + 1) + "</td><td bgcolor='red'width='240' height='100px' style='font-size:20pt'>" +
                    self.file_number[i] + '</td></tr>')
        self.recognize_result.setText(''.join(self.html_part))
        self.recognize_error_sum.setText(
            """
								<table border="1">
								<tr>
								<td bgcolor='green'width='200'>序号</td>
								<td bgcolor='green' width='500'>错误类型</td>
								<td bgcolor='green' width='230'>端子排号</td>
								<td bgcolor='green' width='300'>端子排线号</td>
								<td bgcolor='green' width='300'>图纸线号</td>
								</tr>
								<tr>
								<td bgcolor='lightgray'>1</td>
								<td bgcolor='lightgray'>打印错误</td>
								<td bgcolor='lightgray'>1K1D3</td>
								<td bgcolor='lightgray'>133B</td>
								<td bgcolor='lightgray'>133C</td>
								</tr>
								</table>
										"""
        )


class data_pro():  # 处理登录信息
    def __init__(self):
        self.data_file = open("userdata.txt", 'r')
        self.data_file_read = self.data_file.readlines()
        self.data_file.close()
        self.all_users = []
        self.all_codes = []
        for data in self.data_file_read:
            self.all_users.append(data.replace('\n', '').split(',')[0])
            self.all_codes.append(data.replace('\n', '').split(',')[1])

    def username_check(self):
        return self.all_users

    def usercode_check(self):
        return self.all_codes

    def userdata_write(self, name, code):
        self.home_dir = str(Path.home())
        self.data_file = open(self.home_dir + 'data.txt', 'w+')
        self.all_users.append(name)
        self.all_codes.append(code)
        for i in range(len(self.all_users)):
            self.data_file.write(self.all_users[i] + ',' + self.all_codes[i] + '\n')
        self.data_file.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = main_window()
    mainwindow.showFullScreen()
    sys.exit(app.exec_())
