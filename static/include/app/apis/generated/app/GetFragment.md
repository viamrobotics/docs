### GetFragment

{{< tabs >}}
{{% tab name="Python" %}}

Get a fragment.

**Parameters:**

- `fragment_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the fragment to get.

**Returns:**

- [(Fragment)](INSERT RETURN TYPE LINK): The fragment.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_fragment).

``` python {class="line-numbers linkable-line-numbers"}
# Get a fragment and print its name and when it was created.
the_fragment = await cloud.get_fragment(
    fragment_id="12a12ab1-1234-5678-abcd-abcd01234567")
print("Name: ", the_fragment.name, "\nCreated on: ", the_fragment.created_on)
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getFragment.html).

{{% /tab %}}
{{< /tabs >}}
