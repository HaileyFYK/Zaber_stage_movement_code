# %% Imports
import zaber_motion as zm
import zaber_motion.ascii as zm_ascii
import serial.tools.list_ports
import threading
import random


# %% Detect hardware
name_map = {'X-MCC4 (rev 2/3)': 'stage_controller',
           'X-RSW60A-E03': 'rotation_stage',
           'LSA25A-T4A': 'linear_stage'}

port_map = {n: None for n in name_map.values()}
available_ports = [p.device for p in serial.tools.list_ports.comports()]

for port in available_ports:
   try:
       with zm_ascii.Connection.open_serial_port(port) as connection:
           connection.enable_alerts()
           try:
               device_list = connection.detect_devices()
               for device in device_list:
                   if device.name in name_map:
                       if 'controller' in name_map[device.name]:
                           output = {}
                           for axis_number in range(1, device.axis_count + 1):
                               axis = device.get_axis(axis_number)
                               if axis.peripheral_name != "Unused":
                                   output[name_map[axis.peripheral_name]] = \
                                       (port, axis_number)
                       else:
                           output = port
                       port_map[name_map[device.name]] = output
           except zm.NoDeviceFoundException:
               pass
   except zm.ConnectionFailedException:
       pass


connections = {}
axes = {}


# rotation stage
rotation_port= port_map['rotation_stage']
connections['rotation'] = zm_ascii.Connection.open_serial_port(rotation_port)
connections['rotation'].enable_alerts()
rotation_device_list = connections['rotation'].detect_devices()
axes['rotation_stage'] = rotation_device_list[0].get_axis(1)


# controller
controller_port = next(iter(port_map['stage_controller'].values()))[0]
connections['controller'] = zm_ascii.Connection.open_serial_port(controller_port)
connections['controller'].enable_alerts()
controller_device_list = connections['controller'].detect_devices()
controller_device = controller_device_list[0]


for peripheral_name, (_, axis_number) in port_map['stage_controller'].items():
   axes[peripheral_name] = controller_device.get_axis(axis_number)




for axis in axes.values():
   if not axis.is_homed():
       axis.home()


UNITS = {
   'degree': zm.Units.ANGLE_DEGREES,
   'mm':     zm.Units.LENGTH_MILLIMETRES,
}


def move_stage(stage_name, amount, unit, home_if_needed=True, relative=True):
   axis = axes[stage_name]
   zaber_unit = UNITS[unit]
   print(f'{stage_name} pos: ', axis.get_position())
   if relative:
       axis.move_relative(amount, zaber_unit)
   else:
       axis.move_absolute(amount, zaber_unit)


def linear_motion():
   for i in range(20): #move stage through 20 positions 
       move_stage(
           "linear_stage",
           i * 1, #move in 1mm increments
           "mm",
           relative=False
       )


def circular_motion():
   for angle in range(0, 360, 10): #(start at 0 degree, stop before 360, and 10 degrees increments)
       move_stage(
           "rotation_stage",
           angle,
           "degree",
           relative=False
       )


def linear_circular_motion(): #a cruve line continuously movement
    t1 = threading.Thread(target=move_stage,
        args=("linear_stage", 20, "mm"),
        kwargs={"relative": False}
    )

    t2 = threading.Thread(
        target=move_stage,
        args=("rotation_stage", 150, "degree"),
        kwargs={"relative": True}
    )

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def brownian_motion():
    # Start at the middle of the linear travel range
    linear = 5
    angle = 0

    # Perform a small number of random movements
    for _ in range(5):

        # Random step forward or backward
        linear += random.uniform(-1.5, 1.5)

        # Keep the linear stage between 0 and 10 mm
        linear = max(0, min(10, linear))

        # Random rotation
        angle += random.uniform(-30, 30)

        # Keep rotation within a reasonable range
        angle = max(-180, min(180, angle))

        t1 = threading.Thread(
            target=move_stage,
            args=("linear_stage", linear, "mm"),
            kwargs={"relative": False}
        )

        t2 = threading.Thread(
            target=move_stage,
            args=("rotation_stage", angle, "degree"),
            kwargs={"relative": False}
        )

        t1.start()
        t2.start()

        t1.join()
        t2.join()



def spiral_motion():
   for i in range(10):
       linear = i * 1
       angle = i * 20
       t1 = threading.Thread(
           target=move_stage,
           args=("linear_stage", linear, "mm"),
           kwargs={"relative":False}
       )
       t2 = threading.Thread(
           target=move_stage,
           args=("rotation_stage", angle, "degree"),
           kwargs={"relative":False}
       )
       t1.start()
       t2.start()

       t1.join()
       t2.join()


def random_back_forth():
   position = 0
   for i in range(20):
       position += random.choice([-1,1]) * 0.5
       move_stage(
           "linear_stage",
           position,
           "mm",
           relative=False
       )
       

"""Choose pattern here, delete the # sign in the front """
#linear_motion()
#circular_motion()
#linear_circular_motion()
#brownian_motion()
#spiral_motion()
random_back_forth()



for conn in connections.values():
   conn.close()



