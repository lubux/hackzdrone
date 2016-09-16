import dronekit_sitl
from dronekit import connect, VehicleMode

sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()


#vehicle = connect(connection_string, wait_ready=True)
vehicle = connect("/dev/ttyAMA0", baud=57600, wait_ready=True)



