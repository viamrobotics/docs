### CreateFragment

{{< tabs >}}
{{% tab name="Python" %}}

Create a new private fragment.

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Name of the fragment.
- `config` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Optional Dictionary representation of new config to assign to specified fragment. Can be assigned by updating the fragment.


**Returns:**

- [(Fragment)](INSERT RETURN TYPE LINK): The newly created fragment.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_fragment).

``` python {class="line-numbers linkable-line-numbers"}
new_fragment = await cloud.create_fragment(
    name="cool_smart_machine_to_configure_several_of")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `config` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createFragment.html).

{{% /tab %}}
{{< /tabs >}}
