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
aliases:
  - /program/apis/data-client/
  - /build/program/apis/data-client/
---

The data client API allows you to upload and retrieve data to and from the [Viam app](https://app.viam.com).

{{% alert title="Support Notice" color="note" %}}

Data client API methods are only available in the Python SDK.

{{% /alert %}}

## Establish a connection

To use the Viam data client API, you first need to instantiate a [`ViamClient`](https://python.viam.dev/autoapi/viam/app/viam_client/index.html#viam.app.viam_client.ViamClient) and then instantiate a [`DataClient`](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient).

You will also need an API key and API key ID to authenticate your session.
To get an API key (and corresponding ID), you have two options:

- [Create an API key using the Viam app](/cloud/rbac/#add-an-api-key)
- [Create an API key using the Viam CLI](/cli/#create-an-organization-api-key)

The following example instantiates a `ViamClient`, authenticating with an API key, and then instantiates a `DataClient`:

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


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


async def main():
    # Make a ViamClient
    viam_client = await connect()
    # Instantiate a DataClient to run data client API methods on
    data_client = viam_client.data_client

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Once you have instantiated a `DataClient`, you can run [API methods](#api) against the `DataClient` object (named `data_client` in the examples).

## API

The data client API supports the following methods (among [others](https://python.viam.dev/autoapi/viam/app/data_client/index.html)):

{{< readfile "/static/include/services/apis/data-client.md" >}}

### TabularDataByFilter

Filter and download optionally filtered tabular data from the [Viam app](https://app.viam.com).
The data will be paginated into pages of `limit` items, and the pagination ID will be included in the returned tuple.
If a destination is provided, the data will be saved to that file.
If the file is not empty, it will be overwritten.
You can also find your tabular data under the **Sensors** subtab of the app's [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filter` [(Optional[viam.proto.app.data.Filter])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional `Filter` specifying tabular data to retrieve. Specify no filter to download all tabular data.
- `limit` [(Optional[int])](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex): The maximum number of entries to include in a page. Default: `50`.
- `sort_order` (Optional[Order.ValueType]): The desired sort order of the data.
- `last` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional string indicating the ID of the last-returned data. If provided, the server will return the next data entries after the `last` ID.
- `count_only` [(bool)](https://docs.python.org/3/library/stdtypes.html): Whether to return only the total count of entries. Default: `False`.
- `include_internal_data` [(bool)](https://docs.python.org/3/library/stdtypes.html): Whether to return the internal data. Internal data is used for Viam-specific data ingestion, like cloud SLAM. Default: `False`.
- `dest` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Filepath to write retrieved data to. If not populated, writes to your current directory.

**Returns**:

- [(List[TabularData])](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.TabularData), int, str]): The tabular data retrieved from the [Viam app](https://app.viam.com).
- [(int)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex): The count (number of entries).
- [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The last-returned page ID.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_name="left_motor")
tabular_data, count, id = await data_client.tabular_data_by_filter(my_filter)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_by_filter).

{{% /tab %}}
{{< /tabs >}}

### BinaryDataByFilter

Filter and download binary data from the [Viam app](https://app.viam.com).
The data will be paginated into pages of `limit` items, and the pagination ID will be included in the returned tuple.
If a destination is provided, the data will be saved to that file.
If the file is not empty, it will be overwritten.

You can also find your binary data under the **Images**, **Point clouds**, or **Files** subtab of the app's [**Data** tab](https://app.viam.com/data), depending on the type of data that you have uploaded.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filter` [(Optional[viam.proto.app.data.Filter])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional `Filter` specifying binary data to retrieve. Specify no filter to download all binary data.
- `limit` [(Optional[int])](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex): The maximum number of entries to include in a page. Default: `50`.
- `sort_order` (Optional[Order.ValueType]): The desired sort order of the data.
- `last` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional string indicating the ID of the last-returned data. If provided, the server will return the next data entries after the `last` ID.
- `include_binary_data` [(bool)](https://docs.python.org/3/library/stdtypes.html): Boolean specifying whether to actually include the binary file data with each retrieved file. Whether to return the internal data. Internal data is used for Viam-specific data ingestion, like cloud SLAM. Default: `True` meaning both the files' data and metadata are returned.
- `count_only` [(bool)](https://docs.python.org/3/library/stdtypes.html): Whether to return only the total count of entries. Default: `False`.
- `include_internal_data` [(bool)](https://docs.python.org/3/library/stdtypes.html): Whether to return the internal data. Internal data is used for Viam-specific data ingestion, like cloud SLAM. Default: `False`.
- `dest` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Filepath to write retrieved data to. If not populated, writes to your current directory.

**Returns**:

- [(List[BinaryData])](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.BinaryData): The binary data retrieved from the [Viam app](https://app.viam.com).
- [(int)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex): The count (number of entries).
- [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The last-returned page ID.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_type="camera")
binary_data, count, id = await data_client.binary_data_by_filter(my_filter)
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

- `binary_ids` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): `BinaryID` objects specifying the desired data.
  Must be non-empty.
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

### TabularDataBySQL

Obtain unified tabular data and metadata, queried with SQL.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The ID of the organization that owns the data.
- `sql_query` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The SQL query to run.

**Returns:**

- (List[Dict[str, ValueTypes]]): An array of data objects.

```python {class="line-numbers linkable-line-numbers"}
tabular_data = await data_client.tabular_data_by_sql(
    organization_id=organization_id,
    sql_query="SELECT * FROM readings LIMIT 5"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_by_sql).

{{% /tab %}}
{{< /tabs >}}

### TabularDataByMQL

Obtain unified tabular data and metadata, queried with MQL.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The ID of the organization that owns the data.
- `mql_binary` (List[bytes]): The MQL query to run as a list of BSON documents.

**Returns:**

- (List[Dict[str, ValueTypes]]): An array of data objects.

```python {class="line-numbers linkable-line-numbers"}
tabular_data = await data_client.tabular_data_by_mql(
    organization_id=organization_id,
    mql_query=[
        bson.dumps({'$match': {'location_id': '<location-id>'}}),
        bson.dumps({"$limit": 5})
    ]
)
```

You must `import bson` to create valid bson binary objects as input for the `tabular_data_by_mql` method.
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_by_mql).

{{% /tab %}}
{{< /tabs >}}

### DeleteTabularData

Delete tabular data older than a specified number of days.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): ID of organization to delete data from.
  You can obtain your organization id from the [organization settings page](/cloud/organizations/).
- `delete_older_than_days` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): Delete data that was captured up to this many days ago.
  For example if delete_older_than_days is `10`, this deletes any data that was captured up to 10 days ago.
  If it is `0`, all existing data is deleted.

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

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter "viam.proto.app.data.Filter")): Optional Filter specifying binary data to delete.
  Passing an empty Filter will lead to all data being deleted.
  Exercise caution when using this option.

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

- `binary_ids` (List[[viam.proto.app.data.BinaryID](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID "viam.proto.app.data.BinaryID")]): BinaryID objects specifying the data to be deleted.
  Must be non-empty.

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

- `tags` ([List[str]](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): List of tags to add to specified binary data.
  Must be non-empty.
- `binary_ids` (List[viam.app.proto.BinaryID]): List of BinaryID objects specifying binary data to tag.
  Must be non-empty.

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

- `tags` ([List[str]](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): List of tags to add to specified binary data.
  Must be non-empty.
- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter "viam.proto.app.data.Filter")): Filter specifying binary data to tag. If no Filter is provided, all data will be tagged.

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

- `tags` ([List[str]](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): List of tags to remove from specified binary data.
  Must be non-empty.
- `file_ids` ([List[str]](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): List of BinaryID objects specifying binary data to untag.
  Must be non-empty.

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

- `tags` ([List[str]](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): List of tags to remove from specified binary data.
- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter "viam.proto.app.data.Filter")): Filter specifying binary data to untag.
  If no Filter is provided, all data will be untagged.

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

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter "viam.proto.app.data.Filter")): Filter specifying data to retrieve from. If no Filter is provided, all data tags are returned.

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

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter "viam.proto.app.data.Filter")): Filter specifying data to retrieve from. If no Filter is provided, all labels will return.

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

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): Organization to retrieve the connection for.
  You can obtain your organization id from the [organization settings page](/cloud/organizations/).

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
- `part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): Part ID of the component used to capture the data. See [Find part ID](#find-part-id) for instructions on retrieving this value.
- `component_type` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): Type of the component used to capture the data.
- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): Name of the component used to capture the data.
- `method_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): Name of the method used to capture the data.
- `tags` ([Optional[List[str]]](https://docs.python.org/3/library/stdtypes.html#typesseq-list)): Optional list of [image tags](/services/data/dataset/#image-tags) to allow for tag-based data filtering when retrieving data.
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
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Part ID of the component used to capture the data. See [Find part ID](#find-part-id) for instructions on retrieving this value.
- `component_type` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Type of the component used to capture the data.
- `component_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the component used to capture the data.
- `method_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the method used to capture the data.
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/services/data/dataset/#image-tags) to allow for tag-based data filtering when retrieving data.
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

### StreamingDataCaptureUpload

Upload the contents of streaming binary data and the relevant metadata to the [Viam app](https://app.viam.com).
Uploaded streaming data can be found under the [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `data` [(bytes)](https://docs.python.org/3/library/stdtypes.html#bytes-objects): Data to be uploaded, represented in bytes.
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Part ID of the resource associated with the file.
- `file_ext` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): File extension type for the data. required for determining MIME type.
- `component_type` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional type of the component associated with the file (For example, “movement_sensor”).
- `component_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional name of the component associated with the file.
- `method_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional name of the method associated with the file.
- `method_parameters` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional dictionary of the method parameters. No longer in active use.
- `data_request_times` [(Optional[Tuple[datetime.datetime, datetime.datetime]])](https://docs.python.org/3/library/stdtypes.html#tuples): Optional tuple containing [`datetime`](https://docs.python.org/3/library/datetime.html) objects denoting the times this data was requested and received by the appropriate sensor.
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/services/data/dataset/#image-tags) to allow for tag-based data filtering when retrieving data.

**Returns:**

- [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The `file_id` of the uploaded data.

**Raises:**

- `GRPCError` – If an invalid part ID is passed.

```python {class="line-numbers linkable-line-numbers"}
time_requested = datetime(2023, 6, 5, 11)
time_received = datetime(2023, 6, 5, 11, 0, 3)

file_id = await data_client.streaming_data_capture_upload(
    data="byte-data-to-upload",
    part_id="INSERT YOUR PART ID",
    file_ext="png",
    component_type='motor',
    component_name='left_motor',
    method_name='IsPowered',
    data_request_times=[(time_requested, time_received)],
    tags=["tag_1", "tag_2"]
)

print(file_id)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.streaming_data_capture_upload).

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
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Part ID of the component used to capture the data. See [Find part ID](#find-part-id) for instructions on retrieving this value.
- `component_type` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Type of the component used to capture the data.
- `component_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the component used to capture the data.
- `file_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional name of the file. The empty string `""` will be assigned as the filename if one isn’t provided.
- `file_extension` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional file extension. The empty string `""` will be assigned as the file extension if one isn’t provided.
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/services/data/dataset/#image-tags) to allow for tag-based data filtering when retrieving data.

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
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Part ID of the component used to capture the data. See [Find part ID](#find-part-id) for instructions on retrieving this value.
- `component_type` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Type of the component used to capture the data.
- `component_name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the component used to capture the data.
- `tags` [(Optional[List[str]])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): Optional list of [image tags](/services/data/dataset/#image-tags) to allow for tag-based data filtering when retrieving data.

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

### AddBoundingBoxToImageById

Add a bounding box to an image specified by its BinaryID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_id` ([viam.proto.app.data.BinaryID](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)): The ID of the image to add the bounding box to.
- `label` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): A label for the bounding box.
- `x_min_normalized` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): Minimum X value of the bounding box normalized from `0` to `1`.
- `y_min_normalized` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): Minimum Y value of the bounding box normalized from `0` to `1`.
- `x_max_normalized` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): Maximum X value of the bounding box normalized from `0` to `1`.
- `y_max_normalized` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): Maximum Y value of the bounding box normalized from `0` to `1`.

**Returns:**

- [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The bounding box ID of the image.

**Raises:**

- `GRPCError` – If the X or Y values are outside of the [0, 1] range.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import BinaryID

MY_BINARY_ID = BinaryID(
    file_id=your-file_id,
    organization_id=your-org-id,
    location_id=your-location-id
)

bbox_label = await data_client.add_bounding_box_to_image_by_id(
  binary_id=MY_BINARY_ID,
  label="label",
  x_min_normalized=0,
  y_min_normalized=.1,
  x_max_normalized=.2,
  y_max_normalized=.3
)

print(bbox_label)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_bounding_box_to_image_by_id).

{{% /tab %}}
{{< /tabs >}}

### RemoveBoundingBoxFromImageById

Removes a bounding box from an image specified by its BinaryID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `bbox_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The ID of the bounding box to remove.
- `binary_id` ([viam.proto.app.data.BinaryID](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)): Binary ID of the image to to remove the bounding box from.

**Returns:**

- None.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import BinaryID

MY_BINARY_ID = BinaryID(
    file_id=your-file_id,
    organization_id=your-org-id,
    location_id=your-location-id
)

await data_client.remove_bounding_box_from_image_by_id(
  binary_id=MY_BINARY_ID,
  bbox_id="your-bounding-box-id-to-delete"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_bounding_box_from_image_by_id).

{{% /tab %}}
{{< /tabs >}}

### CreateDataset

Create a new dataset.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The name of the dataset being created.
- `organization_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The ID of the organization where the dataset is being created.

**Returns:**

- [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The dataset ID of the created dataset.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.create_dataset).

```python {class="line-numbers linkable-line-numbers"}
name = await data_client.create_dataset(
  name="<dataset-name>",
  organization_id="<your-org-id>"
)
print(name)
```

{{% /tab %}}
{{< /tabs >}}

### ListDatasetByIds

Get a list of datasets using their IDs.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `ids` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): The IDs of the datasets being called for.

**Returns:**

- (Sequence[[Dataset](https://python.viam.dev/autoapi/viam/gen/app/dataset/v1/dataset_pb2/index.html#viam.gen.app.dataset.v1.dataset_pb2.Dataset)]): The list of datasets.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.list_dataset_by_ids).

```python {class="line-numbers linkable-line-numbers"}
datasets = await data_client.list_dataset_by_ids(
  ids=["abcd-1234xyz-8765z-123abc"]
)
print(datasets)
```

{{% /tab %}}
{{< /tabs >}}

### ListDatasetByOrganizationId

Get the datasets in an organization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The ID of the organization.

**Returns:**

- (Sequence[[Dataset](https://python.viam.dev/autoapi/viam/gen/app/dataset/v1/dataset_pb2/index.html#viam.gen.app.dataset.v1.dataset_pb2.Dataset)]): The list of datasets in the organization.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.list_datasets_by_organization_id).

```python {class="line-numbers linkable-line-numbers"}
datasets = await data_client.list_datasets_by_organization_id(
  organization_id="<your-org-id>"
)
print(datasets)
```

{{% /tab %}}
{{< /tabs >}}

### RenameDataset

Rename a dataset specified by the dataset ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The ID of the dataset. To retrieve this, navigate to your dataset's page in the [Viam app](https://app.viam.com/data/datasets), click **...** in the left-hand menu, and click **Copy dataset ID**.
- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The new name of the dataset.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.rename_dataset).

```python {class="line-numbers linkable-line-numbers"}
await data_client.rename_dataset(
    id="abcd-1234xyz-8765z-123abc",
    name="<dataset-name>"
)
```

{{% /tab %}}
{{< /tabs >}}

### DeleteDataset

Delete a dataset.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The ID of the dataset.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_dataset).

```python {class="line-numbers linkable-line-numbers"}
await data_client.delete_dataset(
  id="abcd-1234xyz-8765z-123abc"
)
```

{{% /tab %}}
{{< /tabs >}}

### AddBinaryDataToDatasetByIds

Add the [BinaryData](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryData) to the provided dataset.
This BinaryData will be tagged with the VIAM_DATASET\_{id} label.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_ids` (List[[BinaryID](https://python.viam.dev/autoapi/viam/gen/app/data/v1/data_pb2/index.html#viam.gen.app.data.v1.data_pb2.BinaryID "viam.gen.app.data.v1.data_pb2.BinaryID")]): The IDs of binary data to add to dataset.
- `dataset_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The ID of the dataset to be added to.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_binary_data_to_dataset_by_ids).

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import BinaryID

binary_metadata = await data_client.binary_data_by_filter(
    include_file_data=False
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
    dataset_id="abcd-1234xyz-8765z-123abc"
)
```

{{% /tab %}}
{{< /tabs >}}

### RemoveBinaryDataFromDatasetByIds

Remove the BinaryData from the provided dataset.
This BinaryData will lose the VIAM_DATASET\_{id} tag.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_ids` (List[[BinaryID](https://python.viam.dev/autoapi/viam/gen/app/data/v1/data_pb2/index.html#viam.gen.app.data.v1.data_pb2.BinaryID "viam.gen.app.data.v1.data_pb2.BinaryID")]): The IDs of binary data to remove from dataset.
- `dataset_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The ID of the dataset to be removed from.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_binary_data_from_dataset_by_ids).

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import BinaryID

binary_metadata = await data_client.binary_data_by_filter(
    include_file_data=False
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
    dataset_id="abcd-1234xyz-8765z-123abc"
)
```

{{% /tab %}}
{{< /tabs >}}

### ConfigureDatabaseUser

Configure a database user for the Viam organization’s MongoDB Atlas Data Federation instance.
You can also use this to reset the password of the existing database user.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The ID of the organization.
- `password` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The password of the user.

**Returns:**

- None.

```python {class="line-numbers linkable-line-numbers"}
await data_client.configure_database_user(
    organization_id=organization_id,
    password="CHANGE-ME"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.configure_database_user).

{{% /tab %}}
{{< /tabs >}}

## Find part ID

To copy the ID of your machine part, select the part status dropdown to the right of your machine's location and name on the top of its page and click the copy icon next to **Part ID**.

For example:

![Part ID displayed in the Viam app.](/build/program/data-client/grab-part-id.png)
