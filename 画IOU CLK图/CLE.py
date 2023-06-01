# -*- coding: utf-8 -*-
"""
Author : LiYue
Date   : 2023年02月03日 上午 10:09
Project: yolov5terminal
IDE    : PyCharm
"""
import math
import matplotlib.pyplot as plt

def calculateCLE(rect1, rect2):
    # groundtruth标注的真实框的中心位置
    x1 = rect1[0] + rect1[2] / 2
    y1 = rect1[1] + rect1[3] / 2

    # 各种算法跟踪结果框的中心位置
    x2 = rect2[0] + rect2[2] / 2
    y2 = rect2[1] + rect2[3] / 2

    CLE = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    return CLE

def read_txt(f):
    lines = f.readlines()  # 真实框
    i = 0

    for number, line in enumerate(lines, 1):
        i += 1
        if number == i & i <= 1800:
            pose = line.split()  # 将字符串切片并转换为列表，默认为空格
            fps = int(pose[0])  # 返回当前帧
            x1 = int(pose[1])    # groundtruth目标框
            y1 = int(pose[2])
            w1 = int(pose[3])
            h1 = int(pose[4])
            rect1 = [x1, y1, w1, h1]  # 将每行数据赋值给变量rect1

            x2 = int(pose[5])    # KCF目标框
            y2 = int(pose[6])
            w2 = int(pose[7])
            h2 = int(pose[8])
            rect2 = [x2, y2, w2, h2]  # 将每行数据赋值给变量rect1

            x3 = int(pose[9])  # hdk1目标框
            y3 = int(pose[10])
            w3 = int(pose[11])
            h3 = int(pose[12])
            rect3 = [x3, y3, w3, h3]  # 将每行数据赋值给变量rect1

            x4 = int(pose[29])  # ydk0.45目标框
            y4 = int(pose[30])
            w4 = int(pose[31])
            h4 = int(pose[32])
            rect4 = [x4, y4, w4, h4]  # 将每行数据赋值给变量rect1
            # print(frame, rect1, rect2, rect3, rect4)

        kcf_cle = calculateCLE(rect1, rect2)  # 计算两个矩形重叠率
        hdk_cle = calculateCLE(rect1, rect3)
        ydk_cle = calculateCLE(rect1, rect4)
        KCFCLE.append(kcf_cle)
        HDKCLE.append(hdk_cle)
        YDKCLE.append(ydk_cle)
        frame.append(fps)

        # print(frame)
    return frame, KCFCLE, HDKCLE, YDKCLE

if __name__ == '__main__':
    f = open("C:/Users/lenovo/Desktop/CLEResult/guizheng/all.txt", "r")
    frame = []
    KCFCLE = []
    HDKCLE = []
    YDKCLE = []
    frame, KCFCLE, HDKCLE, YDKCLE = read_txt(f)

    sum1, sum2, sum3 = 0, 0, 0
    for item1 in KCFCLE:
        sum1 += item1
        avg1 = sum1 / len(KCFCLE)
    for item2 in HDKCLE:
        sum2 += item2
        avg2 = sum2 / len(HDKCLE)
    for item3 in YDKCLE:
        sum3 += item3
        avg3 = sum3 / len(YDKCLE)
    print(avg1, avg2, avg3)

    # 使用plt.plot()画图
    plt.plot(frame, KCFCLE, linewidth=0.5, c='y', label='KCF_CLE')
    plt.plot(frame, HDKCLE, linewidth=0.5, c='c', label='HDK_CLE')
    plt.plot(frame, YDKCLE, linewidth=0.5, c='m', label='YDK_CLE')
    plt.plot(900, avg1, "yo")
    plt.plot(900, avg2, "co")
    plt.plot(900, avg3, "mo")
    # plt.yticks([0, 2, 4, 6, 8, 10, 12, 14])
    plt.legend(loc='upper left')
    plt.title('CLE', fontsize=15)
    plt.xlabel('frame', fontsize=10)
    plt.ylabel('center position error', fontsize=10)
    plt.show()