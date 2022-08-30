import cv2
from abc import abstractmethod
from numpy import array
import json
import math

CLOTH_INFO = "cloth_info.txt"


def load_shirts():
    data = {}
    ans = []
    with open(CLOTH_INFO) as file_reader:
        data = json.load(file_reader)
    for i in data["shirts"]:
        ans.append(Shirt(data[i]["path"], data[i]["dots"]))


class Cloth:
    def __init__(self, path: str, dots: dict):
        self.texture = cv2.imread(path, -1)
        self.dots = dots

        if "top_right" in dots and "top_left" in dots:
            self.width = math.dist(dots["top_right"], dots["top_left"])

        if "bot_right" in dots and "bot_left" in dots:
            self.height = math.dist(dots["top_right"], dots["bot_right"])

    @abstractmethod
    def get_sprite(self, dots: dict) -> array:
        pass


class Shirt(Cloth):
    def __init__(self, path: str, dots: dict):
        super().__init__(path, dots)

    def get_sprite(self, dots: dict) -> array:

        if "top_right" in dots and "top_left" in dots:
            width = math.dist(dots["top_right"], dots["top_left"])

        if "top_right" in dots and "bot_left" in dots:
            height = math.dist(dots["top_right"], dots["bot_right"])

        h, w = self.texture.shape[:2]
        x_scale, y_scale = width / self.width, height / self.height

        width = int(w * x_scale)
        height = int(h * y_scale)

        return cv2.resize(self.texture, (width, height)), \
               int(dots["top_left"][1] - (self.dots["top_left"][1] * y_scale)), \
               int(dots["top_left"][0] - (self.dots["top_left"][0] * x_scale))


class Pants(Cloth):
    def __init__(self, path: str, dots: dict):
        super().__init__(path, dots)

    def get_sprite(self, dots: dict) -> array:
        if "top_right" in dots and "top_left" in dots:
            width = math.sqrt(
                (dots["top_right"][0] - dots["top_left"][0]) ** 2 + (dots["top_right"][1] - dots["top_left"][1]) ** 2)
        if "top_right" in dots and "bot_left" in dots:
            height = math.sqrt(
                (dots["top_right"][0] - dots["bot_right"][0]) ** 2 + (dots["top_right"][1] - dots["bot_right"][1]) ** 2)

        H, W = self.texture.shape[:2]
        x_scale, y_scale = width / self.width, height / self.height

        width = int(W * x_scale)
        height = int(H * y_scale)

        return cv2.resize(self.texture, (width, height)), \
               int(dots["top_left"][1] - (self.dots["top_left"][1] * y_scale)), \
               int(dots["top_left"][0] - (self.dots["top_left"][0] * x_scale))


if __name__ == "__main__":
    shirt = Shirt("IMG02.png", {"top_right": (417.0, 82.0), "top_left": (82.0, 80.0), "bot_right": (359.0, 553.0),
                                "bot_left": (161.0, 459.0)})
    cv2.imshow("shirt",
               shirt.get_sprite({"top_right": (500.0, 200.0), "top_left": (100.0, 700.0), "bot_right": (500.0, 500.0),
                                 "bot_left": (100.0, 1000.0)}))
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
