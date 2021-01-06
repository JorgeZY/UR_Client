#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/4 15:12
# @Author  : AI001

import struct
import numpy as np
import math
import socket


def client_interface(host, port, info):
    dic = {'MessageSize': 'i', 'Time': 'd', 'q target': '6d', 'qd target': '6d', 'qdd target': '6d', 'I target': '6d',
           'M target': '6d', 'q actual': '6d', 'qd actual': '6d', 'I actual': '6d', 'I control': '6d',
           'Tool vector actual': '6d', 'TCP speed actual': '6d', 'TCP force': '6d', 'Tool vector target': '6d',
           'TCP speed target': '6d', 'Digital input bits': 'd', 'Motor temperatures': '6d', 'Controller Timer': 'd',
           'Test value': 'd', 'Robot Mode': 'd', 'Joint Modes': '6d', 'Safety Mode': 'd', 'empty1': '6d',
           'Tool Accelerometer values': '3d',
           'empty2': '6d', 'Speed scaling': 'd', 'Linear momentum norm': 'd', 'SoftwareOnly': 'd', 'softwareOnly2': 'd',
           'V main': 'd',
           'V robot': 'd', 'I robot': 'd', 'V actual': '6d', 'Digital outputs': 'd', 'Program state': 'd',
           'Elbow position': '3d', 'Elbow velocity': '3d',
           'safety-status': 'd'}

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((host, port))
    msg = sock.recv(1204)

    names = []
    ii = range(len(dic))
    for key, i in zip(dic,ii):
        fmtsize = struct.calcsize(dic[key])
        msg1, msg = msg[0:fmtsize], msg[fmtsize:]
        fmt = "!" + dic[key]
        names.append(struct.unpack(fmt, msg1))
        dic[key] = dic[key], struct.unpack(fmt, msg1)

    # print(names)
    # print(dic)
    a = dic[info]
    a2 = np.array(a[1])
    # joint_position = a2*180/math.pi
    sock.close()
    return a2

# A = client_interface("192.168.253.135", 30013, "Safety Mode")
# print(A)