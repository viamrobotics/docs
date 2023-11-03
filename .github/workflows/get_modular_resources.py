import asyncio
import time
import os
import typesense

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


async def connect() -> ViamClient:
    dial_options = DialOptions(
        # The URL of any robot in the location.
        auth_entity='divine-voice-main.b5luvepsyg.viam.cloud',
        credentials=Credentials(
            type='robot-location-secret',
            # The location secret
            payload=os.environ['VIAM_LOCATION_SECRET']
        )
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main():

    typesense_client = typesense.Client({
        'api_key': os.environ['TYPESENSE_API_KEY_MR'],
        'nodes': [{
            'host': 'cgnvrk0xwyj9576lp-1.a1.typesense.net',
            'port': '443',
            'protocol': 'https'
        }],
        'connection_timeout_seconds': 2
    })

    time_now = int(time.time())

    # Make a ViamClient
    viam_client = await connect()
    # Instantiate an AppClient called "cloud" to run cloud app API methods on
    cloud = viam_client.app_client
    module_list = await cloud.list_modules()
    modular_resources = []
    for module in module_list:
        if module.visibility == 2:
            for model in module.models:
                json_m = {
                    "id": module.module_id + '-' + model.model,
                    "module_id": module.module_id,
                    "total_organization_usage": module.total_organization_usage,
                    "total_robot_usage": module.total_robot_usage,
                    "url": module.url,
                    "description": module.description,
                    "model": model.model,
                    "api": model.api,
                    "last_updated": time_now
                }
                insert_resp = typesense_client.collections['modular_resources'].documents.upsert(
        json_m)
                print(insert_resp)

    viam_client.close()

    # Deleting documents that didn't get updated (presumably deleted)
    try:
        typesense_client.collections['modular_resources'].documents.delete({'filter_by': 'last_updated: <' + time_now})
    except Exception as e:
        pass


if __name__ == '__main__':
    asyncio.run(main())