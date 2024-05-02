### AddBoundingBoxToImageByID

{{< tabs >}}
{{% tab name="Python" %}}

Add a bounding box to an image.

**Parameters:**

- `binary_id` [(viam.proto.app.data.BinaryID)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID) (required): The ID of the image to add the bounding box to.
- `label` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): A label for the bounding box.
- `x_min_normalized` [(float)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): Min X value of the bounding box normalized from 0 to 1.
- `y_min_normalized` [(float)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): Min Y value of the bounding box normalized from 0 to 1.
- `x_max_normalized` [(float)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): Max X value of the bounding box normalized from 0 to 1.
- `y_max_normalized` [(float)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): Max Y value of the bounding box normalized from 0 to 1.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): The bounding box ID

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_bounding_box_to_image_by_id).

``` python {class="line-numbers linkable-line-numbers"}
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

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryId` [(BinaryID)](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html) (required):
- `label` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `xMaxNormalized` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html) (required):
- `xMinNormalized` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html) (required):
- `yMaxNormalized` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html) (required):
- `yMinNormalized` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/addBoundingBoxToImageByID.html).

{{% /tab %}}
{{< /tabs >}}
