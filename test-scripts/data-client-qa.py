import asyncio
from datetime import datetime

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.utils import create_filter

import bson
# import bson.json_util
from viam.proto.app.data import BinaryID

async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        payload='<API-KEY>',
      ),
      # Replace "<API-KEY-ID>" (including brackets) with your machine's
      # API key ID
      auth_entity='<API-KEY-ID>'
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def configure_database_user(data_client):
    await data_client.configure_database_user(
        organization_id="<YOUR-ORG-ID>",
        password="Your_Password@1234"
    )


async def main():
    async with await connect() as viam_client:
        # Instantiate a DataClient to run data client API methods on
        data_client = viam_client.data_client

        with open("strain.png", "rb") as img_file:
        img_binary_data = img_file.read()

        # Print the first 50 bytes as an example
        print(img_binary_data[:50])

        time_requested = datetime(2023, 6, 5, 11)
        time_received = datetime(2023, 6, 5, 11, 0, 3)

        file_id = await data_client.binary_data_capture_upload(
            part_id="<YOUR-PART-ID>",
            component_type='camera',
            component_name='camera-1',
            method_name='GetImages',
            method_parameters=None,
            tags=["TEST", "TEST 2"],
            data_request_times=[time_requested, time_received],
            file_extension=".png",
            binary_data=img_binary_data
        )

        print(f"File id: {file_id}")

        time_requested = datetime(2023, 6, 5, 11)
        time_received = datetime(2023, 6, 5, 11, 0, 3)

        file_id = await data_client.tabular_data_capture_upload(
            part_id="<YOUR-PART-ID>",
            component_type='rdk:component:motor',
            component_name='left_motor',
            method_name='IsPowered',
            tags=["TEST TABULAR"],
            data_request_times=[(time_requested, time_received)],
            tabular_data=[{'PowerPCT': 0, 'IsPowered': False}]
        )

        print(f"File id: {file_id}")

        with open("testfileupload.txt", "rb") as text_file:
        text_binary_data = text_file.read()

        file_id = await data_client.file_upload(
        data=text_binary_data,
        part_id="<YOUR-PART-ID>",
        tags=["TEST FILE UPLOAD"],
        file_name="testfileupload",
        file_extension=".txt"
        )

        print(f"File id: {file_id}")

        file_id = await data_client.file_upload_from_path(
        part_id="<YOUR-PART-ID>",
        tags=["TEST FILE UPLOAD FROM PATH"],
        filepath="/Users/sierraguequierre/desktop/testfileupload.txt"
        )

        print(f"File id: {file_id}")

        time_requested = datetime(2023, 6, 5, 11)
        time_received = datetime(2023, 6, 5, 11, 0, 3)

        file_id = await data_client.streaming_data_capture_upload(
            data=img_binary_data,
            part_id="<YOUR-PART-ID>",
            file_ext="png",
            component_type='camera',
            component_name='camera-1',
            data_request_times=[time_requested, time_received],
            tags=["TEST STREAMING UPLOAD"]
        )

        print(f"File id: {file_id}")

        my_data = []
        my_filter = create_filter(component_name="motor-1")
        last = None
        while True:
            tabular_data, count, last = await data_client.tabular_data_by_filter(my_filter, last=last)
            print(f"count {count} last {last}")
            if not tabular_data:
                break
            my_data.extend(tabular_data)

        print(f"My data: {my_data}")

        data = await data_client.tabular_data_by_sql(organization_id="<YOUR-ORG-ID>", sql_query="SELECT * FROM readings LIMIT 5")

        print(f"Testing tabular data by SQL: {data}")

        # using bson package (pip install bson)
        tabular_data = await data_client.tabular_data_by_mql(organization_id="<YOUR-ORG-ID>", mql_binary=[
            bson.dumps({ '$match': { 'location_id': '<YOUR-LOCATION-ID>' } }),
            bson.dumps({ '$limit': 5 })
        ])

        print(tabular_data)

        # using pymongo package (pip install pymongo)
        tabular_data = await data_client.tabular_data_by_mql(organization_id="<YOUR-ORG-ID>", mql_binary=[
            bson.encode({ '$match': { 'location_id': '<YOUR-LOCATION-ID>' } }),
            bson.encode({ '$limit': 5 })
        ])

        print(tabular_data)

        my_data = []
        last = None
        my_filter = create_filter(component_name="camera-1")
        while True:
            data, count, last = await data_client.binary_data_by_filter(my_filter, limit=1, last=last)
            if not data:
                break
            my_data.extend(data)

        print(f"My data: {my_data}")

        my_ids = []

        for obj in binary_metadata:
            my_ids.append(
                BinaryID(
                    file_id=obj.metadata.id,
                    organization_id=obj.metadata.capture_metadata.organization_id,
                    location_id=obj.metadata.capture_metadata.location_id
                )
            )

        binary_data = await data_client.binary_data_by_ids(my_ids)
        print(f"binary data: {binary_data}")

        tabular_data = await data_client.delete_tabular_data(
            organization_id="<YOUR-ORG-ID>",
            delete_older_than_days=150
        )

        print(f"tabular data {tabular_data}")

        my_filter = create_filter(component_name="my-webcam", organization_ids=["<YOUR-ORG-ID>"])
        res = await data_client.delete_binary_data_by_filter(my_filter)
        print(f"response {res}")


        my_filter = create_filter(component_name="camera-2", organization_ids=["<YOUR-ORG-ID>"])
        binary_metadata, count, last = await data_client.binary_data_by_filter(
        filter=my_filter,
        limit=20,
        include_binary_data=False
        )

        my_ids = []

        for obj in binary_metadata:
            my_ids.append(
                BinaryID(
                    file_id=obj.metadata.id,
                    organization_id=obj.metadata.capture_metadata.organization_id,
                    location_id=obj.metadata.capture_metadata.location_id
                )
            )

        print(f"length of my ids {len(my_ids)}")

        binary_data = await data_client.delete_binary_data_by_ids(my_ids)

        tags = ["tag1", "tag2"]

        my_filter = create_filter(component_name="camera-2", organization_ids=["<YOUR-ORG-ID>"])
        binary_metadata, count, last = await data_client.binary_data_by_filter(
        filter=my_filter,
        limit=20,
        include_binary_data=False
        )

        my_ids = []

        for obj in binary_metadata:
            my_ids.append(
                BinaryID(
                    file_id=obj.metadata.id,
                    organization_id=obj.metadata.capture_metadata.organization_id,
                    location_id=obj.metadata.capture_metadata.location_id
                )
            )

        binary_data = await data_client.add_tags_to_binary_data_by_ids(tags, my_ids)

        my_filter = create_filter(component_name="camera-1")
        tags = ["test 1"]
        res = await data_client.add_tags_to_binary_data_by_filter(tags, my_filter)
        print("response: {}")

        tags = ["TEST"]

        my_filter = create_filter(component_name="camera-1")

        binary_metadata, count, last = await data_client.binary_data_by_filter(
            filter=my_filter,
            limit=50,
            include_binary_data=False
        )

        my_ids = []

        for obj in binary_metadata:
            my_ids.append(
                BinaryID(
                    file_id=obj.metadata.id,
                    organization_id=obj.metadata.capture_metadata.organization_id,
                    location_id=obj.metadata.capture_metadata.location_id
                )
            )

        # TODO: Uncomment this when deleting tags works again
        #  binary_data = await data_client.remove_tags_from_binary_data_by_ids(
        #     tags, my_ids)

        print(f"Binary data {binary_data}")

        my_filter = create_filter(component_name="camera-2")
        tags = ["TEST"]
        res = await data_client.remove_tags_from_binary_data_by_filter(tags, my_filter)

        print(f"response: {res}")

        my_filter = create_filter(component_name="camera-1")
        tags = await data_client.tags_by_filter(my_filter)
        print(f"TAGS: {tags}")

        MY_BINARY_ID = BinaryID(
            file_id="<YOUR-FILE-ID>",
            organization_id="<YOUR-ORG-ID>",
            location_id="<YOUR-LOCATION-ID>"
        )

        bbox_id = await data_client.add_bounding_box_to_image_by_id(
            binary_id=MY_BINARY_ID,
            label="TEST BOUNDING BOXES",
            x_min_normalized=0,
            y_min_normalized=.1,
            x_max_normalized=.2,
            y_max_normalized=.3
        )

        print(bbox_id)

        MY_BINARY_ID = BinaryID(
            file_id="<YOUR-FILE-ID>",
            organization_id="<YOUR-ORG-ID>",
            location_id="<YOUR-LOCATION-ID>"
        )

        await data_client.remove_bounding_box_from_image_by_id(
        binary_id=MY_BINARY_ID,
        bbox_id="<YOUR-BBOX-ID>"
        )

        my_filter = create_filter(component_name="camera-2")
        bounding_box_labels = await data_client.bounding_box_labels_by_filter(
            my_filter)

        print(bounding_box_labels)

        hostname = await data_client.get_database_connection(organization_id="<YOUR-ORG-ID>")
        print(hostname)

        await data_client.configure_database_user(
            organization_id="<YOUR-ORG-ID>",
            password="Your_Password@1234"
        )

        binary_metadata, count, last = await data_client.binary_data_by_filter(
            include_binary_data=False
        )

        my_binary_ids = []

        for obj in binary_metadata:
            my_binary_ids.append(
                BinaryID(
                    file_id=obj.metadata.id,
                    organization_id=obj.metadata.capture_metadata.organization_id,
                    location_id=obj.metadata.capture_metadata.location_id
                    )
                )

        await data_client.add_binary_data_to_dataset_by_ids(
            binary_ids=my_binary_ids,
            dataset_id="<YOUR-DATASET-ID>"
        )

        binary_metadata, count, last = await data_client.binary_data_by_filter(
            include_binary_data=False
        )

        my_binary_ids = []

        for obj in binary_metadata:
            my_binary_ids.append(
                BinaryID(
                    file_id=obj.metadata.id,
                    organization_id=obj.metadata.capture_metadata.organization_id,
                    location_id=obj.metadata.capture_metadata.location_id
                )
            )

        await data_client.remove_binary_data_from_dataset_by_ids(
            binary_ids=my_binary_ids,
            dataset_id="<YOUR-DATASET-ID>"
        )

        name = await data_client.create_dataset(
            name="test-dataset",
            organization_id="<YOUR-ORG-ID>"
        )
        print(name)

        await data_client.rename_dataset(
            id="<YOUR-DATASET-ID>",
            name="MyDataset"
        )

        datasets = await data_client.list_datasets_by_organization_id(
            organization_id="<YOUR-ORG-ID>"
        )
        print(datasets)

        datasets = await data_client.list_dataset_by_ids(
            ids=["<YOUR-DATASET-ID>"]
        )
        print(datasets)

        my_filter = create_filter(component_name="camera-1")
        binary_metadata, count, last = await data_client.binary_data_by_filter(
            filter=my_filter,
            limit=20,
            include_binary_data=False
        )

        my_ids = []

        for obj in binary_metadata:
            my_ids.append(
                BinaryID(
                    file_id=obj.metadata.id,
                    organization_id=obj.metadata.capture_metadata.organization_id,
                    location_id=obj.metadata.capture_metadata.location_id
                )
            )

        binary_data = await data_client.binary_data_by_ids(my_ids)
        print(f"Binary data {binary_data}")

        my_binary_ids = []

        for obj in binary_metadata:
            my_binary_ids.append(
                BinaryID(
                    file_id=obj.metadata.id,
                    organization_id=obj.metadata.capture_metadata.organization_id,
                    location_id=obj.metadata.capture_metadata.location_id
                    )
                )

        await data_client.add_binary_data_to_dataset_by_ids(
            binary_ids=my_binary_ids,
            dataset_id="<YOUR-DATASET-ID>"
        )


if __name__ == '__main__':
    asyncio.run(main())
