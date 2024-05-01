### LocationAuth

{{< tabs >}}
{{% tab name="Python" %}}

Get a location’s LocationAuth (location secret(s)).

**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>) (optional): ID of the location to retrieve LocationAuth from. Defaults to the location ID provided at AppClient instantiation.


**Returns:**

- [(viam.proto.app.LocationAuth)](INSERT RETURN TYPE LINK): The LocationAuth containing location secrets.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.location_auth).

``` python {class="line-numbers linkable-line-numbers"}
loc_auth = await cloud.location_auth(location_id="123xy12345")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/locationAuth.html).

{{% /tab %}}
{{< /tabs >}}
