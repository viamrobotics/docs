---
linkTitle: "Create a training dataset"
title: "Create a training dataset"
weight: 30
layout: "docs"
type: "docs"
description: "Create a dataset to use for AI model training"
---

{{< tabs >}}
{{% tab name="Viam app" %}}

1. Open the [**DATA** page](https://app.viam.com/data/view) of the Viam app.

1. Navigate to the **ALL DATA** tab.

1. Use the checkbox in the upper left of each image to select labeled images.

1. Click the **Add to dataset** button, select a dataset, and click the **Add ... images** button to add the selected images to the dataset.

{{% /tab %}}
{{% tab name="CLI" %}}

Use the Viam CLI to filter images by label and add the filtered images to a dataset:

1. First, [create a dataset](#create-a-dataset), if you haven't already.

1. If you just created a dataset, use the dataset ID output by the creation command.
   If your dataset already exists, run the following command to get a list of dataset names and corresponding IDs:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset list
   ```

1. Run the following [command](/dev/tools/cli/#dataset) to add all images labeled with a subset of tags to the dataset, replacing the `<dataset-id>` placeholder with the dataset ID output by the command in the previous step:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset data add filter --dataset-id=<dataset-id> --tags=red_star,blue_square
   ```

{{% /tab %}}
{{% tab name="Data Client API" %}}

The following script adds all images captured from a certain machine to a new dataset. Complete the following steps to use the script:

1. Copy and paste the following code into a file named <file>add_images_from_machine_to_dataset.py</file> on your machine.

   ```python {class="line-numbers linkable-line-numbers" data-line="9-13" }
   import asyncio
   from typing import List, Optional

   from viam.rpc.dial import DialOptions, Credentials
   from viam.app.viam_client import ViamClient
   from viam.utils import create_filter

   # Configuration constants – replace with your actual values
   DATASET_NAME = "" # a unique, new name for the dataset you want to create
   ORG_ID = "" # your organization ID, find in your organization settings
   PART_ID = "" # id of machine that captured target images, find in machine config
   API_KEY = "" # API key, find or create in your organization settings
   API_KEY_ID = "" # API key ID, find or create in your organization settings

   # Adjust the maximum number of images to add to the dataset
   MAX_MATCHES = 500

   async def connect() -> ViamClient:
       """Establish a connection to the Viam client using API credentials."""
       dial_options = DialOptions(
           credentials=Credentials(
               type="api-key",
               payload=API_KEY,
           ),
           auth_entity=API_KEY_ID,
       )
       return await ViamClient.create_from_dial_options(dial_options)


   async def fetch_binary_data_ids(data_client, part_id: str) -> List[str]:
       """Fetch binary data metadata and return a list of BinaryData objects."""
       data_filter = create_filter(part_id=part_id)
       all_matches = []
       last: Optional[str] = None

       print("Getting data for part...")

       while len(all_matches) < MAX_MATCHES:
           print("Fetching more data...")
           data, _, last = await data_client.binary_data_by_filter(
               data_filter,
               limit=50,
               last=last,
               include_binary_data=False,
           )
           if not data:
               break
           all_matches.extend(data)

       return all_matches


   async def main() -> int:
       """Main execution function."""
       viam_client = await connect()
       data_client = viam_client.data_client

       matching_data = await fetch_binary_data_ids(data_client, PART_ID)

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

       print("Adding data to dataset...")

       await data_client.add_binary_data_to_dataset_by_ids(
           binary_ids=[obj.metadata.binary_data_id for obj in matching_data],
           dataset_id=dataset_id
       )

       print("Added files to dataset.")
       print(f"See dataset: https://app.viam.com/data/datasets?id={dataset_id}")

       viam_client.close()
       return 0


   if __name__ == "__main__":
       asyncio.run(main())
   ```

1. Fill in the placeholders with values for your own organization, API key, machine, and dataset.

1. Install the [Viam Python SDK](https://python.viam.dev/) by running the following command:

   ```sh {class="command-line" data-prompt="$"}
   pip install viam-sdk
   ```

1. Finally, run the following command to add the images to the dataset:

   ```sh {class="command-line" data-prompt="$"}
   python add_images_from_machine_to_dataset.py
   ```

{{% /tab %}}
{{< /tabs >}}
