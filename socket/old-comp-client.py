import socket


def client_program():
    host = '169.254.204.23'  
    port = 5000  

    client_socket = socket.socket()  
    client_socket.connect(('', port)) 

    message = input(" -> ") 

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode()) 
        data = client_socket.recv(1024).decode() 

        print('Received from server: ' + data)

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()