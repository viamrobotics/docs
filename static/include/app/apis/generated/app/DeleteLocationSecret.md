### DeleteLocationSecret

{{< tabs >}}
{{% tab name="Python" %}}

Delete a location secret.

**Parameters:**

- `secret_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the secret to delete.
- `location_id` [(str)](<INSERT PARAM TYPE LINK>) (optional): ID of the location to delete secret from. Defaults to the location ID provided at AppClient instantiation.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_location_secret).

``` python {class="line-numbers linkable-line-numbers"}
await cloud.delete_location_secret(
    secret_id="abcd123-456-7890ab-cxyz98-989898xyzxyz")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `secretId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteLocationSecret.html).

{{% /tab %}}
{{< /tabs >}}
