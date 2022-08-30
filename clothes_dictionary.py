SHIRT_IMAGES_DIRECTORY_PATH = "ShirtImages/"

PANTS_KEY = "pants"
SHIRTS_KEY = "shirts"

def get_clothes_dictionary() -> dict:
    clothes = {
        "shirts": {},
        "pants": {}
    }
    clothes[SHIRTS_KEY][1] = (SHIRT_IMAGES_DIRECTORY_PATH + "IMG01.png",
                            {"top_right": (456.0, 100.0), "top_left": (86.0, 79.0), "bot_right": (364.0, 641.0),
                             "bot_left": (149.0, 641.0)})
    clothes[SHIRTS_KEY][2] = (SHIRT_IMAGES_DIRECTORY_PATH + "IMG02.png",
                            {"top_right": (417.0, 82.0), "top_left": (82.0, 80.0), "bot_right": (359.0, 553.0),
                             "bot_left": (161.0, 459.0)})
    clothes[SHIRTS_KEY][3] = (SHIRT_IMAGES_DIRECTORY_PATH + "IMG03.png",
                            {"top_right": (385.0, 92.0), "top_left": (92.0, 72.0), "bot_right": (339.0, 551.0),
                             "bot_left": (157.0, 559.0)})
    clothes[SHIRTS_KEY][4] = (SHIRT_IMAGES_DIRECTORY_PATH + "IMG04.png",
                            {"top_right": (383.0, 126.0), "top_left": (105.0, 105.0), "bot_right": (321.0, 536.0),
                             "bot_left": (122.0, 545.0)})
    clothes[SHIRTS_KEY][5] = (SHIRT_IMAGES_DIRECTORY_PATH + "IMG05.png",
                            {"top_right": (328.0, 76.0), "top_left": (68.0, 65.0), "bot_right": (262.0, 470.0),
                             "bot_left": (87.0, 463.0)})
    clothes[SHIRTS_KEY][6] = (SHIRT_IMAGES_DIRECTORY_PATH + "IMG06.png",
                            {"top_right": (426.0, 97.0), "top_left": (111.0, 86.0), "bot_right": (332.0, 570.0),
                             "bot_left": (187.0, 561.0)})

    return clothes


if __name__ == '__main__':
    print(get_clothes_dictionary()["shirts"][2])