# :snippet-start: create-dataset
import asyncio
# :remove-start:
import os
import time
# :remove-end:

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

# Configuration constants – replace with your actual values
DATASET_NAME = ""  # a unique, new name for the dataset you want to create
ORG_ID = ""  # your organization ID, find in your organization settings
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings

# :remove-start:
DATASET_NAME = "test-" + time.strftime("%Y%m%d%H%M%S")  # a unique, new name for the dataset you want to create
ORG_ID = os.environ["TEST_ORG_ID"]  # your organization ID, find in your organization settings
API_KEY = os.environ["VIAM_API_KEY"]  # API key, find or create in your organization settings
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]  # API key ID, find or create in your organization settings
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
    """Main execution function."""
    viam_client = await connect()
    data_client = viam_client.data_client

    print("Creating dataset...")
    try:
        dataset_id = await data_client.create_dataset(
            name=DATASET_NAME,
            organization_id=ORG_ID,
        )
        print(f"Created dataset: {dataset_id}")
    except Exception as e:
        print("Error creating dataset. It may already exist.")
        print("See: https://app.viam.com/data/datasets")
        print(f"Exception: {e}")
        return 1

    # :remove-start:
    # Teardown - delete the dataset
    await data_client.delete_dataset(dataset_id)
    print(f"Deleted dataset: {dataset_id}")
    # :remove-end:
    viam_client.close()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
# :snippet-end: