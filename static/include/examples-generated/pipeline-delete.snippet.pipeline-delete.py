import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.gen.app.data.v1.data_pb2 import TabularDataSourceType


# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
PIPELINE_ID = ""


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
        data_client = viam_client.data_client

        await data_client.delete_data_pipeline(PIPELINE_ID)
        print(f"Pipeline deleted with ID: {PIPELINE_ID}")

        return 0

if __name__ == "__main__":
    asyncio.run(main())
