import cv2


def FindTarget(img, threshold_gray=100, threshold_area=10000):
    cx = cy = 0
    # cv2.imshow('myPicture', img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray", img_gray)
    _, binary = cv2.threshold(img_gray, threshold_gray, 255, cv2.THRESH_BINARY)
    binary_G = cv2.GaussianBlur(binary, (3, 3), 15)
    # cv2.imshow("binary_G", binary_G)
    # 获取轮廓  cv2.RETR_EXTERNAL   cv2.RETR_TREE
    img_1,contours, hierarchy = cv2.findContours(binary_G, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # # 画出轮廓
    draw_img = img.copy()
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)  # 求轮廓的面积，得到第几个轮廓的面积
        # cv2.drawContours(draw_img, contours, i, (0, 0, 255), -1)
        if area > threshold_area:
            cv2.drawContours(draw_img, contours, i, (0, 0, 255), -1)
            M = cv2.moments(contours[i])  # 求矩
            cx = int(M['m10'] / M['m00'])  # 求x坐标
            cy = int(M['m01'] / M['m00'])  # 求y坐标
            print(cx, cy)
            # f.write(str(cx)+' '+str(cy)+'\n')
            draw_img = cv2.circle(draw_img, (cx, cy), 2, (0, 255, 0), 4)  # 画出重心
    #         # print(area)

    # imgs = np.hstack([img, draw_img])
    # cv2.imshow('imgs', imgs)
    # cv2.waitKey()
    # cv2.destroyWindow('myPicture')
    return draw_img, cx, cy
