### TagsByFilter

{{< tabs >}}
{{% tab name="Python" %}}

Get a list of tags using a filter.

**Parameters:**

- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter) (optional): Filter specifying data to retrieve from. If no Filter is provided, all data tags will return.


**Returns:**

- [(List[str])](INSERT RETURN TYPE LINK): The list of tags.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tags_by_filter).

``` python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_name="my_camera")
tags = await data_client.tags_by_filter(my_filter)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `filter` [(Filter)](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/tagsByFilter.html).

{{% /tab %}}
{{< /tabs >}}
