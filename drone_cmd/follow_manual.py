#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
followme - Tracks GPS position of your computer (Linux only).

This example uses the python gps package to read positions from a GPS attached to your
laptop and sends a new vehicle.simple_goto command every two seconds to move the
vehicle to the current point.

When you want to stop follow-me, either change vehicle modes or type Ctrl+C to exit the script.

Example documentation: http://python.dronekit.io/examples/follow_me.html
"""

from dronekit import connect, VehicleMode, LocationGlobalRelative
from qrtools import QR
import socket
import time
import sys
import struct
import os
import picamera
import threading
import math
from threading import Timer



END = False
SECRET = "Banana!!"

os.popen("sudo -S %s"%("./banana/PiBits/ServoBlaster/user/servod"), 'w').write('hack')
os.popen("sudo -S %s"%("echo P1-12=20% > /dev/servoblaster"), 'w').write('hack')

rover = connect('udpout:127.0.0.1:14550', wait_ready=True, heartbeat_timeout=15)
rover.mode = VehicleMode("GUIDED")
rover.armed = True



UDP_IP = ""
UDP_IP_S = "255.255.255.255"
UDP_PORT = 8080
LAT, LONG = 0.0, 0.0

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

class locationThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name

        while not END:
            if rover.mode == VehicleMode("MANUAL"):
                curlat, curlong = rover.location.global_frame.lat, rover.location.global_frame.lon
                heading = rover.heading

                d_lat = LAT - curlat
                d_lon = LONG - curlong

                alpha = math.atan2(d_lat, d_lon)*180.0/math.pi
                if alpha < 0:
                    alpha += 360
                #total_dist = math.sqrt(d_lat*d_lat + d_lon*d_lon)

                d_alpha = alpha - heading
                if d_alpha < -180:
                    d_alpha += 360
                if d_alpha > 180:
                    d_alpha -= 360

                print heading, alpha, d_alpha

                steering = d_alpha * 5 + 1512
                if abs(d_alpha) < 6:
                    steering = d_alpha * 3 + 1512
                if steering < 1200:
                    steering = 1200
                if steering > 1800:
                    steering = 1800

                rc_steer = steering
                dist = rover.rangefinder.distance
                rc_throttle = 1490 - dist*50
                if rc_throttle < 1440:
                  rc_throttle = 1440
                rover.channels.overrides['1'] = rc_steer
                rover.channels.overrides['3'] = rc_throttle
            time.sleep(0.5)

        print "Exiting " + self.name

def wait_QR_code():
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(0.8)
        while True:
            print "take pic"
            camera.capture('QR.jpg')
            myCode = QR(filename=u"QR.jpg")
            if myCode.decode():
                print myCode.data
                if myCode.data == SECRET:
                    return
            time.sleep(0.1)

try:
    locThread = locationThread(1, "locThread", 1)
    locThread.start()
    while True:
        print "waiting..."
        data, _ = sock.recvfrom(17)
        print data
        if bytearray(data)[0] == 2:
            print "Stopped"
            rover.mode = VehicleMode("HOLD")
            wait_QR_code()
            Timer(5.0, os.popen("sudo -S %s"%("echo P1-12=20% > /dev/servoblaster"), 'w').write('hack')).start()
            send_ok_msg()
        elif bytearray(data)[0] == 1:
            os.popen("sudo -S %s"%("echo P1-12=20% > /dev/servoblaster"), 'w').write('hack')
            LAT, LONG = struct.unpack("!xdd", data)
            print "lat long:", LAT, LONG
            rover.mode = VehicleMode("MANUAL")

except socket.error:
    print socket.error.strerror
    print "Error: gpsd service does not seem to be running, plug in USB GPS or run run-fake-gps.sh"
    sys.exit(1)

#Close vehicle object before exiting script
print "Close vehicle object"
END = True
rover.close()

print("Completed")
