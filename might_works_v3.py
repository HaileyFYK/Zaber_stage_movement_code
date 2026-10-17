# %% Imports

import zaber_motion as zm
import zaber_motion.ascii as zm_ascii
import serial.tools.list_ports
import threading

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

# rotation stage (separate adapter)
rotation_port = port_map['rotation_stage']
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


UNITS = {
    'degree': zm.Units.ANGLE_DEGREES,
    'mm':     zm.Units.LENGTH_MILLIMETRES,
}


def move_stage(stage_name, amount, unit, home_if_needed=True, relative=True):
    axis = axes[stage_name]
    zaber_unit = UNITS[unit]
    print(f'{stage_name} home, pos: ', axis.is_homed(), axis.get_position())
    if home_if_needed and not axis.is_homed():
        axis.home()
    if relative:
        axis.move_relative(amount, zaber_unit)
    else:
        axis.move_absolute(amount, zaber_unit)


t1 = threading.Thread(target=move_stage, args=('rotation_stage', 20, 'degree'))
t2 = threading.Thread(target=move_stage, args=('linear_stage', 5, 'mm'))

t1.start()
t2.start()

t1.join()
t2.join()

for conn in connections.values():
    conn.close()