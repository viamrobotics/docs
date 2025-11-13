# :snippet-start: add-to-dataset
import asyncio
# :remove-start:
import os
import time
# :remove-end:

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
DATASET_ID = ""  # the ID of the dataset you want to add the image to
BINARY_DATA_ID = ""  # the ID of the image you want to add to the dataset

# :remove-start:
DATASET_NAME = "test-" + time.strftime("%Y%m%d%H%M%S")
ORG_ID = os.environ["TEST_ORG_ID"]
API_KEY = os.environ["VIAM_API_KEY"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]
BINARY_DATA_ID = "83da9642-3785-4db3-9d60-a3662a03bb04/cj53ft1jy1/fJFzEoxrv459YUxbH3gC9YNzgm8SfEjyLt70aNJbL1GxOovyU7gf69vQSCcMNNV5"
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
        data_client = viam_client.data_client
        # :remove-start:
        print("Creating dataset...")
        try:
            DATASET_ID = await data_client.create_dataset(
                name=DATASET_NAME,
                organization_id=ORG_ID,
            )
            print(f"Created dataset: {DATASET_ID}")
        except Exception as e:
            print("Error creating dataset. It may already exist.")
            print("See: https://app.viam.com/data/datasets")
            print(f"Exception: {e}")
            return 1
        # :remove-end:

        print("Adding image to dataset...")
        await data_client.add_binary_data_to_dataset_by_ids(
            binary_ids=[BINARY_DATA_ID],
            dataset_id=DATASET_ID
        )

        # :remove-start:
        # Teardown - delete the dataset
        await data_client.delete_dataset(DATASET_ID)
        print(f"Deleted dataset: {DATASET_ID}")
        # :remove-end:
        return 0

if __name__ == "__main__":
    asyncio.run(main())
# :snippet-end: