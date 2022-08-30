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
        # cv2.namedWindow("Image", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions
        # self.last_cap_date =

    def display_pic(self, shirt: Shirt, signal: str=None):
        success, img = self.camera.read()

        if success:
            img2 = np.copy(img)
            h, w, c = img.shape
            img = self.detector.findPose(img)
            lmList, bboxInfo = self.detector.findPosition(img, bboxWithHands=False)

            if len(lmList) >= 24:
                    sprite, index_y, index_x = shirt.get_sprite({
                        "top_left": (lmList[12][1], lmList[12][2]),
                        "top_right": (lmList[11][1], lmList[11][2]),
                        "bot_left": (lmList[24][1], lmList[24][2]),
                        "bot_right": (lmList[23][1], lmList[23][2])
                    })
                    cv2.imshow("shirt", sprite)

                    y1, y2 = max(0, index_y), min(index_y + sprite.shape[0], h)
                    x1, x2 = max(0, index_x), min(index_x + sprite.shape[1], w)
                    sprite_y_index, sprite_x_index = min(0, index_y) * -1, min(0, index_x) * -1
                    sprite = sprite[sprite_y_index: sprite_y_index + (y2 - y1),
                              sprite_x_index : sprite_x_index + (x2 - x1), :]
                    alpha_s = sprite[:, :, 3] / 255.0
                    alpha_l = 1.0 - alpha_s
                    if alpha_l.shape == (y2 - y1, x2 - x1):
                        for c in range(0, 3):
                            main_pic_with_deleted_shirt = alpha_l * img2[y1:y1 + (y2 - y1), x1:x1 + (x2 - x1), c]
                            putted_shirt = alpha_s * sprite[:, :, c]
                            img2[y1:y2, x1:x2, c] = (main_pic_with_deleted_shirt + putted_shirt)

                    # cv2.circle(img2, (lmList[11][1], lmList[11][2]), RADIUS, COLOR, THIKNESS)
                    # cv2.circle(img2, (lmList[12][1], lmList[12][2]), RADIUS, COLOR, THIKNESS)
                    # cv2.circle(img2, (lmList[23][1], lmList[23][2]), RADIUS, COLOR, THIKNESS)
                    # cv2.circle(img2, (lmList[24][1], lmList[24][2]), RADIUS, COLOR, THIKNESS)

            cv2.imshow("Image", img2)
            if (cv2.waitKey(1) & 0xFF == ord(EXIT_SIGNAL)) or signal == EXIT_SIGNAL:
                self.camera.release()
                cv2.destroyAllWindows()
                return EXIT_SIGNAL
        return NO_SIGNAL


if __name__ == "__main__":
    shirt = Shirt("IMG02.png", {"top_right": (417.0, 82.0), "top_left": (82.0, 80.0), "bot_right": (359.0, 553.0), "bot_left": (161.0, 459.0)})
    displayer = Display()
    while displayer.display_pic(shirt) != EXIT_SIGNAL:
        pass
    # """https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client"""
    # server_socket = socket.socket()  # get instance
    # # look closely. The bind() function takes tuple as argument
    # server_socket.bind((HOST, PORT))  # bind host address and port together
    #
    # # configure how many client the server can listen simultaneously
    # server_socket.listen(1)
    # while True:
    #     displayer = Display()
    #     signal = None
    #     conn, address = server_socket.accept()  # accept new connection
    #     print("Connection from: " + str(address))
    #     conn.setblocking(False)
    #     while displayer.display_pic(shirt, signal) != EXIT_SIGNAL:
    #         # receive data stream. it won't accept data packet greater than 1024 bytes
    #         ready = select.select([conn], [], [], 0.01)
    #         if ready[0]:
    #             data = conn.recv(1024).decode()
    #             if not data:
    #                 signal = EXIT_SIGNAL
    #                 continue
    #             print("from connected user: " + str(data))
    #
    #     conn.close()  # close the connection
