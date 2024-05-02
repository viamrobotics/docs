### BoundingBoxLabelsByFilter

{{< tabs >}}
{{% tab name="Python" %}}

Get a list of bounding box labels using a Filter.

**Parameters:**

- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter) (optional): Filter specifying data to retrieve from. If no Filter is provided, all labels will return.

**Returns:**

- [(List[str])](INSERT RETURN TYPE LINK): The list of bounding box labels.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.bounding_box_labels_by_filter).

``` python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_name="my_camera")
bounding_box_labels = await data_client.bounding_box_labels_by_filter(
    my_filter)
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `filter` [(Filter)](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/boundingBoxLabelsByFilter.html).

{{% /tab %}}
{{< /tabs >}}
