import asyncio
import os
import time

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.proto.app import Authorization
from viam.proto.app import AuthorizedPermissions
from viam.proto.app.packages import PackageType
from viam.proto.app import Visibility, RegistryItemStatus
from viam.proto.app import Model, ModuleFileInfo
from viam.app.app_client import APIKeyAuthorization

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
ORG_ID = ""  # Organization ID, find or create in your organization settings
EMAIL_ADDRESS = ""  # Email address of the user to get the user id for
LOCATION_ID = ""  # Location ID, find or create in your organization settings

# :remove-start:
ORG_ID = os.environ["TEST_ORG_ID"]
ORG_ID_2 = "b5e9f350-cbcf-4d2a-bbb1-a2e2fd6851e1"
API_KEY = os.environ["VIAM_API_KEY"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]
LOCATION_ID = "pg5q3j3h95"
TEST_EMAIL = os.environ["TEST_EMAIL"]
# :remove-end:

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

    # Make a ViamClient
    viam_client = await connect()
    # Instantiate an AppClient called "cloud"
    # to run fleet management API methods on
    cloud = viam_client.app_client


    fragments_list = await cloud.list_fragments(org_id=ORG_ID, visibilities=[])
    fragment_list_len = len(fragments_list)
    assert fragment_list_len >= 0

    new_fragment = await cloud.create_fragment(org_id=ORG_ID, name="test-fragment", config={
        "components": [
            {
            "name": "camera-1",
            "api": "rdk:component:camera",
            "model": "rdk:builtin:fake",
            "attributes": {}
            },
        ]
    })
    assert new_fragment is not None
    assert new_fragment.name == "test-fragment"
    fragments_list = await cloud.list_fragments(org_id=ORG_ID, visibilities=[])
    assert len(fragments_list) == fragment_list_len + 1

    the_fragment = await cloud.get_fragment(
      fragment_id=new_fragment.id)
    assert the_fragment.name == "test-fragment"

    updated_fragment = await cloud.update_fragment(
    fragment_id=new_fragment.id,
    name="test-fragment-new-name")
    assert updated_fragment.name == "test-fragment-new-name"

    fragment_history = await cloud.get_fragment_history(
        id = new_fragment.id,
        page_limit = 10
    )
    assert fragment_history

    await cloud.delete_fragment(
    fragment_id=new_fragment.id)

    registry_items = await cloud.list_registry_items(
        organization_id="",
        types=[PackageType.PACKAGE_TYPE_ML_TRAINING],
        visibilities=[Visibility.VISIBILITY_PUBLIC],
        platforms=["linux/any"],
        statuses=[RegistryItemStatus.REGISTRY_ITEM_STATUS_PUBLISHED]
    )
    assert len(registry_items) >= 0

    item = await cloud.get_registry_item("viam:classification-tflite")
    assert item is not None
    assert item.type == PackageType.PACKAGE_TYPE_ML_TRAINING
    assert item.item_id == "viam:classification-tflite"

    # await cloud.create_registry_item(ORG_ID, "new-registry-item", PackageType.PACKAGE_TYPE_ML_MODEL)
    # new_registry_items = await cloud.get_registry_item("docs-test:new-registry-item")
    # assert new_registry_items is not None
    # assert new_registry_items.type == PackageType.PACKAGE_TYPE_ML_MODEL
    # assert new_registry_items.name == "new-registry-item"

    await cloud.update_registry_item("docs-test:new-registry-item", PackageType.PACKAGE_TYPE_ML_MODEL, "Test registry item.", Visibility.VISIBILITY_PRIVATE)
    updated_registry_items = await cloud.get_registry_item("docs-test:new-registry-item")
    assert updated_registry_items is not None
    assert updated_registry_items.description == "Test registry item."
    assert updated_registry_items.visibility == Visibility.VISIBILITY_PRIVATE

    await cloud.delete_registry_item("docs-test:new-registry-item")
    try:
       await cloud.get_registry_item("docs-test:new-registry-item")
       assert False
    except Exception as e:
        print(e)

    new_module = await cloud.create_module(org_id=ORG_ID, name="new_test_module")
    assert new_module[0] == "docs-test:new_test_module"

    model = Model(
        api="rdk:service:generic",
        model="docs-test:new_test_module:test_model"
    )

    url_of_my_module = await cloud.update_module(
      module_id="docs-test:new_test_module",
      url="https://docsformymodule.viam.com",
      models=[model],
      description="A generic test service.",
      entrypoint="exec")
    assert url_of_my_module is not None

    registry_items = await cloud.list_registry_items(
        organization_id="",
        types=[PackageType.PACKAGE_TYPE_MODULE],
        visibilities=[Visibility.VISIBILITY_PUBLIC],
        platforms=["linux/any"],
        statuses=[RegistryItemStatus.REGISTRY_ITEM_STATUS_PUBLISHED]
    )
    assert len(registry_items) >= 0

    module_file_info = ModuleFileInfo(
        module_id = "docs-test:new_test_module",
        version = "1.0.0",
        platform = "darwin/arm64"
    )

    file_id = await cloud.upload_module_file(module_file_info=module_file_info, file=b"empty.txt")
    assert file_id is not None

    the_module = await cloud.get_module(module_id="docs-test:new_test_module")
    assert the_module is not None

    modules_list = await cloud.list_modules(ORG_ID)
    num_modules = len(modules_list)
    assert num_modules >= 1

    await cloud.delete_registry_item("docs-test:new_test_module")

    modules_list = await cloud.list_modules(ORG_ID)
    assert len(modules_list) == num_modules - 1


    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
