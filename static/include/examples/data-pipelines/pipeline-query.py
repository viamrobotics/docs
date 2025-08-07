# :snippet-start: pipeline-query
import asyncio
# :remove-start:
import os
# :remove-end:

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.gen.app.data.v1.data_pb2 import TabularDataSourceType


# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
ORG_ID = ""  # Organization ID, find or create in your organization settings
PIPELINE_ID = ""

# :remove-start:
ORG_ID = os.environ["TEST_ORG_ID"]
API_KEY = os.environ["VIAM_API_KEY"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]
PIPELINE_ID = "16b8a3e5-7944-4e1c-8ccd-935c1ba3be59"
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
    viam_client = await connect()
    data_client = viam_client.data_client

    tabular_data = await data_client.tabular_data_by_mql(
        organization_id=ORG_ID,
        query=[
            {
                "$match": {
                    "location": { "$exists": True }
                },
            }, {
                "$limit": 10
            }
        ],
        tabular_data_source_type=TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_PIPELINE_SINK,
        pipeline_id=PIPELINE_ID
    )
    print(f"Tabular Data: {tabular_data}")

    viam_client.close()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
# :snippet-end: