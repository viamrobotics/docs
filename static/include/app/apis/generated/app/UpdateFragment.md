### UpdateFragment

{{< tabs >}}
{{% tab name="Python" %}}

Update a fragment name AND its config and/or visibility.

**Parameters:**

- `fragment_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the fragment to update.
- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): New name to associate with the fragment.
- `config` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Optional Dictionary representation of new config to assign to specified fragment. Not passing this parameter will leave the fragment’s config unchanged.
- `public` [(bool)](<INSERT PARAM TYPE LINK>) (optional): Boolean specifying whether the fragment is public. Not passing this parameter will leave the fragment’s visibility unchanged. A fragment is private by default when created.

**Returns:**

- [(Fragment)](INSERT RETURN TYPE LINK): The newly updated fragment.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_fragment).

``` python {class="line-numbers linkable-line-numbers"}
updated_fragment = await cloud.update_fragment(
    fragment_id="12a12ab1-1234-5678-abcd-abcd01234567",
    name="better_name")
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `config` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `public` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateFragment.html).

{{% /tab %}}
{{< /tabs >}}
