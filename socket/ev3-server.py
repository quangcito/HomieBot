import socket
import ev3dev2.motor as ev3_motor

left_motor = ev3_motor.LargeMotor(ev3_motor.OUTPUT_B)
right_motor = ev3_motor.LargeMotor(ev3_motor.OUTPUT_C)

def server_program():
    host = '0.0.0.0'  
    port = 5000  

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind((host, port))
    
    server_socket.listen(5)
    print("Server is listening...")

    while True:
        client_socket, address = server_socket.accept()
        print("Connection from:", address)

        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break 

            print("Received:", data)
            if data.lower().strip() == 'forward':
                left_motor.on_for_seconds(50, 50, 2, block=False)
                right_motor.on_for_seconds(50, 50, 2, block=False)
            elif data.lower().strip() == 'backward':
                left_motor.on_for_seconds(-50, -50, 2, block=False)
                right_motor.on_for_seconds(-50, -50, 2, block=False)
            # Add more cases for other commands as needed

        client_socket.close()

if __name__ == '__main__':
    server_program()
