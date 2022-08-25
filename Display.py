from cvzone.PoseModule import PoseDetector
import cv2
import numpy as np

RADIUS = 5
COLOR = (0, 255, 0)
THIKNESS = -1
EXIT_SIGNAL = 'q'
NO_SIGNAL = ''


class Display:
    def __init__(self):
        self.detector = PoseDetector()
        self.camera = cv2.VideoCapture(0)

    def display_pic(self, shirt: np.array):
        success, img = self.camera.read()
        y_offset = x_offset = 100
        shirt2 = cv2.resize(shirt, [200, 200])
        y1, y2 = y_offset, y_offset + shirt2.shape[0]
        x1, x2 = x_offset, x_offset + shirt2.shape[1]

        alpha_s = shirt2[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        if success:
            img2 = np.copy(img)
            img = self.detector.findPose(img)
            lmList, bboxInfo = self.detector.findPosition(img, bboxWithHands=False)
            if len(lmList) >= 12:
                cv2.circle(img2, (lmList[11][1], lmList[11][2]), RADIUS, COLOR, THIKNESS)
                cv2.circle(img2, (lmList[12][1], lmList[12][2]), RADIUS, COLOR, THIKNESS)
                cv2.circle(img2, (lmList[23][1], lmList[23][2]), RADIUS, COLOR, THIKNESS)
                cv2.circle(img2, (lmList[24][1], lmList[24][2]), RADIUS, COLOR, THIKNESS)

            for c in range(0, 3):
                img2[y1:y2, x1:x2, c] = (alpha_s * shirt2[:, :, c] + alpha_l * img2[y1:y2, x1:x2, c])
            cv2.imshow("Image", img2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.camera.release()
                cv2.destroyAllWindows()
                return EXIT_SIGNAL
        return NO_SIGNAL


if __name__ == "__main__":
    shirt = cv2.imread("9088.png", -1)
    displayer = Display()
    while displayer.display_pic(shirt) != EXIT_SIGNAL:
        i = 5
