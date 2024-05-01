### DeleteLocation

{{< tabs >}}
{{% tab name="Python" %}}

Delete a location.

**Parameters:**

- `location_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the location to delete. Must be specified.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_location).

``` python {class="line-numbers linkable-line-numbers"}
await cloud.delete_location(location_id="abc12abcde")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteLocation.html).

{{% /tab %}}
{{< /tabs >}}
