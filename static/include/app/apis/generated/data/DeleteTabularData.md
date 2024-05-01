### DeleteTabularData

{{< tabs >}}
{{% tab name="Python" %}}

Delete tabular data older than a specified number of days.

**Parameters:**

- `organization_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of organization to delete data from.
- `delete_older_than_days` [(int)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): Delete data that was captured up to this many days ago. For example if delete_older_than_days is 10, this deletes any data that was captured up to 10 days ago. If it is 0, all existing data is deleted.


**Returns:**

- [(int)](INSERT RETURN TYPE LINK): The number of items deleted.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_tabular_data).

``` python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.data import Filter

my_filter = Filter(component_name="left_motor")
days_of_data_to_delete = 10
tabular_data = await data_client.delete_tabular_data(
    org_id="a12b3c4e-1234-1abc-ab1c-ab1c2d345abc", days_of_data_to_delete)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `deleteOlderThanDays` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/deleteTabularData.html).

{{% /tab %}}
{{< /tabs >}}
