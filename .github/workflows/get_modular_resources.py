import asyncio
import time
import os
import typesense

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.proto.app import ListRegistryItemsRequest, ListRegistryItemsResponse


async def connect() -> ViamClient:
    dial_options = DialOptions(
        auth_entity='b82783ad-b306-4512-98d2-5b23cc6b73da',
        credentials=Credentials(
            type='api-key',
            payload='owbj8gznshr3u9va57hqttsim3uotep3'
        )
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main():

    typesense_client = typesense.Client({
        # 'api_key': os.environ['TYPESENSE_API_KEY_MR'],
        'api_key': 'p2oTlVFR7xQgcs9lTqquIiXe35716Veu',
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

    # Create a request to list registry items and get the response from the app 
    request = ListRegistryItemsRequest(organization_id=cloud._organization_id)
    response : ListRegistryItemsResponse = await cloud._app_client.ListRegistryItems(request)

    ml_models_list = []
    for item in response.items:
        if item.type == 2:
            ml_models_list.append(item)

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

    for model in ml_models_list:
        print(model.visibility)
        if model.visibility == 2:
            json_m = {
                "model_id": model.item_id,
                "total_organization_usage": model.total_organization_usage,
                "total_robot_usage": model.total_robot_usage,
                "description": model.description,
                "last_updated": time_now
            }
            insert_resp = typesense_client.collections['mlmodels'].documents.upsert(
        json_m)
            print(insert_resp)

    viam_client.close()

    # Deleting documents that didn't get updated (presumably deleted)
    try:
        typesense_client.collections['modular_resources'].documents.delete({'filter_by': 'last_updated: <' + time_now})
        typesense_client.collections['mlmodels'].documents.delete({'filter_by': 'last_updated: <' + time_now})
    except Exception as e:
        pass


if __name__ == '__main__':
    asyncio.run(main())
