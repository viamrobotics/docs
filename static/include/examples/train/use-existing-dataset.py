# :snippet-start: use-existing-dataset
# Assumption: The dataset was exported using the `viam dataset export` command.
# This script is being run from the `destination` directory.

import asyncio
import os
import json
# :remove-start:
import os
import time
import random
# :remove-end:

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
ORG_ID = ""  # the ID of the organization you want to add the image to
PART_ID = ""  # the ID of the machine part you want to add the image to
LOCATION_ID = ""  # the ID of the location you want to add the image to
DATASET_NAME = ""  # the name of the dataset you want to add the image to
FOLDER_NAME = ""  # the name of the folder that contains the dataset

# :remove-start:
DATASET_NAME = "test-" + time.strftime("%Y%m%d%H%M%S")
API_KEY = os.environ["VIAM_API_KEY"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]
ORG_ID = os.environ["TEST_ORG_ID"]
PART_ID = "824b6570-7b1d-4622-a19d-37c472dba467"
LOCATION_ID = "pg5q3j3h95"
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


async def main():
    async with await connect() as viam_client:
        data_client = viam_client.data_client

        # :remove-start:
        # Download test dataset
        datasets = [
            "https://storage.googleapis.com/docs-blog/dataset-figure.zip",
            "https://storage.googleapis.com/docs-blog/dataset-shapes.zip",
        ]
        rand_num = random.randint(0, len(datasets) - 1)
        FOLDER_NAME = datasets[rand_num].split("/")[-1].split(".")[0]
        os.system(f"curl -o dataset.zip {datasets[rand_num]}")
        os.system(f"unzip dataset.zip")
        os.system(f"rm dataset.zip")
        # :remove-end:

        print("Creating dataset...")
        try:
            dataset_id = await data_client.create_dataset(
                name=DATASET_NAME,
                organization_id=ORG_ID,
            )
            print(f"Created dataset: {dataset_id}")
        except Exception as e:
            print("Error creating dataset. It may already exist.")
            print("See: https://app.viam.com/data/datasets")
            print(f"Exception: {e}")
            return 1

        file_ids = []

        for file_name in os.listdir(FOLDER_NAME + "/metadata/"):
            with open(FOLDER_NAME + "/metadata/" + file_name) as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    print(f"Skipping file: {file_name} because it is not valid JSON")
                    print(f"Exception: {e}")
                    continue

                tags = None

                if "captureMetadata" in data.keys():
                    if "tags" in data["captureMetadata"].keys():
                        tags = data["captureMetadata"]["tags"]

                annotations = None
                if "annotations" in data.keys():
                    annotations = data["annotations"]
                print(data)
                print(annotations)

                image_file = file_name.replace(".json", "")

                print("Uploading: " + image_file)

                file_id = await data_client.file_upload_from_path(
                    part_id=PART_ID,
                    tags=tags,
                    filepath=os.path.join(FOLDER_NAME + "/data/", image_file)
                )
                print("FileID: " + file_id)

                if annotations:
                    bboxes = annotations["bboxes"]
                    for box in bboxes:
                        await data_client.add_bounding_box_to_image_by_id(
                            binary_id=file_id,
                            label=box["label"],
                            x_min_normalized=box["xMinNormalized"],
                            y_min_normalized=box["yMinNormalized"],
                            x_max_normalized=box["xMaxNormalized"],
                            y_max_normalized=box["yMaxNormalized"]
                        )

                if tags:
                    await data_client.add_tags_to_binary_data_by_ids(
                        tags=tags,
                        binary_ids=[file_id]
                    )

                file_ids.append(file_id)

        await data_client.add_binary_data_to_dataset_by_ids(
            binary_ids=file_ids,
            dataset_id=dataset_id
        )
        print("Added files to dataset.")
        print("https://app.viam.com/data/datasets?id=" + dataset_id)

        # :remove-start:
        # Teardown - delete the dataset
        await data_client.delete_dataset(dataset_id)
        print(f"Deleted dataset: {dataset_id}")

        # Delete the data
        await data_client.delete_binary_data_by_ids(file_ids)
        print(f"Deleted files: {file_ids}")
        os.system("rm -rf dataset-shapes")
        os.system("rm -rf dataset-figure")
        # :remove-end:


if __name__ == '__main__':
    asyncio.run(main())
# :snippet-end: