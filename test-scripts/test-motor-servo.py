import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.motor import Motor
from viam.components.movement_sensor import MovementSensor
from viam.components.power_sensor import PowerSensor
from viam.components.sensor import Sensor
from viam.components.servo import Servo

async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key='<YOUR-API-KEY>',
        api_key_id='<YOUR-API-KEY-ID>'
    )
    return await RobotClient.at_address('<YOUR-REMOTE-ADDRESS>', opts)

async def main():
    async with await connect() as machine:
        print('Resources:')
        print(machine.resource_names)

        # motor-1
        motor_1 = Motor.from_robot(machine, "motor-1")
        motor_1_return_value = await motor_1.is_moving()
        print(f"motor-1 is_moving return value: {motor_1_return_value}")

        # Set the power to 40% forwards.
        await motor_1.set_power(power=0.4)

        # Spin the motor at 75 RPM.
        await motor_1.set_rpm(rpm=75)

        # Turn the motor 7.2 revolutions at 60 RPM.
        await motor_1.go_for(rpm=60, revolutions=7.2)

        await motor_1.go_to(rpm=75, position_revolutions=8.3)

        await motor_1.reset_zero_position(offset=0.0)

        position = await motor_1.get_position()
        print(position)

        properties = await motor_1.get_properties()

        # Print out the properties.
        print(f'Properties: {properties}')

        # Check whether the motor is currently running.
        powered = await motor_1.is_powered()

        print('Powered: ', powered)

        # BUG: unimplemented error
        geometries = await motor_1.get_geometries()

        if geometries:
            # Get the center of the first geometry
            print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")

        moving = await motor_1.is_moving()
        print('Moving: ', moving)

        await motor_1.stop()

        # BUG: docommand unimplemented?
        # raise GRPCError(status, message, details)
        # grpclib.exceptions.GRPCError: (<Status.UNKNOWN: 2>, 'DoCommand unimplemented', None)
        command = {"cmd": "test", "data1": 500}
        result = await motor_1.do_command(command)
        print(result)

        my_motor_name= motor_1.get_resource_name("motor_1")
        print(my_motor_name)

        await motor_1.close()

        # movement_sensor-1
        my_movement_sensor = MovementSensor.from_robot(machine, "movement_sensor-1")

        # Get the current linear velocity of the movement sensor.
        lin_vel = await my_movement_sensor.get_linear_velocity()
        print(lin_vel)

        # Get the current angular velocity of the movement sensor.
        ang_vel = await my_movement_sensor.get_angular_velocity()

        # Get the y component of angular velocity.
        y_ang_vel = ang_vel.y
        print(y_ang_vel)

        # Get the current compass heading of the movement sensor.
        heading = await my_movement_sensor.get_compass_heading()
        print(heading)

        # Get the current orientation vector of the movement sensor.
        orientation = await my_movement_sensor.get_orientation()
        print(orientation)

        position = await my_movement_sensor.get_position()
        print(position)

        # properties = await my_movement_sensor.get_properties()
        print(properties)

        accuracy = await my_movement_sensor.get_accuracy()
        print(accuracy)

        lin_accel = await my_movement_sensor.get_linear_acceleration()

        # Get the x component of linear acceleration.
        x_lin_accel = lin_accel.x
        print(x_lin_accel)

        geometries = await my_movement_sensor.get_geometries()

        if geometries:
            # Get the center of the first geometry
            print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")

        readings = await my_movement_sensor.get_readings()
        print(readings)

        command = {"cmd": "test", "data1": 500}
        result = await my_movement_sensor.do_command(command)
        print(result)

        my_movement_sensor_name = my_movement_sensor.get_resource_name("movement_sensor-1")
        print(my_movement_sensor_name)

        await my_movement_sensor.close()

        # power_sensor-1
        my_power_sensor = PowerSensor.from_robot(machine, "power_sensor-1")

        # Get the voltage reading from the power sensor
        voltage, is_ac = await my_power_sensor.get_voltage()
        print("The voltage is", voltage, "V, Is AC:", is_ac)

        # Get the power reading from the power sensor
        power = await my_power_sensor.get_power()
        print("The power is", power, "Watts")

        # Get the current reading from the power sensor
        current, is_ac = await my_power_sensor.get_current()
        print("The current is ", current, " A, Is AC: ", is_ac)

        # Get the readings provided by the sensor.
        readings = await my_power_sensor.get_readings()
        print(readings)

        command = {"cmd": "test", "data1": 500}
        result = await my_power_sensor.do_command(command)
        print(result)

        my_ps_name = my_power_sensor.get_resource_name("power_sensor-1")
        print(my_ps_name)

        await my_power_sensor.close()

        geometries = await power_sensor_1.get_geometries()

        if geometries:
            # Get the center of the first geometry
            print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")

        # sensor-1
        sensor_1 = Sensor.from_robot(machine, "sensor-1")
        sensor_1_return_value = await sensor_1.get_readings()
        print(f"sensor-1 get_readings return value: {sensor_1_return_value}")

        geometries = await sensor_1.get_geometries()

        if geometries:
            # Get the center of the first geometry
            print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")

        # BUG: docommand unimplemented
        command = {"cmd": "test", "data1": 500}
        result = await sensor_1.do_command(command)

        my_sensor_name = sensor_1.get_resource_name("sensor-1")
        print(my_sensor_name)

        await sensor_1.close()

        # servo-1
        my_servo = Servo.from_robot(machine, "servo-1")

        # Move the servo from its origin to the desired angle of 10 degrees.
        await my_servo.move(10)

        # Move the servo from its origin to the desired angle of 90 degrees.
        await my_servo.move(90)

        # Move the servo from its origin to the desired angle of 10 degrees.
        await my_servo.move(10)

        # Get the current set angle of the servo.
        pos1 = await my_servo.get_position()
        print(pos1)

        # Move the servo from its origin to the desired angle of 20 degrees.
        await my_servo.move(20)

        # Get the current set angle of the servo.
        pos2 = await my_servo.get_position()
        print(pos2)

        # Move the servo from its origin to the desired angle of 10 degrees.
        await my_servo.move(10)

        # Stop the servo. It is assumed that the servo stops moving immediately.
        await my_servo.stop()

        print(await my_servo.is_moving())

        command = {"cmd": "test", "data1": 500}
        result = await my_servo.do_command(command)

        geometries = await servo_1.get_geometries()

        if geometries:
            # Get the center of the first geometry
            print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")


if __name__ == '__main__':
    asyncio.run(main())

