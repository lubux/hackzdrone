"""
Older main file with dronekit follower, deprecated
"""

from dronekit import connect, VehicleMode, LocationGlobalRelative
from qrtools import QR
import socket
import time
import sys
import struct
import os
import picamera

SECRET = "Banana!!"

os.popen("sudo -S %s"%("./banana/PiBits/ServoBlaster/user/servod"), 'w').write('hack')
os.popen("sudo -S %s"%("echo P1-12=20% > /dev/servoblaster"), 'w').write('hack')

rover = connect('udpout:127.0.0.1:14550', wait_ready=True, heartbeat_timeout=15)
rover.mode = VehicleMode("GUIDED")
rover.armed = True

UDP_IP = ""
UDP_IP_S = "255.255.255.255"
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


def send_ok_msg():
    print "SEND OK SCAN MESSAGE"
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto( bytearray([3]), (UDP_IP_S, UDP_PORT))


def send_err_msg():
    print "SEND ERROR SCAN MESSAGE"
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto( bytearray([4]), (UDP_IP_S, UDP_PORT))


def wait_QR_code():
    print "TEST2"
    with picamera.PiCamera() as camera:
        print "TEST2.5"
        camera.start_preview()
        time.sleep(1)
        print "TEST3"
        while True:
            print "take pic"
            camera.capture('QR.jpg')
            myCode = QR(filename=u"QR.jpg")
            if myCode.decode():
                print myCode.data
                if myCode.data == SECRET:
                    return

try:
    while True:
        print "waiting..."
        data, _ = sock.recvfrom(17)
        print data
        if bytearray(data)[0] == 2:
            print "Stopped"
            rover.mode = VehicleMode("HOLD")
            wait_QR_code()
            os.popen("sudo -S %s"%("echo P1-12=80% > /dev/servoblaster"), 'w').write('hack')
            send_ok_msg()
        elif bytearray(data)[0] == 1:
            os.popen("sudo -S %s"%("echo P1-12=20% > /dev/servoblaster"), 'w').write('hack')
            rover.mode = VehicleMode("GUIDED")
            lat, long = struct.unpack("!xdd", data)
            print "lat long:", lat, long
            dest = LocationGlobalRelative(lat, long, 0)
            print "Going to: %s" % dest

            # A better implementation would only send new waypoints if the position had changed significantly
            rover.simple_goto(dest, 0.4, 0.4)

except socket.error:
    print "Error: gpsd service does not seem to be running, plug in USB GPS or run run-fake-gps.sh"
    sys.exit(1)

#Close vehicle object before exiting script
print "Close vehicle object"
rover.close()

print("Completed")
