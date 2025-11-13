import asyncio
import os

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
ORG_ID = ""  # Organization ID, find or create in your organization settings
PART_ID = ""  # Part ID of machine part that should be associated with the data
FILE_PATH = "file.txt"  # Path to the file to upload

async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        payload=API_KEY,
      ),
      # Replace "<API-KEY-ID>" (including brackets) with your machine's
      # API key ID
      auth_entity=API_KEY_ID
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main():
    async with await connect() as viam_client:
        data_client = viam_client.data_client

        binary_data_id = await data_client.file_upload_from_path(
          # The ID of the machine part the file should be associated with
          part_id=PART_ID,
          # Any tags you want to apply to this file
          tags=["uploaded"],
          # Path to the file
          filepath=FILE_PATH
        )


if __name__ == '__main__':
    asyncio.run(main())
