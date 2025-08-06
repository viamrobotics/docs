# :snippet-start: pipeline-delete
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
PIPELINE_ID = ""

# :remove-start:
ORG_ID = "b5e9f350-cbcf-4d2a-bbb1-a2e2fd6851e1"
API_KEY = os.environ["VIAM_API_KEY_DATA_REGIONS"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID_DATA_REGIONS"]
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

    # :remove-start:
    pipelines = await data_client.list_data_pipelines(ORG_ID)
    for pipeline in pipelines:
        await data_client.delete_data_pipeline(pipeline.id)
        print(f"Deleted pipeline: {pipeline.id}")

    PIPELINE_ID = await data_client.create_data_pipeline(
        name="test-pipeline",
        organization_id=ORG_ID,
        mql_binary=[
            {"$match": {"component_name": "temperature-sensor"}},
            {
                "$group": {
                    "_id": "$location_id",
                    "avg_temp": {"$avg": "$data.readings.temperature"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "location": "$_id",
                    "avg_temp": 1,
                    "count": 1
                }
            }
        ],
        schedule="0 * * * *",
        data_source_type=TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_STANDARD,
        enable_backfill=False,
    )
    print(f"Pipeline created with ID: {PIPELINE_ID}")
    # :remove-end:
    await data_client.delete_data_pipeline(PIPELINE_ID)
    print(f"Pipeline deleted with ID: {PIPELINE_ID}")

    viam_client.close()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
# :snippet-end: