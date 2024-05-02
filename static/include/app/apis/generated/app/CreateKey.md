### CreateKey

{{< tabs >}}
{{% tab name="Python" %}}

Creates a new [API key](/fleet/cli/#authenticate).

**Parameters:**

- `authorizations` [(List[APIKeyAuthorization])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization) (required): A list of authorizations to associate with the key.
- `name` [(str)](<INSERT PARAM TYPE LINK>) (optional): A name for the key. If None, defaults to the current timestamp.

**Returns:**

- [(Tuple[str, str])](INSERT RETURN TYPE LINK): The api key and api key ID.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_key).

``` python {class="line-numbers linkable-line-numbers"}
from viam.app.app_client import APIKeyAuthorization

auth = APIKeyAuthorization(
role="owner",
resource_type="robot",
resource_id="your-robot-id123"
)

api_key, api_key_id = cloud.create_key([auth], "my_key")
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `authorizations` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)> (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createKey.html).

{{% /tab %}}
{{< /tabs >}}
