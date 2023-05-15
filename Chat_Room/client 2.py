import socket
import sys
import errno

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

def send_message(sock, message):
    if message:
        encoded_message = message.encode('utf-8')
        message_header = f"{len(encoded_message):<{HEADER_LENGTH}}".encode('utf-8')
        sock.send(message_header + encoded_message)

def receive_message(sock):
    try:
        username_header = sock.recv(HEADER_LENGTH)
        if not len(username_header):
            return None, None
        username_length = int(username_header.decode('utf-8').strip())
        username = sock.recv(username_length).decode('utf-8')
        message_header = sock.recv(HEADER_LENGTH)
        message_length = int(message_header.decode('utf-8').strip())
        message = sock.recv(message_length).decode('utf-8')
        return username, message
    except IOError as e:
        if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
            return None, None
        print(f"Reading error: {str(e)}")
        sys.exit()
    except Exception as e:
        print(f"Reading error: {str(e)}")
        sys.exit()

def run_client():
    username = input("Username: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)
    send_message(client_socket, username)
    while True:
        message = input(f"{username} > ")
        send_message(client_socket, message)
        username, message = receive_message(client_socket)
        if username and message:
            print(f"{username} > {message}")

if __name__ == '__main__':
    run_client()
