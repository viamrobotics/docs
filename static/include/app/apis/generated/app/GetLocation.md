### GetLocation

{{< tabs >}}
{{% tab name="Python" %}}

Get a location.

**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>) (optional): ID of the location to get. Defaults to the location ID provided at AppClient instantiation.


**Returns:**

- [(viam.proto.app.Location)](INSERT RETURN TYPE LINK): The location.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_location).

``` python {class="line-numbers linkable-line-numbers"}
location = await cloud.get_location(location_id="123ab12345")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getLocation.html).

{{% /tab %}}
{{< /tabs >}}
