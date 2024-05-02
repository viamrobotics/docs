### GetModule

{{< tabs >}}
{{% tab name="Python" %}}

Get a module.

**Parameters:**

- `module_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the module being retrieved, containing module name or namespace and module name.

**Returns:**

- [(viam.proto.app.Module)](INSERT RETURN TYPE LINK): The module.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_module).

``` python {class="line-numbers linkable-line-numbers"}
the_module = await cloud.get_module(module_id="my-cool-modular-base")
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `moduleId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getModule.html).

{{% /tab %}}
{{< /tabs >}}
