# -*- coding: utf-8 -*-
"""
Author : LiYue
Date   : 2022年08月29日 上午 10:00
Project: AAATrackering
IDE    : PyCharm
"""
import sys
import cv2
import serial
import time
import math
import torch
import numpy as np
import pandas as pd
import threading as td
from tracker import KCFTracker
from twomotor import Motor

def TerminalDetect(cap, model):
    global conf, terminal, KCF_flag, stop_flag, frame
    while True:
        stop_flag = 1   # 线程结束标志位
        _, frame = cap.read()   # 读取帧
        t1 = cv2.getTickCount()
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   # yolov5读取图片为RGB格式
        result = model(frame).pandas().xyxy[0]   # 通过hub获取终端的坐标信息，置信度
       # print("result:", result)
        df = pd.DataFrame(result)
        df = df.empty

        if df is False:
            terminal[0] = result['xmin'][0]
            terminal[1] = result['ymin'][0]
            terminal[2] = result['xmax'][0] - result['xmin'][0]
            terminal[3] = result['ymax'][0] - result['ymin'][0]
            conf = round(result['confidence'][0], 3)
            name = str(result['name'][0])
            frame = cv2.rectangle(frame, (int(result['xmin'][0]), int(result['ymin'][0])),
                                (int(result['xmax'][0]), int(result['ymax'][0])), (0, 255, 0), 3)
            frame = cv2.putText(frame, name + ',' + str(conf), (int(result['xmin'][0]) - 5, int(result['ymin'][0])),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            # print('conf的值:', conf)
            
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        t2 = cv2.getTickCount() - t1
        detectfps = int(cv2.getTickFrequency() / t2)

        if conf >= 0.55:
            com1.write(bytearray([0x02, 0xFD, 0x10, 0x00, 0xFF, 0x00, 0x19, 0x00, 0X6B]))    # 电机停止工作
            com2.write(bytearray([0x01, 0xFD, 0x10, 0x00, 0xFF, 0x00, 0x19, 0x00, 0X6B]))
            stop_flag = 0
            break
            cv2.destroyAllWindows()

def MotorScale():
    global counter, angle_base, angle_delta, i, direction, stop_flag
    while True:
        i = round(i, 2) 
        #print("i的值为:", i)
        
        if counter % 2 == 0:
            motor1.control(2, angle_base, direction)  # 控制水平电机1旋转角与方向，发送一次指令
            time.sleep(i)
            
        else:
            motor2.control(1, angle_base, direction)   # 控制垂直电机2旋转角与方向，发送指令（电机脉冲）
            time.sleep(i)

            #print("方向的值为：", direction)
            direction += 1  # 电机旋转方向反转


            angle_base += angle_delta   # 给转台增加一个角度

        if i == 3:
            i = 3
        else:
            i += 0.1

        if direction > 1:
            direction = 0

        counter += 1    # 计数
        if angle_base == 0:
            counter = 0
        # print("counter的值为:", counter)
        
        if stop_flag == 0:
            print("电机扫描结束")
            break

def tracker():
    global frame_old2
    while True:
        _, frame_old1 = cap.read()  # 读取帧
        frame_old2 = cv2.resize(frame_old1, (640, 480))
        frame_old = frame_old2
        timer = cv2.getTickCount()

        bbox, peak_value = tracker.update(frame_old)
        # print('peak_value的值为:',peak_value)
        bbox = list(map(int, bbox))

        p1 = (int(bbox[0]), int(bbox[1]))  # 左上角
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))  # 右下角,
        target_point = (int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2))  # 目标中心点坐标
        # center_point = (320, int(240 + sx))  # 拍摄画面中心点坐标
        # center_point = (320, 240)  # 拍摄画面中心点坐标

        cv2.rectangle(frame_old, p1, p2, (255, 0, 0), 2, 1)  # 画矩形框与点
        cv2.circle(frame_old, target_point, 3, (255, 0, 0), cv2.FILLED)  # 显示目标中心点
        cv2.circle(frame_old, center_point, 3, (0, 255, 0), cv2.FILLED)  # 显示画面中心点
        # cv2.circle(frame_old, a_point, 3, (0, 0, 255), cv2.FILLED)
        loop_time = cv2.getTickCount() - timer
        fps = int(cv2.getTickFrequency() / loop_time)
        cv2.putText(frame_old, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        cv2.imshow("Tracking", frame_old)

        original_x = np.arctan(((abs(center_point[0] - target_point[0])) * dx) / f)  # np.arctan(x/f)
        angle_x = (original_x / math.pi) * 180  # 水平方向需要旋转角度
        angle_x = abs(angle_x)
        # print("水平旋转角度为：", angle_x)

        original_y = np.arctan(((abs(center_point[1] - target_point[1])) * dy) / f)
        angle_y = (original_y / math.pi) * 180  # 垂直方向需要旋转角度
        angle_y = abs(angle_y)
        # print("垂直旋转角度为：", angle_y)

        if (center_point[0] - target_point[0]) > 0:  # 说明目标中心点在中心点左边，电机须向左运动
            direction_x = 1
        else:
            direction_x = 0

        if (center_point[1] - target_point[1]) > 0:  # 说明目标中心点在中心点上方，电机须向上运动
            direction_y = 0
        else:
            direction_y = 1

        if angle_x > 0.1:
            motor1.control(2, angle_x, direction_x)  # 水平
        else:
            motor1.control(2, 0, direction_x)  # 水平

        if angle_y > 0.1:
            motor2.control(1, angle_y, direction_y)  # 垂直
        else:
            motor2.control(1, 0, direction_y)  # 垂直

        if peak_value <= 0.5:
            print("目标跟踪失败，重新进行终端检测！")
            break
        if cv2.waitKey(30) & 0xff == ord('q'):
            print("结束跟踪任务！")
            sys.exit(0)
def fpsdetect():
    global frame_old2, KCF_flag
    g = 0
    while True:
        frame_old = cv2.cvtColor(frame_old2, cv2.COLOR_BGR2RGB)  # yolov5读取图片为RGB格式
        result = model(frame_old).pandas().xyxy[0]  # 通过hub获取终端的坐标信息，置信度
        df = pd.DataFrame(result)
        df = df.empty
        if g == 10:
            if df is False:
                terminal[0] = result['xmin'][0]
                terminal[1] = result['ymin'][0]
                terminal[2] = result['xmax'][0] - result['xmin'][0]
                terminal[3] = result['ymax'][0] - result['ymin'][0]
                conf = round(result['confidence'][0], 3)
                if conf <= 0.65:
                    KCF_flag = False
                    break
        g += 1


if __name__ == '__main__':
    KCF_flag = False  # 首次不进行KCF
    counter = 0

    angle_base = 1   # 第一次转台需要转的角度
    angle_delta = 0.5   # 每次转台需要增加的角度
    direction = 0  # 电机旋转方向
    i = 0.2
    conf = 0.00

    f = 3.6   # 焦距，单位mm
    h = 480
    w = 640 
    a = 81   # 水平视场角q
    b = 50    # 垂直视场角
    l = 71.55    # 相机中心点与激光发射点实际距离，单位：mm
    m = 1190  # 两激光发射点实际距离, 单位：mm

    dx = (2*f*math.tan(a / 2)) / w   # 水平方向像素实际大小
    dy = (2*f*math.tan(b / 2)) / h    # 垂直方向像素实际大小
    # print("单个水平像素值：{0},单个垂直像素值:{1}".format(dx, dy))

    s = (f * l) / (f + m)   # 在平面坐标系中的距离，单位mm
    sx = abs((s / dy) / 4) # 转化为像素坐标系中的距离
    # sx = abs(s / dy)
    # print("像素坐标系中的距离{0}".format(sx))

    cap = cv2.VideoCapture(0)  # 调用摄像头的
    pthfile = r'/home/jetson/.cache/torch/hub/ultralytics_yolov5_master'
    model = torch.hub.load(pthfile, 'custom', path='/home/jetson/Desktop/AAATrackering/KCFTrackering/yolov5/runs/train/exp3/weights/best1.pt', source='local')

    com1 = serial.Serial("/dev/ttyUSB1", 38400, timeout=0.01)  # 设置水平方向电机的串口与波特率，通讯地址为0x02
    com2 = serial.Serial("/dev/ttyUSB0", 38400, timeout=0.01)   # 设置垂直方向电机的串口与波特率,通信地址为0x01
    # com = serial.Serial("/dev/ttyUSB0", 38400)  # 设置水平方向电机的串口与波特率，通讯地址为0x02

    motor1 = Motor(com1)  # 水平方向
    motor2 = Motor(com2)   # 垂直方向
    # motor = Motor(com)
    terminal = [0, 0, 0, 0]

    center_point = (335, int(240 + sx))  # 拍摄画面中心点坐标
    # center_point = (315, 240)
    print("center位置:", center_point)

    while True:

        if KCF_flag is False:   # detect检测
            # TerminalDetect(cap, model)
            # MotorScale()  
            thread1 = td.Thread(target=TerminalDetect, args=(cap, model))
            thread2 = td.Thread(target=MotorScale, args=())
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
            stop_flag = 0
            print("正确识别终端，开启跟踪！")
            # global tracker, bbox
            tracker = KCFTracker(True, True, True)
            bbox = terminal
            tracker.init(bbox, frame)
            KCF_flag = True
            counter = 0
            # cv2.destroyAllWindows()
            com1.write(bytearray([0x02, 0x0A, 0x6D, 0X6B]))
            com2.write(bytearray([0x01, 0x0A, 0x6D, 0X6B]))

        else:     # KCF跟踪
           thread3 = td.Thread(target=tracker, args=())
           thread3.start()
           thread3.join()
           KCF_flag = False
           angle_base = 1  # 第一次转台需要转的角度
           angle_delta = 0.5  # 每次转台需要增加的角度
           i = 0.2