# :snippet-start: add-metadata-location
import asyncio
import time
# :remove-start:
import os
# :remove-end:

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.robot.client import RobotClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
LOCATION_ID = ""  # the ID of the location you want to add metadata to

# :remove-start:
API_KEY = os.environ["VIAM_API_KEY"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]
LOCATION_ID = "pg5q3j3h95"
# :remove-end:

async def connect() -> ViamClient:
    """Establish a connection to the Viam client using API credentials."""
    dial_options = DialOptions(
        credentials=Credentials(
            type="api-key",
            payload=API_KEY,
        ),
        auth_entity=API_KEY_ID
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main() -> int:

    async with await connect() as viam_client:
        app_client = viam_client.app_client

        await app_client.update_location_metadata(location_id=LOCATION_ID, metadata={
            "TEST_API_KEY": "ABC123",
        })

        # :remove-start:
        metadata = await app_client.get_location_metadata(location_id=LOCATION_ID)
        assert metadata["TEST_API_KEY"] == "ABC123"
        await app_client.update_location_metadata(location_id=LOCATION_ID, metadata={})
        metadata = await app_client.get_location_metadata(location_id=LOCATION_ID)
        assert not metadata
        # :remove-end:
        return 0

if __name__ == "__main__":
    asyncio.run(main())
# :snippet-end: