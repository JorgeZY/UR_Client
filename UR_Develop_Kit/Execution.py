# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/12/31 15:06
# @Author : yi_zeng
# @File : Execution.py

import sys
import math
import socket
import threading
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI import Ui_MainWindow
from client_interface import client_interface


class Functionality(Ui_MainWindow):

    def __init__(self, MainWindow):
        super().__init__()
        self.setupUi(MainWindow)
        self.connect_slot()
        self.server_validator()
        self.PoseButton.setEnabled(False)

    def start_tcp_client(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.sock.setblocking(False)
        try:
            ipText = self.ipLineEdit.text()
            portValue = int(self.portLineEdit.text())
        except:
            print("连接失败，请检查端口号与IP地址！")
            self.SendText.setPlainText("连接失败，请检查端口号与IP地址！")
            self.connectButton.setDisabled(False)
            print(Exception)
        else:
            try:
                self.sock.settimeout(1)
                # test = self.sock.gettimeout()
                self.sock.connect((ipText, portValue))
                self.connectButton.setDisabled(True)
                # client_th = threading.Thread(target=self.tcp_concurrency)
                # position_th = threading.Thread(target=self.get_pose_data)
                # client_th.start()
                # position_th.start()
                print('连接成功！')
                self.PoseButton.setEnabled(True)
            except:
                print("连接失败，请检查端口号与IP地址！")
                self.SendText.setPlainText("连接失败，请检查端口号与IP地址！")

    def get_pose_data(self):
        # while True:
        try:
            ip = self.ipLineEdit.text()
            port = int(self.portLineEdit.text())
            raw_data = client_interface(ip, port, "q actual")
            data = raw_data*180/math.pi
            data0 = float('%.2f' % data[0])
            data1 = float('%.2f' % data[1])
            data2 = float('%.2f' % data[2])
            data3 = float('%.2f' % data[3])
            data4 = float('%.2f' % data[4])
            data5 = float('%.2f' % data[5])

            self.baselink.setText(str(data0))
            self.link2.setText(str(data1))
            self.link3.setText(str(data2))
            self.link4.setText(str(data3))
            self.link5.setText(str(data4))
            self.link6.setText(str(data5))

            raw_data2 = client_interface(ip, port, "Tool vector actual")
            raw_x = raw_data2[0]*1000
            raw_y = raw_data2[1]*1000
            raw_z = raw_data2[2]*1000
            x_data = float('%.2f' % raw_x)
            y_data = float('%.2f' % raw_y)
            z_data = float('%.2f' % raw_z)
            rx_data = float('%.3f' % raw_data2[3])
            ry_data = float('%.3f' % raw_data2[4])
            rz_data = float('%.3f' % raw_data2[5])
            self.xline.setText(str(x_data))
            self.yline.setText(str(y_data))
            self.zline.setText(str(z_data))
            self.rxline.setText(str(rx_data))
            self.ryline.setText(str(ry_data))
            self.rzline.setText(str(rz_data))
        except:
            print("未连接机器人！")
            self.SendText.setPlainText("未连接机器人！")

    def tcp_concurrency(self):
        while True:
            recv_msg = self.sock.recv(1116)
            # self.SendText.toPlainText(recv_msg.decode('hex'))
        pass

    def move_robot(self):
        try:
            if self.comboBox.currentIndex() == 0:
                x_value = float(self.xline.text())/1000
                y_value = float(self.yline.text())/1000
                z_value = float(self.zline.text())/1000
                rx_value = self.rxline.text()
                ry_value = self.ryline.text()
                rz_value = self.rzline.text()
                acc_value = float(self.accLine.text())*math.pi/180
                vel_value = float(self.velLine.text())*math.pi/180
                move_command = "movej(p[%s, %s, %s, %s, %s, %s], a = %s, v = %s)\n" % (str(x_value), str(y_value), str(z_value), rx_value, ry_value, rz_value, str(acc_value), str(vel_value))
                print(move_command)
                self.sock.send(move_command.encode('utf-8'))
            if self.comboBox.currentIndex() == 1:
                x_value = float(self.xline.text())/1000
                y_value = float(self.yline.text())/1000
                z_value = float(self.zline.text())/1000
                rx_value = self.rxline.text()
                ry_value = self.ryline.text()
                rz_value = self.rzline.text()
                acc_value = float(self.accLine.text())/1000
                vel_value = float(self.velLine.text())/1000
                move_command = "movel(p[%s, %s, %s, %s, %s, %s], a = %s, v = %s)\n" % (str(x_value), str(y_value), str(z_value), rx_value, ry_value, rz_value, str(acc_value), str(vel_value))
                print(move_command)
                self.sock.send(move_command.encode('utf-8'))
        except:
            print("未连接机器人！")
            self.SendText.setPlainText("未连接机器人！")

    def reset(self):
        self.SendText.clear()
        self.xline.clear()
        self.yline.clear()
        self.zline.clear()
        self.rxline.clear()
        self.ryline.clear()
        self.rzline.clear()
        self.baselink.clear()
        self.link2.clear()
        self.link3.clear()
        self.link4.clear()
        self.link5.clear()
        self.link6.clear()
        self.accLine.clear()
        self.velLine.clear()

    def tcp_close(self):
        if not self.disconnectButton.isEnabled():
            self.connectButton.setDissabled(False)
        try:
            self.sock.close()
        except AttributeError as a:
            print(a)
        except Exception as e:
            print(e)
        self.connectButton.setDisabled(False)
        self.PoseButton.setDisabled(True)

    def change_move_method(self):
        count = self.comboBox.currentIndex()
        # print(count)
        if count == 1:
            self.label_5.setText('工具速度')
            self.label_29.setText('工具加速')
            self.label_30.setText('mm/s')
            self.label_31.setText('mm/s^2')
        if count == 0:
            self.label_5.setText('关节速度')
            self.label_29.setText('关节加速')
            self.label_30.setText('°/s')
            self.label_31.setText('°/s^2')

    def send_text(self):
        try:
            send_msg = self.SendText.toPlainText() + '\n'
            self.sock.send(send_msg.encode('utf-8'))
        except:
            print("未连接机器人！")
            self.SendText.setPlainText("未连接机器人！")

    def server_validator(self):
        ipValidator = QRegExpValidator(QRegExp('^((2[0-4]\d|25[0-5]|\d?\d|1\d{2})\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$'))
        portValidator = QIntValidator(0, 65536)
        self.ipLineEdit.setValidator(ipValidator)
        self.portLineEdit.setValidator(portValidator)
        self.ipLineEdit.setPlaceholderText("请输入ip")
        self.portLineEdit.setPlaceholderText("端口")

    def connect_slot(self):
        self.connectButton.clicked.connect(self.start_tcp_client)
        self.disconnectButton.clicked.connect(self.tcp_close)
        self.sendButton.clicked.connect(self.send_text)
        self.PoseButton.clicked.connect(self.get_pose_data)
        self.comboBox.activated.connect(self.change_move_method)
        self.moveButton.clicked.connect(self.move_robot)
        self.ResetButton.clicked.connect(self.reset)


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    app.setStyle('WindowsXP')
    mainWindow = Ui_MainWindow()
    ui = Functionality(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())


