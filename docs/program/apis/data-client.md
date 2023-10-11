---
title: "Upload and Retrieve Data with Viam's Data Client API"
linkTitle: "Data Client"
weight: 10
type: "docs"
description: "Use the data client API to upload data directly to the Viam app."
tags:
  [
    "cloud",
    "sdk",
    "viam-server",
    "networking",
    "apis",
    "robot api",
    "cloud management",
    "data management",
    "data"
  ]
---

The data client API allows you to upload and retrieve data to and from the [Viam app](https://app.viam.com) directly.
{{% alert title="Support Notice" color="note" %}}

Data client API methods are only available in the Python SDK.

{{% /alert %}}

## Establish a connection

To use the Viam data client API, you first need to instantiate a [`ViamClient`](https://python.viam.dev/autoapi/viam/app/viam_client/index.html#viam.app.viam_client.ViamClient) and then instantiate an [`DataClient`](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient).
See the following example for reference.
To find the location secret, go to [Viam app](https://app.viam.com/), and go to the [**Code sample**](https://docs.viam.com/manage/fleet/robots/#code-sample) tab of any of the robots in the location.
Toggle **Include secret** on and copy the `payload`.
For the URL, use the address of any of the robots in the location (also found on the **Code sample** tab).

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


async def connect() -> ViamClient:
    dial_options = DialOptions(
        # The URL of any robot in the location.
        auth_entity='beepboop-main.YOUR LOCATION ID.viam.cloud',
        credentials=Credentials(
            type='robot-location-secret',
            # The location secret
            payload='YOUR LOCATION SECRET'
        )
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def main():

    # Make a ViamClient
    viam_client = await connect()
    # Instantiate a DataClient called "data" to run data client API methods on
    data_client = viam_client.data_client

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Once you have instantiated an `DataClient`, you can run the following [API methods](#api) against the `DataClient` object (named `data_client` in the examples).

## API

The data client API supports the following methods (among [others](https://python.viam.dev/autoapi/viam/app/data_client/index.html)):

{{< readfile "/static/include/services/apis/data-client.md" >}}

### BinaryDataCaptureUpload

Upload binary data collected on your machine through a specific component and the relevant metadata to the [Viam app](https://app.viam.com).
Binary data can be found under the **Files** subtab of the app's [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_data` [(bytes)](https://docs.python.org/3/library/stdtypes.html#bytes-objects): The data to be uploaded, represented in bytes.
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Part ID of the component used to capture the data. See [Find Part ID](#find-part-id) for instructions on retrieving this value.
- `component_type` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Type of the component used to capture the data.
- `component_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the component used to capture the data.
- `method_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the method used to capture the data.
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/manage/data/label/#image-tags) to allow for tag-based data filtering when retrieving data.
- `data_request_times` [(Optional[Tuple[datetime.datetime, datetime.datetime]])](https://docs.python.org/3/library/stdtypes.html#tuples): Optional tuple containing [`datetime`](https://docs.python.org/3/library/datetime.html) objects denoting the times this data was requested and received by the appropriate sensor.

**Returns**:

- [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the new file.

```python {class="line-numbers linkable-line-numbers"}
time_requested = datetime(2023, 6, 5, 11)
time_received = datetime(2023, 6, 5, 11, 0, 3)

file_id = await data_client.binary_data_capture_upload(
    part_id="INSERT YOUR PART ID",
    component_type='motor',
    component_name='left_motor',
    method_name='IsPowered',
    method_parameters=None,
    tags=["tag_1", "tag_2"],
    data_request_times=[time_requested, time_received],
    binary_data= b"Some data"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_capture_upload).

{{% /tab %}}
{{< /tabs >}}

### TabularDataCaptureUpload

Upload tabular data collected on your machine through a specific [component](/components/) to the [Viam app](https://app.viam.com).
Uploaded tabular data can be found under the **Sensors** subtab of the app's [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `tabular_data` [(List[Mapping[str, Any]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): List of the data to be uploaded, represented tabularly as a collection of dictionaries.
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Part ID of the component used to capture the data. See [Find Part ID](#find-part-id) for instructions on retrieving this value.
- `component_type` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Type of the component used to capture the data.
- `component_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the component used to capture the data.
- `method_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the method used to capture the data.
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/manage/data/label/#image-tags) to allow for tag-based data filtering when retrieving data.
- `data_request_times` [(Optional[Tuple[datetime.datetime, datetime.datetime]])](https://docs.python.org/3/library/stdtypes.html#tuples): Optional tuple containing [`datetime`](https://docs.python.org/3/library/datetime.html) objects denoting the times this data was requested and received by the appropriate sensor.

**Returns**:

- [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the new file.

```python {class="line-numbers linkable-line-numbers"}
time_requested = datetime(2023, 6, 5, 11)
time_received = datetime(2023, 6, 5, 11, 0, 3)

file_id = await data_client.tabular_data_capture_upload(
    part_id="INSERT YOUR PART ID",
    component_type='motor',
    component_name='left_motor',
    method_name='IsPowered',
    tags=["tag_1", "tag_2"],
    data_request_times=[(time_requested, time_received)],
    tabular_data=[{'PowerPCT': 0, 'IsPowered': False}]
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_capture_upload).

{{% /tab %}}
{{< /tabs >}}

### FileUpload

Upload arbitrary files stored on your machine to the [Viam app](https://app.viam.com) by file name.
Uploaded files can be found under the **Files** subtab of the app's [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Part ID of the component used to capture the data.  See [Find Part ID](#find-part-id) for instructions on retrieving this value.
- `component_type` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Type of the component used to capture the data.
- `component_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the component used to capture the data.
- `method_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the method used to capture the data.
- `file_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional name of the file. The empty string `“”` will be assigned as the filename if one isn’t provided.
- `file_extension` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional file extension. The empty string `“”` will be assigned as the file extension if one isn’t provided.
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/manage/data/label/#image-tags) to allow for tag-based data filtering when retrieving data.
- `data` [(Optional[bytes])](https://docs.python.org/3/library/stdtypes.html#bytes-objects): Optional bytes representing file data to upload.

**Returns**:

- [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the new file.

```python {class="line-numbers linkable-line-numbers"}
file_id = await data_client.file_upload(
    part_id="INSERT YOUR PART ID",
    component_type='motor',
    component_name='left_motor',
    method_name='IsPowered',
    tags=["tag_1", "tag_2"],
    file_name="your-file",
    file_extension=".txt"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload).

{{% /tab %}}
{{< /tabs >}}

### FileUploadFromPath

Upload files stored on your machine to the [Viam app](https://app.viam.com) by filepath.
Uploaded files can be found under the **Files** subtab of the app's [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filepath` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The absolute filepath of the file to be uploaded.
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Part ID of the component used to capture the data. See [Find Part ID](#find-part-id) for instructions on retrieving this value.
- `component_type` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Type of the component used to capture the data.
- `component_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the component used to capture the data.
- `method_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the method used to capture the data.
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/manage/data/label/#image-tags) to allow for tag-based data filtering when retrieving data.

**Returns**:

- [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the new file.

```python {class="line-numbers linkable-line-numbers"}
file_id = await data_client.file_upload_from_path(
    part_id="INSERT YOUR PART ID",
    component_type='motor',
    component_name='left_motor',
    method_name='IsPowered',
    tags=["tag_1", "tag_2"],
    filepath="/Users/<your-username>/<your-directory>/<your-file.txt>"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload_from_path).

{{% /tab %}}
{{< /tabs >}}

## Find Part ID

To find the ID of your robot part, navigate to its **Setup** tab in the [Viam app](https://app.viam.com).
Keep architecture selection at default.
In Step 1, grab the part id from the second string of the generated command as the token following `id=`.
For example:

![Part ID displayed in the Viam app.](/program/data-client/grab-part-id.png)
