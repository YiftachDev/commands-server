
LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    commands = ["DELETE", "DIR", "COPY", "EXECUTE", "TAKE_SCREENSHOT", "SEND_PHOTO", 'EXIT']
    data = data.split(" ")
    if data[0] not in commands:
        return False
    if data[0] == "DIR" or data[0] == "DELETE" or data[0] == "EXECUTE":
        if len(data) <= 1:
            return False
    elif data[0] == "COPY":
        if len(data) <= 2:
            return False
    return True


def create_msg(data) -> str:
    """
    Create a valid protocol message, with length field
    """
    str_data = str(data)
    length = str(len(str_data)).zfill(4)
    msg = length + str_data
    return msg


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    length = my_socket.recv(4).decode()
    try:
        length = int(length)
    except:
        return False, "Error"
    msg = my_socket.recv(length).decode()
    return True, msg


