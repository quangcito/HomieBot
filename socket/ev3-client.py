import socket
import ev3dev2.motor as ev3_motor

left_motor = ev3_motor.LargeMotor(ev3_motor.OUTPUT_C)
right_motor = ev3_motor.LargeMotor(ev3_motor.OUTPUT_B)

def client_program():
    host = '169.254.184.97' 
    port = 5000  

    client_socket = socket.socket()  
    client_socket.connect((host, port))   

    while True:
        message = client_socket.recv(1024).decode() 
        
        if message.lower().strip() == 'forward':
            left_motor.on_for_seconds(50, 50, 2, block=False)
            right_motor.on_for_seconds(50, 50, 2, block=False)
        elif message.lower().strip() == 'backward':
            left_motor.on_for_seconds(-50, -50, 2, block=False)
            right_motor.on_for_seconds(-50, -50, 2, block=False)

    # client_socket.close() 

if __name__ == '__main__':
    client_program()
