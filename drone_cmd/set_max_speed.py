from dronekit import connect, VehicleMode, LocationGlobalRelative
import socket
import time
import sys
import struct

rover = connect('udpout:127.0.0.1:14550', wait_ready=True, heartbeat_timeout=15)

rover.parameters['CRUISE_SPEED']=1
rover.parameters['CRUISE_THROTTLE']=20