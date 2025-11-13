# :snippet-start: data-region
import asyncio
import os

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
ORG_ID = ""  # Organization ID, find or create in your organization settings

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
    async with await connect() as viam_client:
        # Check organization region
        org = await viam_client.app_client.get_organization(org_id=ORG_ID)
        print(f"Current region: {org.default_region}")

        # Update organization region
        try:
            updated_org = await viam_client.app_client.update_organization(
                org_id=ORG_ID,
                region="us-central"  # or "us-central"
            )
            print(f"Organization region updated to: {updated_org.default_region}")
        except Exception as e:
            print(f"Error updating organization region: {e}")
            # :remove-start:
            # testing if the error is the expected one
            if "region cannot be changed after syncing data or uploading packages" not in str(e):
                raise e
            # :remove-end:

        return 0

if __name__ == "__main__":
    asyncio.run(main())
# :snippet-end: