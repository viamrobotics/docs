---
title: "Upload and Retrieve Data with Viam's Data Client API"
linkTitle: "Data Client"
weight: 10
type: "docs"
description: "Use the data client API to upload and retrieve data directly to the Viam app."
tags:
  [
    "cloud",
    "sdk",
    "viam-server",
    "networking",
    "apis",
    "robot api",
    "data management",
    "data",
  ]
---

The data client API allows you to upload and retrieve data to and from the [Viam app](https://app.viam.com).

{{% alert title="Support Notice" color="note" %}}

Data client API methods are only available in the Python SDK.

{{% /alert %}}

## Establish a connection

To use the Viam data client API, you first need to instantiate a [`ViamClient`](https://python.viam.dev/autoapi/viam/app/viam_client/index.html#viam.app.viam_client.ViamClient) and then instantiate an [`DataClient`](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient).
See the following example for reference.

<!-- After sveltekit migration we should also be able to get a key from the UI-->

Use the Viam CLI [to generate an api key to authenticate](/manage/cli/#authenticate).

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        # Replace "<API-KEY>" (including brackets) with your robot's api key
        payload='<API-KEY>',
      ),
      # Replace "<API-KEY-ID>" (including brackets) with your robot's api key
      # id
      auth_entity='<API-KEY-ID>'
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def main():
    # Make a ViamClient
    viam_client = await connect()
    # Instantiate a DataClient to run data client API methods on
    data_client = viam_client.data_client

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Once you have instantiated a `DataClient`, you can run the following [API methods](#api) against the `DataClient` object (named `data_client` in the examples).

## Find Part ID

To find the ID of your robot part, navigate to its **Setup** tab in the [Viam app](https://app.viam.com).
Keep architecture selection at default.
In Step 1, grab the part id from the second string of the generated command as the token following `id=`.
For example:

![Part ID displayed in the Viam app.](/program/data-client/grab-part-id.png)

## API

The data client API supports the following methods (among [others](https://python.viam.dev/autoapi/viam/app/data_client/index.html)):

{{< readfile "/static/include/services/apis/data-client.md" >}}

### TabularDataByFilter

Retrieve optionally filtered tabular data from the [Viam app](https://app.viam.com).
You can also find your tabular data under the **Sensors** subtab of the app's [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filter` [(Optional[viam.proto.app.data.Filter])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional `Filter` specifying tabular data to retrieve. Specify no filter to download all tabular data.
- `dest` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Filepath to write retrieved data to. If not populated, writes to your current directory.

**Returns**:

- [(List[TabularData])](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.TabularData): The tabular data retrieved from the [Viam app](https://app.viam.com).

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_name="left_motor")
tabular_data = await data_client.tabular_data_by_filter(my_filter)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_by_filter).

{{% /tab %}}
{{< /tabs >}}

### BinaryDataByFilter

Retrieve optionally filtered binary data from the [Viam app](https://app.viam.com).
You can also find your binary data under the **Images**, **Point clouds**, or **Files** subtab of the app's [**Data** tab](https://app.viam.com/data), depending on the type of data that you have uploaded.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filter` [(Optional[viam.proto.app.data.Filter])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional `Filter` specifying binary data to retrieve. Specify no filter to download all binary data.
- `dest` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Filepath to write retrieved data to. If not populated, writes to your current directory.
- `include_file_data` [(bool)](https://docs.python.org/3/c-api/bool.html#boolean-objects): Boolean specifying whether to include the binary file data with each retrieved file. Defaults to `true`, where both the files’ data and metadata are returned.
- `num_files` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Number of binary data to return. Passing `0` returns all binary data matching the filter. Defaults to `100` if no binary data is requested, otherwise `10`.

**Returns**:

- [(List[BinaryData])](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.BinaryData): The binary data retrieved from the [Viam app](https://app.viam.com).

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_type="camera")
binary_data = await data_client.binary_data_by_filter(my_filter)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_by_filter).

{{% /tab %}}
{{< /tabs >}}

### BinaryDataByIDs

Retrieve binary data from the [Viam app](https://app.viam.com) by [`BinaryID`](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID).
You can also find your binary data under the **Images**, **Point clouds**, or **Files** subtab of the app's [**Data** tab](https://app.viam.com/data), depending on the type of data that you have uploaded.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_ids` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): `BinaryID` objects specifying the desired data. Must be non-empty.
- `dest` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Filepath to write retrieved data to. If not populated, writes to your current directory.

**Returns**:

- [(List[BinaryData])](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.BinaryData): The binary data retrieved from the [Viam app](https://app.viam.com).

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import BinaryID

binary_metadata = await data_client.binary_data_by_filter(
    include_file_data=False
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
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_by_ids).

{{% /tab %}}
{{< /tabs >}}

### DeleteTabularData

Delete tabular data older than a specified number of days.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- organization_id ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): ID of organization to delete data from.
- delete_older_than_days ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): Delete data that was captured up to this many days ago. For example if delete_older_than_days
  is 10, this deletes any data that was captured up to 10 days ago. If it is 0, all existing data is deleted.

**Returns:**

- None.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_name="left_motor")
days_of_data_to_delete = 10
tabular_data = await data_client.delete_tabular_data(
    "a12b3c4e-1234-1abc-ab1c-ab1c2d345abc", days_of_data_to_delete)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_tabular_data).

{{% /tab %}}
{{< /tabs >}}

### DeleteBinaryDataByFilter

Filter and delete binary data.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- filter ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter "viam.proto.app.data.Filter")): Optional Filter specifying binary data to delete. Passing an empty Filter will lead to
  all data being deleted. Exercise caution when using this option.

**Returns:**

- None.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_name="left_motor")
res = await data_client.delete_binary_data_by_filter(my_filter)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_binary_data_by_filter).

{{% /tab %}}
{{< /tabs >}}

### DeleteBinaryDataByIds

Filter and delete binary data by ids.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- binary_ids (List[[viam.proto.app.data.BinaryID](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID "viam.proto.app.data.BinaryID")]): BinaryID objects specifying the data to be deleted. Must be non-empty.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The number of items deleted.

**Raises:**

- `GRPCError` – This error is raised if no BinaryID objects are provided.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import BinaryID

binary_metadata = await data_client.binary_data_by_filter(
    include_file_data=False
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

binary_data = await data_client.delete_binary_data_by_ids(my_ids)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_binary_data_by_ids).

{{% /tab %}}
{{< /tabs >}}

### AddTagsToBinaryDataByIds

Add tags to binary data by ids.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- tags ([List[str]](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): List of tags to add to specified binary data. Must be non-empty.
- binary_ids (List[viam.app.proto.BinaryID]): List of BinaryID objects specifying binary data to tag. Must be non-empty.

**Returns:**

- None.

**Raises:**

- `GRPCError` – This error is raised if no BinaryID objects or tags are provided.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import BinaryID

tags = ["tag1", "tag2"]

binary_metadata = await data_client.binary_data_by_filter(
    include_file_data=False
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
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_tags_to_binary_data_by_ids).

{{% /tab %}}
{{< /tabs >}}

### AddTagsToBinaryDataByFilter

Add tags to binary data by filter.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- tags ([List[str]](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): List of tags to add to specified binary data. Must be non-empty.
- filter ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter "viam.proto.app.data.Filter")): Filter specifying binary data to tag. If no Filter is provided, all data will be
  tagged.

**Returns:**

- None.

**Raises:**

- `GRPCError` – This error is raised if no Btags are provided.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_name="my_camera")
tags = ["tag1", "tag2"]
res = await data_client.add_tags_to_binary_data_by_filter(tags, my_filter)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_tags_to_binary_data_by_filter).

{{% /tab %}}
{{< /tabs >}}

### RemoveTagsFromBinaryDataByIds

Remove tags from binary by ids.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- tags ([List[str]](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): List of tags to remove from specified binary data. Must be non-empty.
- file_ids ([List[str]](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): List of BinaryID objects specifying binary data to untag. Must be non-empty.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The number of tags removed.

**Raises:**

- `GRPCError` – This error is raised if no BinaryID objects or tags are provided.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import BinaryID

tags = ["tag1", "tag2"]

binary_metadata = await data_client.binary_data_by_filter(
    include_file_data=False
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

binary_data = await data_client.remove_tags_from_binary_data_by_ids(
    tags, my_ids)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_tags_from_binary_data_by_ids).

{{% /tab %}}
{{< /tabs >}}

### RemoveTagsFromBinaryDataByFilter

Remove tags from binary data by filter.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- tags ([List[str]](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): List of tags to remove from specified binary data.
- filter ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter "viam.proto.app.data.Filter")): Filter specifying binary data to untag. If no Filter is provided, all data will be
  untagged.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The number of tags removed.

**Raises:**

- `GRPCError` – This error is raised if no tags are provided.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_name="my_camera")
tags = ["tag1", "tag2"]
res = await data_client.remove_tags_from_binary_data_by_filter(tags, my_filter)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_tags_from_binary_data_by_filter).

{{% /tab %}}
{{< /tabs >}}

### TagsByFilter

Get a list of tags using a filter.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- filter ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter "viam.proto.app.data.Filter")): Filter specifying data to retrieve from. If no Filter is provided, all data tags will
  return.

**Returns:**

- ([List[str]](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The list of tags.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_name="my_camera")
tags = await data_client.tags_by_filter(my_filter)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tags_by_filter).

{{% /tab %}}
{{< /tabs >}}

### BoundingBoxLabelsByFilter

Get a list of bounding box labels using a Filter.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- filter ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter "viam.proto.app.data.Filter")): Filter specifying data to retrieve from. If no Filter is provided, all labels will
  return.

**Returns:**

- ([List[str]](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The list of bounding box labels.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_name="my_camera")
bounding_box_labels = await data_client.bounding_box_labels_by_filter(
    my_filter)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.bounding_box_labels_by_filter).

{{% /tab %}}
{{< /tabs >}}

### GetDatabaseConnection

Get a connection to access a MongoDB Atlas Data federation instance.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- organization_id ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): Organization to retrieve the connection for.

**Returns:**

- ([`str`](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The hostname of the federated database.

```python {class="line-numbers linkable-line-numbers"}
data_client.get_database_connection("a12b3c4e-1234-1abc-ab1c-ab1c2d345abc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.get_database_connection).

{{% /tab %}}
{{< /tabs >}}

### BinaryDataCaptureUpload

Upload binary data collected on your machine through a specific component and the relevant metadata to the [Viam app](https://app.viam.com).
Uploaded binary data can be found under the **Images**, **Point clouds**, or **Files** subtab of the app's [**Data** tab](https://app.viam.com/data), depending on the type of data that you upload.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_data` [(bytes)](https://docs.python.org/3/library/stdtypes.html#bytes-objects): The data to be uploaded, represented in bytes.
- `part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): Part ID of the component used to capture the data. See [Find Part ID](#find-part-id) for instructions on retrieving this value.
- `component_type` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): Type of the component used to capture the data.
- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): Name of the component used to capture the data.
- `method_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): Name of the method used to capture the data.
- `tags` ([Optional[List[str]]](https://docs.python.org/3/library/stdtypes.html#typesseq-list)): Optional list of [image tags](/manage/data/label/#image-tags) to allow for tag-based data filtering when retrieving data.
- `data_request_times` ([Optional[Tuple[datetime.datetime, datetime.datetime]]](https://docs.python.org/3/library/stdtypes.html#tuples)): Optional tuple containing [`datetime`](https://docs.python.org/3/library/datetime.html) objects denoting the times this data was requested and received by the appropriate sensor.
- `file_extension` ([Optional[str]](https://docs.python.org/3/library/typing.html#typing.Optional)): The file extension of binary data including the period. For example, `".jpg"`, `".png"`, or `".pcd"`. Specify this to route the binary data to its corresponding mime type in storage in the [Viam app](https://app.viam.com).

**Returns**:

- ([`str`](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): ID of the new file.

```python {class="line-numbers linkable-line-numbers"}
time_requested = datetime(2023, 6, 5, 11)
time_received = datetime(2023, 6, 5, 11, 0, 3)

file_id = await data_client.binary_data_capture_upload(
    part_id="INSERT YOUR PART ID",
    component_type='camera',
    component_name='my_camera',
    method_name='GetImages',
    method_parameters=None,
    tags=["tag_1", "tag_2"],
    data_request_times=[time_requested, time_received],
    file_extension=".jpg",
    binary_data=b"Encoded image bytes"
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

- ([`str`](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): ID of the new file.

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
If uploaded with a file extension of <file>.jpeg/.jpg/.png</file>, uploaded files can be found in the **Images** subtab of the app's [**Data** tab](https://app.viam.com/data).
If <file>.pcd</file>, the uploaded files can be found in the **Point clouds** subtab.
All other types of uploaded files can be found under the **Files** subtab of the app's [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `data` [(bytes)](https://docs.python.org/3/library/stdtypes.html#bytes-objects): Bytes representing the file data to upload.
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Part ID of the component used to capture the data. See [Find Part ID](#find-part-id) for instructions on retrieving this value.
- `component_type` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Type of the component used to capture the data.
- `component_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the component used to capture the data.
- `file_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional name of the file. The empty string `""` will be assigned as the filename if one isn’t provided.
- `file_extension` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional file extension. The empty string `""` will be assigned as the file extension if one isn’t provided.
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/manage/data/label/#image-tags) to allow for tag-based data filtering when retrieving data.

**Returns**:

- [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the new file.

```python {class="line-numbers linkable-line-numbers"}
file_id = await data_client.file_upload(
    data=b"Encoded image bytes",
    part_id="INSERT YOUR PART ID",
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
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/manage/data/label/#image-tags) to allow for tag-based data filtering when retrieving data.

**Returns**:

- [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the new file.

```python {class="line-numbers linkable-line-numbers"}
file_id = await data_client.file_upload_from_path(
    part_id="INSERT YOUR PART ID",
    tags=["tag_1", "tag_2"],
    filepath="/Users/<your-username>/<your-directory>/<your-file.txt>"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload_from_path).

{{% /tab %}}
{{< /tabs >}}
