import time
import numpy as np
import cv2
import time


# video = cv2.VideoCapture("01.wmv")
def FindTarget(frame, threshold_gray=100, threshold_area=10000):
    red_lower = np.array([156, 43, 46])
    red_upper = np.array([180, 255, 255])
    red_lower2 = np.array([0, 43, 46])
    red_upper2 = np.array([10, 255, 255])
    blue_lower = np.array([90, 100, 100])
    blue_upper = np.array([120, 255, 255])
    cx = cy = 0
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # cv2.imshow('hsv', hsv)
    mask1 = cv2.inRange(hsv, red_lower, red_upper)
    mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
    mask = cv2.add(mask1, mask2)
    # mask = cv2.inRange(hsv, blue_lower, blue_upper)
    mask = cv2.erode(mask, None, iterations=3)  # 腐蚀操作
    mask = cv2.dilate(mask, None, iterations=3)  # 膨胀操作
    mask = cv2.GaussianBlur(mask, (5, 5), 0)  # 高斯滤波
    # cv2.imshow('mask', mask)
    img_1, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # # 画出轮廓
    draw_img = frame.copy()
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)  # 求轮廓的面积，得到第几个轮廓的面积
        # cv2.drawContours(draw_img, contours, i, (0, 0, 255), -1)
        if area > threshold_area:
            cv2.drawContours(draw_img, contours, i, (0, 0, 255), -1)
            M = cv2.moments(contours[i])  # 求矩
            cx = int(M['m10'] / M['m00'])  # 求x坐标
            cy = int(M['m01'] / M['m00'])  # 求y坐标
            # print(cx, cy)
            # f.write(str(cx)+' '+str(cy)+'\n')
            draw_img = cv2.circle(draw_img, (cx, cy), 2, (0, 255, 0), 4)  # 画出重心
    #         # print(area)
    # cv2.imshow("video", draw_img)
    return draw_img, cx, cy
# threshold_area=10000
# if video.isOpened():
#     # video.read() 一帧一帧地读取
#     # open 得到的是一个布尔值，就是 True 或者 False
#     # frame 得到当前这一帧的图像
#     open, frame = video.read()
# else:
#     open = False
#
#
# while open:
#     ret, frame = video.read()
#     # 如果读到的帧数不为空，那么就继续读取，如果为空，就退出
#     if frame is None:
#         break
#     if ret == True:
#         FindTarget(frame)
#         # 这里使用 waitKey 可以控制视频的播放速度，数值越小，播放速度越快
#         # 这里等于 27 也即是说按下 ESC 键即可退出该窗口
#         if cv2.waitKey(10) & 0xFF == 27:
#             break
#     time.sleep(0.1)
# video.release()
# cv2.destroyAllWindows()
