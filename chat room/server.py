import socket
import threading

# Connection Data
host_address = '127.0.0.1'
port_number = 7000

# Starting Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_address, port_number))
server_socket.listen()

# Lists For Clients and Their Usernames
connected_clients = []
usernames = []

# Sending Messages To All Connected Clients
def broadcast(message, current_client):
    for client in connected_clients:
        if client == current_client:
            continue
        client.send(message)
        
# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message, client)
        except:
            # Removing And Closing Clients
            index = connected_clients.index(client)
            connected_clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast('{} left!'.format(username).encode('ascii'), client)
            usernames.remove(username)
            break
        
# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client_socket, client_address = server_socket.accept()
        print("Connected with {}".format(str(client_address)))

        # Request And Store Username
        client_socket.send('USERNAME'.encode('ascii'))
        username = client_socket.recv(1024).decode('ascii')
        usernames.append(username)
        connected_clients.append(client_socket)

        # Print And Broadcast Username
        print("Username is {}".format(username))
        broadcast("{} joined!".format(username).encode('ascii'), client_socket)
        client_socket.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client_socket,))
        thread.start()

# Start the receive function in a separate thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()
