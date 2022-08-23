from cvzone.PoseModule import PoseDetector
import cv2
import numpy as np


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()
    radius = 5
    color = (0,255,0)
    thikness = -1
    while True:

        success, img = cap.read()
        img2 = np.copy(img)
        img = detector.findPose(img)
        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)
        if bboxInfo:
            center = bboxInfo["center"]
            cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
        if len(lmList) >= 12:
            cv2.circle(img2, (lmList[11][1], lmList[11][2]), radius, color, thikness)
            cv2.circle(img2, (lmList[12][1], lmList[12][2]), radius, color, thikness)
            cv2.circle(img2, (lmList[23][1], lmList[23][2]), radius, color, thikness)
            cv2.circle(img2, (lmList[24][1], lmList[24][2]), radius, color, thikness)
        cv2.imshow("Image", img2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()