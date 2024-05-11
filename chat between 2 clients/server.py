import socket
import threading
import ast

def handle_client(session, address):
    while True:
        try:
            size_bytes = session.recv(8)
            size = int.from_bytes(size_bytes, 'big')
            data = session.recv(size).decode('utf-8')
            if not data:
                break
            print(f"Received from {address}: {data} : with size {size}")

            # Extract the recipient client's address from the message
            recipient_address, message = data.split(':', 1)

            # Find the recipient client's socket
            recipient_socket = None
            for user in users:
                if user[1] == ast.literal_eval(recipient_address): 
                    recipient_socket = user[0]
                    break
            if recipient_socket:
                # Send the message to the recipient client
                recipient_socket.send(size_bytes)
                recipient_socket.send(message.encode('utf-8'))
            else:
                print(f"Recipient not found: {recipient_address}")

        except socket.error:
            break

    print(f"Connection closed with {address}")
    users.remove((session, address))
    session.close()

def start_server():
    server_host = 'localhost'
    server_port = 8000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"Server started on {server_host}:{server_port}")
    while True:
        session, address = server_socket.accept()
        users.append((session, address))
        print(f"Connected with {address}")
        threading.Thread(target=handle_client, args=(session, address)).start()

if __name__ == '__main__':
    users = []
    start_server()
