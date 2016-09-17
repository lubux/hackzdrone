import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = struct.pack("=cdd", '1', 3.434, 5343.4232)

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


while True:
    data, _ = sock.recvfrom(17)
    lat, long = struct.unpack("=xdd", data)
    print "received message:", lat, long