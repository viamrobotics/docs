### BinaryDataByIDs

{{< tabs >}}
{{% tab name="Python" %}}

Filter and download binary data.

**Parameters:**

- `binary_ids` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID) (required): BinaryID objects specifying the desired data. Must be non-empty.
- `dest` [(str)](<INSERT PARAM TYPE LINK>) (optional): Optional filepath for writing retrieved data.

**Returns:**

- [(List[BinaryData])](INSERT RETURN TYPE LINK): The binary data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_by_ids).

``` python {class="line-numbers linkable-line-numbers"}
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

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryIds` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)> (required):
- `includeBinary` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/binaryDataByIDs.html).

{{% /tab %}}
{{< /tabs >}}
