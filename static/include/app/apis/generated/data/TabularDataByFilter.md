### TabularDataByFilter

{{< tabs >}}
{{% tab name="Python" %}}

Filter and download tabular data. The data will be paginated into pages of limit items, and the pagination ID will be included in the returned tuple. If a destination is provided, the data will be saved to that file. If the file is not empty, it will be overwritten.

**Parameters:**

- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter) (optional): Optional Filter specifying tabular data to retrieve. No Filter implies all tabular data.
- `limit` [(int)](<INSERT PARAM TYPE LINK>) (optional): The maximum number of entries to include in a page. Defaults to 50 if unspecified.
- `sort_order` [(viam.proto.app.data.Order.ValueType)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Order) (optional): The desired sort order of the data.
- `last` [(str)](<INSERT PARAM TYPE LINK>) (optional): Optional string indicating the ID of the last-returned data. If provided, the server will return the next data entries after the last ID.
- `count_only` [(bool)](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool) (required): Whether to return only the total count of entries.
- `include_internal_data` [(bool)](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool) (required): Whether to return the internal data. Internal data is used for Viam-specific data ingestion, like cloud SLAM. Defaults to False
- `dest` [(str)](<INSERT PARAM TYPE LINK>) (optional): Optional filepath for writing retrieved data.

**Returns:**

- [(Tuple[List[TabularData], int, str])](INSERT RETURN TYPE LINK): The tabular data. int: The count (number of entries) str: The last-returned page ID.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_by_filter).

``` python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_data = []
last = None
my_filter = Filter(component_name="left_motor")
while True:
    tabular_data, count, last = await data_client.tabular_data_by_filter(my_filter, last)
    if not tabular_data:
        break
    my_data.extend(tabular_data)
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `countOnly` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required):
- `dataRequest` [(DataRequest)](https://flutter.viam.dev/viam_protos.app.data/DataRequest-class.html) (required):
- `includeInternalData` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/tabularDataByFilter.html).

{{% /tab %}}
{{< /tabs >}}
