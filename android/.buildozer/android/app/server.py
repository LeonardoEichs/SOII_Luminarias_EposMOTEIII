import socket
import sys
import os
import serial
import atexit

ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
        )

ser.isOpen()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('localhost', 10003)
print("Starting up  on {} port {}".format(server_address[0], server_address[1]))
sock.bind(server_address)

sock.listen(1)
fd = os.open("/dev/ttyACM0", os.O_RDWR)
while True:
    print("Waiting for a connection")
    connection, client_address = sock.accept()

    try:
        print("Connection from " + str(client_address))
        while True:
            data = connection.recv(32)
            print("Received " + str(data))
            if data:
                print("Sending data back to the client")
                ser.write(str(data))
                connection.sendall(data)
            else:
                print("No more data")
                break

    finally:
        connection.close()

def exit_handler():
    print("Closing serial")
    ser.close()
atexit.register(exit_handler)
