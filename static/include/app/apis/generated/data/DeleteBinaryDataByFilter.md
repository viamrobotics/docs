### DeleteBinaryDataByFilter

{{< tabs >}}
{{% tab name="Python" %}}

Filter and delete binary data.

**Parameters:**

- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter) (optional): Optional Filter specifying binary data to delete. Passing an empty Filter will lead to all data being deleted. Exercise caution when using this option.


**Returns:**

- [(int)](INSERT RETURN TYPE LINK): The number of items deleted.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_binary_data_by_filter).

``` python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_name="left_motor")
res = await data_client.delete_binary_data_by_filter(my_filter)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `filter` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required):
- `includeInternalData` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/deleteBinaryDataByFilter.html).

{{% /tab %}}
{{< /tabs >}}
