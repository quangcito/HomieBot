import socket
from ev3dev2.sound import Sound

sound = Sound()


def introduce_homiebot():
    """
    Introduces HomieBot with a greeting message.
    """
    intro_message = "What's up dog, my name is HomieBot and my perogative is to be your homie. Let's chat! What is your name?"
    sound.speak(intro_message)

def server_program():
    host = '0.0.0.0'  
    port = 5043 

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind((host, port))
    
    server_socket.listen(5)
    print("Server is listening...")
    while True:
        client_socket, address = server_socket.accept()
        print("Connection from:", address)

        introduce_homiebot()
        
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break 

            print("Received:", data)
            sound.speak(data)

        client_socket.close()

if __name__ == '__main__':
    server_program()
