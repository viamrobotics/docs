### DeleteBinaryDataByIDs

{{< tabs >}}
{{% tab name="Python" %}}

Filter and delete binary data.

**Parameters:**

- `binary_ids` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID) (required): BinaryID objects specifying the data to be deleted. Must be non-empty.


**Returns:**

- [(int)](INSERT RETURN TYPE LINK): The number of items deleted.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_binary_data_by_ids).

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

binary_data = await data_client.delete_binary_data_by_ids(my_ids)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryIds` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)> (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/deleteBinaryDataByIDs.html).

{{% /tab %}}
{{< /tabs >}}
