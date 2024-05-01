### AddTagsToBinaryDataByIDs

{{< tabs >}}
{{% tab name="Python" %}}

Add tags to binary data.

**Parameters:**

- `tags` [(List[str])](<INSERT PARAM TYPE LINK>) (required): List of tags to add to specified binary data. Must be non-empty.
- `binary_ids` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID) (required): List of BinaryID objects specifying binary data to tag. Must be non-empty.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_tags_to_binary_data_by_ids).

``` python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import BinaryID

tags = ["tag1", "tag2"]

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

binary_data = await data_client.add_tags_to_binary_data_by_ids(tags, my_ids)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryIds` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)> (required):
- `tags` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)> (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/addTagsToBinaryDataByIDs.html).

{{% /tab %}}
{{< /tabs >}}
