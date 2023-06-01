# -*- coding: utf-8 -*-
"""
Author : LiYue
Date   : 2023年02月03日 上午 10:09
Project: yolov5terminal
IDE    : PyCharm
"""
import math
import matplotlib.pyplot as plt

# calculate IOU,rect1 and rect2 are rectangles(x,y,width,height)
"""
    将每帧真实框用rect1表示，各种算法的框用rect2表示，
    分别计算它们的区域重叠度。
"""
def calculateIOU(rect1, rect2):
    # calculate the area
    area1 = rect1[2] * rect1[3]   # w*h区域1面积
    area2 = rect2[2] * rect2[3]   # w*h区域2面积
    # calculate the sum area
    area = area1 + area2

    # calculate the edge line of every rect
    top1 = rect1[1]   # y
    left1 = rect1[0]   # x
    bottom1 = rect1[1] + rect1[3]   # y+h
    right1 = rect1[0] + rect1[2]   # x+w

    top2 = rect2[1]
    left2 = rect2[0]
    bottom2 = rect2[1] + rect2[3]
    right2 = rect2[0] + rect2[2]

    # calculate the intersect rectangle
    top = max(top1, top2)
    left = max(left1, left2)
    bottom = min(bottom1, bottom2)
    right = min(right1, right2)

    # if no intersect
    if top >= bottom or right <= left:
        return 0
    else:
        intersectArea = (bottom - top) * (right - left)
        iou = intersectArea / (area - intersectArea)   # 区域重叠度

        return iou

def calculateCLE(rect1, rect2):
    # groundtruth标注的真实框的中心位置
    x1 = rect1[0] + rect1[2] / 2
    y1 = rect1[1] + rect1[3] / 2

    # 各种算法跟踪结果框的中心位置
    x2 = rect2[0] + rect2[2] / 2
    y2 = rect2[1] + rect2[3] / 2

    CLE = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

    # 使用plt.plot()画图
    # plt.plot(frame, CLE)
    # plt.show()
    return CLE

def read_txt(f):
    lines = f.readlines()  # 真实框
    i = 0

    for number, line in enumerate(lines, 1):
        i += 1
        if number == i & i <= 1800:
            pose = line.split()  # 将字符串切片并转换为列表，默认为空格
            fps1 = int(pose[0])  # 返回当前帧
            x1 = int(pose[1])  # groundtruth目标框
            y1 = int(pose[2])
            w1 = int(pose[3])
            h1 = int(pose[4])
            rect1 = [x1, y1, w1, h1]  # 将每行数据赋值给变量rect1

            x1 = int(pose[9])    # hdk1目标框
            y1 = int(pose[10])
            w1 = int(pose[11])
            h1 = int(pose[12])
            rect2 = [x1, y1, w1, h1]  # 将每行数据赋值给变量rect1

            x2 = int(pose[13])    # hdk2目标框
            y2 = int(pose[14])
            w2 = int(pose[15])
            h2 = int(pose[16])
            rect3 = [x2, y2, w2, h2]  # 将每行数据赋值给变量rect1

            x3 = int(pose[17])  # hdk3目标框
            y3 = int(pose[18])
            w3 = int(pose[19])
            h3 = int(pose[20])
            rect4 = [x3, y3, w3, h3]  # 将每行数据赋值给变量rect1

        iou1 = calculateIOU(rect1, rect2)  # 计算两个矩形重叠率
        iou2 = calculateIOU(rect1, rect3)
        iou3 = calculateIOU(rect1, rect4)
        hdk1iou.append(iou1)
        hdk2iou.append(iou2)
        hdk3iou.append(iou3)
        frame.append(fps1)

    # print(frame)
    return frame, hdk1iou, hdk2iou, hdk3iou

if __name__ == '__main__':
    f = open("C:/Users/lenovo/Desktop/CLEResult/guizheng/all.txt", "r")
    frame = []
    hdk1iou = []
    hdk2iou = []
    hdk3iou = []
    frame, hdk1iou, hdk2iou, hdk3iou = read_txt(f)

    sum1, sum2, sum3 = 0, 0, 0
    for item1 in hdk1iou:
        sum1 += item1
        avg1 = sum1 / len(hdk1iou)
    for item2 in hdk2iou:
        sum2 += item2
        avg2 = sum2 / len(hdk2iou)
    for item3 in hdk3iou:
        sum3 += item3
        avg3 = sum3 / len(hdk3iou)
    print(avg1, avg2, avg3)

    # 使用plt.plot()画图
    plt.plot(frame, hdk1iou, linewidth=0.5, c='m', label='hdk1')
    plt.plot(frame, hdk2iou, linewidth=0.5, c='c', label='hdk2')
    plt.plot(frame, hdk3iou, linewidth=0.5, c='y', label='hdk3')
    plt.plot(900, avg1, "mo")
    plt.plot(900, avg2, "co")
    plt.plot(900, avg3, "yo")
    # plt.xticks([0, 300, 600, 900, 1200, 1500, 1800, 2500, 3500])
    plt.legend(loc='upper right')
    plt.title('IOU', fontsize=15)
    plt.xlabel('frame', fontsize=10)
    plt.ylabel('overlap rate', fontsize=10)
    plt.show()