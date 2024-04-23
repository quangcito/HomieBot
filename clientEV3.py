import socket
import ev3dev2.motor as ev3_motor

# Initialize motors
left_motor = ev3_motor.LargeMotor(ev3_motor.OUTPUT_B)
right_motor = ev3_motor.LargeMotor(ev3_motor.OUTPUT_C)

def client_program():
    host = '172.20.10.2'  # IP address of the server
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    while True:
        message = client_socket.recv(1024).decode()  # receive response from server

        # Process message and control EV3 motors accordingly
        if message.lower().strip() == 'forward':
            left_motor.on_for_seconds(50, 50, 2, block=False)
            right_motor.on_for_seconds(50, 50, 2, block=False)
        elif message.lower().strip() == 'backward':
            left_motor.on_for_seconds(-50, -50, 2, block=False)
            right_motor.on_for_seconds(-50, -50, 2, block=False)
        # Add more cases for other commands as needed

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()
