# -*- coding:utf-8 -*-
"""
姓名：LiYue
日期：2022年03月22日
"""
import cv2
import numpy as np

# a, b = 360, 240


def findTerminal(frame):
    cascade = cv2.CascadeClassifier('./examples/pos/cascade1.xml')
    framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    Terminal = cascade.detectMultiScale(framegray, 1.3, 200)  # 参数意思：（输入图像，每次缩小图像比例，匹配成功所需要的周围矩形框的数目）

    TerminalListC = []
    TerminalListArea = []

    for (x, y, w, h) in Terminal:
        cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), (255, 0, 0), 2)
        cv2.putText(frame, 'Terminal', (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1)
        cx = int(x + w // 2)
        cy = int(y + w // 2)
        area = int(w * h)
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        # strContent = str(x)+','+str(y)+','+str(w)+',' +str(h)
        # print('终端的坐标为：', strContent)
        TerminalListC.append([cx, cy])
        TerminalListArea.append(area)

    if len(TerminalListArea) != 0:
        i = TerminalListArea.index(max(TerminalListArea))
        return Terminal[i]
            # frame, [TerminalListC[i], TerminalListArea[i]]
    else:
        return frame
            # , [[0, 0], 0]