### ListLocations

{{< tabs >}}
{{% tab name="Python" %}}

Get a list of all locations under the currently authed-to organization.

**Parameters:**

- None.

**Returns:**

- [(List[viam.proto.app.Location])](INSERT RETURN TYPE LINK): The list of locations.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_locations).

``` python {class="line-numbers linkable-line-numbers"}
locations = await cloud.list_locations()
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listLocations.html).

{{% /tab %}}
{{< /tabs >}}
