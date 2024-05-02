### RemoveBoundingBoxFromImageByID

{{< tabs >}}
{{% tab name="Python" %}}

Removes a bounding box from an image.

**Parameters:**

- `bbox_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The ID of the bounding box to remove.
- `binary_id` [(viam.proto.app.data.BinaryID)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID) (required):

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_bounding_box_from_image_by_id).

``` python {class="line-numbers linkable-line-numbers"}
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

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `bboxId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `binaryId` [(BinaryID)](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/removeBoundingBoxFromImageByID.html).

{{% /tab %}}
{{< /tabs >}}
