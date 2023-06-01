# -*- coding: utf-8 -*-
"""
Author : LiYue
Date   : 2022年08月29日 上午 10:00
Project: AAATrackering
IDE    : PyCharm
"""
import sys
import cv2
import time
import math
import torch
import numpy as np
import pandas as pd
from tracker import KCFTracker

if __name__ == '__main__':
    KCF_flag = False  # 首次不进行KCF
    conf = 0

    c = 1
    framerate = 1
    file_handle = open("/home/jetson/Desktop/gpu_peakvalue/yolov5+dsst+kcf.txt", "a")
    
    # cap = cv2.VideoCapture('/home/jetson/Desktop/AAATrackering/KCFTrackering/terminal1.mp4')  # 调用摄像头的
    cap = cv2.VideoCapture(0)
    pthfile = r'/home/jetson/.cache/torch/hub/ultralytics_yolov5_master'
    # model = torch.hub.load('ultralytics/yolov5', 'custom',
    #                        path='/home/jetson/Desktop/AAATrackering/KCFTrackering/yolov5/runs/train/exp3/weights/best.pt')
    model = torch.hub.load(pthfile, 'custom',
                            path='/home/jetson/Desktop/AAATrackering/KCFTrackering/yolov5/runs/train/exp3/weights/best.pt', source='local')

    terminal = [0, 0, 0, 0]
    while True:
        ret, frame_old = cap.read()   # 读取帧
        t1 = cv2.getTickCount()
        # frame_old = cv2.resize(frame_old, (640, 480))
        frame = cv2.cvtColor(frame_old, cv2.COLOR_BGR2RGB)   # yolov5读取图片为RGB格式

        if KCF_flag is False:   # detect建
            result = model(frame).pandas().xyxy[0]   # 通过hub获取终端的坐标，置信度
            print("result:", result)
            df = pd.DataFrame(result)    # 获取result中的数据
            df = df.empty

            if df is False:    # 判断数据是否为空
                terminal[0] = result['xmin'][0]
                terminal[1] = result['ymin'][0]
                terminal[2] = result['xmax'][0] - result['xmin'][0]
                terminal[3] = result['ymax'][0] - result['ymin'][0]
                conf = round(result['confidence'][0], 3)
                name = str(result['name'][0])
                frame = cv2.rectangle(frame, (int(result['xmin'][0]), int(result['ymin'][0])),
                                      (int(result['xmax'][0]), int(result['ymax'][0])), (0, 255, 0), 3)
                frame = cv2.putText(frame, name + ',' + str(conf), (int(result['xmin'][0]) - 5, int(result['ymin'][0])),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1.5, (0, 255, 0), 3)
                print('conf的值:', conf)
            cv2.imshow('frame', frame)
            t2 = cv2.getTickCount()
            detectfps = int(cv2.getTickFrequency()/(t2 - t1))
            if (c % framerate == 0):
                print("第{0}帧的conf的值为:{1}, 帧率fps为:{2}".format(str(c), conf, round(detectfps, 0)), file=file_handle)
                c += 1
            # print("终端检测的帧率为：", detectfps)
            cv2.waitKey(1)
            if conf > 0.69:
                print("正确识别终端，开启跟踪！")
                tracker = KCFTracker(True, True, True)
                bbox = terminal
                tracker.init(bbox, frame)
                KCF_flag = True
                cv2.destroyAllWindows()

        else:
            ret, frame = cap.read()   # 读取帧
            timer = cv2.getTickCount()

            bbox, peak_value = tracker.update(frame_old)
            print('peak_value的值为:',peak_value)
            bbox = list(map(int, bbox))

            p1 = (int(bbox[0]), int(bbox[1]))   # 左上角
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))   #右下角, 
            target_point = (int(bbox[0] + bbox[2]/2), int(bbox[1] + bbox[3]/2))  # 目标中心点坐标
            center_point = (320, 240)  # 拍摄画面中心点坐标

            cv2.rectangle(frame_old, p1, p2, (255, 0, 0), 2, 1)  #画矩形框与点
            cv2.circle(frame_old, target_point, 3, (255, 0, 0), cv2.FILLED)   # 显示目标中心点
            cv2.circle(frame_old, center_point, 3, (0, 255, 0), cv2.FILLED)  # 显示目标中心点
            loop_time = cv2.getTickCount() - timer
            fps = int(cv2.getTickFrequency() / loop_time)
            cv2.putText(frame_old, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
            cv2.imshow("Tracking", frame_old)
            if (c % framerate == 0):
                print("第{0}帧的peak_value的值为:{1}, 帧率fps为：{2}".format(str(c), round(peak_value, 3), round(fps, 0)), file=file_handle)
                c += 1
            if peak_value < 0.5:
                print("目标跟踪失败，重新进行终端检测！")
                cv2.destroyAllWindows()
                KCF_flag = False
            if cv2.waitKey(30) & 0xff == ord('q'):
                print("结束跟踪任务！")
                sys.exit(0)
