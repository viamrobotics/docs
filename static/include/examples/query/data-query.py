# :snippet-start: data-query
import asyncio
# :remove-start:
import os
# :remove-end:

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
ORG_ID = ""  # Organization ID, find or create in your organization settings

# :remove-start:
ORG_ID = os.environ["TEST_ORG_ID"]
API_KEY = os.environ["VIAM_API_KEY"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]
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

    tabular_data_mql = await data_client.tabular_data_by_mql(
        organization_id=ORG_ID,
        query=[
            {
                "$match": {
                    "component_name": "sensor-1"
                },
            }, {
                "$limit": 5
            }
        ]
    )
    print(f"Tabular Data: {tabular_data_mql}")

    tabular_data_sql = await data_client.tabular_data_by_sql(
        organization_id=ORG_ID,
        sql_query="SELECT * FROM readings WHERE component_name = 'sensor-1' LIMIT 5"
    )
    print(f"Tabular Data: {tabular_data_sql}")

    viam_client.close()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
# :snippet-end: