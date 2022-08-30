import numpy
from cvzone.PoseModule import PoseDetector
import cv2
import numpy as np

import Cloths
from Cloths import Shirt, Pants
import math

RADIUS = 5
COLOR = (0, 255, 0)
THIKNESS = -1
EXIT_SIGNAL = 'q'
NO_SIGNAL = ''


# noinspection PyUnresolvedReferences
class Display:
    # Pose Landmark Model:
    # The landmark model in MediaPipe
    # Pose predicts the location of 33 pose landmarks
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28

    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.detector = PoseDetector()

    def add_cloth(self, cloth: Cloths, img: numpy.array, dots: dict) ->numpy.array:
        cloth_sprite, index_y, index_x = cloth.get_sprite(dots)

        y1, y2 = max(0, index_y), min(index_y + cloth_sprite.shape[0], img.shape[0])
        x1, x2 = max(0, index_x), min(index_x + cloth_sprite.shape[1], img.shape[1])
        sprite_y_index, sprite_x_index = min(0, index_y) * -1, min(0, index_x) * -1
        pants_sprite = cloth_sprite[sprite_y_index: sprite_y_index + (y2 - y1),
                       sprite_x_index: sprite_x_index + (x2 - x1), :]
        alpha_s = cloth_sprite[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        if alpha_l.shape == (y2 - y1, x2 - x1):
            for c in range(0, 3):
                main_pic_with_deleted_shirt = alpha_l * img[y1:y1 + (y2 - y1), x1:x1 + (x2 - x1), c]
                putted_cloth = alpha_s * pants_sprite[:, :, c]
                img[y1:y2, x1:x2, c] = (main_pic_with_deleted_shirt + putted_cloth)

    def display_pic(self, shirt: Shirt, pants: Pants, signal:str = None):
        success, generated_img = self.camera.read()

        if success:
            final_image = np.copy(generated_img)
            generated_img = self.detector.findPose(generated_img)
            lm_list, bbox_info = self.detector.findPosition(generated_img, bboxWithHands=True)
            if len(lm_list) >= 28:
                self.add_cloth(pants, final_image, {
                        "top_left": (lm_list[24][1], lm_list[24][2]),
                        "top_right": (lm_list[23][1], lm_list[23][2]),
                        "bot_left": (lm_list[28][1], lm_list[28][2]),
                        "bot_right": (lm_list[27][1], lm_list[27][2])
                })
            if len(lm_list) >= 24:
                self.add_cloth(shirt, final_image, {
                    "top_left": (lm_list[12][1], lm_list[12][2]),
                    "top_right": (lm_list[11][1], lm_list[11][2]),
                    "bot_left": (lm_list[24][1], lm_list[24][2]),
                    "bot_right": (lm_list[23][1], lm_list[23][2])
                })
            cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("Image", final_image)

        if (cv2.waitKey(1) & 0xFF == ord(EXIT_SIGNAL)) or signal == EXIT_SIGNAL:
            self.camera.release()
            cv2.destroyAllWindows()
            return EXIT_SIGNAL
        return NO_SIGNAL


if __name__ == "__main__":
    shirt = Shirt("IMG02.png", {"top_right": (417.0, 82.0), "top_left": (82.0, 80.0), "bot_right": (359.0, 553.0),
                                "bot_left": (161.0, 459.0)})
    pants = Pants("P-IMG01.png", {"top_right": (467.0, 44.0), "top_left": (147.0, 55.0), "bot_right": (509.0, 1377.0),
                                  "bot_left": (136.0, 1368.0)})
    displayer = Display()
    while displayer.display_pic(shirt, pants) != EXIT_SIGNAL:
        pass
