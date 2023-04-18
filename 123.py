import cv2
import datetime
if __name__ == "__main__":
    webcam = cv2.VideoCapture(0)

    if not webcam.isOpened():
        print("can't open the camera!!!")
    # cv2.namedWindow("video", 0)
    # cv2.resizeWindow("video", 960, 720)
    # method 1:
    # webcam.set(3, 1920)  # width=1920
    # webcam.set(4, 1080)  # height=1080
    # method 2:
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while True:
        ret, frame = webcam.read()
        # print(frame.shape[:2])  # just need the first two values.
        # cv2.resizeWindow("video", 640, 480)
        cv2.imshow("video", frame)
        dt_ms = datetime.datetime.now().strftime('---%Y-%m-%d %H:%M:%S.%f')
        print(dt_ms)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    webcam.release()
    cv2.destroyAllWindows()
