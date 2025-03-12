### GetLatestTabularData

Gets the most recent tabular data captured from the specified data source, as long as it was synced within the last year.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the part that owns the data.
- `resource_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the requested resource that captured the data. Ex: “my-sensor”.
- `resource_api` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The API of the requested resource that captured the data. Ex: “rdk:component:sensor”.
- `method_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The data capture method name. Ex: “Readings”.

**Returns:**

- (Tuple[[datetime.datetime](https://docs.python.org/3/library/datetime.html), [datetime.datetime](https://docs.python.org/3/library/datetime.html), Dict[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]] | None): A return value of None means that data hasn’t been synced yet for the data source or the most recently captured data was over a year ago, otherwise the returned tuple contains the following: datetime: The time captured, datetime: The time synced, Dict[str, ValueTypes]: The latest tabular data captured from the specified data source.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
tabular_data = await data_client.get_latest_tabular_data(
    part_id="77ae3145-7b91-123a-a234-e567cdca8910",
    resource_name="camera-1",
    resource_api="rdk:component:camera",
    method_name="GetImage"
)

if tabular_data:
    time_captured, time_synced, payload = tabular_data
    print(f"Time Captured: {time_captured}")
    print(f"Time Synced: {time_synced}")
    print(f"Payload: {payload}")
else:
    print(f"No data returned: {tabular_data}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.get_latest_tabular_data).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `partId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `resourceName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `resourceSubtype` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `methodName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<({[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic> payload, [DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html) timeCaptured, [DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html) timeSynced})?>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 try {
   // Get latest tabular data
   final response = await dataClient.getLatestTabularData(
     "<YOUR-PART-ID>",
     "movement_sensor-1",
     "rdk:component:movement_sensor",
     "Position"
   );
   print('Successfully retrieved latest tabular data: $response');
 } catch (e) {
   print('Error retrieving latest tabular data: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/getLatestTabularData.html).

{{% /tab %}}
{{< /tabs >}}

### ExportTabularData

Obtain unified tabular data and metadata from the specified data source.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the part that owns the data.
- `resource_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the requested resource that captured the data.
- `resource_api` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The API of the requested resource that captured the data.
- `method_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The data capture method name.
- `start_time` ([datetime.datetime](https://docs.python.org/3/library/datetime.html)) (optional): Optional start time for requesting a specific range of data.
- `end_time` ([datetime.datetime](https://docs.python.org/3/library/datetime.html)) (optional): Optional end time for requesting a specific range of data.

**Returns:**

- ([List[TabularDataPoint]](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.TabularDataPoint)): The unified tabular data and metadata.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
tabular_data = await data_client.export_tabular_data(
    part_id="<PART-ID>",
    resource_name="<RESOURCE-NAME>",
    resource_api="<RESOURCE-API>",
    method_name="<METHOD-NAME>",
    start_time="<START_TIME>"
    end_time="<END_TIME>"
)

print(f"My data: {tabular_data}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.export_tabular_data).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `partId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `resourceName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `resourceSubtype` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `methodName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `startTime` [DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html)? (required)
- `endTime` [DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html)? (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[TabularDataPoint](https://flutter.viam.dev/viam_sdk/TabularDataPoint-class.html)>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
 _viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 try {
  // Define date request times
  final startTime = DateTime(2025, 1, 23, 11);
  final endTime = DateTime(2025, 1, 23, 11, 0, 3);

  final tabularData = await dataClient.exportTabularData(
    "<YOUR-PART-ID>",
    "movement_sensor-1",
    "rdk:component:movement_sensor",
    "Position",
    startTime,
    endTime
  );

  for (var dataPoint in tabularData) {
    print(dataPoint.partId);
    print(dataPoint.resourceName);
    print(dataPoint.methodName);
    print(dataPoint.payload);
  }

  print('Successfully exported tabular data');
 } catch (e) {
  print('Error exporting tabular data: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/exportTabularData.html).

{{% /tab %}}
{{< /tabs >}}

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
my_filter = create_filter(component_name="motor-1")
last = None
while True:
    tabular_data, count, last = await data_client.tabular_data_by_filter(my_filter, last=last)
    if not tabular_data:
        break
    my_data.extend(tabular_data)

print(f"My data: {my_data}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_by_filter).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `filter` [Filter](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html)? (optional)
- `limit` [int](https://api.flutter.dev/flutter/dart-core/int-class.html)? (optional)
- `sortOrder` [Order](https://flutter.viam.dev/viam_protos.app.data/Order-class.html)? (optional)
- `last` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `countOnly` dynamic (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[TabularDataByFilterResponse](https://flutter.viam.dev/viam_protos.app.data/TabularDataByFilterResponse-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
    dotenv.env['API_KEY_ID'] ?? '',
    dotenv.env['API_KEY'] ?? ''
);
final dataClient = _viam.dataClient;

try {
 // Create a filter to target specific tabular data
 final filter = Filter(
  componentName: "arm-1",
 );

 final response = await dataClient.tabularDataByFilter(
   filter: filter,
   limit: 10
 );
 print('Number of items: ${response.count.toInt()}');
 print('Total size: ${response.totalSizeBytes.toInt()}');
 for (var metadata in response.metadata) {
   print(metadata);
 }
 for (var data in response.data) {
   print(data);
 }

 print('Successfully retrieved tabular data by filter');
} catch (e) {
 print('Error retrieving tabular data by filter: $e');
}
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/tabularDataByFilter.html).

{{% /tab %}}
{{< /tabs >}}

### TabularDataBySQL

Obtain unified tabular data and metadata, queried with SQL. Make sure your API key has permissions at the organization level in order to use this.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that owns the data. You can obtain your organization ID from the Viam app’s organization settings page.
- `sql_query` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The SQL query to run.

**Returns:**

- (List[Dict[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes | [datetime.datetime](https://docs.python.org/3/library/datetime.html)]]): An array of decoded BSON data objects.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
data = await data_client.tabular_data_by_sql(
    organization_id="<YOUR-ORG-ID>",
    sql_query="SELECT * FROM readings LIMIT 5"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_by_sql).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `query` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>\>>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// List<Map<String, dynamic>>? _responseData;

 _viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 // Example SQL query
 final sqlQuery = "SELECT * FROM readings LIMIT 5";

 _responseData = await dataClient.tabularDataBySql(
   "<YOUR-ORG-ID>",
   sqlQuery
 );
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/tabularDataBySql.html).

{{% /tab %}}
{{< /tabs >}}

### TabularDataByMQL

Obtain unified tabular data and metadata, queried with MQL.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that owns the data. You can obtain your organization ID from the Viam app’s organization settings page.
- `query` (List[[bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)] | List[Dict[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]]) (required): The MQL query to run, as a list of MongoDB aggregation pipeline stages. Note: Each stage can be provided as either a dictionary or raw BSON bytes, but support for bytes will be removed in the future, so using a dictionary is preferred.
- `use_recent_data` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (optional): Whether to query blob storage or your recent data store. Defaults to False.

**Returns:**

- (List[Dict[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes | [datetime.datetime](https://docs.python.org/3/library/datetime.html)]]): An array of decoded BSON data objects.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
import bson

tabular_data = await data_client.tabular_data_by_mql(organization_id="<YOUR-ORG-ID>", query=[
    { '$match': { 'location_id': '<YOUR-LOCATION-ID>' } },
    { "$limit": 5 }
])

print(f"Tabular Data: {tabular_data}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_by_mql).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `query` dynamic (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>\>>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// import 'package:bson/bson.dart';

// List<Map<String, dynamic>>? _responseData;

 _viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 final query = BsonCodec.serialize({
  "\$match": {
     "location_id": "<YOUR-LOCATION-ID>",
  }
 });

 final sort = BsonCodec.serialize({
   "\$sort": {"time_requested": -1}
   sqlQuery
 });

 final limit = BsonCodec.serialize({"\$limit": 1});

 final pipeline = [query.byteList, sort.byteList, limit.byteList];
 _responseData = await dataClient.tabularDataByMql(
  "<YOUR-ORG-ID>",
  pipeline
 );
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/tabularDataByMql.html).

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
from viam.proto.app.data import Filter, TagsFilter, TagsFilterType

# Get data captured from camera components
my_data = []
last = None
my_filter = create_filter(component_name="camera-1")

while True:
    data, count, last = await data_client.binary_data_by_filter(
        my_filter, limit=1, last=last)
    if not data:
        break
    my_data.extend(data)

print(f"My data: {my_data}")

# Get untagged data from a dataset

my_untagged_data = []
last = None
tags_filter = TagsFilter(type=TagsFilterType.TAGS_FILTER_TYPE_UNTAGGED)
my_filter = Filter(
    dataset_id="66db6fe7d93d1ade24cd1dc3",
    tags_filter=tags_filter
)

while True:
    data, count, last = await data_client.binary_data_by_filter(
        my_filter, last=last, include_binary_data=False)
    if not data:
        break
    my_untagged_data.extend(data)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_by_filter).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `filter` [Filter](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html)? (optional)
- `limit` [int](https://api.flutter.dev/flutter/dart-core/int-class.html)? (optional)
- `sortOrder` [Order](https://flutter.viam.dev/viam_protos.app.data/Order-class.html)? (optional)
- `last` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `countOnly` [bool](https://api.flutter.dev/flutter/dart-core/bool-class.html) (optional)
- `includeBinary` [bool](https://api.flutter.dev/flutter/dart-core/bool-class.html) (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[BinaryDataByFilterResponse](https://flutter.viam.dev/viam_protos.app.data/BinaryDataByFilterResponse-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
    dotenv.env['API_KEY_ID'] ?? '',
    dotenv.env['API_KEY'] ?? ''
);
final dataClient = _viam.dataClient;

try {
 // Create a filter to target specific binary data
 final filter = Filter(
  componentName: "camera-1",
 );

 final response = await dataClient.binaryDataByFilter(filter: filter, limit: 1);

 print('Number of items: ${response.count.toInt()}');
 print('Total size: ${response.totalSizeBytes.toInt()} bytes');
 for (var dataPoint in response.data) {
   print(dataPoint.binary);
   print(dataPoint.metadata);
 }

 print('Successfully retrieved binary data by filter');
} catch (e) {
 print('Error retrieving binary data by filter: $e');
}
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/binaryDataByFilter.html).

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

binary_metadata, count, last = await data_client.binary_data_by_filter(
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
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_by_ids).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryIds` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)> (required)
- `includeBinary` [bool](https://api.flutter.dev/flutter/dart-core/bool-class.html) (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[BinaryDataByIDsResponse](https://flutter.viam.dev/viam_protos.app.data/BinaryDataByIDsResponse-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
 _viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 try {
  final binaryIDs = [
   BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>'),
   BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>')
  ];

  final response = await dataClient.binaryDataByIds(
    binaryIDs,
    includeBinary: true
  );

  for (var dataPoint in response.data) {
    print(dataPoint.binary);
    print(dataPoint.metadata);
  }

  print('Successfully retrieved binary data by IDs');
 } catch (e) {
  print('Error retrieving binary data by IDs: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/binaryDataByIds.html).

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
tabular_data = await data_client.delete_tabular_data(
    organization_id="<YOUR-ORG-ID>",
    delete_older_than_days=150
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_tabular_data).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `olderThanDays` [int](https://api.flutter.dev/flutter/dart-core/int-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
    dotenv.env['API_KEY_ID'] ?? '',
    dotenv.env['API_KEY'] ?? ''
);
final dataClient = _viam.dataClient;

try {
  dataClient.deleteTabularData("<YOUR-ORG-ID>", 5);

 print('Successfully deleted tabular data');
} catch (e) {
 print('Error deleting tabular data: $e');
}
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/deleteTabularData.html).

{{% /tab %}}
{{< /tabs >}}

### DeleteBinaryDataByFilter

Filter and delete binary data.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter)) (optional): Optional Filter specifying binary data to delete. Passing an empty Filter will lead to all data being deleted. Exercise caution when using this option. You must specify an organization ID with “organization_ids” when using this option.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The number of items deleted.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.utils import create_filter

my_filter = create_filter(component_name="left_motor", organization_ids=["<YOUR-ORG-ID>"])

res = await data_client.delete_binary_data_by_filter(my_filter)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_binary_data_by_filter).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `filter` [Filter](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html)? (required)
- `includeInternalData` [bool](https://api.flutter.dev/flutter/dart-core/bool-class.html) (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
 _viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 try {
  // Create a filter to target specific binary data. Must include at least one org ID.
  final filter = Filter(
   componentName: "camera-1",
   organizationIds: ["<YOUR-ORG-ID>"]
  );

  final deletedCount = await dataClient.deleteBinaryDataByFilter(filter);

  print('Successfully deleted binary data by filter: count $deletedCount');
 } catch (e) {
  print('Error deleting binary data by filter: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/deleteBinaryDataByFilter.html).

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
from viam.utils import create_filter

my_filter = create_filter(component_name="camera-1", organization_ids=["<YOUR-ORG-ID>"])
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

binary_data = await data_client.delete_binary_data_by_ids(my_ids)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_binary_data_by_ids).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryIds` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
 _viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 try {
  final binaryIDs = [
   BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>'),
   BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>')
  ];

  // Call the function to delete binary data
  await dataClient.deleteBinaryDataByIds(binaryIDs);

  print('Successfully deleted binary data');
 } catch (e) {
  print('Error deleting binary data: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/deleteBinaryDataByIds.html).

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
from viam.utils import create_filter

tags = ["tag1", "tag2"]

my_filter = create_filter(component_name="camera-1", organization_ids=["<YOUR-ORG-ID>"])
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
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_tags_to_binary_data_by_ids).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `tags` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)> (required)
- `binaryIds` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
 _viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 try {
  // List of tags to add
  final List<String> tags = ['tag_1', 'tag_2'];

  final binaryIDs = [
   BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>'),
   BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>')
  ];

  // Call the function with both tags and IDs
  await dataClient.addTagsToBinaryDataByIds(tags, binaryIDs);

  print('Successfully added tags to binary IDs');
 } catch (e) {
  print('Error adding tags: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/addTagsToBinaryDataByIds.html).

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
await data_client.add_tags_to_binary_data_by_filter(tags, my_filter)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_tags_to_binary_data_by_filter).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `tags` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)> (required)
- `filter` [Filter](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html)? (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
 _viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 try {
  // List of tags to add
  final List<String> tags = ['tag_1', 'tag_2'];

  // Create a filter to target specific binary data
  final filter = Filter(
   componentName: "camera-1",
  );

  await dataClient.addTagsToBinaryDataByFilter(tags, filter);

  print('Successfully added tags to binary data by filter');
 } catch (e) {
  print('Error adding tags to binary data by filter: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/addTagsToBinaryDataByFilter.html).

{{% /tab %}}
{{< /tabs >}}

### RemoveTagsFromBinaryDataByIDs

Remove tags from binary by ids.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (required): List of tags to remove from specified binary data. Must be non-empty.
- `binary_ids` ([List[viam.proto.app.data.BinaryID]](https://python.viam.dev/autoapi/viam/gen/app/data/v1/data_pb2/index.html#viam.gen.app.data.v1.data_pb2.BinaryID)) (required): List of BinaryID objects specifying binary data to untag. Must be non-empty.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The number of tags removed.

**Raises:**

- (GRPCError): If no binary_ids or tags are provided.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import BinaryID
from viam.utils import create_filter

tags = ["tag1", "tag2"]

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

binary_data = await data_client.remove_tags_from_binary_data_by_ids(
    tags, my_ids)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_tags_from_binary_data_by_ids).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `tags` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)> (required)
- `binaryIds` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
 _viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 try {
  // List of tags to remove
  final List<String> tags = ['tag_1', 'tag_2'];

  final binaryIDs = [
   BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>'),
   BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>')
  ];

  // Call the function with both tags and IDs
  await dataClient.removeTagsFromBinaryDataByIds(tags, binaryIDs);

  print('Successfully removed tags from binary IDs');
 } catch (e) {
  print('Error removing tags: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/removeTagsFromBinaryDataByIds.html).

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
{{% tab name="Flutter" %}}

**Parameters:**

- `tags` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)> (required)
- `filter` [Filter](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html)? (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
    dotenv.env['API_KEY_ID'] ?? '',
    dotenv.env['API_KEY'] ?? ''
);
final dataClient = _viam.dataClient;

try {
 // List of tags to remove
 final List<String> tags = ['tag_1', 'tag_2'];

 // Create a filter to target specific binary data
 final filter = Filter(
  componentName: "camera-1",
 );

 await dataClient.removeTagsFromBinaryDataByFilter(tags, filter);

 print('Successfully removed tags from binary data by filter');
} catch (e) {
 print('Error removing tags from binary data by filter: $e');
}
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/removeTagsFromBinaryDataByFilter.html).

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
{{% tab name="Flutter" %}}

**Parameters:**

- `filter` [Filter](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html)? (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
);
final dataClient = _viam.dataClient;

try {
 // Create a filter to target specific binary data
 final filter = Filter(
   componentName: "camera-1",
 );

 // Call the function to get tags by filter
 final tags = await dataClient.tagsByFilter(filter);

 print('Successfully got tags: $tags');
} catch (e) {
 print('Error getting tags: $e');
}
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/tagsByFilter.html).

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
    file_id="<YOUR-FILE-ID>",
    organization_id="<YOUR-ORG-ID>",
    location_id="<YOUR-LOCATION-ID>"
)

bbox_id = await data_client.add_bounding_box_to_image_by_id(
    binary_id=MY_BINARY_ID,
    label="label",
    x_min_normalized=0,
    y_min_normalized=.1,
    x_max_normalized=.2,
    y_max_normalized=.3
)

print(bbox_id)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_bounding_box_to_image_by_id).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `label` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `binaryId` [BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html) (required)
- `xMinNormalized` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `yMinNormalized` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `xMaxNormalized` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `yMaxNormalized` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

// Example binary ID to add a bounding box to
final binaryId = BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>');

try {
  await dataClient.addBoundingBoxToImageById(
    "label",
    binaryId,
    0,
   .1,
   .2,
   .3
  );
  print('Successfully added bounding box');
} catch (e) {
  print('Error adding bounding box: $e');
}
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/addBoundingBoxToImageById.html).

{{% /tab %}}
{{< /tabs >}}

### RemoveBoundingBoxFromImageByID

Removes a bounding box from an image specified by its BinaryID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `bbox_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the bounding box to remove.
- `binary_id` ([viam.proto.app.data.BinaryID](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)) (required): Binary ID of the image to remove the bounding box from.

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
{{% tab name="Flutter" %}}

**Parameters:**

- `bboxId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `binaryId` [BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

// Example binary ID to remove a bounding box from
final binaryId = BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>');

// Example bbox ID (label)
final bboxId = "label";
try {
  await dataClient.removeBoundingBoxFromImageById(
    bboxId,
    binaryId,
  );

  print('Successfully removed bounding box');
} catch (e) {
  print('Error removing bounding box: $e');
}
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/removeBoundingBoxFromImageById.html).

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

print(bounding_box_labels)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.bounding_box_labels_by_filter).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `filter` [Filter](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html)? (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
);
final dataClient = _viam.dataClient;

try {
 // Create a filter to target specific binary data
 final filter = Filter(
   componentName: "camera-1",
 );

 // Call the function to get bounding box labels by filter
 final labels = await dataClient.boundingBoxLabelsByFilter(filter);

 print('Successfully got bounding box labels: $labels');
} catch (e) {
 print('Error getting bounding box labels: $e');
}
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/boundingBoxLabelsByFilter.html).

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
hostname = await data_client.get_database_connection(organization_id="<YOUR-ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.get_database_connection).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[DatabaseConnection](https://flutter.viam.dev/viam_sdk/DatabaseConnection.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
);
final dataClient = _viam.dataClient;

try {
 final String organizationId = "<YOUR-ORG-ID>";
 // Get the database connection
 final connection = await dataClient.getDatabaseConnection(organizationId);

 final hostname = connection.hostname;
 final mongodbUri = connection.mongodbUri;

 print('Successfully got database connection: with hostname $hostname and mongodbUri $mongodbUri');
} catch (e) {
 print('Error getting database connection: $e');
}
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/getDatabaseConnection.html).

{{% /tab %}}
{{< /tabs >}}

### ConfigureDatabaseUser

Configure a database user for the Viam organization’s MongoDB Atlas Data Federation instance.
It can also be used to reset the password of the existing database user.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization. You can obtain your organization ID from the Viam app’s organization settings page.
- `password` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The password of the user.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await data_client.configure_database_user(
    organization_id="<YOUR-ORG-ID>",
    password="Your_Password@1234"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.configure_database_user).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `password` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
);
final dataClient = _viam.dataClient;

try {
 await dataClient.configureDatabaseUser(
   "<YOUR-ORG-ID>",
   "PasswordLikeThis1234",
 );

 print('Successfully configured database user for this organization');
} catch (e) {
 print('Error configuring database user: $e');
}
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/configureDatabaseUser.html).

{{% /tab %}}
{{< /tabs >}}

### AddBinaryDataToDatasetByIDs

Add the `BinaryData` to the provided dataset.
This BinaryData will be tagged with the VIAM_DATASET\_{id} label.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_ids` ([List[viam.proto.app.data.BinaryID]](https://python.viam.dev/autoapi/viam/gen/app/data/v1/data_pb2/index.html#viam.gen.app.data.v1.data_pb2.BinaryID)) (required): The IDs of binary data to add to dataset. To retrieve these IDs, navigate to your data page, click on an image and copy its File ID from the details tab. To retrieve the dataset ID, navigate to your dataset's page in the Viam app, and use the left-hand menu to copy the dataset ID.
- `dataset_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the dataset to be added to.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import BinaryID

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
    dataset_id="abcd-1234xyz-8765z-123abc"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_binary_data_to_dataset_by_ids).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryIds` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)> (required)
- `datasetId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

// Example binary IDs to add to the dataset
 final binaryIds = [
   BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>'),
   BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>')
 ];

 // Dataset ID where the binary data will be added
 const datasetId = '<YOUR-DATASET-ID>';

 try {
   // Add the binary data to the dataset
   await dataClient.addBinaryDataToDatasetByIds(
     binaryIds,
     datasetId
 );
   print('Successfully added binary data to dataset');
 } catch (e) {
   print('Error adding binary data to dataset: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/addBinaryDataToDatasetByIds.html).

{{% /tab %}}
{{< /tabs >}}

### RemoveBinaryDataFromDatasetByIDs

Remove the BinaryData from the provided dataset.
This BinaryData will lose the VIAM_DATASET\_{id} tag.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_ids` ([List[viam.proto.app.data.BinaryID]](https://python.viam.dev/autoapi/viam/gen/app/data/v1/data_pb2/index.html#viam.gen.app.data.v1.data_pb2.BinaryID)) (required): The IDs of binary data to remove from the dataset. To retrieve these IDs, navigate to your data page, click on an image and copy its File ID from the details tab. To retrieve the dataset ID, navigate to your dataset's page in the Viam app, and use the left-hand menu to copy the dataset ID.
- `dataset_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the dataset to be removed from.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import BinaryID

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
    dataset_id="abcd-1234xyz-8765z-123abc"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_binary_data_from_dataset_by_ids).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryIds` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)> (required)
- `datasetId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

// Example binary IDs to remove from the dataset
 final binaryIds = [
   BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>'),
   BinaryID(fileId: '<YOUR-FILE-ID>', organizationId: '<YOUR-ORG-ID>', locationId: '<YOUR-LOCATION-ID>')
 ];

 // Dataset ID where the binary data will be removed
 const datasetId = '<YOUR-DATASET-ID>';

 try {
   // Remove the binary data from the dataset
   await dataClient.removeBinaryDataFromDatasetByIds(
     binaryIds,
     datasetId
 );
   print('Successfully removed binary data from dataset');
 } catch (e) {
   print('Error removing binary data from dataset: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/removeBinaryDataFromDatasetByIds.html).

{{% /tab %}}
{{< /tabs >}}
