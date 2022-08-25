import cv2
from abc import abstractmethod
from numpy import array
import json
from numpy import arcsin
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
        self.texture = cv2.imread(path)
        self.dots = dots
        if "top_right" in dots and "top_left" in dots:
            self.width = math.sqrt((dots["top_right"][0] - dots["top_left"][0])**2 + (dots["top_right"][1] - dots["top_left"][1])**2)
        if "bot_right" in dots and "bot_left" in dots:
            self.height = math.sqrt((dots["top_right"][0] - dots["bot_right"][0])**2 + (dots["top_right"][1] - dots["bot_right"][1])**2)

    @abstractmethod
    def get_sprite(self) -> array:
        pass


class Shirt(Cloth):
    def __init__(self, path: str, dots: dict):
        super().__init__(path,dots)

    def get_sprite(self, dots: dict) -> array:
        if "top_right" in dots and "top_left" in dots:
            width = math.sqrt((dots["top_right"][0] - dots["top_left"][0])**2 + (dots["top_right"][1] - dots["top_left"][1])**2)
        if "bot_right" in dots and "bot_left" in dots:
            height = math.sqrt((dots["top_right"][0] - dots["bot_right"][0])**2 + (dots["top_right"][1] - dots["bot_right"][1])**2)

        #angle = math.degrees(arcsin(height / width))
        #rotation = cv2.getRotationMatrix2D((self.dots["top_left"][0] + (self.width/2), self.dots["top_left"][1]
        #                                    + (self.height/2)), angle, 1)
        H, W = self.texture.shape[:2]
        #ans = cv2.warpAffine(self.texture.copy(), rotation, (H, W))
        width = int(W * (width / self.width))
        height = int(H * (height / self.height))

        return cv2.resize(self.texture, (height, width))


if __name__ == "__main__":
    shirt = Shirt("9088.png", {"top_right": (845.0, 300.0), "top_left": (375.0, 300.0), "bot_right": (845.0, 1000.0), "bot_left": (375.0, 1000.0)})
    cv2.imshow("shirt", shirt.get_sprite({"top_right": (500.0, 200.0), "top_left": (100.0, 700.0), "bot_right": (500.0, 500.0), "bot_left": (100.0, 1000.0)}))
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
