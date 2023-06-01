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

            x2 = int(pose[9])    # hdk1目标框
            y2 = int(pose[10])
            w2 = int(pose[11])
            h2 = int(pose[12])
            rect2 = [x2, y2, w2, h2]  # 将每行数据赋值给变量rect1

            x3 = int(pose[13])  # hdk2目标框
            y3 = int(pose[14])
            w3 = int(pose[15])
            h3 = int(pose[16])
            rect3 = [x3, y3, w3, h3]  # 将每行数据赋值给变量rect1

            x4 = int(pose[17])  # hdk3目标框
            y4 = int(pose[18])
            w4 = int(pose[19])
            h4 = int(pose[20])
            rect4 = [x4, y4, w4, h4]  # 将每行数据赋值给变量rect1
            # print(frame, rect1, rect2, rect3, rect4)

        hdk1_cle = calculateCLE(rect1, rect2)  # 计算两个矩形重叠率
        hdk2_cle = calculateCLE(rect1, rect3)
        hdk3_cle = calculateCLE(rect1, rect4)
        HDK1CLE.append(hdk1_cle)
        HDK2CLE.append(hdk2_cle)
        HDK3CLE.append(hdk3_cle)
        frame.append(fps)


        # print(frame)
    return frame, HDK1CLE, HDK2CLE, HDK3CLE,

if __name__ == '__main__':
    f = open("C:/Users/lenovo/Desktop/CLEResult/guizheng/all.txt", "r")
    frame = []
    HDK1CLE = []
    HDK2CLE = []
    HDK3CLE = []
    frame, HDK1CLE, HDK2CLE, HDK3CLE = read_txt(f)

    sum1, sum2, sum3 = 0, 0, 0
    for item1 in HDK1CLE:
        sum1 += item1
        avg1 = sum1 / len(HDK1CLE)
    for item2 in HDK2CLE:
        sum2 += item2
        avg2 = sum2 / len(HDK2CLE)
    for item3 in HDK3CLE:
        sum3 += item3
        avg3 = sum3 / len(HDK3CLE)
    print(avg1, avg2, avg3)

    # 使用plt.plot()画图
    plt.plot(frame, HDK1CLE, linewidth=0.5, c='r', label='HDK1_CLE')
    plt.plot(frame, HDK2CLE, linewidth=0.5, c='b', label='HDK2_CLE')
    plt.plot(frame, HDK3CLE, linewidth=0.5, c='m', label='HDK3_CLE')
    plt.plot(900, avg1, "ro")
    plt.plot(900, avg2, "bo")
    plt.plot(900, avg3, "mo")
    # plt.yticks([0, 2, 4, 6, 8, 10, 12, 14])
    plt.legend(loc='upper right')
    plt.title('CLE', fontsize=15)
    plt.xlabel('frame', fontsize=10)
    plt.ylabel('center position error', fontsize=10)
    plt.show()
