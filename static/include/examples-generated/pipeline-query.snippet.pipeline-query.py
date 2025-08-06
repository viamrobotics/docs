import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.gen.app.data.v1.data_pb2 import TabularDataSourceType


# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
ORG_ID = ""  # Organization ID, find or create in your organization settings
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
    viam_client = await connect()
    data_client = viam_client.data_client

    tabular_data = await data_client.tabular_data_by_mql(
        organization_id=ORG_ID,
        query=[
            {"$match": {"component_name": "sensor-1"}},
            {
                "$group": {
                    "_id": "$location_id",
                    "avg_val": {"$avg": "$data.readings.a"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "location": "$_id",
                    "avg_val": 1,
                    "count": 1
                }
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
