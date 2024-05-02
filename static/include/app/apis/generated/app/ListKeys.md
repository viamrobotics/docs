### ListKeys

{{< tabs >}}
{{% tab name="Python" %}}

Lists all keys for the currently-authed-to org.

**Parameters:**

- None.

**Returns:**

- [(List[viam.proto.app.APIKeyWithAuthorizations])](INSERT RETURN TYPE LINK): The existing API keys and authorizations.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_keys).

``` python {class="line-numbers linkable-line-numbers"}
keys = cloud.list_keys()
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `orgId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listKeys.html).

{{% /tab %}}
{{< /tabs >}}
