### TabularDataByFilter

Retrieve optionally filtered tabular data from the [Viam app](https://app.viam.com).
You can also find your tabular data under the **Sensors** subtab of the app's [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter)) (optional): Optional Filter specifying tabular data to retrieve. No Filter implies all tabular data.
- `limit` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): The maximum number of entries to include in a page. Defaults to 50 if unspecified.
- `sort_order` ([viam.proto.app.data.Order.ValueType](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Order)) (optional): The desired sort order of the data.
- `last` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional string indicating the object identifier of the last-returned data. This object identifier is returned by calls to `TabularDataByFilter` as the last value. If provided, the server will return the next data entries after the last object identifier.
- `count_only` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Whether to return only the total count of entries.
- `include_internal_data` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Whether to return the internal data. Internal data is used for Viam-specific data ingestion, like cloud SLAM. Defaults to False.
- `dest` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional filepath for writing retrieved data.

**Returns:**

- (Tuple[List[TabularData], [int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex), [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): A tuple containing the following: List[TabularData]: The tabular data, int: The count (number of entries), str: The last-returned page ID.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.utils import create_filter

my_data = []
last = None
my_filter = create_filter(component_name="left_motor")
while True:
    tabular_data, count, last = await data_client.tabular_data_by_filter(my_filter, last)
    if not tabular_data:
        break
    my_data.extend(tabular_data)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_by_filter).

{{% /tab %}}
{{< /tabs >}}

### TabularDataBySQL

Obtain unified tabular data and metadata, queried with SQL.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that owns the data. You can obtain your organization ID from the Viam app’s organization settings page.
- `sql_query` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The SQL query to run.

**Returns:**

- (List[Dict[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]]): An array of data objects.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
data = await data_client.tabular_data_by_sql(org_id="<your-org-id>", sql_query="SELECT * FROM readings LIMIT 5")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_by_sql).

{{% /tab %}}
{{< /tabs >}}

### TabularDataByMQL

Obtain unified tabular data and metadata, queried with MQL.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that owns the data. You can obtain your organization ID from the Viam app’s organization settings page.
- `mql_binary` (List[[bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)]) (required): The MQL query to run as a list of BSON queries. You can encode your bson queries using a library like pymongo or bson.

**Returns:**

- (List[Dict[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]]): An array of data objects.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# using bson
import bson
tabular_data = await data_client.tabular_data_by_mql(org_id="<your-org-id>", mql_binary=[
    bson.dumps({ '$match': { 'location_id': '<location-id>' } }),
    bson.dumps({ "$limit": 5 })
])

# using pymongo
import bson
tabular_data = await data_client.tabular_data_by_mql(org_id="<your-org-id>", mql_binary=[
    bson.encode({ '$match': { 'location_id': '<location-id>' } }),
    bson.encode({ "$limit": 5 })
])
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_by_mql).

{{% /tab %}}
{{< /tabs >}}

### BinaryDataByFilter

Retrieve optionally filtered binary data from the [Viam app](https://app.viam.com).
You can also find your binary data under the **Images**, **Point clouds**, or **Files** subtab of the app's [**Data** tab](https://app.viam.com/data), depending on the type of data that you have uploaded.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter)) (optional): Optional Filter specifying tabular data to retrieve. No Filter implies all binary data.
- `limit` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): The maximum number of entries to include in a page. Defaults to 50 if unspecified.
- `sort_order` ([viam.proto.app.data.Order.ValueType](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Order)) (optional): The desired sort order of the data.
- `last` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional string indicating the object identifier of the last-returned data. This object identifier is returned by calls to `BinaryDataByFilter` as the last value. If provided, the server will return the next data entries after the last object identifier.
- `include_binary_data` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Boolean specifying whether to actually include the binary file data with each retrieved file. Defaults to true (that is, both the files’ data and metadata are returned).
- `count_only` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Whether to return only the total count of entries.
- `include_internal_data` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Whether to return the internal data. Internal data is used for Viam-specific data ingestion, like cloud SLAM. Defaults to False.
- `dest` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional filepath for writing retrieved data.

**Returns:**

- (Tuple[List[viam.proto.app.data.BinaryData], [int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex), [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): A tuple containing the following: List[viam.proto.app.data.BinaryData]: The binary data, int: The count (number of entries), str: The last-returned page ID.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.utils import create_filter


my_data = []
last = None
my_filter = create_filter(component_name="camera")
while True:
    data, count, last = await data_client.binary_data_by_filter(my_filter, last)
    if not data:
        break
    my_data.extend(data)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_by_filter).

{{% /tab %}}
{{< /tabs >}}

### BinaryDataByIDs

Retrieve binary data from the [Viam app](https://app.viam.com) by `BinaryID`.
You can also find your binary data under the **Images**, **Point clouds**, or **Files** subtab of the app's [**Data** tab](https://app.viam.com/data), depending on the type of data that you have uploaded.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_ids` ([List[viam.proto.app.data.BinaryID]](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)) (required): BinaryID objects specifying the desired data. Must be non-empty.
- `dest` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional filepath for writing retrieved data.

**Returns:**

- ([List[viam.proto.app.data.BinaryData]](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryData)): The binary data.

**Raises:**

- (GRPCError): If no BinaryID objects are provided.

**Example:**

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

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of organization to delete data from. You can obtain your organization ID from the Viam app’s organization settings page.
- `delete_older_than_days` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Delete data that was captured up to this many days ago. For example if delete_older_than_days is 10, this deletes any data that was captured up to 10 days ago. If it is 0, all existing data is deleted.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The number of items deleted.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.utils import create_filter

my_filter = create_filter(component_name="left_motor")
days_of_data_to_delete = 10
tabular_data = await data_client.delete_tabular_data(
    org_id="a12b3c4e-1234-1abc-ab1c-ab1c2d345abc", days_of_data_to_delete)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_tabular_data).

{{% /tab %}}
{{< /tabs >}}

### DeleteBinaryDataByFilter

Filter and delete binary data.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter)) (optional): Optional Filter specifying binary data to delete. Passing an empty Filter will lead to all data being deleted. Exercise caution when using this option.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The number of items deleted.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.utils import create_filter

my_filter = create_filter(component_name="left_motor")
res = await data_client.delete_binary_data_by_filter(my_filter)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_binary_data_by_filter).

{{% /tab %}}
{{< /tabs >}}

### DeleteBinaryDataByIDs

Filter and delete binary data by ids.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_ids` ([List[viam.proto.app.data.BinaryID]](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)) (required): BinaryID objects specifying the data to be deleted. Must be non-empty.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The number of items deleted.

**Raises:**

- (GRPCError): If no BinaryID objects are provided.

**Example:**

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

### AddTagsToBinaryDataByIDs

Add tags to binary data by ids.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (required): List of tags to add to specified binary data. Must be non-empty.
- `binary_ids` ([List[viam.proto.app.data.BinaryID]](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)) (required): List of BinaryID objects specifying binary data to tag. Must be non-empty.

**Returns:**

- None.

**Raises:**

- (GRPCError): If no BinaryID objects or tags are provided.

**Example:**

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

- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (required): List of tags to add to specified binary data. Must be non-empty.
- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter)) (optional): Filter specifying binary data to tag. If no Filter is provided, all data will be tagged.

**Returns:**

- None.

**Raises:**

- (GRPCError): If no tags are provided.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.utils import create_filter

my_filter = create_filter(component_name="my_camera")
tags = ["tag1", "tag2"]
res = await data_client.add_tags_to_binary_data_by_filter(tags, my_filter)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_tags_to_binary_data_by_filter).

{{% /tab %}}
{{< /tabs >}}

### RemoveTagsFromBinaryDataByIDs

Remove tags from binary by ids.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (required): List of tags to remove from specified binary data. Must be non-empty.
- `binary_ids` ([List[viam.proto.app.data.BinaryID]](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.BinaryID)) (required): List of BinaryID objects specifying binary data to untag. Must be non-empty.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The number of tags removed.

**Raises:**

- (GRPCError): If no binary_ids or tags are provided.

**Example:**

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

- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (required): List of tags to remove from specified binary data.
- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter)) (optional): Filter specifying binary data to untag. If no Filter is provided, all data will be untagged.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The number of tags removed.

**Raises:**

- (GRPCError): If no tags are provided.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.utils import create_filter

my_filter = create_filter(component_name="my_camera")
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

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter)) (optional): Filter specifying data to retrieve from. If no Filter is provided, all data tags will return.

**Returns:**

- (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): The list of tags.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.utils import create_filter

my_filter = create_filter(component_name="my_camera")
tags = await data_client.tags_by_filter(my_filter)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tags_by_filter).

{{% /tab %}}
{{< /tabs >}}

### AddBoundingBoxToImageByID

Add a bounding box to an image specified by its BinaryID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_id` ([viam.proto.app.data.BinaryID](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)) (required): The ID of the image to add the bounding box to.
- `label` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): A label for the bounding box.
- `x_min_normalized` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Min X value of the bounding box normalized from 0 to 1.
- `y_min_normalized` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Min Y value of the bounding box normalized from 0 to 1.
- `x_max_normalized` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Max X value of the bounding box normalized from 0 to 1.
- `y_max_normalized` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Max Y value of the bounding box normalized from 0 to 1.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The bounding box ID.

**Raises:**

- (GRPCError): If the X or Y values are outside of the [0, 1] range.

**Example:**

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

### RemoveBoundingBoxFromImageByID

Removes a bounding box from an image specified by its BinaryID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `bbox_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the bounding box to remove.
- `binary_id` ([viam.proto.app.data.BinaryID](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)) (required): Binary ID of the image to to remove the bounding box from.

**Returns:**

- None.

**Example:**

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

### BoundingBoxLabelsByFilter

Get a list of bounding box labels using a Filter.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter)) (optional): Filter specifying data to retrieve from. If no Filter is provided, all labels will return.

**Returns:**

- (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): The list of bounding box labels.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.utils import create_filter

my_filter = create_filter(component_name="my_camera")
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

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Organization to retrieve the connection for. You can obtain your organization ID from the Viam app’s organization settings page.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The hostname of the federated database.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
data_client.get_database_connection(org_id="a12b3c4e-1234-1abc-ab1c-ab1c2d345abc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.get_database_connection).

{{% /tab %}}
{{< /tabs >}}

### AddBinaryDataToDatasetByIDs

Add the `BinaryData` to the provided dataset.
This BinaryData will be tagged with the VIAM_DATASET\_{id} label.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_ids` ([List[viam.proto.app.data.BinaryID]](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.BinaryID)) (required): The IDs of binary data to add to dataset. To retrieve these IDs, navigate to your dataset’s page in the Viam app, click … in the left-hand menu, and click Copy dataset ID.
- `dataset_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the dataset to be added to.

**Returns:**

- None.

**Example:**

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

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_binary_data_to_dataset_by_ids).

{{% /tab %}}
{{< /tabs >}}

### RemoveBinaryDataFromDatasetByIDs

Remove the BinaryData from the provided dataset.
This BinaryData will lose the VIAM_DATASET\_{id} tag.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_ids` ([List[viam.proto.app.data.BinaryID]](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.BinaryID)) (required): The IDs of binary data to remove from dataset. To retrieve these IDs, navigate to your dataset’s page in the Viam app, click … in the left-hand menu, and click Copy dataset ID.
- `dataset_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the dataset to be removed from.

**Returns:**

- None.

**Example:**

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

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_binary_data_from_dataset_by_ids).

{{% /tab %}}
{{< /tabs >}}
