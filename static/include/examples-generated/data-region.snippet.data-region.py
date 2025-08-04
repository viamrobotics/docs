import asyncio
import os

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

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
    viam_client = await connect()

    # Check organization region
    org = await viam_client.app_client.get_organization(org_id=ORG_ID)
    print(f"Current region: {org.default_region}")

    # Update organization region
    try:
        updated_org = await viam_client.app_client.update_organization(
            org_id=ORG_ID,
            region="us-central"  # or "us-central"
        )
        print(f"Organization region updated to: {updated_org.region}")
    except Exception as e:
        print(f"Error updating organization region: {e}")

    viam_client.close()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
