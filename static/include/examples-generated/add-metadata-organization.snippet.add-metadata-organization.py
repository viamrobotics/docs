import asyncio
import time

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.robot.client import RobotClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
ORG_ID = ""  # the ID of the organization you want to add metadata to


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

        await app_client.update_organization_metadata(org_id=ORG_ID, metadata={
            "TEST_API_KEY": "ABC123",
        })

        return 0

if __name__ == "__main__":
    asyncio.run(main())
