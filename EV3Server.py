# ------- #
# Author - Duy Huynh
# Modified by - Devinn Chi, Arnika Abeysekera, Quang Nguyen 
# ------- #


# Install dependencies --> "pip install -r requirements.txt"


# import statements
import socket
from ev3dev2.sound import Sound


# create sound object
sound = Sound()


def introduce_homiebot():
    """
    Introduces HomieBot with a greeting message.
    """
    intro_message = "What's up dog, my name is HomieBot and my perogative is to be your homie. Let's chat! What is your name?"
    sound.speak(intro_message)


def server_program():
    """
    Creates socket connection for pc client. Runs Homiebot program
    inside of while loop
    """

    # initialize host ip and port number
    host = '0.0.0.0'  
    port = 5043 

    # create socket connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # bind host to port 
    server_socket.bind((host, port))
    
    # listen for client connections
    server_socket.listen(5)
    print("Server is listening...")

    # connect to client and print address
    while True:
        client_socket, address = server_socket.accept()
        print("Connection from:", address)

        # speak homiebot intro (handles EV3 speak)
        introduce_homiebot()
        
        # recieve data from user recorded audio
        while True:
            data = client_socket.recv(1024).decode()

            # if data invalid, break
            if not data:
                break 
            
            # if data valid, EV3 speak data / print OLlama response
            print("Received:", data)
            sound.speak(data)

        # close socket connection
        client_socket.close()

# run main program
if __name__ == '__main__':
    server_program()
