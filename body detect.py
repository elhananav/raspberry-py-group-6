from cvzone.PoseModule import PoseDetector
import cv2
import numpy as np
from Cloths import Shirt

RADIUS = 5
COLOR = (0, 255, 0)
THIKNESS = -1
EXIT_SIGNAL = 'q'
NO_SIGNAL = ''


class Display:
    def __init__(self):
        self.detector = PoseDetector()
        self.camera = cv2.VideoCapture(0)

    def display_pic(self, shirt: Shirt):
        success, img = self.camera.read()
        y_offset = x_offset = 100

        if success:
            img2 = np.copy(img)
            img = self.detector.findPose(img)
            lmList, bboxInfo = self.detector.findPosition(img, bboxWithHands=False)

            if len(lmList) >= 24:
                    shirt2 = shirt.get_sprite({
                        "top_left": (float(lmList[12][1]), float(lmList[12][2])),
                        "top_right": (float(lmList[11][1]), float(lmList[11][2])),
                        "bot_left": (float(lmList[24][1]), float(lmList[24][2])),
                        "bot_right": (float(lmList[23][1]), float(lmList[23][2]))
                    })

                    cv2.imshow("shirt", shirt2)
                    y1, y2 = y_offset, y_offset + shirt2.shape[0]
                    x1, x2 = x_offset, x_offset + shirt2.shape[1]
                    alpha_s = shirt2[:, :, 2] / 255.0
                    alpha_l = 1.0 - alpha_s

                    for c in range(0, 3):
                        img2[y1:y2, x1:x2, c] = (alpha_s * shirt2[:, :, c] + alpha_l * img2[y1:y2, x1:x2, c])

                    cv2.circle(img2, (lmList[11][1], lmList[11][2]), RADIUS, COLOR, THIKNESS)
                    cv2.circle(img2, (lmList[12][1], lmList[12][2]), RADIUS, COLOR, THIKNESS)
                    cv2.circle(img2, (lmList[23][1], lmList[23][2]), RADIUS, COLOR, THIKNESS)
                    cv2.circle(img2, (lmList[24][1], lmList[24][2]), RADIUS, COLOR, THIKNESS)

            cv2.imshow("Image", img2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.camera.release()
                cv2.destroyAllWindows()
                return EXIT_SIGNAL
        return NO_SIGNAL


if __name__ == "__main__":
    shirt = Shirt("9088.png", {"top_right": (845.0, 300.0), "top_left": (375.0, 300.0), "bot_right": (845.0, 1000.0),
                               "bot_left": (375.0, 1000.0)})
    displayer = Display()
    while displayer.display_pic(shirt) != EXIT_SIGNAL:
        i = 5
