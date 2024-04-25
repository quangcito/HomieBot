import socket

def client_program():
    host = '169.254.184.97'  # Replace w EV3 IP
    port = 5000   

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))
    print("Connected to EV3 robot server.")

    try:
        while True:
            message = input("Enter command (e.g., 'forward', 'backward', 'stop'): ")

            # Send the command to the server
            client_socket.send(message.encode())

            # Receive the response from the server
            data = client_socket.recv(1024).decode()
            print("Received:", data)
    except KeyboardInterrupt:
        print("Closing connection...")
    finally:
        client_socket.close()

if __name__ == '__main__':
    client_program()
