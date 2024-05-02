### CreateLocationSecret

{{< tabs >}}
{{% tab name="Python" %}}

Create a new location secret.

**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>) (optional): ID of the location to generate a new secret for. Defaults to the location ID provided at AppClient instantiation.

**Returns:**

- [(viam.proto.app.LocationAuth)](INSERT RETURN TYPE LINK): The specified location’s LocationAuth containing the newly created secret.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_location_secret).

``` python {class="line-numbers linkable-line-numbers"}
new_loc_auth = await cloud.create_location_secret()
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createLocationSecret.html).

{{% /tab %}}
{{< /tabs >}}
