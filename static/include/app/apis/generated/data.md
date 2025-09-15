### GetLatestTabularData

Gets the most recent tabular data captured from the specified data source, as long as it was synced within the last year.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the part that owns the data.
- `resource_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the requested resource that captured the data. For example, “my-sensor”.
- `resource_api` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The API of the requested resource that captured the data. For example, “rdk:component:sensor”.
- `method_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The data capture method name. For exampe, “Readings”.
- `additional_params` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]) (optional): Optional additional parameters of the resource that captured the data.

**Returns:**

- (Tuple[[datetime.datetime](https://docs.python.org/3/library/datetime.html), [datetime.datetime](https://docs.python.org/3/library/datetime.html), Dict[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]] | None): A return value of `None` means that this data source
has not synced data in the last year. Otherwise, the data source has synced some data in the last year, so the returned
tuple contains the following:

    * `time_captured` (*datetime*): The time captured.
    * `time_synced` (*datetime*): The time synced.
    * `payload` (*Dict\[str, ValueTypes]*): The latest tabular data captured from the specified data source.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
tabular_data = await data_client.get_latest_tabular_data(
    part_id="77ae3145-7b91-123a-a234-e567cdca8910",
    resource_name="camera-1",
    resource_api="rdk:component:camera",
    method_name="GetImage",
    additional_params={"docommand_input": {"test": "test"}}
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
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `partID`
- `resourceName`
- `resourceSubtype`
- `methodName` [(string)](https://pkg.go.dev/builtin#string)
- `opts` [(*TabularDataOptions)](https://pkg.go.dev/go.viam.com/rdk/app#TabularDataOptions)

**Returns:**

- [(*GetLatestTabularDataResponse)](https://pkg.go.dev/go.viam.com/rdk/app#GetLatestTabularDataResponse)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.GetLatestTabularData).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `partId` (string) (required): The ID of the part that owns the data.
- `resourceName` (string) (required): The name of the requested resource that captured the
  data. Ex: "my\-sensor".
- `resourceSubtype` (string) (required): The subtype of the requested resource that captured
  the data. Ex: "rdk:component:sensor".
- `methodName` (string) (required): The data capture method name. Ex: "Readings".
- `additionalParams` (Record) (optional)

**Returns:**

- (Promise<null | [Date, Date, Record<string, [JsonValue](https://ts.viam.dev/types/JsonValue.html)>]>): A tuple containing \[timeCaptured, timeSynced, payload] or null if
no data has been synced for the specified resource OR the most recently
captured data was over a year ago.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const data = await dataClient.getLatestTabularData(
  '123abc45-1234-5678-90ab-cdef12345678',
  'my-sensor',
  'rdk:component:sensor',
  'Readings'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#getlatesttabulardata).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `partId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `resourceName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `resourceSubtype` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `methodName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `additionalParams` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<({[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\> payload, [DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html) timeCaptured, [DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html) timeSynced})?\>

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
- `additional_params` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]) (optional): Optional additional parameters of the resource that captured the data.

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
    additional_params="<ADDITIONAL_PARAMETERS>"
)

print(f"My data: {tabular_data}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.export_tabular_data).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `partID`
- `resourceName`
- `resourceSubtype`
- `method` [(string)](https://pkg.go.dev/builtin#string)
- `interval` [(CaptureInterval)](https://pkg.go.dev/go.viam.com/rdk/app#CaptureInterval)
- `opts` [(*TabularDataOptions)](https://pkg.go.dev/go.viam.com/rdk/app#TabularDataOptions)

**Returns:**

- [([]*ExportTabularDataResponse)](https://pkg.go.dev/go.viam.com/rdk/app#ExportTabularDataResponse)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.ExportTabularData).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `partId` (string) (required): The ID of the part that owns the data.
- `resourceName` (string) (required): The name of the requested resource that captured the
  data.
- `resourceSubtype` (string) (required): The subtype of the requested resource that captured
  the data.
- `methodName` (string) (required): The data capture method name.
- `startTime` (Date) (optional): Optional start time (`Date` object) for requesting a
  specific range of data.
- `endTime` (Date) (optional): Optional end time (`Date` object) for requesting a specific
  range of data.
- `additionalParams` (Record) (optional)

**Returns:**

- (Promise<TabularDataPoint[]>): An array of unified tabular data and metadata.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const data = await dataClient.exportTabularData(
  '123abc45-1234-5678-90ab-cdef12345678',
  'my-sensor',
  'rdk:component:sensor',
  'Readings',
  new Date('2025-03-25'),
  new Date('2024-03-27')
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#exporttabulardata).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `partId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `resourceName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `resourceSubtype` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `methodName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `startTime` [DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html)? (required)
- `endTime` [DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html)? (required)
- `additionalParams` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[TabularDataPoint](https://flutter.viam.dev/viam_sdk/TabularDataPoint-class.html)\>\>

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

Retrieve optionally filtered tabular data from [Viam](https://app.viam.com).
You can also find your tabular data under the **Sensors** subtab of the [**Data** tab](https://app.viam.com/data).
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter)) (optional): Optional, specifies tabular data to retrieve. If missing, matches all tabular data.
- `limit` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): The maximum number of entries to include in a page. Defaults to 50 if unspecified.
- `sort_order` ([viam.proto.app.data.Order.ValueType](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Order)) (optional): The desired sort order of the data.
- `last` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional string indicating the object identifier of the last-returned data. This object identifier is returned by calls to `TabularDataByFilter` as the last value. If provided, the server will return the next data entries after the last object identifier.
- `count_only` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Whether to return only the total count of entries.
- `include_internal_data` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Whether to return the internal data. Internal data is used for Viam-specific data ingestion, like cloud SLAM. Defaults to False.
- `dest` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional filepath for writing retrieved data.

**Returns:**

- (Tuple[List[TabularData], [int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex), [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): A tuple containing the following:

    * `tabular_data` (*List\[TabularData]*): The tabular data.
    * `count` (*int*): The count (number of entries).
    * `last` (*str*): The last\-returned page ID.

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
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `opts` [(*DataByFilterOptions)](https://pkg.go.dev/go.viam.com/rdk/app#DataByFilterOptions)

**Returns:**

- [(*TabularDataByFilterResponse)](https://pkg.go.dev/go.viam.com/rdk/app#TabularDataByFilterResponse)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.TabularDataByFilter).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `filter` ([Filter](https://ts.viam.dev/classes/dataApi.Filter.html)) (optional): Optional `pb.Filter` specifying tabular data to retrieve. No
  `filter` implies all tabular data.
- `limit` (number) (optional): The maximum number of entries to include in a page. Defaults
  to 50 if unspecfied.
- `sortOrder` ([Order](https://ts.viam.dev/enums/dataApi.Order.html)) (optional): The desired sort order of the data.
- `last` (string) (optional): Optional string indicating the ID of the last\-returned data. If
  provided, the server will return the next data entries after the `last`
  ID.
- `countOnly` (boolean) (optional): Whether to return only the total count of entries.
- `includeInternalData` (boolean) (optional): Whether to retun internal data. Internal data is
  used for Viam\-specific data ingestion, like cloud SLAM. Defaults to
  `false`.

**Returns:**

- (Promise<{ count: bigint; data: TabularData[]; last: string }>): An array of data objects, the count (number of entries), and the
last\-returned page ID.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const data = await dataClient.tabularDataByFilter(
  {
    componentName: 'sensor-1',
    componentType: 'rdk:component:sensor',
  } as Filter,
  5
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#tabulardatabyfilter).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `filter` [Filter](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html)? (optional)
- `limit` [int](https://api.flutter.dev/flutter/dart-core/int-class.html)? (optional)
- `sortOrder` [Order](https://flutter.viam.dev/viam_protos.app.data/Order-class.html)? (optional)
- `last` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `countOnly` dynamic (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[TabularDataByFilterResponse](https://flutter.viam.dev/viam_protos.app.data/TabularDataByFilterResponse-class.html)\>

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

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that owns the data. To find your organization ID, visit the organization settings page.
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
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `organizationID`
- `sqlQuery` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]map[string]interface{})](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.TabularDataBySQL).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization that owns the data.
- `query` (string) (required): The SQL query to run.

**Returns:**

- (Promise<(Object | any[])[]>): An array of data objects.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const data = await dataClient.tabularDataBySQL(
  '123abc45-1234-5678-90ab-cdef12345678',
  'SELECT * FROM readings LIMIT 5'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#tabulardatabysql).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `query` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>\>\>

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

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that owns the data. To find your organization ID, visit the organization settings page.
- `query` (List[[bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)] | List[Dict[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]]) (required): The MQL query to run, as a list of MongoDB aggregation pipeline stages. Each stage can be provided as either a dictionary or raw BSON bytes, but support for bytes will be removed in the future, so prefer the dictionary option.
- `use_recent_data` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (optional): Whether to query blob storage or your recent data store. Defaults to False.. Deprecated, use tabular_data_source_type instead.
- `tabular_data_source_type` ([viam.proto.app.data.TabularDataSourceType.ValueType](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.TabularDataSourceType)) (required): The data source to query. Defaults to TABULAR_DATA_SOURCE_TYPE_STANDARD.
- `pipeline_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): The ID of the data pipeline to query. Defaults to None. Required if tabular_data_source_type is TABULAR_DATA_SOURCE_TYPE_PIPELINE_SINK.

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
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `organizationID` [(string)](https://pkg.go.dev/builtin#string)
- `query` [([]map[string]interface{})](https://pkg.go.dev/builtin#string)
- `opts` [(*TabularDataByMQLOptions)](https://pkg.go.dev/go.viam.com/rdk/app#TabularDataByMQLOptions)

**Returns:**

- [([]map[string]interface{})](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.TabularDataByMQL).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization that owns the data.
- `query` (Uint8Array) (required): The MQL query to run as a list of BSON documents.
- `useRecentData` (boolean) (optional): Whether to query blob storage or your recent data
  store. Defaults to false. Deprecated \- use dataSource instead.
- `tabularDataSource` ([TabularDataSource](https://ts.viam.dev/classes/dataApi.TabularDataSource.html)) (optional)

**Returns:**

- (Promise<(Object | any[])[]>): An array of data objects.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
// {@link JsonValue} is imported from @bufbuild/protobuf
const mqlQuery: Record<string, JsonValue>[] = [
  {
    $match: {
      component_name: 'sensor-1',
    },
  },
  {
    $limit: 5,
  },
];

const data = await dataClient.tabularDataByMQL(
  '123abc45-1234-5678-90ab-cdef12345678',
  mqlQuery
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#tabulardatabymql).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `query` dynamic (required)
- `useRecentData` [bool](https://api.flutter.dev/flutter/dart-core/bool-class.html) (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>\>\>

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

Retrieve optionally filtered binary data from [Viam](https://app.viam.com).
You can also find your binary data under the **Images**, **Point clouds**, or **Files** subtab of the [**Data** tab](https://app.viam.com/data), depending on the type of data that you have uploaded.
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter)) (optional): Optional, specifies tabular data to retrieve. An empty filter matches all binary data.
- `limit` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): The maximum number of entries to include in a page. Defaults to 50 if unspecified.
- `sort_order` ([viam.proto.app.data.Order.ValueType](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Order)) (optional): The desired sort order of the data.
- `last` ([str](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_by_filter)) (optional): Optional string indicating the object identifier of the last-returned data. This object identifier is returned by calls to `BinaryDataByFilter` as the last value. If provided, the server will return the next data entries after the last object identifier.
- `include_binary_data` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Boolean specifying whether to actually include the binary file data with each retrieved file. Defaults to true (that is, both the files’ data and metadata are returned).
- `count_only` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Whether to return only the total count of entries.
- `include_internal_data` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Whether to return the internal data. Internal data is used for Viam-specific data ingestion, like cloud SLAM. Defaults to False.
- `dest` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional filepath for writing retrieved data.

**Returns:**

- (Tuple[List[viam.proto.app.data.BinaryData], [int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex), [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): A tuple containing the following:

    * `data` (*List\[* [`BinaryData`](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryData "viam.proto.app.data.BinaryData") *]*): The binary data.
    * `count` (*int*): The count (number of entries).
    * `last` (*str*): The last\-returned page ID.

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
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `includeBinary` [(bool)](https://pkg.go.dev/builtin#bool)
- `opts` [(*DataByFilterOptions)](https://pkg.go.dev/go.viam.com/rdk/app#DataByFilterOptions)

**Returns:**

- [(*BinaryDataByFilterResponse)](https://pkg.go.dev/go.viam.com/rdk/app#BinaryDataByFilterResponse)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.BinaryDataByFilter).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `filter` ([Filter](https://ts.viam.dev/classes/dataApi.Filter.html)) (optional): Optional `pb.Filter` specifying binary data to retrieve. No
  `filter` implies all binary data.
- `limit` (number) (optional): The maximum number of entries to include in a page. Defaults
  to 50 if unspecfied.
- `sortOrder` ([Order](https://ts.viam.dev/enums/dataApi.Order.html)) (optional): The desired sort order of the data.
- `last` (string) (optional): Optional string indicating the ID of the last\-returned data. If
  provided, the server will return the next data entries after the `last`
  ID.
- `includeBinary` (boolean) (optional): Whether to include binary file data with each
  retrieved file.
- `countOnly` (boolean) (optional): Whether to return only the total count of entries.
- `includeInternalData` (boolean) (optional): Whether to retun internal data. Internal data is
  used for Viam\-specific data ingestion, like cloud SLAM. Defaults to
  `false`.

**Returns:**

- (Promise<{ count: bigint; data: [BinaryData](https://ts.viam.dev/classes/dataApi.BinaryData.html)[]; last: string }>): An array of data objects, the count (number of entries), and the
last\-returned page ID.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const data = await dataClient.binaryDataByFilter(
  {
    componentName: 'camera-1',
    componentType: 'rdk:component:camera',
  } as Filter,
  1
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#binarydatabyfilter).

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

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[BinaryDataByFilterResponse](https://flutter.viam.dev/viam_protos.app.data/BinaryDataByFilterResponse-class.html)\>

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

Retrieve binary data from Viam by `BinaryID`.
You can also find your binary data under the **Images**, **Point clouds**, or **Files** subtab of the app's [**Data** tab](https://app.viam.com/data), depending on the type of data that you have uploaded.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_ids` ([List[viam.proto.app.data.BinaryID] | List[str]](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)) (required): Binary data ID strings specifying the desired data or BinaryID objects. Must be non-empty. DEPRECATED: BinaryID is deprecated and will be removed in a future release. Instead, pass binary data IDs as a list of strings.
- `dest` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional filepath for writing retrieved data.

**Returns:**

- ([List[viam.proto.app.data.BinaryData]](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryData)): The binary data.

**Raises:**

- (GRPCError): If no binary data ID strings or BinaryID objects are provided.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
binary_metadata, count, last = await data_client.binary_data_by_filter(
    include_binary_data=False
)

my_ids = []

for obj in binary_metadata:
    my_ids.append(obj.metadata.binary_data_id)

binary_data = await data_client.binary_data_by_ids(my_ids)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_by_ids).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `binaryDataIDs` [([]string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*BinaryData)](https://pkg.go.dev/go.viam.com/rdk/app#BinaryData)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.BinaryDataByIDs).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `ids` (string) (required): The IDs of the requested binary data.

**Returns:**

- (Promise<[BinaryData](https://ts.viam.dev/classes/dataApi.BinaryData.html)[]>): An array of data objects.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const data = await dataClient.binaryDataByIds([
  'ccb74b53-1235-4328-a4b9-91dff1915a50/x5vur1fmps/YAEzj5I1kTwtYsDdf4a7ctaJpGgKRHmnM9bJNVyblk52UpqmrnMVTITaBKZctKEh',
]);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#binarydatabyids).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryIds` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)\> (required)
- `includeBinary` [bool](https://api.flutter.dev/flutter/dart-core/bool-class.html) (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[BinaryDataByIDsResponse](https://flutter.viam.dev/viam_protos.app.data/BinaryDataByIDsResponse-class.html)\>

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

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to delete the data from. To find your organization ID, visit the organization settings page.
- `delete_older_than_days` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Delete data that was captured up to this many days ago. For example, a value of 10 deletes any data that was captured up to 10 days ago. A value of 0 deletes all existing data.

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
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `organizationID` [(string)](https://pkg.go.dev/builtin#string)
- `deleteOlderThanDays` [(int)](https://pkg.go.dev/builtin#int)

**Returns:**

- [(int)](https://pkg.go.dev/builtin#int)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.DeleteTabularData).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of organization to delete data from.
- `deleteOlderThanDays` (number) (required): Delete data that was captured more than this
  many days ago. For example if `deleteOlderThanDays` is 10, this deletes
  any data that was captured more than 10 days ago. If it is 0, all
  existing data is deleted.

**Returns:**

- (Promise<bigint>): The number of items deleted.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const data = await dataClient.deleteTabularData(
  '123abc45-1234-5678-90ab-cdef12345678',
  10
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#deletetabulardata).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `olderThanDays` [int](https://api.flutter.dev/flutter/dart-core/int-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)\>

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

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter)) (optional): Optional, specifies binary data to delete. CAUTION: Passing an empty Filter deletes all binary data! You must specify an organization ID with organization_ids when using this option. To find your organization ID, visit the organization settings page.

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
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `filter` [(*Filter)](https://pkg.go.dev/go.viam.com/rdk/app#Filter)

**Returns:**

- [(int)](https://pkg.go.dev/builtin#int)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.DeleteBinaryDataByFilter).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `filter` ([Filter](https://ts.viam.dev/classes/dataApi.Filter.html)) (optional): Optional `pb.Filter` specifying binary data to delete. No
  `filter` implies all binary data.
- `includeInternalData` (boolean) (optional): Whether or not to delete internal data. Default
  is true.

**Returns:**

- (Promise<bigint>): The number of items deleted.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const data = await dataClient.deleteBinaryDataByFilter({
  componentName: 'camera-1',
  componentType: 'rdk:component:camera',
  organizationIds: ['123abc45-1234-5678-90ab-cdef12345678'],
  startTime: new Date('2025-03-19'),
  endTime: new Date('2025-03-20'),
} as Filter);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#deletebinarydatabyfilter).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `filter` [Filter](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html)? (required)
- `includeInternalData` [bool](https://api.flutter.dev/flutter/dart-core/bool-class.html) (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)\>

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

- `binary_ids` ([List[viam.proto.app.data.BinaryID] | List[str]](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)) (required): Binary data ID strings specifying the data to be deleted or BinaryID objects. Must be non-empty. DEPRECATED: BinaryID is deprecated and will be removed in a future release. Instead, pass binary data IDs as a list of strings.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The number of items deleted.

**Raises:**

- (GRPCError): If no binary data ID strings or BinaryID objects are provided.

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
        obj.metadata.binary_data_id
    )

binary_data = await data_client.delete_binary_data_by_ids(my_ids)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_binary_data_by_ids).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `binaryDataIDs` [([]string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(int)](https://pkg.go.dev/builtin#int)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.DeleteBinaryDataByIDs).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `ids` (string) (required): The IDs of the data to be deleted. Must be non\-empty.

**Returns:**

- (Promise<bigint>): The number of items deleted.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const data = await dataClient.deleteBinaryDataByIds([
  'ccb74b53-1235-4328-a4b9-91dff1915a50/x5vur1fmps/YAEzj5I1kTwtYsDdf4a7ctaJpGgKRHmnM9bJNVyblk52UpqmrnMVTITaBKZctKEh',
]);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#deletebinarydatabyids).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryDataIds` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
 _viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 try {
  final binaryDataIds = [
  '<YOUR-BINARY-DATA-ID>',
  '<YOUR-BINARY-DATA-ID>'
  ];

  // Call the function to delete binary data
  await dataClient.deleteBinaryDataByIds(binaryDataIds);

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
- `binary_ids` ([List[viam.proto.app.data.BinaryID] | List[str]](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)) (required): Binary data ID strings specifying the data to be tagged or BinaryID objects. Must be non-empty. DEPRECATED: BinaryID is deprecated and will be removed in a future release. Instead, pass binary data IDs as a list of strings.

**Returns:**

- None.

**Raises:**

- (GRPCError): If no binary data ID strings or BinaryID objects are provided.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
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
        obj.metadata.binary_data_id
    )

binary_data = await data_client.add_tags_to_binary_data_by_ids(tags, my_ids)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_tags_to_binary_data_by_ids).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `tags`
- `binaryDataIDs` [([]string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.AddTagsToBinaryDataByIDs).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `tags` (string) (required): The list of tags to add to specified binary data. Must be
  non\-empty.
- `ids` (string) (required): The IDs of the data to be tagged. Must be non\-empty.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const data = await dataClient.addTagsToBinaryDataByIds(
  ['tag1', 'tag2'],
  [
    'ccb74b53-1235-4328-a4b9-91dff1915a50/x5vur1fmps/YAEzj5I1kTwtYsDdf4a7ctaJpGgKRHmnM9bJNVyblk52UpqmrnMVTITaBKZctKEh',
  ]
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#addtagstobinarydatabyids).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `tags` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\> (required)
- `binaryDataIds` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

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

  final binaryDataIds = [
  '<YOUR-BINARY-DATA-ID>',
  '<YOUR-BINARY-DATA-ID>'
  ];

  // Call the function with both tags and IDs
  await dataClient.addTagsToBinaryDataByIds(tags, binaryDataIds);

  print('Successfully added tags to binary IDs');
 } catch (e) {
  print('Error adding tags: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/addTagsToBinaryDataByIds.html).

{{% /tab %}}
{{< /tabs >}}

### TagsByFilter

Get a list of tags using a filter.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter)) (optional): Specifies subset ofdata to retrieve tags from. If none is provided, returns all tags.

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
{{% tab name="TypeScript" %}}

**Parameters:**

- `filter` ([Filter](https://ts.viam.dev/classes/dataApi.Filter.html)) (optional): Optional `pb.Filter` specifying what data to get tags from.
  No `filter` implies all data.

**Returns:**

- (Promise<string[]>): The list of tags.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const data = await dataClient.tagsByFilter({
  componentName: 'camera-1',
} as Filter);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#tagsbyfilter).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `filter` [Filter](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html)? (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\>\>

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

- `binary_id` ([viam.proto.app.data.BinaryID | str](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)) (required): The binary data ID or BinaryID of the image to add the bounding box to. DEPRECATED: BinaryID is deprecated and will be removed in a future release. Instead, pass binary data IDs as a list of strings.
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
bbox_id = await data_client.add_bounding_box_to_image_by_id(
    binary_id="<YOUR-BINARY-DATA-ID>",
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
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `binaryDataID` [(string)](https://pkg.go.dev/builtin#string)
- `label` [(string)](https://pkg.go.dev/builtin#string)
- `xMinNormalized` [(float64)](https://pkg.go.dev/builtin#float64)
- `yMinNormalized` [(float64)](https://pkg.go.dev/builtin#float64)
- `xMaxNormalized` [(float64)](https://pkg.go.dev/builtin#float64)
- `yMaxNormalized` [(float64)](https://pkg.go.dev/builtin#float64)

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.AddBoundingBoxToImageByID).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `binaryId` (string) (required): The ID of the image to add the bounding box to.
- `label` (string) (required): A label for the bounding box.
- `xMinNormalized` (number) (required): The min X value of the bounding box normalized from 0
  to 1.
- `yMinNormalized` (number) (required): The min Y value of the bounding box normalized from 0
  to 1.
- `xMaxNormalized` (number) (required): The max X value of the bounding box normalized from 0
  to 1.
- `yMaxNormalized` (number) (required): The max Y value of the bounding box normalized from 0
  to 1.

**Returns:**

- (Promise<string>): The bounding box ID.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const bboxId = await dataClient.addBoundingBoxToImageById(
  'ccb74b53-1235-4328-a4b9-91dff1915a50/x5vur1fmps/YAEzj5I1kTwtYsDdf4a7ctaJpGgKRHmnM9bJNVyblk52UpqmrnMVTITaBKZctKEh',
  'label1',
  0.3,
  0.3,
  0.6,
  0.6
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#addboundingboxtoimagebyid).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `label` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `binaryDataId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `xMinNormalized` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `yMinNormalized` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `xMaxNormalized` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `yMaxNormalized` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

// Example binary ID to add a bounding box to
final binaryDataId = '<YOUR-BINARY-DATA-ID>';

try {
  await dataClient.addBoundingBoxToImageById(
    "label",
    binaryDataId,
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
- `binary_id` ([viam.proto.app.data.BinaryID | str](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)) (required): The binary data ID or BinaryID of the image to remove the bounding box from. DEPRECATED: BinaryID is deprecated and will be removed in a future release. Instead, pass binary data IDs as a list of strings.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await data_client.remove_bounding_box_from_image_by_id(
binary_id="<YOUR-BINARY-DATA-ID>",
bbox_id="your-bounding-box-id-to-delete"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_bounding_box_from_image_by_id).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `bboxID` [(string)](https://pkg.go.dev/builtin#string)
- `binaryDataID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.RemoveBoundingBoxFromImageByID).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `binId` (string) (required): The ID of the image to remove the bounding box from.
- `bboxId` (string) (required): The ID of the bounding box to remove.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await dataClient.removeBoundingBoxFromImageById(
  'ccb74b53-1235-4328-a4b9-91dff1915a50/x5vur1fmps/YAEzj5I1kTwtYsDdf4a7ctaJpGgKRHmnM9bJNVyblk52UpqmrnMVTITaBKZctKEh',
  '5Z9ryhkW7ULaXROjJO6ghPYulNllnH20QImda1iZFroZpQbjahK6igQ1WbYigXED'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#removeboundingboxfromimagebyid).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `bboxId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `binaryDataId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

// Example binary ID to remove a bounding box from
final binaryDataId = '<YOUR-BINARY-DATA-ID>';

// Example bbox ID (label)
final bboxId = "label";
try {
  await dataClient.removeBoundingBoxFromImageById(
    bboxId,
    binaryDataId,
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

- `filter` ([viam.proto.app.data.Filter](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter)) (optional): Specifies data to retrieve bounding box labels from. If none is provided, returns labels.

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
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `filter` [(*Filter)](https://pkg.go.dev/go.viam.com/rdk/app#Filter)

**Returns:**

- [([]string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.BoundingBoxLabelsByFilter).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `filter` ([Filter](https://ts.viam.dev/classes/dataApi.Filter.html)) (optional): Optional `pb.Filter` specifying what data to get tags from.
  No `filter` implies all labels.

**Returns:**

- (Promise<string[]>): The list of bounding box labels.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const data = await dataClient.boundingBoxLabelsByFilter({
  componentName: 'camera-1',
} as Filter);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#boundingboxlabelsbyfilter).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `filter` [Filter](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html)? (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\>\>

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

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization you’d like to connect to. To find your organization ID, visit the organization settings page.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The hostname of the federated database.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
hostname = await data_client.get_database_connection(organization_id="<YOUR-ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.get_database_connection).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `organizationID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*GetDatabaseConnectionResponse)](https://pkg.go.dev/go.viam.com/rdk/app#GetDatabaseConnectionResponse)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.GetDatabaseConnection).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): Organization to retrieve connection for.

**Returns:**

- (Promise<string>): Hostname of the federated database.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const hostname = await dataClient.getDatabaseConnection(
  '123abc45-1234-5678-90ab-cdef12345678'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#getdatabaseconnection).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[DatabaseConnection](https://flutter.viam.dev/viam_sdk/DatabaseConnection.html)\>

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

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization you’d like to configure a database user for. To find your organization ID, visit the organization settings page.
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
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `organizationID` [(string)](https://pkg.go.dev/builtin#string)
- `password` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.ConfigureDatabaseUser).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization.
- `password` (string) (required): The password of the user.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await dataClient.configureDatabaseUser(
  '123abc45-1234-5678-90ab-cdef12345678',
  'Password01!'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#configuredatabaseuser).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `password` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

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

- `binary_ids` ([List[viam.proto.app.data.BinaryID] | List[str]](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)) (required): Unique identifiers for binary data to add to the dataset. To retrieve these IDs, navigate to the DATA page, click on an image, and copy its Binary Data ID from the details tab.
- `dataset_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the dataset to be added to.  To retrieve the dataset ID:  Navigate to the DATASETS tab of the DATA page. Click on the dataset. Click the … menu. Select Copy dataset ID.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
binary_metadata, count, last = await data_client.binary_data_by_filter(
    include_binary_data=False
)

my_binary_data_ids = []

for obj in binary_metadata:
    my_binary_data_ids.append(
        obj.metadata.binary_data_id
        )

await data_client.add_binary_data_to_dataset_by_ids(
    binary_ids=my_binary_data_ids,
    dataset_id="abcd-1234xyz-8765z-123abc"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_binary_data_to_dataset_by_ids).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `binaryDataIDs` [([]string)](https://pkg.go.dev/builtin#string)
- `datasetID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.AddBinaryDataToDatasetByIDs).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `ids` (string) (required): The IDs of binary data to add to dataset.
- `datasetId` (string) (required): The ID of the dataset to be added to.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await dataClient.addBinaryDataToDatasetByIds(
  [
    'ccb74b53-1235-4328-a4b9-91dff1915a50/x5vur1fmps/YAEzj5I1kTwtYsDdf4a7ctaJpGgKRHmnM9bJNVyblk52UpqmrnMVTITaBKZctKEh',
  ],
  '12ab3de4f56a7bcd89ef0ab1'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#addbinarydatatodatasetbyids).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryDataIds` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\> (required)
- `datasetId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

// Example binary IDs to add to the dataset
 final binaryDataIds = [
  '<YOUR-BINARY-DATA-ID>',
  '<YOUR-BINARY-DATA-ID>'
 ];

 // Dataset ID where the binary data will be added
 const datasetId = '<YOUR-DATASET-ID>';

 try {
   // Add the binary data to the dataset
   await dataClient.addBinaryDataToDatasetByIds(
     binaryDataIds,
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

- `binary_ids` ([List[viam.proto.app.data.BinaryID] | List[str]](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID)) (required): Unique identifiers for the binary data to remove from the dataset. To retrieve these IDs, navigate to the DATA page, click on an image and copy its Binary Data ID from the details tab. DEPRECATED: BinaryID is deprecated and will be removed in a future release. Instead, pass binary data IDs as a list of strings.
- `dataset_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the dataset to be removed from. To retrieve the dataset ID:  Navigate to the DATASETS tab of the DATA page. Click on the dataset. Click the … menu. Select Copy dataset ID.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
binary_metadata, count, last = await data_client.binary_data_by_filter(
    include_binary_data=False
)

my_binary_data_ids = []

for obj in binary_metadata:
    my_binary_data_ids.append(
        obj.metadata.binary_data_id
    )

await data_client.remove_binary_data_from_dataset_by_ids(
    binary_ids=my_binary_data_ids,
    dataset_id="abcd-1234xyz-8765z-123abc"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_binary_data_from_dataset_by_ids).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `binaryDataIDs` [([]string)](https://pkg.go.dev/builtin#string)
- `datasetID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.RemoveBinaryDataFromDatasetByIDs).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `ids` (string) (required): The IDs of the binary data to remove from dataset.
- `datasetId` (string) (required): The ID of the dataset to be removed from.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await dataClient.removeBinaryDataFromDatasetByIds(
  [
    'ccb74b53-1235-4328-a4b9-91dff1915a50/x5vur1fmps/YAEzj5I1kTwtYsDdf4a7ctaJpGgKRHmnM9bJNVyblk52UpqmrnMVTITaBKZctKEh',
  ],
  '12ab3de4f56a7bcd89ef0ab1'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#removebinarydatafromdatasetbyids).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryDataIds` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\> (required)
- `datasetId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

// Example binary IDs to remove from the dataset
 final binaryDataIds = [
  '<YOUR-BINARY-DATA-ID>',
  '<YOUR-BINARY-DATA-ID>'
 ];

 // Dataset ID where the binary data will be removed
 const datasetId = '<YOUR-DATASET-ID>';

 try {
   // Remove the binary data from the dataset
   await dataClient.removeBinaryDataFromDatasetByIds(
     binaryDataIds,
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

### GetDataPipeline

Get the configuration for a [data pipeline](/data-ai/data/data-pipelines/).
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the data pipeline to get.

**Returns:**

- ([DataPipeline](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.DataPipeline)): The data pipeline with the given ID.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
data_pipeline = await data_client.get_data_pipeline(id="<YOUR-DATA-PIPELINE-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.get_data_pipeline).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*DataPipeline)](https://pkg.go.dev/go.viam.com/rdk/app#DataPipeline)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.GetDataPipeline).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `pipelineId` (string) (required): The ID of the data pipeline.

**Returns:**

- (Promise<null | DataPipeline>): The data pipeline configuration or null if it does not exist.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const pipeline = await dataClient.getPipeline(
  '123abc45-1234-5678-90ab-cdef12345678'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#getdatapipeline).

{{% /tab %}}
{{< /tabs >}}

### ListDataPipelines

List all of the [data pipelines](/data-ai/data/data-pipelines/) in an organization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that owns the pipelines. You can obtain your organization ID from the organization settings page.

**Returns:**

- ([List[DataPipeline]](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.DataPipeline)): A list of all of the data pipelines for the given organization.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
data_pipelines = await data_client.list_data_pipelines(organization_id="<YOUR-ORGANIZATION-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.list_data_pipelines).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `organizationID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*DataPipeline)](https://pkg.go.dev/go.viam.com/rdk/app#DataPipeline)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.ListDataPipelines).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization.

**Returns:**

- (Promise<DataPipeline[]>): The list of data pipelines.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const pipelines = await dataClient.listDataPipelines(
  '123abc45-1234-5678-90ab-cdef12345678'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#listdatapipelines).

{{% /tab %}}
{{< /tabs >}}

### CreateDataPipeline

Create a [data pipeline](/data-ai/data/data-pipelines/).
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that will own the pipeline. You can obtain your organization ID from the organization settings page.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the pipeline.
- `mql_binary` (List[Dict[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]]) (required): The MQL pipeline to run, as a list of MongoDB aggregation pipeline stages.
- `schedule` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): A cron expression representing the expected execution schedule in UTC (note this also defines the input time window; an hourly schedule would process 1 hour of data at a time).
- `enable_backfill` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): When true, pipeline runs will be scheduled for the organization’s past data.
- `data_source_type` ([viam.proto.app.data.TabularDataSourceType.ValueType](https://python.viam.dev/autoapi/viam/gen/app/data/v1/data_pb2/index.html#viam.gen.app.data.v1.data_pb2.TabularDataSourceType)) (required): The type of data source to use for the pipeline. Defaults to TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_STANDARD.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The ID of the newly created pipeline.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
data_pipeline_id = await data_client.create_data_pipeline(
    organization_id="<YOUR-ORGANIZATION-ID>",
    name="<YOUR-PIPELINE-NAME>",
    mql_binary=[<YOUR-MQL-PIPELINE-AGGREGATION>],
    schedule="<YOUR-SCHEDULE>",
    enable_backfill=False,
    data_source_type=TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_STANDARD,
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.create_data_pipeline).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `organizationID`
- `name` [(string)](https://pkg.go.dev/builtin#string)
- `query` [([]map[string]interface{})](https://pkg.go.dev/builtin#string)
- `schedule` [(string)](https://pkg.go.dev/builtin#string)
- `enableBackfill` [(bool)](https://pkg.go.dev/builtin#bool)
- `opts` [(*CreateDataPipelineOptions)](https://pkg.go.dev/go.viam.com/rdk/app#CreateDataPipelineOptions)

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.CreateDataPipeline).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization.
- `name` (string) (required): The name of the data pipeline.
- `query` (Uint8Array) (required): The MQL query to run as a list of BSON documents.
- `schedule` (string) (required): The schedule to run the query on (cron expression).
- `enableBackfill` (boolean) (required)
- `dataSourceType` ([TabularDataSourceType](https://ts.viam.dev/enums/dataApi.TabularDataSourceType.html)) (optional): The type of data source to use for the data pipeline.

**Returns:**

- (Promise<string>): The ID of the created data pipeline.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
// {@link JsonValue} is imported from @bufbuild/protobuf
const mqlQuery: Record<string, JsonValue>[] = [
  {
    $match: {
      component_name: 'sensor-1',
    },
  },
  {
    $limit: 5,
  },
];

const pipelineId = await dataClient.createDataPipeline(
  '123abc45-1234-5678-90ab-cdef12345678',
  'my-pipeline',
  mqlQuery,
  '0 0 * * *'
  false
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#createdatapipeline).

{{% /tab %}}
{{< /tabs >}}

### DeleteDataPipeline

Delete a [data pipeline](/data-ai/data/data-pipelines/), its execution history, and all of its output data.
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the data pipeline to delete.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await data_client.delete_data_pipeline(id="<YOUR-DATA-PIPELINE-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_data_pipeline).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.DeleteDataPipeline).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `pipelineId` (string) (required): The ID of the data pipeline.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await dataClient.deleteDataPipeline(
  '123abc45-1234-5678-90ab-cdef12345678'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#deletedatapipeline).

{{% /tab %}}
{{< /tabs >}}

### ListDataPipelineRuns

Get information about individual executions of a [data pipeline](/data-ai/data/data-pipelines/).
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the pipeline to list runs for.
- `page_size` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): The number of runs to return per page. Defaults to 10.

**Returns:**

- ([DataPipelineRunsPage](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.DataPipelineRunsPage)): A page of data pipeline runs with pagination support.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
data_pipeline_runs = await data_client.list_data_pipeline_runs(id="<YOUR-DATA-PIPELINE-ID>")
while len(data_pipeline_runs.runs) > 0:
    data_pipeline_runs = await data_pipeline_runs.next_page()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.list_data_pipeline_runs).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)
- `pageSize` [(uint32)](https://pkg.go.dev/builtin#uint32)

**Returns:**

- [(*ListDataPipelineRunsPage)](https://pkg.go.dev/go.viam.com/rdk/app#ListDataPipelineRunsPage)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.ListDataPipelineRuns).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `pipelineId` (string) (required): The ID of the data pipeline.
- `pageSize` (number) (optional): The number of runs to return per page.

**Returns:**

- (Promise<ListDataPipelineRunsPage>): A page of data pipeline runs.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const page = await dataClient.listDataPipelineRuns(
  '123abc45-1234-5678-90ab-cdef12345678'
);
page.runs.forEach((run) => {
  console.log(run);
});
page = await page.nextPage();
page.runs.forEach((run) => {
  console.log(run);
});
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#listdatapipelineruns).

{{% /tab %}}
{{< /tabs >}}

### RenameDataPipeline

Rename a [data pipeline](/data-ai/data/data-pipelines/).

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id`
- `name` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.RenameDataPipeline).

{{% /tab %}}
{{< /tabs >}}
