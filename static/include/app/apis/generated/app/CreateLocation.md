### CreateLocation

{{< tabs >}}
{{% tab name="Python" %}}

Create and name a location under the currently authed-to organization and the specified parent location.

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Name of the location.
- `parent_location_id` [(str)](<INSERT PARAM TYPE LINK>) (optional): Optional parent location to put the location under. Defaults to a root-level location if no location ID is provided.

**Returns:**

- [(viam.proto.app.Location)](INSERT RETURN TYPE LINK): The newly created location.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_location).

``` python {class="line-numbers linkable-line-numbers"}
my_new_location = await cloud.create_location(name="Robotville",
                                              parent_location_id="111ab12345")
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `parentLocationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createLocation.html).

{{% /tab %}}
{{< /tabs >}}
