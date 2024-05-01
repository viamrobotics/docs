### DeleteFragment

{{< tabs >}}
{{% tab name="Python" %}}

Delete a fragment.

**Parameters:**

- `fragment_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the fragment to delete.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_fragment).

``` python {class="line-numbers linkable-line-numbers"}
await cloud.delete_fragment(
    fragment_id="12a12ab1-1234-5678-abcd-abcd01234567")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteFragment.html).

{{% /tab %}}
{{< /tabs >}}
