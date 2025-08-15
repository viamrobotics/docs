# :snippet-start: pipeline-execution
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

    pipeline_runs = await data_client.list_data_pipeline_runs(PIPELINE_ID, 10)
    for run in pipeline_runs.runs:
        print(f"Run: ID: {run.id}, status: {run.status}, start_time: {run.start_time}, end_time: {run.end_time}, data_start_time: {run.data_start_time}, data_end_time: {run.data_end_time}")
    # :remove-start:
    if len(pipeline_runs.runs) != 10:
        raise Exception("Expected 10 runs, got " + str(len(pipeline_runs.runs)))
    # :remove-end:

    viam_client.close()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
# :snippet-end: