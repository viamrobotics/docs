# :snippet-start: add-machine-images-to-dataset
import asyncio
from typing import List, Optional
from viam.utils import create_filter
# :remove-start:
import os
import time
# :remove-end:

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
ORG_ID = ""  # your organization ID, find in your organization settings
PART_ID = ""  # the part ID of the machine part that captured the images
DATASET_ID = ""  # the ID of the dataset you want to add the image to
MAX_MATCHES = 50  # the maximum number of binary data objects to fetch

# :remove-start:
DATASET_NAME = "test-" + time.strftime("%Y%m%d%H%M%S")
ORG_ID = os.environ["TEST_ORG_ID"]
API_KEY = os.environ["VIAM_API_KEY"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]
PART_ID = "824b6570-7b1d-4622-a19d-37c472dba467"
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

async def fetch_binary_data_ids(data_client, part_id: str) -> List[str]:
    """Fetch binary data metadata and return a list of BinaryData objects."""
    data_filter = create_filter(part_id=part_id)
    all_matches = []
    last: Optional[str] = None

    print("Getting data for part...")

    while len(all_matches) < MAX_MATCHES:
        print("Fetching more data...")
        data, _, last = await data_client.binary_data_by_filter(
            data_filter,
            limit=50,
            last=last,
            include_binary_data=False,
        )
        if not data:
            break
        all_matches.extend(data)

    return all_matches

async def main() -> int:
    async with await connect() as viam_client:
        data_client = viam_client.data_client

        matching_data = await fetch_binary_data_ids(data_client, PART_ID)

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
        await data_client.add_binary_data_to_dataset_by_ids(
            binary_ids=[
                obj.metadata.binary_data_id for obj in matching_data
            ],
            dataset_id=DATASET_ID
        )

        print("Added files to dataset:")
        print(f"https://app.viam.com/data/datasets?id={DATASET_ID}")

        # :remove-start:
        # Teardown - delete the dataset
        await data_client.delete_dataset(DATASET_ID)
        print(f"Deleted dataset: {DATASET_ID}")
        # :remove-end:
        return 0

if __name__ == "__main__":
    asyncio.run(main())
# :snippet-end: