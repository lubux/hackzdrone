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

SECRET = "Banana!!"

os.popen("sudo -S %s"%("./banana/PiBits/ServoBlaster/user/servod"), 'w').write('hack')
os.popen("sudo -S %s"%("echo P1-12=20% > /dev/servoblaster"), 'w').write('hack')

rover = connect('udpout:127.0.0.1:14550', wait_ready=True, heartbeat_timeout=15)
rover.mode = VehicleMode("GUIDED")
rover.armed = True


UDP_IP = ""
UDP_PORT = 8080
LAT, LONG = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

class locationThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name

        while True:
            if rover.mode == VehicleMode("MANUAL"):
                print ""
                curlat, curlong = rover.location.global_frame.lat, rover.location.global_frame.long
                heading = rover.heading

                d_lat = LAT-curlat
                d_lon = LONG-curlong

                alpha = math.atan2(d_lat, d_lon)*180/math.pi
                #total_dist = math.sqrt(d_lat*d_lat + d_lon*d_lon)

                d_alpha = alpha-heading
                if d_alpha < -180:
                    d_alpha += 180

                steering = d_alpha * 5 + 1512
                if abs(d_alpha) < 6:
                    steering = d_alpha * 3 + 1512
                if steering < 1200:
                    steering = 1200
                if steering > 1800:
                    steering = 1800

                rc_steer = steering
                dist = rover.rangefinder.distance
                rc_throttle = 1512 - dist*50
                if rc_throttle < 1440:
                  rc_throttle = 1440
                rover.channels.overrides['1'] = rc_steer
                rover.channels.overrides['3'] = rc_throttle

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
            os.popen("sudo -S %s"%("echo P1-12=80% > /dev/servoblaster"), 'w').write('hack')
        else:
            os.popen("sudo -S %s"%("echo P1-12=20% > /dev/servoblaster"), 'w').write('hack')
            LAT, LONG = struct.unpack("!xdd", data)
            print "lat long:", LAT, LONG
            rover.mode = VehicleMode("MANUAL")

except socket.error:
    print "Error: gpsd service does not seem to be running, plug in USB GPS or run run-fake-gps.sh"
    sys.exit(1)

#Close vehicle object before exiting script
print "Close vehicle object"
locationThread.join()
rover.close()

print("Completed")
