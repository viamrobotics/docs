### UploadModuleFile

{{< tabs >}}
{{% tab name="Python" %}}

Upload a module file

**Parameters:**

- `module_file_info` [(viam.proto.app.ModuleFileInfo)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.ModuleFileInfo) (optional): Relevant metadata.
- `file` [(bytes)](https://docs.python.org/3/library/stdtypes.html#bytes-objects) (required): Bytes of file to upload.


**Returns:**

- [(str)](INSERT RETURN TYPE LINK): ID of uploaded file.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.upload_module_file).

``` python {class="line-numbers linkable-line-numbers"}
file_id = await cloud.upload_module_file(file=b"<file>")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `first` [(Future)](dart-async/Future-class.html)<[int](dart-core/int-class.html)> (required):
- `isBroadcast` [(Future)](dart-async/Future-class.html)<[int](dart-core/int-class.html)> (required):
- `isEmpty` [(Future)](dart-async/Future-class.html)<[int](dart-core/int-class.html)> (required):
- `last` [(Future)](dart-async/Future-class.html)<[int](dart-core/int-class.html)> (required):
- `length` [(Future)](dart-async/Future-class.html)<[int](dart-core/int-class.html)> (required):
- `single` [(Future)](dart-async/Future-class.html)<[int](dart-core/int-class.html)> (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/uploadModuleFile.html).

{{% /tab %}}
{{< /tabs >}}
