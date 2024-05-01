### AddBinaryDataToDatasetByIDs

{{< tabs >}}
{{% tab name="Python" %}}

Add the BinaryData to the provided dataset.

**Parameters:**

- `binary_ids` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/gen/app/data/v1/data_pb2/index.html#viam.gen.app.data.v1.data_pb2.BinaryID) (required): The IDs of binary data to add to dataset.
- `dataset_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The ID of the dataset to be added to.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_binary_data_to_dataset_by_ids).

``` python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import BinaryID

binary_metadata = await data_client.binary_data_by_filter(
    include_file_data=False
)

my_binary_ids = []

for obj in binary_metadata:
    my_binary_ids.append(
        BinaryID(
            file_id=obj.metadata.id,
            organization_id=obj.metadata.capture_metadata.organization_id,
            location_id=obj.metadata.capture_metadata.location_id
            )
        )

await data_client.add_binary_data_to_dataset_by_ids(
    binary_ids=my_binary_ids,
    dataset_id="abcd-1234xyz-8765z-123abc"
)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryIds` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)> (required):
- `datasetId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)> (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/addBinaryDataToDatasetByIDs.html).

{{% /tab %}}
{{< /tabs >}}
