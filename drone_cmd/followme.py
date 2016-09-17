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

#Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Tracks GPS position of your computer (Linux only).')
parser.add_argument('--connect',
                   help="vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string, wait_ready=True)

UDP_IP = ""
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

try:
    while True:
        data, _ = sock.recvfrom(17)
        print data
        lat, long = struct.unpack("=xdd", data)

        dest = LocationGlobalRelative(lat, long, 0)
        print "Going to: %s" % dest

        # A better implementation would only send new waypoints if the position had changed significantly
        vehicle.simple_goto(dest)

except socket.error:
    print "Error: gpsd service does not seem to be running, plug in USB GPS or run run-fake-gps.sh"
    sys.exit(1)

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()

print("Completed")