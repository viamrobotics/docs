### RemoveTagsFromBinaryDataByFilter

{{< tabs >}}
{{% tab name="Python" %}}

Remove tags from binary data.

**Parameters:**

- `tags` [(List[str])](<INSERT PARAM TYPE LINK>) (required): List of tags to remove from specified binary data.
- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter) (optional): Filter specifying binary data to untag. If no Filter is provided, all data will be untagged.


**Returns:**

- [(int)](INSERT RETURN TYPE LINK): The number of tags removed.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_tags_from_binary_data_by_filter).

``` python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_name="my_camera")
tags = ["tag1", "tag2"]
res = await data_client.remove_tags_from_binary_data_by_filter(tags, my_filter)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `filter` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)> (required):
- `tags` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)> (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/removeTagsFromBinaryDataByFilter.html).

{{% /tab %}}
{{< /tabs >}}
