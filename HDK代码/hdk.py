import cv2
from tracker import KCFTracker
import time
import platform
from contour import contour
from testvideo import findTerminal
print('系统:', platform.system())

def tracker(cam, frame, bbox):
    tracker = KCFTracker(True, True, True)  # (hog, fixed_Window, multi_scale)
    tracker.init(bbox, frame)
    global c
    # file_handle = open("C:/Users/lenovo/Desktop/CLEResult/hdk.txt", "a")  # a代表原来基础上累加  中心位置误差
    # file_handle = open("C:/Users/lenovo/Desktop/identificationtracksummary/littlearticle/peak_result/haar+dsst+kcf.txt", "a")
    while True:
        ok, frame = cam.read()
        # frame = cv2.resize(frame, (640, 480))
        timer = cv2.getTickCount()
        bbox, peak_value = tracker.update(frame)
        bbox = list(map(int, bbox))
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # if (c % frameRate == 0):
            # print("第{0}帧的peak_value的值为:{1}, 帧率fps为：{2}".format(str(c), round(peak_value, 3), round(fps, 0)), file=file_handle)
            # c += 1

        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))  # 左上角坐标  bbox[2]:为方框的宽  bbox[3]:为方框的高
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        center = (int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2))
        # print('左上角坐标：', p1, '右下角坐标：', p2)
        print('矩形框中心点：', center)
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        if (c % frameRate == 0):
            print("第{0}帧x:{1},y:{2},w:{3},h:{4}".format(str(c), bbox[0], bbox[1], bbox[2], bbox[3]), file=file_handle)
            c += 1
        # Put FPS
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        cv2.imshow("Tracking", frame)
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if (k == ord('q')) | (k == 27):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # video = cv2.VideoCapture('terminal1.mp4')
    video = cv2.VideoCapture(0)
    file_handle = open("C:/Users/lenovo/Desktop/CLEResult/hdk3.txt", "a")  # a代表原来基础上累加  中心位置误差
    c = 1
    frameRate = 1
    # print("开启识别二维码：")
    # while True:
    #     ok, frame = video.read()
    #     frame = cv2.resize(frame, (320,240))
    #     Terminal = contour(frame)
    #     _key = cv2.waitKey(1) & 0xFF  # 一直等待按键按下，并判断是哪个按键
    #     cv2.imshow("pick frame", frame)
    #     if (_key == ord('y')):  # 点击y选择当前帧
    #         print('正确识别二维码,开启识别终端！')
    #         break
    # cv2.destroyWindow('pick frame')
    while True:

        while True:
            ok, frame = video.read()
            # frame = cv2.resize(frame, (640, 480))
            Terminal = findTerminal(frame)
            cv2.imshow("distinguish", frame)
            if (c % frameRate == 0):
                print("检测第{0}帧x:{1},y:{2},w:{3},h:{4}".format(str(c), Terminal[0], Terminal[1], Terminal[2], Terminal[3]), file=file_handle)
                c += 1

            _key = cv2.waitKey(1) & 0xFF
            if (_key == ord('y')):  # 点击y选择当前帧
                print('正确识别终端,开启跟踪！')
                break

        bbox = Terminal
        cv2.destroyWindow('distinguish')
        tracker(video, frame, bbox)
