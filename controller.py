import clothes_dictionary as c_dict
import Cloths
import Display
import select
import socket


HOST = "10.32.5.34"
#HOST = "127.0.0.1"
PORT = 62223
CLOTHES_TYPE_CELL = 0
CLOTHES_IMAGE_NUM_CELL = 1
NUM_OF_DATA_KEYS = 2


def change_clothes(clothes_dictionary: dict, data: str, shirt: Cloths.Shirt, pants: Cloths.Pants) -> (Cloths.Shirt, Cloths.Pants):
    split_data = data.split()
    if split_data[CLOTHES_TYPE_CELL] in clothes_dictionary and len(split_data) >= NUM_OF_DATA_KEYS and \
            split_data[CLOTHES_IMAGE_NUM_CELL].isnumeric():
        number_of_img = int(split_data[CLOTHES_IMAGE_NUM_CELL])
        if split_data[CLOTHES_TYPE_CELL] == c_dict.SHIRTS_KEY and \
                number_of_img in clothes_dictionary[c_dict.SHIRTS_KEY]:
            return Cloths.Shirt(*clothes_dictionary[c_dict.SHIRTS_KEY][number_of_img]), pants
        elif split_data[CLOTHES_TYPE_CELL] == c_dict.PANTS_KEY and  \
                number_of_img in clothes_dictionary[c_dict.PANTS_KEY]:
            return shirt, Cloths.Pants(*clothes_dictionary[c_dict.PANTS_KEY][number_of_img])
    return shirt, pants


def main() -> None :
    """https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client"""
    clothes_dictionary = c_dict.get_clothes_dictionary()
    server_socket = socket.socket()  # get instance
    server_socket.bind((HOST, PORT))  # bind host address and port together
    server_socket.listen(1)
    try:
        while True:
            shirt = Cloths.Shirt(*clothes_dictionary[c_dict.SHIRTS_KEY][1])
            pants = Cloths.Pants(*clothes_dictionary[c_dict.PANTS_KEY][1])
            displayer = Display.Display()
            signal = None
            conn, address = server_socket.accept()  # accept new connection
            print("Connection from: " + str(address))
            conn.setblocking(False)
            while displayer.display_pic(shirt, pants, signal) != Display.EXIT_SIGNAL:
                # receive data stream. it won't accept data packet greater than 1024 bytes
                ready = select.select([conn], [], [], 0.01)
                if ready[0]:
                    data = conn.recv(1024).decode()
                    if not data:
                        signal = Display.EXIT_SIGNAL
                        continue
                    else:
                        shirt, pants = change_clothes(clothes_dictionary, data, shirt, pants)
                    print("from connected user: " + str(data))

            conn.close()  # close the connection
    except KeyboardInterrupt:
        server_socket.close()
        print("Exit server.")


if __name__ == '__main__':
    main()
