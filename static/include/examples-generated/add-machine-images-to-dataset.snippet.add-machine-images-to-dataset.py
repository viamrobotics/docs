import asyncio
from typing import List, Optional
from viam.utils import create_filter

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
ORG_ID = ""  # your organization ID, find in your organization settings
PART_ID = ""  # the part ID of the machine part that captured the images
DATASET_ID = ""  # the ID of the dataset you want to add the image to
MAX_MATCHES = 50  # the maximum number of binary data objects to fetch


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
    viam_client = await connect()
    data_client = viam_client.data_client

    matching_data = await fetch_binary_data_ids(data_client, PART_ID)

    await data_client.add_binary_data_to_dataset_by_ids(
        binary_ids=[
            obj.metadata.binary_data_id for obj in matching_data
        ],
        dataset_id=DATASET_ID
    )

    print("Added files to dataset:")
    print(f"https://app.viam.com/data/datasets?id={DATASET_ID}")

    viam_client.close()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
