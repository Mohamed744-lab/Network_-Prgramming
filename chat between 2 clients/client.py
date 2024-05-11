import socket
import threading

def receive_msgs(connection):
    while True:
        try:
            size_bytes = connection.recv(8)
            size = int.from_bytes(size_bytes, 'big')
            data = connection.recv(size).decode('utf-8')
            print(data)
        except socket.error:
            break

def send_msg(connection):
    while True:
        message = input()
        recipient = input("Enter recipient address (host:port): ")
        data = f"{recipient}:{message}"
        connection.send(len(data).to_bytes(8,'big'))
        connection.send(data.encode('utf-8'))

def start_chat():
    host = 'localhost'
    port = 8000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port)) # connected to server

    receive_thread = threading.Thread(target=receive_msgs, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_msg, args=(client_socket,))
    send_thread.start()

if __name__ == '__main__':
    start_chat()
