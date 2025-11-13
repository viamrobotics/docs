import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.gen.app.data.v1.data_pb2 import TabularDataSourceType


# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
ORG_ID = ""  # Organization ID, find or create in your organization settings


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

        pipelines = await data_client.list_data_pipelines(ORG_ID)
        for pipeline in pipelines:
            print(f"Pipeline: {pipeline.name}, ID: {pipeline.id}, schedule: {pipeline.schedule}, data_source_type: {pipeline.data_source_type}")

        return 0

if __name__ == "__main__":
    asyncio.run(main())
