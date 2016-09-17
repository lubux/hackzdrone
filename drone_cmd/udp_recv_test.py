import socket
import struct

UDP_IP = ""
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    print "waiting"
    data, _ = sock.recvfrom(17)
    print data
    print struct.unpack("!xdd", data)