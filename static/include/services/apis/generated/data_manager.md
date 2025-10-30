### Sync

{{% alert title="Important" color="info" %}}

This method is not yet available in the Viam Python SDK.

{{% /alert %}}

Sync data stored on the machine to the cloud.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
data, err := datamanager.FromProvider(machine, "my_data_manager")
// Sync data stored on the machine to the cloud.
err := data.Sync(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/datamanager#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional): Extra arguments to pass to the sync request.
- `callOptions` (CallOptions) (optional): Call options for the sync request.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const dataManager = new VIAM.DataManagerClient(
  machine,
  'my_data_manager'
);
await dataManager.sync();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataManagerClient.html#sync).

{{% /tab %}}
{{< /tabs >}}

### UploadImageToDatasets

Upload an image data to the specified datasets.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `image` [(image.Image)](https://pkg.go.dev/image#Image)
- `datasetIDs`
- `tags` [([]string)](https://pkg.go.dev/builtin#string)
- `mimeType` [(datasyncpb.MimeType)](https://pkg.go.dev/go.viam.com/api/app/datasync/v1#MimeType)
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/datamanager#Service).

{{% /tab %}}
{{< /tabs >}}

### UploadBinaryDataToDatasets

Upload Binary data to the specified datasets.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `binaryData` [([]byte)](https://pkg.go.dev/builtin#byte)
- `datasetIDs`
- `tags` [([]string)](https://pkg.go.dev/builtin#string)
- `mimeType` [(datasyncpb.MimeType)](https://pkg.go.dev/go.viam.com/api/app/datasync/v1#MimeType)
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/datamanager#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `binaryData` (Uint8Array) (required): The binary data to upload.
- `tags` (string) (required): Tags to associate with the binary data.
- `datasetIds` (string) (required): IDs of the datasets to associate the binary data with.
- `mimeType` (MimeType) (required): The MIME type of the binary data.
- `extra` (None) (optional): Extra arguments to pass to the upload request.
- `callOptions` (CallOptions) (optional): Call options for the upload request.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const dataManager = new VIAM.DataManagerClient(
  machine,
  'my_data_manager'
);
await dataManager.uploadBinaryDataToDatasets(
  new Uint8Array([1, 2, 3]),
  ['tag1', 'tag2'],
  ['datasetId1', 'datasetId2'],
  MimeType.MIME_TYPE_JPEG
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataManagerClient.html#uploadbinarydatatodatasets).

{{% /tab %}}
{{< /tabs >}}

### Reconfigure

Reconfigure this resource.
Reconfigure must reconfigure the resource atomically and in place.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `deps` [(Dependencies)](https://pkg.go.dev/go.viam.com/rdk/resource#Dependencies): The resource dependencies.
- `conf` [(Config)](https://pkg.go.dev/go.viam.com/rdk/resource#Config): The resource configuration.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
Most models do not implement `DoCommand`.
Any available model-specific commands should be covered in the model's documentation.
If you are implementing your own data manager service and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myDataManagerSvc, err := datamanager.FromRobot(machine, "my_data_manager_svc")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myDataManagerSvc.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `command` ([Struct](https://ts.viam.dev/classes/Struct.html)) (required): The command to do.
- `callOptions` (CallOptions) (optional): Call options for the command.

**Returns:**

- (Promise<[JsonValue](https://ts.viam.dev/types/JsonValue.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const dataManager = new VIAM.DataManagerClient(
  machine,
  'my_data_manager'
);
await dataManager.doCommand(new Struct({ cmd: 'test', data1: 500 }));
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataManagerClient.html#docommand).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this instance of the service.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
data, err := datamanager.FromRobot(machine, "my_data_manager")

err := data.Name()
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (string): The name of the resource.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
data_manager.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataManagerClient.html#name).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
data, err := datamanager.FromRobot(machine, "my_data_manager")

err := data.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
