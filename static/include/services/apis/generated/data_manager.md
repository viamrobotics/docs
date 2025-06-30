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

### UploadImageToDataset

Upload an image directly to specified datasets for machine learning workflows.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `image` (bytes): The image data as bytes.
- `dataset_ids` (List[str]): List of dataset IDs to upload the image to.
- `tags` (List[str]): List of tags to apply to the uploaded image.
- `extra` (Mapping[str, Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` (float) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.services.data_manager import DataManagerClient

# Get the data manager service
data_manager = DataManagerClient.from_robot(robot, "builtin")

# Read image file
with open("path/to/image.jpg", "rb") as f:
    image_data = f.read()

# Upload to datasets with tags
await data_manager.upload_image_to_dataset(
    image=image_data,
    dataset_ids=["dataset_1", "dataset_2"],
    tags=["training", "outdoor", "robot_vision"]
)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `image` ([]byte): The image data as bytes.
- `datasetIDs` ([]string): List of dataset IDs to upload the image to.
- `tags` ([]string): List of tags to apply to the uploaded image.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the data manager service
dataManager, err := datamanager.FromRobot(machine, "builtin")

// Read image file
imageData, err := os.ReadFile("path/to/image.jpg")
if err != nil {
    return err
}

// Upload to datasets with tags
err = dataManager.UploadImageToDataset(
    context.Background(),
    imageData,
    []string{"dataset_1", "dataset_2"},
    []string{"training", "outdoor", "robot_vision"},
    nil,
)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/datamanager#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `image` (Uint8Array): The image data as bytes.
- `datasetIds` (string[]): List of dataset IDs to upload the image to.
- `tags` (string[]): List of tags to apply to the uploaded image.
- `extra` (Struct) (optional): Extra options to pass to the underlying RPC call.
- `callOptions` (CallOptions) (optional): Call options for the request.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const dataManager = new VIAM.DataManagerClient(
  machine,
  'builtin'
);

// Read image file (example using File API in browser)
const fileInput = document.getElementById('imageFile') as HTMLInputElement;
const file = fileInput.files[0];
const imageData = new Uint8Array(await file.arrayBuffer());

// Upload to datasets with tags
await dataManager.uploadImageToDataset(
  imageData,
  ['dataset_1', 'dataset_2'],
  ['training', 'outdoor', 'robot_vision']
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataManagerClient.html).

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
