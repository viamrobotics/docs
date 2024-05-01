### CreateKeyFromExistingKeyAuthorizations

{{< tabs >}}
{{% tab name="Python" %}}

Creates a new [API key](/fleet/cli/#authenticate) with an existing key’s authorizations

**Parameters:**

- `id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): the ID of the API key to duplication authorizations from


**Returns:**

- [(Tuple[str, str])](INSERT RETURN TYPE LINK): The API key and API key id

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_key_from_existing_key_authorizations).

``` python {class="line-numbers linkable-line-numbers"}
api_key, api_key_id = cloud.create_key_from_existing_key_authorizations(
    id="INSERT YOUR API KEY ID")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createKeyFromExistingKeyAuthorizations.html).

{{% /tab %}}
{{< /tabs >}}
