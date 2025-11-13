import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.gantry import Gantry
from viam.components.gripper import Gripper
from viam.components.generic import Generic
from viam.components.input import Controller, Control, EventType

async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key='<API-KEY>',
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address('<REMOTE-ADDRESS>', opts)

# Define a function to handle pressing the Start Menu Button "BUTTON_START" on
# your controller, printing out the start time.
def print_start_time(event):
    print(f"Start Menu Button was pressed at this time: {event.time}")


# Define a function that handles the controller.
async def handle_controller(controller):
    # Get the list of Controls on the controller.
    controls = await controller.get_controls()

    # If the "BUTTON_START" Control is found, register the function
    # print_start_time to fire when "BUTTON_START" has the event "ButtonPress"
    # occur.
    if Control.BUTTON_START in controls:
        controller.register_control_callback(
            Control.BUTTON_START, [EventType.BUTTON_PRESS], print_start_time)
    else:
        print("Oops! Couldn't find the start button control! Is your "
            "controller connected?")
        exit()

    while True:
        await asyncio.sleep(1.0)

async def main():
    async with await connect() as machine:
        # gantry-1
        my_gantry = Gantry.from_robot(machine, "gantry-1")

        # Get the current positions of the axes of the gantry in millimeters.
        positions = await my_gantry.get_position()
        print(f"positions: {positions}")

        # Create a list of positions for the axes of the gantry to move to. Assume in
        # this example that the gantry is multi-axis, with 3 axes.
        examplePositions = [1, 2, 3]

        exampleSpeeds = [3, 9, 12]

        # Move the axes of the gantry to the positions specified.
        await my_gantry.move_to_position(
            positions=examplePositions, speeds=exampleSpeeds)

        # Get the lengths of the axes of the gantry in millimeters.
        lengths_mm = await my_gantry.get_lengths()
        print(f"lengths: {lengths_mm}")

        await my_gantry.home()

        # Unimplemented
        geometries = await my_gantry.get_geometries()

        if geometries:
            # Get the center of the first geometry
            print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")

        # Print if the gantry is currently moving.
        print(await my_gantry.is_moving())

        await my_gantry.stop()

        # Unimplemented
        command = {"cmd": "test", "data1": 500}
        result = await my_gantry.do_command(command)
        print(result)

        my_gantry_name = Gantry.get_resource_name("gantry_1")
        print(f"Gantry resource name: {my_gantry_name}")

        await my_gantry.close()

        my_generic_component = Generic.from_robot(machine, "generic-1")

        command = {"cmd": "test", "data1": 500}
        result = await my_generic_component.do_command(command)
        print(result)

        # Unimplemented
        geometries = await my_generic_component.get_geometries()

        if geometries:
            # Get the center of the first geometry
            print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")

        my_generic_component_name = Generic.get_resource_name("my_generic_component")
        print(my_generic_component_name)

        await my_generic_component.close()

        # gripper-1
        my_gripper = Gripper.from_robot(machine, "gripper-1")

        # Open the gripper.
        await my_gripper.open()

        # Grab with the gripper.
        grabbed = await my_gripper.grab()
        print(f"Grabbed: {grabbed}")

        # Check whether the gripper is currently moving.
        moving = await my_gripper.is_moving()
        print('Moving:', moving)

        # Stop the gripper.
        await my_gripper.stop()

        geometries = await my_gripper.get_geometries()

        if geometries:
            # Get the center of the first geometry
            print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")

        command = {"cmd": "test", "data1": 500}
        result = await my_gripper.do_command(command)
        print(result)

        my_gripper_name = Gripper.get_resource_name("my_gripper")
        print(my_gripper_name)

        await my_gripper.close()

        # input_controller-1
        my_controller = Controller.from_robot(machine, "input_controller-2")

        # Get the list of Controls provided by the controller.
        controls = await my_controller.get_controls()

        # Print the list of Controls provided by the controller.
        print(f"Controls: {controls}")

        # Get the most recent Event for each Control.
        recent_events = await my_controller.get_events()

        # Print out the most recent Event for each Control.
        print(f"Recent Events: {recent_events}")

        geometries = await my_controller.get_geometries()

        if geometries:
            # Get the center of the first geometry
            print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")

        # Run the handleController function.
        await handle_controller(my_controller)

        command = {"cmd": "test", "data1": 500}
        result = await my_controller.do_command(command)
        print(result)

        my_input_controller_name = Controller.get_resource_name("my_input_controller")
        print(my_input_controller_name)

        await my_controller.close()


if __name__ == '__main__':
    asyncio.run(main())

