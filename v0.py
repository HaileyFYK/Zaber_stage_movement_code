#72 degrees
#2 mm


from zaber_motion import Units
from zaber_motion.ascii import Connection

with Connection.open_serial_port("COM3") as connection:
    connection.enable_alters()

    device_list = connection.detect_devices()
    print("Found {} devices:".format(len(device_list)))

    device = device_list[0]
    axis = device.get_axis(1)
    rotation_axis = device.get_axis(2)

    if not axis.is_homed():
        axis.home()
    if not rotation_axis.is_homed():
        rotation_axis.home()

    # Move both axes simultaneously to (72 degrees, 2 mm)
    axis.move_absolute(72, Units.ANGLE_DEGREES, wait_until_idle=False)
    rotation_axis.move_absolute(2, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
    # Wait for both movements to complete
    axis.wait_until_idle()
    rotation_axis.wait_until_idle()
