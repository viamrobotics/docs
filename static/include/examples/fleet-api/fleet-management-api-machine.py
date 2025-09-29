import asyncio
import os
import time

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.proto.app import Authorization
from viam.proto.app import AuthorizedPermissions
from viam.proto.app.packages import PackageType
from viam.proto.app import Visibility, RegistryItemStatus
from viam.proto.app import Model, ModuleFileInfo
from viam.app.app_client import APIKeyAuthorization

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
ORG_ID = ""  # Organization ID, find or create in your organization settings
EMAIL_ADDRESS = ""  # Email address of the user to get the user id for
LOCATION_ID = ""  # Location ID, find or create in your organization settings

# :remove-start:
ORG_ID = os.environ["TEST_ORG_ID"]
ORG_ID_2 = "b5e9f350-cbcf-4d2a-bbb1-a2e2fd6851e1"
API_KEY = os.environ["VIAM_API_KEY"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]
LOCATION_ID = "pg5q3j3h95"
TEST_EMAIL = os.environ["TEST_EMAIL"]
MACHINE_ID = "5ec7266e-f762-4ea8-9c29-4dd592718b48"
PART_ID = "deb8782c-7b48-4d35-812d-2caa94b61f77"
# :remove-end:

async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        payload=API_KEY,
      ),
      # Replace "<API-KEY-ID>" (including brackets) with your machine's
      # API key ID
      auth_entity=API_KEY_ID
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main():

    # Make a ViamClient
    viam_client = await connect()
    # Instantiate an AppClient called "cloud"
    # to run fleet management API methods on
    cloud = viam_client.app_client

    robot = await cloud.get_robot(robot_id=MACHINE_ID)
    assert robot.id == MACHINE_ID

    api_keys = await cloud.get_robot_api_keys(robot_id=MACHINE_ID)
    assert len(api_keys) >= 1
    assert api_keys[0].authorizations[0].resource_id == MACHINE_ID

    list_of_parts = await cloud.get_robot_parts(
        robot_id=MACHINE_ID
    )
    assert len(list_of_parts) == 1
    assert list_of_parts[0].id == PART_ID

    my_robot_part = await cloud.get_robot_part(
      robot_part_id=PART_ID)
    assert my_robot_part.id == PART_ID

    part_logs = await cloud.get_robot_part_logs(
        robot_part_id=PART_ID, num_log_entries=5
    )
    assert len(part_logs) == 5

    logs_stream = await cloud.tail_robot_part_logs(
        robot_part_id=PART_ID
    )
    assert logs_stream is not None

    part_history = await cloud.get_robot_part_history(
        robot_part_id=PART_ID
    )
    assert len(part_history) >= 1

    new_part_id = await cloud.new_robot_part(
        robot_id=MACHINE_ID, part_name="new-part"
    )
    assert new_part_id is not None
    list_of_parts = await cloud.get_robot_parts(
        robot_id=MACHINE_ID
    )
    assert len(list_of_parts) == 2

    await cloud.mark_part_as_main(
        robot_part_id=new_part_id
    )
    new_machine_part = await cloud.get_robot_part(
        robot_part_id=new_part_id
    )
    assert new_machine_part.main_part == True
    await cloud.mark_part_as_main(
        robot_part_id=PART_ID
    )
    old_machine_part = await cloud.get_robot_part(
        robot_part_id=PART_ID
    )
    assert old_machine_part.main_part == True

    await cloud.mark_part_for_restart(
        robot_part_id=new_part_id
    )

    part_with_new_secret = await cloud.create_robot_part_secret(
        robot_part_id=new_part_id
    )
    assert part_with_new_secret is not None
    assert part_with_new_secret.id == new_part_id

    await cloud.delete_robot_part_secret(
        robot_part_id=new_part_id,
        secret_id=part_with_new_secret.secrets[0].id)

    await cloud.delete_robot_part(
        robot_part_id=new_part_id
    )
    list_of_parts = await cloud.get_robot_parts(
        robot_id=MACHINE_ID
    )
    assert len(list_of_parts) == 1


    list_of_machines = await cloud.list_robots(location_id=LOCATION_ID)
    len_machines = len(list_of_machines)
    assert len_machines >= 1
    assert list_of_machines[0].id == MACHINE_ID

    new_machine_id = await cloud.new_robot(name="test-robot", location_id=LOCATION_ID)
    assert new_machine_id is not None
    list_of_machines = await cloud.list_robots(location_id=LOCATION_ID)
    assert len(list_of_machines) == len_machines + 1

    updated_machine = await cloud.update_robot(
      robot_id=new_machine_id,
      name="test-robot-new-name",
      location_id=LOCATION_ID
    )
    assert updated_machine.name == "test-robot-new-name"

    await cloud.delete_robot(robot_id=new_machine_id)
    list_of_machines = await cloud.list_robots(location_id=LOCATION_ID)
    assert len(list_of_machines) == len_machines

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
