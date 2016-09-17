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
import socket
import time
import sys
import struct

rover = connect('udpout:127.0.0.1:14550', wait_ready=True, heartbeat_timeout=15)
rover.mode = VehicleMode("GUIDED")
rover.armed = True


UDP_IP = ""
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


try:
    while True:
        print "waiting..."
        data, _ = sock.recvfrom(17)
        print data
        lat, long = struct.unpack("!xdd", data)
        print "lat long:", lat, long
        dest = LocationGlobalRelative(lat, long, 0)
        print "Going to: %s" % dest

        # A better implementation would only send new waypoints if the position had changed significantly
        rover.simple_goto(dest)

except socket.error:
    print "Error: gpsd service does not seem to be running, plug in USB GPS or run run-fake-gps.sh"
    sys.exit(1)

#Close vehicle object before exiting script
print "Close vehicle object"
rover.close()

print("Completed")