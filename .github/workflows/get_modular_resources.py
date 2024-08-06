import asyncio
import time
import os
import typesense
import json

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.proto.app import ListRegistryItemsRequest, ListRegistryItemsResponse


async def connect() -> ViamClient:
    dial_options = DialOptions(
        auth_entity='fc5301b4-af27-4421-88fb-31352510bac1',
        credentials=Credentials(
            type='api-key',
            payload=os.environ['VIAM_API_KEY']
        )
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main():

    typesense_client = typesense.Client({
        'api_key': os.environ['TYPESENSE_API_KEY_R'],
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
    module_list = await cloud.list_modules(org_id=os.environ['TEST_ORG_ID'])

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
                insert_resp = typesense_client.collections['resources'].documents.upsert(
        json_m)
                print(insert_resp)

    # Get built-in resources from components/typesense.json
    with open('components/typesense.json') as f:
        resources = json.load(f)
        for r in resources:
            print("RESOURCE")
            print(r)
            r["last_updated"] = time_now
            r["total_organization_usage"] = int(r["total_organization_usage"])
            r["total_robot_usage"] = int(r["total_robot_usage"])
            print(r)
            insert_resp = typesense_client.collections['resources'].documents.upsert(r)
            print("INSERTED")
            print(insert_resp)

    # Get built-in resources from services/typesense.json
    with open('services/typesense.json') as f:
        resources = json.load(f)
        for r in resources:
            print("RESOURCE")
            print(r)
            r["last_updated"] = time_now
            r["total_organization_usage"] = int(r["total_organization_usage"])
            r["total_robot_usage"] = int(r["total_robot_usage"])
            print(r)
            insert_resp = typesense_client.collections['resources'].documents.upsert(r)
            print("INSERTED")
            print(insert_resp)

    # Create a request to list registry items and get the response from the app
    request = ListRegistryItemsRequest(organization_id=cloud._organization_id)
    response : ListRegistryItemsResponse = await cloud._app_client.ListRegistryItems(request)

    ml_models_list = []
    training_scripts_list = []
    for item in response.items:
        if item.type == 2:
            ml_models_list.append(item)
        if item.type == 5:
            training_scripts_list.append(item)

    for model in ml_models_list:
        if model.visibility == 2:
            json_m = {
                "id": model.item_id,
                "model_id": model.item_id,
                "total_organization_usage": int(model.total_organization_usage),
                "total_robot_usage": int(model.total_robot_usage),
                "description": model.description,
                "last_updated": time_now,
                "url": "https://app.viam.com/ml-model/" + model.public_namespace + "/" + model.name + "/"
            }
            insert_resp = typesense_client.collections['mlmodels'].documents.upsert(
        json_m)
            print(insert_resp)

    for script in training_scripts_list:
        if script.visibility == 2:
            json_m = {
                "id": script.item_id,
                "model_id": script.item_id,
                "name": script.name,
                "description": script.description,
                "last_updated": time_now,
                "url": "https://app.viam.com/ml-training/" + script.public_namespace + "/" + script.name + "/"
            }
            insert_resp = typesense_client.collections['trainingscripts'].documents.upsert(
        json_m)
            print(insert_resp)

    viam_client.close()

    # Deleting documents that didn't get updated (presumably deleted)
    try:
        res = typesense_client.collections['resources'].documents.delete({'filter_by': 'last_updated: <' + str(time_now)})
        print("Resources deleted")
        print(res)
        res = typesense_client.collections['mlmodels'].documents.delete({'filter_by': 'last_updated: <' + str(time_now)})
        print("ML models deleted")
        print(res)
        res = typesense_client.collections['trainingscripts'].documents.delete({'filter_by': 'last_updated: <' + time_now})
        print("Training scripts deleted")
        print(res)
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    asyncio.run(main())
