import asyncio
from typing import List, Optional
from viam.utils import create_filter

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

# Configuration constants – replace with your actual values
DATASET_NAME = ""  # a unique, new name for the dataset you want to create
ORG_ID = ""  # your organization ID, find in your organization settings
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
PART_ID = ""  # the part ID of the binary data you want to add to the dataset
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
    """Main execution function."""
    viam_client = await connect()
    data_client = viam_client.data_client

    matching_data = await fetch_binary_data_ids(data_client, PART_ID)

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

    await data_client.add_binary_data_to_dataset_by_ids(
        binary_ids=[
            obj.metadata.binary_data_id for obj in matching_data
        ],
        dataset_id=dataset_id
    )

    print("Added files to dataset.")
    print(
        f"See dataset: https://app.viam.com/data/datasets?id={dataset_id}"
    )

    viam_client.close()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
