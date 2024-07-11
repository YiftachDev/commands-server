
import socket
import os
import protocol
import utils
import glob
import shutil
import subprocess
import pyautogui


IP = "0.0.0.0"
PORT = 8821
PHOTO_PATH = "C:\\Users\\user\\Downloads\\screen.jpg" # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd: str):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol.check_cmd first
    if protocol.check_cmd(cmd):
        data = cmd.split(" ")
        print(data)
        command, params = data[0], data[1:]
        print(params)
        for i in range(len(params)):
            if not utils.check_valid_path(params[i]):
                return False, "", []
            print(params[i])
            params[i] = utils.make_raw_string(params[i])
            print(params[i])
        return True, command, params
    return False, "", []


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data
    """

    # (7)
    response = ""
    if command == "DIR":
        files_list = glob.glob(f"{params[0]}\\*.*",)
        for file in files_list:
            response += file
    elif command == "DELETE":
        os.remove(params[0])
        response = "Deleted the file successfully!"
    elif command == "COPY":
        shutil.copy(params[0], params[1])
        response = "Copied the file successfully!"
    elif command == "EXECUTE":
        subprocess.call(params[0])
        response = "Executed the program successfully!"
    elif command == "TAKE_SCREENSHOT":
        image = pyautogui.screenshot()
        image.save(PHOTO_PATH)
        response = "Screenshot saved!"
    elif command == "SEND_PHOTO":
        image_size = os.path.getsize(PHOTO_PATH)
        response = image_size
    return response


def main():
    # open socket with client
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen()
    (client_socket, client_addr) = server_socket.accept()
    # (1)

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            print(params)
            if valid_cmd:
                # prepare a response using "handle_client_request"
                data = handle_client_request(command, params)
                print(data)
                # add length field using "create_msg"
                response = protocol.create_msg(data)
                print(response)
                # send to client
                client_socket.send(response.encode())
                if command == 'SEND_PHOTO':
                    # Send the data itself to the client
                    with open(PHOTO_PATH, "rb") as image:
                        image_data = image.read()
                        client_socket.send(image_data)
                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                msg = protocol.create_msg(response)
                # send to client
                client_socket.send(msg.encode())

        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            #send to client
            msg = protocol.create_msg(response)
            client_socket.send(msg.encode())

            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")
    server_socket.close()
    client_socket.close()


if __name__ == '__main__':
    main()
