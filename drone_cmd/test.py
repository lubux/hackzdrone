import dronekit_sitl
from dronekit import connect, VehicleMode

#sitl = dronekit_sitl.start_default()
#connection_string = sitl.connection_string()


#vehicle = connect(connection_string, wait_ready=True)
#vehicle = connect("/dev/ttyAMA0", baud=57600, wait_ready=True)
import socket

UDP_IP = ""
UDP_IP_S = "255.255.255.255"
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


def send_ok_msg():
    print "SEND OK SCAN MESSAGE"
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(bytearray([3]), (UDP_IP_S, UDP_PORT))

send_ok_msg()