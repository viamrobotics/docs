import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
DATASET_ID = ""  # the ID of the dataset you want to add the image to
BINARY_DATA_ID = ""  # the ID of the image you want to add to the dataset


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
    viam_client = await connect()
    data_client = viam_client.data_client


    print("Adding image to dataset...")
    await data_client.add_binary_data_to_dataset_by_ids(
        binary_ids=[BINARY_DATA_ID],
        dataset_id=DATASET_ID
    )

    viam_client.close()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
