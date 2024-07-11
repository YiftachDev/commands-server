
import socket
import protocol


IP = "127.0.0.1"
PORT = 8821
SAVED_PHOTO_LOCATION = "C:\\Users\\user\\Downloads\\screen2.jpg" # The path + filename where the copy of the screenshot at the client should be saved

def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # (8) treat all responses except SEND_PHOTO
    is_valid, msg = protocol.get_msg(my_socket)
    if cmd != 'SEND_PHOTO':
        print(msg)
    else:
        image_size = msg
        print(image_size)
        image_data = my_socket.recv(int(image_size))
        with open(SAVED_PHOTO_LOCATION, "wb") as image:
            image.write(image_data)
    # (10) treat SEND_PHOTO


def main():
    # open socket with the server
    my_socket = socket.socket()
    my_socket.connect((IP, PORT))
    # (2)

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet.encode())
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()

if __name__ == '__main__':
    main()