### CreateModule

{{< tabs >}}
{{% tab name="Python" %}}

Create a module under the currently authed-to organization.

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The name of the module. Must be unique within your organization.

**Returns:**

- [(Tuple[str, str])](INSERT RETURN TYPE LINK): A tuple containing the ID [0] of the new module and its URL [1].

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_module).

``` python {class="line-numbers linkable-line-numbers"}
new_module = await cloud.create_module(name="cool_new_hoverboard_module")
print("Module ID:", new_module[0])
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createModule.html).

{{% /tab %}}
{{< /tabs >}}
