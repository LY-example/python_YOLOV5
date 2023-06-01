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

            x4 = int(pose[29])  # ydk0.5目标框
            y4 = int(pose[30])
            w4 = int(pose[31])
            h4 = int(pose[32])
            rect4 = [x4, y4, w4, h4]  # 将每行数据赋值给变量rect1
            # print(frame, rect1, rect2, rect3, rect4)

        iou1 = calculateIOU(rect1, rect2)  # 计算两个矩形重叠率
        iou2 = calculateIOU(rect1, rect3)
        iou3 = calculateIOU(rect1, rect4)
        kcfiou.append(iou1)
        hdk2iou.append(iou2)
        ydk3iou.append(iou3)
        frame.append(fps)

        # print(frame)
    return frame, kcfiou, hdk2iou, ydk3iou

if __name__ == '__main__':
    f = open("C:/Users/lenovo/Desktop/CLEResult/guizheng/all.txt", "r")
    # f = open("D:/新建文件夹/学校/大论文/CLEResult/guizheng/all.txt", "r")
    frame = []
    kcfiou = []
    hdk2iou = []
    ydk3iou = []
    frame, kcfiou, hdk2iou, ydk3iou = read_txt(f)

    sum1, sum2, sum3 = 0, 0, 0
    for item1 in kcfiou:
        sum1 += item1
        avg1 = sum1 / len(kcfiou)
    for item2 in hdk2iou:
        sum2 += item2
        avg2 = sum2 / len(hdk2iou)
    for item3 in ydk3iou:
        sum3 += item3
        avg3 = sum3 / len(ydk3iou)
    print(avg1, avg2, avg3)

    # 使用plt.plot()画图
    plt.plot(frame, kcfiou, linewidth=0.5, c='y', label='KCF_IOU')
    plt.plot(frame, hdk2iou, linewidth=0.5, c='m', label='HDK_IOU')
    plt.plot(frame, ydk3iou, linewidth=0.5, c='c', label='YDK0.5_IOU')
    plt.plot(900, avg1, "yo")
    plt.plot(900, avg2, "mo")
    plt.plot(900, avg3, "co")
    # plt.xticks([0, 300, 600, 900, 1200, 1500, 1800, 2500, 3500])
    plt.legend(loc='lower left')
    plt.title('IOU', fontsize=15)
    plt.xlabel('frame', fontsize=10)
    plt.ylabel('overlap rate', fontsize=10)
    plt.show()