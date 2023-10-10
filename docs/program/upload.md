---
title: "Upload Data using the Python SDK"
linkTitle: "Upload Data"
weight: 50
type: "docs"
description: "Upload data from your robot to the Viam app using the Python"
images: ["/services/icons/sdk.svg"]
tags: ["python", "sdk", "application", "fleet", "program"]
---

You can use the [Viam Python SDK](https://python.viam.dev/) to upload data from your robot to [the Viam app](https://app.viam.com/data/view).
Uploaded data appears under the **Data** tab in the app.

The Python SDK provides the following upload methods:

- Upload binary format - [`binary_data_capture_upload`](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_capture_upload)
- Upload tabular data format - [`tabular_data_capture_upload`](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_capture_upload)
- Upload an arbitrary file - [`file_upload`](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload)
- Upload an arbitrary file from filepath - [`file_upload_from_path`](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload_from_path)

For more details on this functionality, see the [Connect as a client to the app](https://python.viam.dev/examples/example.html#connect-as-a-client-to-app) example in the Python SDK documentation.

## Upload methods

Use these methods to upload data to the Viam app.

### Upload binary data

You can use the [`binary_data_capture_upload`](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_capture_upload) method to upload binary data collected on your robot from a specific [component](/component/) (e.g., a [motor](/component/motor/)) to [the Viam app](https://app.viam.com/data/view).
Uploaded binary data can be found under the [**Files** subtab](https://app.viam.com/data/view?view=files) of the **Data** tab.

**Parameters:**

- `binary_data` [(bytes)](https://docs.python.org/3/library/stdtypes.html#bytes-objects): The data to be uploaded, represented in bytes.
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Part ID of the component used to capture the data.
- `component_type` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Type of the component used to capture the data (e.g., `“movement_sensor”`).
- `component_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the component used to capture the data.
- `method_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the method used to capture the data.
- `method_parameters` [(Optional[Mapping[str, Any]])](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict): Optional dictionary of method parameters. No longer in active use.
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/manage/data/label/#image-tags) to allow for tag-based data filtering when retrieving data.
- `data_request_times` [(Optional[Tuple[datetime.datetime, datetime.datetime]])](https://docs.python.org/3/library/stdtypes.html#tuples): Optional tuple containing [`datetime`](https://docs.python.org/3/library/datetime.html) objects denoting the times this data was requested and received by the appropriate sensor.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_capture_upload).

#### Example

Upload binary example here.

### Upload tabular data

You can use the [`tabular_data_capture_upload`](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_capture_upload) method to upload tabular data collected on your robot from a specific [component](/component/) (e.g., a [motor](/component/motor/)) to [the Viam app](https://app.viam.com/data/view).
Uploaded tabular data can be found under the [**Sensors** subtab](https://app.viam.com/data/view?view=sensors) of the **Data** tab.

**Parameters:**

- `tabular_data` [(List[Mapping[str, Any]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list) – List of the data to be uploaded, represented tabularly as a collection of dictionaries.
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Part ID of the component used to capture the data.
- `component_type` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Type of the component used to capture the data (e.g., `“movement_sensor”`).
- `component_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the component used to capture the data.
- `method_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the method used to capture the data.
- `method_parameters` [(Optional[Mapping[str, Any]])](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict): Optional dictionary of method parameters. No longer in active use.
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/manage/data/label/#image-tags) to allow for tag-based data filtering when retrieving data.
- `data_request_times` [(Optional[Tuple[datetime.datetime, datetime.datetime]])](https://docs.python.org/3/library/stdtypes.html#tuples): Optional tuple containing [`datetime`](https://docs.python.org/3/library/datetime.html) objects denoting the times this data was requested and received by the appropriate sensor.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_capture_upload).

#### Example

Upload tabular example here.

### Upload arbitrary file

You can use the [`file_upload`](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload) method to upload arbitrary files that may be stored on your robot to [the Viam app](https://app.viam.com/data/view).
Uploaded files can be found under the [**Files** subtab](https://app.viam.com/data/view?view=files) of the **Data** tab.

**Parameters:**

- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Part ID of the component used to capture the data.
- `component_type` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Type of the component used to capture the data (e.g., `“movement_sensor”`).
- `component_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the component used to capture the data.
- `method_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the method used to capture the data.
- `file_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional name of the file. The empty string `“”` will be assigned as the filename if one isn’t provided.
- `method_parameters` [(Optional[Mapping[str, Any]])](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict): Optional dictionary of method parameters. No longer in active use.
- `file_extension` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional file extension. The empty string `“”` will be assigned as the file extension if one isn’t provided.
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/manage/data/label/#image-tags) to allow for tag-based data filtering when retrieving data.
- `data` [(Optional[bytes])](https://docs.python.org/3/library/stdtypes.html#bytes-objects): Optional bytes representing file data to upload.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload).

#### Example

Upload arbitrary file example here.

### Upload file by filepath

You can use the [`binary_data_capture_upload`](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload_from_path) method to upload binary data collected on your robot from a specific [component](/component/) (e.g., a [motor](/component/motor/)) to [the Viam app](https://app.viam.com/data/view).
Uploaded binary data can be found under the [**Files** subtab](https://app.viam.com/data/view?view=files) of the **Data** tab.

**Parameters:**

- `filepath` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Absolute filepath of file to be uploaded.
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Part ID of the component used to capture the data.
- `component_type` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Type of the component used to capture the data (e.g., `“movement_sensor”`).
- `component_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the component used to capture the data.
- `method_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the method used to capture the data.
- `method_parameters` [(Optional[Mapping[str, Any]])](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict): Optional dictionary of method parameters. No longer in active use.
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/manage/data/label/#image-tags) to allow for tag-based data filtering when retrieving data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload_from_path).

#### Example

Upload file by filepath example here.

## Next steps

Once you have uploaded data to the Viam app, you might want to perform some of the following related tasks:

- To configure data sync between your robot and the Viam app outside of the Python SDK, you could configure the [data management service](/services/data/)'s [cloud sync](/services/data/#cloud-sync) feature.
- If you need to download data from the Viam app to your robot, you could [export data from the Viam app using the Viam CLI](/tutorials/services/data-management-tutorial/#export-captured-data).

## Walkthrough

First:

```sh
pip install viam-sdk
```

Then, for arbitrary files:

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from datetime import datetime

async def connect() -> ViamClient:
    dial_options = DialOptions(
        auth_entity='macos-laptop-main.yriemen2i2.viam.cloud',  # The URL of your robot.
        credentials=Credentials(
            type='robot-location-secret',
            payload='d7f7n4zc92cjwmlhdqzh545la0xmpc7qnnn9gmtyb28g0nhd'
        )
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main():

    viam_client = await connect()

    data_client = viam_client.data_client


    time_requested_1 = datetime(2023, 6, 5, 11)
    time_recieved_1 = datetime(2023, 6, 5, 11, 0, 3)

    await data_client.file_upload(
        part_id="10101", # Unique ID of the relevant robot part.
        component_type='rdk:component:motor',
        component_name='left_motor',
        method_name='IsPowered',
        method_parameters=None,
        tags=["tag_1", "tag_2"],
        file_name="test"
        file_extension="txt"
    )

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Then, for tabular data file:


```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from datetime import datetime

async def connect() -> ViamClient:
    dial_options = DialOptions(
        auth_entity='macos-laptop-main.yriemen2i2.viam.cloud',  # The URL of your robot.
        credentials=Credentials(
            type='robot-location-secret',
            payload='d7f7n4zc92cjwmlhdqzh545la0xmpc7qnnn9gmtyb28g0nhd'
        )
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main():

    viam_client = await connect()

    data_client = viam_client.data_client


    time_requested_1 = datetime(2023, 6, 5, 11)
    time_recieved_1 = datetime(2023, 6, 5, 11, 0, 3)

    await data_client.tabular_data_capture_upload(
        part_id="10101", # Unique ID of the relevant robot part.
        component_type='rdk:component:motor',
        component_name='left_motor',
        method_name='IsPowered',
        method_parameters=None,
        tags=["tag_1", "tag_2"],
        data_request_times=[(time_requested_1, time_recieved_1)],
        tabular_data=[{'PowerPCT': 0, 'IsPowered': False}]
    )

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Here's the filepath upload example, closest to working:

```python
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from datetime import datetime

async def connect() -> ViamClient:
    dial_options = DialOptions(
        auth_entity='macos-laptop-main.yriemen2i2.viam.cloud',  # The URL of your robot.
        credentials=Credentials(
            type='robot-location-secret',
            payload='d7f7n4zc92cjwmlhdqzh545la0xmpc7qnnn9gmtyb28g0nhd'
        )
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main():

    viam_client = await connect()

    data_client = viam_client.data_client


    time_requested_1 = datetime(2023, 6, 5, 11)
    time_recieved_1 = datetime(2023, 6, 5, 11, 0, 3)

    await data_client.file_upload_from_path(
        part_id="10101", # Unique ID of the relevant robot part.
        component_type='rdk:component:motor',
        component_name='left_motor',
        method_name='IsPowered',
        method_parameters=None,
        tags=["tag_1", "tag_2"],
        filepath="/Users/andf/scratch/pysdk-test/test.txt"
    )

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())

```

Unfortunately errors:

```none
bananajr:pysdk-test andf$ python3 upload_file.py
2023-08-22 16:46:42,686		ERROR	viam (__init__.py:34)	[ERROR] Uncaught exception
Traceback (most recent call last):
  File "/Users/andf/scratch/pysdk-test/upload_file.py", line 40, in <module>
    asyncio.run(main())
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/asyncio/runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/asyncio/base_events.py", line 642, in run_until_complete
    return future.result()
  File "/Users/andf/scratch/pysdk-test/upload_file.py", line 27, in main
    await data_client.file_upload_from_path(
  File "/Users/andf/Library/Python/3.9/lib/python/site-packages/viam/app/data_client.py", line 602, in file_upload_from_path
    await self._file_upload(metadata=metadata, file_contents=FileData(data=data))
  File "/Users/andf/Library/Python/3.9/lib/python/site-packages/viam/app/data_client.py", line 611, in _file_upload
    assert response is not None
AssertionError
Traceback (most recent call last):
  File "/Users/andf/scratch/pysdk-test/upload_file.py", line 40, in <module>
    asyncio.run(main())
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/asyncio/runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/asyncio/base_events.py", line 642, in run_until_complete
    return future.result()
  File "/Users/andf/scratch/pysdk-test/upload_file.py", line 27, in main
    await data_client.file_upload_from_path(
  File "/Users/andf/Library/Python/3.9/lib/python/site-packages/viam/app/data_client.py", line 602, in file_upload_from_path
    await self._file_upload(metadata=metadata, file_contents=FileData(data=data))
  File "/Users/andf/Library/Python/3.9/lib/python/site-packages/viam/app/data_client.py", line 611, in _file_upload
    assert response is not None
AssertionError
```
